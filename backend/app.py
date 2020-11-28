import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from models import  setup_db, db, Actor, Movie, Link #db_create_all_if_table_doesnt_exist,
from auth import AuthError, requires_auth


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO uncomment the following line to initialize the datbase
  !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
  '''


  ## ROUTES

  @app.route("/actors", methods=['GET'])
  @requires_auth('view:actors')
  def get_actor(payload):
      if Actor.query.all():
        actors = [
          {
            "__id": actor.id,
            "__name": actor.name,
            "age": actor.age,
            "gender": actor.gender,
            "_starred_in": [
              {
                "_title": Movie.query.filter_by(id=movie.movie_id).first().title,
                "releasedate": Movie.query.filter_by(id=movie.movie_id).first().releasedate
              }
              for movie in Link.query.filter_by(actor_id=actor.id).all()
              ]
          }
          for actor in Actor.query.all()
        ]
      else:
        actors = "No Actors in Database."
      result = {
          "success": True,
          "actors": actors
      }
      return jsonify(result)

  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actor')
  def add_actor(payload):
      if request.data:
          body = request.get_json()
          name = body.get('name', None)
          age = body.get('age', None)
          gender = body.get('gender', None)
          actor = Actor(name=name, age=age, gender=gender)
          try:
            db.session.add(actor)
            db.session.commit()
          except IntegrityError:
            db.session.rollback()
            return jsonify({
              'success': False,
              'IntegrityError': 'Actor Name already exists'
              })

          new_actor = Actor.query.filter_by(id=actor.id).first()

          result = {
              'success': True,
              'new_actor': new_actor.name
              }
          return jsonify(result)
      else:
          abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('edit:actor')
  def edit_actor(payload, actor_id):
      name = None
      age = None
      gender = None
      if request.data:
          body = request.get_json()
          name = body.get('name', None)
          age = body.get('age', None)
          gender = body.get('gender', None)

          actor = Actor.query.filter_by(id=actor_id).first()
          if actor is None:
            abort(404)
          old_name = actor.name
          old_age = actor.age
          old_gender = actor.gender

          # If no name provided in json body, abort
          if name is None:
            abort(400)

          if name is not None:
              actor.name = name

          if age is not None:
              actor.age = age

          if gender is not None:
              actor.gender = gender

          try:
            db.session.commit()
          except IntegrityError:
            db.session.rollback()
            return jsonify({
              'success': False,
              'IntegrityError': 'Actor cannot be modified - Try Again'
              })

          updated_actor = Actor.query.filter_by(id=actor_id).first()

          result = {
              'success': True,
              'updated_name': updated_actor.name,
              'updated_age': updated_actor.age,
              'updated_gender': updated_actor.gender,
              'old_name': old_name,
              'old_age': old_age,
              'old_gender': old_gender,
          }
          return jsonify(result)
      else:
          abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):

      # Check if the Actor is Linked. If linked, delete Link first.
      if Link.query.filter_by(actor_id=actor_id).first():
        link = Link.query.filter_by(actor_id=actor_id).first()
        try:
            db.session.delete(link)
            db.session.commit()
        except IntegrityError:
          db.session.rollback()
          return jsonify({
              'success': False,
              'IntegrityError': 'Couldnt Delete Actor Link - Try again'
              })

      if not Actor.query.filter_by(id=actor_id).first():
          abort(404)
      try:
        actor = Actor.query.filter_by(id=actor_id).first()
        deleted_actor = actor.name
        try:
          db.session.delete(actor)
          db.session.commit()
        except IntegrityError:
          db.session.rollback()
          return jsonify({
              'success': False,
              'IntegrityError': 'Couldnt Delete Actor - Try again'
              })

        result = {
            'success': True,
            'deleted_actor': deleted_actor
            }
        return jsonify(result)
      except:
        abort(422)

  @app.route("/movies", methods=['GET'])
  @requires_auth('view:movies')
  def get_movies(payload):
      if Movie.query.all():
        movies = [
          {
            "__id": movie.id,
            "__title": movie.title,
            "_releasedate": movie.releasedate,
            "starring": [
              {
                "_name": Actor.query.filter_by(id=actor.actor_id).first().name,
                "age": Actor.query.filter_by(id=actor.actor_id).first().age,
                "gender": Actor.query.filter_by(id=actor.actor_id).first().gender,
              }
              for actor in Link.query.filter_by(movie_id=movie.id).all()
              ]
          }
          for movie in Movie.query.all()
        ]
      else:
        movies = "No Movies in Database."


      result = {
          "success": True,
          "movies": movies
      }
      return jsonify(result)


  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def add_movie(payload):
      if request.data:
          body = request.get_json()
          releasedate = body.get('releasedate', None)
          title = body.get('title', None)
          movie = Movie(title=title, releasedate=releasedate)
          try:
            db.session.add(movie)
            db.session.commit()
          except IntegrityError:
            db.session.rollback()
            return jsonify({
              'success': False,
              'IntegrityError': 'Movie Title already exists'
              })

          new_movie = Movie.query.filter_by(id=movie.id).first()
          result = {
              'success': True,
              'new_movie': new_movie.title
          }
          return jsonify(result)
      else:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('edit:movie')
  def edit_movie(payload, movie_id):

      releasedate = None
      title = None

      if request.data:
          body = request.get_json()
          releasedate = body.get('releasedate', None)
          title = body.get('title', None)

      try:
          movie = Movie.query.filter_by(id=movie_id).first()
          if movie is None:
              abort(404)
          old_title = movie.title
          old_date = movie.releasedate
          if title is None:
              abort(400)

          if title is not None:
              movie.title = title

          if releasedate is not None:
              movie.releasedate = releasedate

          try:
            db.session.commit()
          except IntegrityError:
            db.session.rollback()
            return jsonify({
              'success': False,
              'IntegrityError': 'Movie cannot be modified - Try Again'
              })

          updated_movie = Movie.query.filter_by(id=movie_id).first()

          result = {
              'success': True,
              'updated_movie_title': updated_movie.title,
              'updated_movie_release_date': updated_movie.releasedate,
              'old_movie_title': old_title,
              'old_movie_release_date': old_date
          }
          return jsonify(result)
      except:
          abort(422)


  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(payload,movie_id):

      # Check if the Movie is Linked. If linked, delete Link first.
      if Link.query.filter_by(movie_id=movie_id).first():
        link = Link.query.filter_by(movie_id=movie_id).first()
        try:
            db.session.delete(link)
            db.session.commit()
        except IntegrityError:
          db.session.rollback()
          return jsonify({
              'success': False,
              'IntegrityError': 'Couldnt Delete Movie Link - Try again'
              })

      if not Movie.query.filter_by(id=movie_id).first():
          abort(404)
      try:
        movie = Movie.query.filter_by(id=movie_id).first()
        deleted_movie = movie.title
        try:
          db.session.delete(movie)
          db.session.commit()
        except IntegrityError:
          db.session.rollback()
          return jsonify({
              'success': False,
              'IntegrityError': 'Couldnt Delete Movie - Try again'
              })
        return jsonify({
            'success': True,
            'deleted_movie': deleted_movie
            })
      except:
        abort(422)


  @app.route('/link', methods=['POST'])
  @requires_auth('link:casts')
  def add_link(payload):
      if request.data:
          body = request.get_json()
          movie_id = body.get('movie_id', None)
          actor_id = body.get('actor_id', None)

          if not Actor.query.filter_by(id=actor_id).first():
            result = {
              'success': False,
              'error': "Actor with that ID doesnt Exist"
              }
            return jsonify(result)

          if not Movie.query.filter_by(id=movie_id).first():
            result = {
              'success': False,
              'error': "Movie with that ID doesnt Exist"
              }
            return jsonify(result)

          link = Link(movie_id=movie_id, actor_id=actor_id)
          try:
            db.session.add(link)
            db.session.commit()
          except IntegrityError:
            db.session.rollback()
            return jsonify({
              'success': False,
              'IntegrityError': 'Movie + Actor Link already exists'
              })

          linked_movie = Movie.query.filter_by(id=movie_id).first()
          linked_actor = Actor.query.filter_by(id=actor_id).first()

          result = {
              'success': True,
              'linked_movie': linked_movie.title,
              'linked_actor': linked_actor.name
            }

          return jsonify(result)

      else:
          abort(422)



  ## Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False,
                      "error": 422,
                      "message": "unprocessable",
                      }), 422

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          'success': False,
          'error': 401,
          'message': 'unauthorized'
      } , 401)

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed'
      }, 405)

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
      }, 500)

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code


  return app
app = create_app()