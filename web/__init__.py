import datetime

from flask import Flask, jsonify, request
from typing import List

from psycopg2.extras import RealDictCursor
from database import db_conn

app = Flask(__name__)

@app.route("/rates", methods=['GET'])
def rates():
    # Input data
    args = request.args

    # Checking for the existence of input data
    err = args_validation(request.args)
    if err != None:
        return err

    # Set DB connection
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
            'date_from': args.get("date_from"),
            'date_to': args.get("date_to"),
            'origin': args.get("origin"),
            'destination': args.get("destination")
        }
    )
    
    rates = cur.fetchall()
    cur.close()
    conn.close()    

    return jsonify(rates)


def args_validation(args):    
    date_format = '%Y-%m-%d'

    if args.get("date_from"):
        try:
            datetime.datetime.strptime(args.get("date_from"), date_format)
        except ValueError:         
            return jsonify(error="Incorrect data format, should be YYYY-MM-DD"), 400
    else:
        return jsonify(error="Parameter `date_from` is not found"), 400

    if args.get("date_to"):
        try:
            datetime.datetime.strptime(args.get("date_to"), date_format)
        except ValueError:         
            return jsonify(error="Incorrect data format, should be YYYY-MM-DD"), 400
    else:
        return jsonify(error="Parameter `date_to` is not found"), 400

    if args.get("origin"):
        pass
    else:
        return jsonify(error="Parameter `origin` is not found"), 400

    if args.get("destination"):
        pass
    else:
        return jsonify(error="Parameter `destination` is not found"), 400