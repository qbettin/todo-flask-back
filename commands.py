# commands.py

import click
from flask.cli import with_appcontext
from models import db, User, Todo  # Adjust the import based on your project structure

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    """Create database tables."""
    db.create_all()
    click.echo("Tables created!")
