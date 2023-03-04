from flask.cli import FlaskGroup

from database import database
from web import app

cli = FlaskGroup(app)
app.config.from_object('config.DevConfig')
# database.init_app(app)

if __name__ == "__main__":
    cli()