# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the project  directory first ensure you are working using your created virtual environment.
Navigate to `backend` after activating virtual environment

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Created a new Auth0 Account
2. Selected a unique tenant domain
3. Created a new, single page web application
4. Created a new API `(movietestapi)`
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `view:movies`
    - `edit:movie`
    - `add:movie`
    - `delete:movie`
    - `view:actors`
    - `edit:actor`
    - `add:actor`
    - `delete:actor`
    - `link:cast`
6. Create new roles for:
    - Cast Assistant-
        Can do the following:
        - `view:movies`, 
        - `view:actors`
    - Manager-
        Can perform all from Cast Assitant and:
        - `edit:movie`
        - `edit:actor`
        - `add:actor`
        - `delete:actor`
    - Executive Producer-
        Can perform all from Cast Assitant and:
        - `add:movie`
        - `delete:movie`
        - `link:cast`

## API DOCUMENTATION

### List Of Endpoints:

- GET '/actors'
- POST '/actors'
- PATCH '/actors/<id>'
- DELETE '/actors/<id>'
- GET '/movies'
- POST '/movies'
- PATCH '/movies/<id>'
- DELETE '/movies/<id>'
- POST '/link/'

### GET '/actors'
```
- Handles GET requests Returns a list of actors and what movies they are linked to.

```
### POST '/actors
```
- Uses POST request to add Actor and its properties to Database

- Request Arguments: json body header in the following format:
{
    "name": "Makudeni Goluchu",
    "age": 34,
    "gender": "Male"
}


```
### PATCH '/actors/<id>'
```
- This endpoint will EDIT actors with the specified actor ID. 

- Request Arguments: Actor ID (int)

```

### DELETE '/actors/<id>'
```
- This endpoint will DELETE actors with the specified actor ID. This also deletes the link with the Movies associated with it where applicable.

- Request Arguments: Actor ID (int)

```

### GET '/movies'
```
- Handles GET requests Returns a list of movies and what actors they are linked to.

```
### POST '/movies
```
- Uses POST request to add Movie and its properties to Database

- Request Arguments: json body header in the following format:
{
    "title": "Revenge of the Black Ninja",
    "releasedate": 2005
}

```
### PATCH '/movies/<id>'
```
- This endpoint will EDIT movies with the specified movie ID. 

- Request Arguments: Movie ID (int)

```

### DELETE '/movies/<id>'
```
- This endpoint will DELETE movies with the specified movie ID. This also deletes the link with the Actors associated with it where applicable.

- Request Arguments: Movie ID (int)

```
### POST '/link
```
- Uses POST request to link an Actor with a Movie to create an association in the Database

- Request Arguments: json body header in the following format:
{
    "movie_id": 1,
    "actor_id": 1
}

```

## Testing

To run the tests, I used unittest module. The test code is as shown in this file `test_api.py`. A new sqlite database will be created when test is scheduled. See command below:

```
python3 test_api.py -v

```

The following tests were conducted:
TEST 1: TEST ACCESS TO ADD ACTORS WITHOUT AUTH
TEST 2: TEST ACCESS TO ADD ACTORS WITH insufficient PERMISSION (AS CAST ASSISTANT)
TEST 3: TEST ACCESS TO ADD ACTORS WITH SUFFICIENT PERMISSION (AS CAST DIRECTOR)
TEST 4: TEST ACCESS TO VIEW ACTORS WITHOUT AUTH
TEST 5: TEST ACCESS TO VIEW ACTORS WITH SUFFICIENT PERMISSION (AS CAST ASSISTANT)
TEST 6: TEST ACCESS TO ADD MOVIES WITH INSUFFICIENT PERMISSION (AS CAST DIRECTOR)
TEST 7: TEST ACCESS TO ADD MOVIES WITH SUFFICIENT PERMISSION (AS EXECUTIVE PRODUCER)
TEST 8: TEST ACCESS TO VIEW MOVIES
TEST 9: TEST ACCESS TO LINK MOVIES TO ACTORS (AS EXECUTIVE PRODUCER)
TEST 10: TEST ACCESS TO EDIT ACTOR (AS CAST DIRECTOR)
TEST 11: TEST ACCESS TO EDIT MOVIE (AS CAST DIRECTOR)
TEST 12: TEST ACCESS TO DELETE ACTOR (AS CAST DIRECTOR) [WITH PERMISSION]
TEST 13: TEST ACCESS TO DELETE MOVIE (AS CAST DIRECTOR) [NO PERMISSION]
TEST 14: TEST ACCESS TO DELETE MOVIE (AS EXECUTIVE PRODUCER) [with PERMISSION]


#### Results
See below for the results of the tests:
``` bash
$ python3 test_api.py -v
test_01_add_actor_no_auth (__main__.CastingTestCase) ... ok
test_02_add_actor_no_perm (__main__.CastingTestCase) ... ok
test_03_add_actor_with_perm (__main__.CastingTestCase) ... ok
test_04_view_actors_no_auth (__main__.CastingTestCase) ... ok
test_05_view_actors_with_perm (__main__.CastingTestCase) ... ok
test_06_add_movie_no_perm (__main__.CastingTestCase) ... ok
test_07_add_movie_with_perm (__main__.CastingTestCase) ... ok
test_08_view_movies (__main__.CastingTestCase) ... ok
test_09_actor_movie_link (__main__.CastingTestCase) ... ok
test_10_edit_actor (__main__.CastingTestCase) ... ok
test_11_edit_movie (__main__.CastingTestCase) ... ok
test_12_delete_actor_with_perm (__main__.CastingTestCase) ... ok
test_13_delete_movie_no_perm (__main__.CastingTestCase) ... ok

----------------------------------------------------------------------
Ran 13 tests in 2.143s
```
