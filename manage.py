from flask.cli import FlaskGroup

from web import app

cli = FlaskGroup(app)
app.config.from_object('config.DevConfig')

if __name__ == "__main__":
    cli()