import datetime

from flask import Flask, jsonify, request
from typing import List
from psycopg2.extras import RealDictCursor
from flask_parameter_validation import ValidateParameters, Json, Query

from database import db_conn

app = Flask(__name__)

@app.route("/rates", methods=['GET'])
@ValidateParameters()
def rates(
    date_from: str = Query(pattern="^\d{4}-\d{2}-\d{2}$"),
    date_to: str = Query(pattern="^\d{4}-\d{2}-\d{2}$"),
    origin: str = Query(),
    destination: str = Query(),
):
    conn = db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
   
    # In the first subquery, define what was received in the URL parameters
    # This is either a port code or a region slug
    # If this is a region slug, I get all the ports belonging to this region from the `ports`` table
    #
    # Next, I get price data by day and calculate the average
    # Сonsidering, if less than 3 prices are received per day, zero must be returned
    #
    # Get all the processed data from the last subquery
    # Convert the date and sort by date
    cur.execute(
        """
            WITH search_prices AS (
                SELECT * FROM prices 
                    WHERE day BETWEEN %(date_from)s AND %(date_to)s
                    AND (orig_code = %(origin)s OR orig_code IN (
                        SELECT code FROM ports 
                            WHERE parent_slug = %(origin)s)
                    )
                    AND (dest_code = %(destination)s OR dest_code IN (
                        SELECT code FROM ports 
                            WHERE parent_slug = %(destination)s)
                    )
            ), average_prices AS (
                SELECT 
                    CASE
                        WHEN COUNT(*) < 3 THEN null
                        ELSE round(AVG(price))
                    END AS average_price,
                    day,
                    orig_code,
                    dest_code
                    FROM search_prices
                        GROUP BY day, orig_code, dest_code
            )
            SELECT average_price, to_char(day,'YYYY-MM-DD') As day 
                FROM average_prices 
                ORDER BY day ASC;
        """, 
        {
            'date_from': request.args.get("date_from"),
            'date_to': request.args.get("date_to"),
            'origin': request.args.get("origin"),
            'destination': request.args.get("destination")
        }
    )
    
    rates = cur.fetchall()
    cur.close()
    conn.close()    

    return jsonify(rates)