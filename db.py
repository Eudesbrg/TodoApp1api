import sqlite3

import click
from flask import current_app, g

# get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_URI"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row
    
    return g.db


# close the database connection
def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()


# create the table and colounm in the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))



# helper to execute the init database with the cli
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Database initialized")


# 
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)