import os
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import relationship

database_filename = "casting.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actor(db.Model):
    __tablename__ = 'actor'


    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(), unique=True)
    age = Column(Integer(), nullable=False)
    gender = Column(String(), nullable=False)

    movies = relationship('Movie', secondary = 'link')


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(), unique=True)
    releasedate = Column(Integer(), nullable=False)

    actors = relationship('Actor', secondary = 'link')


class Link(db.Model):
    __tablename__ = 'link'

    actor_id = Column(Integer,ForeignKey('actor.id'),primary_key = True)
    movie_id = Column(Integer,ForeignKey('movie.id'),primary_key = True)

