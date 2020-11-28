import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import  setup_db, db, Actor, Movie, Link # db_create_all_if_table_doesnt_exist,

# Change the following tokens as required
exec_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjVhM2E5MGJkNGMyMDA2OGY2MTQ5MCIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjUzODU3MiwiZXhwIjoxNjA2NTQ1NzcyLCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJsaW5rOmNhc3RzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.I2leTpWWIQmLHVE1sLo-GG5a2nVrdNsRVSA8XbGpMkwg2kVMMlkzRmulo0Iy7u3LECTvl6bJS5qPxWOJp0UvbAMOjtJRrDlwpTA5-WQ379nY4om-S8nEFD4tBzMF_zpIjiC3kZqy_upfE-YHuvC1-eXTwKAUFnTPPLaGuUYGsVyI7i_gWO2pyDYVvg1YHsJsbuCdLjNcD-a78GC3sJ5Gcs_3wRwQgOPBSGJdqLJWqrTuHCg3j5SVvufX7xmyfV8Mn7vPR09qvDfij6yhjc6qYJd06RObPXpfohWLBDonRR6Cuhmik4foaKTWzxe1Zsxo8sm0Jk4i_EmKi0kAimWGlg'
dir_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjVhMzRlYTJkN2YzMDA2ZTZkYTEwMiIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjUzOTIxOSwiZXhwIjoxNjA2NTQ2NDE5LCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.M3UE_b0SFi1jpkCuPB-q0wxB-4PZO4Vnnour_X5H-dgy_zVJXERYeq1udHuR7-7lVzeEUm7mLAs19myb868G_ufLexCpxRsjcLmUJPwQb9FZVWQtIbBjlL-6zzTgvBFYDKZegJZjol0WJ_woa7IEmy5LUxSr4LPJymLJSlkswbOHDV7YggwmxpzLm5qvJkMOYmZuYIzaboPq-rYtzvqYhY5uXjqX7Cw7vymYyhowXQhisDMOi3nV33Top00OdTkAn8Lz5n4UMlWVDYIzDjImrObKLbcw4QTxlbqynb0eKKr9Q3xDYYZBWpmQ5QTUp1M_wY5jitATWH_nlmYdDedc3Q'
asst_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYzFkM2Q4YzNjNmYwMDA3NTgxY2I2MCIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjUzOTQ5MSwiZXhwIjoxNjA2NTQ2NjkxLCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.eojh9TqIabOM8qx5Nu2OXDF00ubDAWwbILQo427avTAlxC91epIH5xmpbZw0shaKe0k5CRQkGw99WGfXF5MeYepyVNu7QLkzVEtIU9FeFNDsdihJuuXurpfs1jmt37i_3MyF2iHACV2CNTqeZfaOO2x3UXbYts_FS9qU5NSXCXllahuVOXzydnjy2_MDYfQPtDgBhSMiKus3Vep4FR3fKH3YYbQb-caRQLtj8knyl1KTcOcstun7LPxzpbx-rKD1TERPEWemtOBMf1HLrNWR-N9xaozGBesBMQyTZQJIxeMnZRWHF_o1n37fggStm5avASfbQ8kIBCQXYiSteNQkOA'



class CastingTestCase(unittest.TestCase):


    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        self.database_filename = "casting_test.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))

        self.headers_asst = {'Content-Type': 'application/json',
                                  'Authorization': asst_token}
        self.headers_dir = {'Content-Type': 'application/json',
                                 'Authorization': dir_token}
        self.headers_exec = {'Content-Type': 'application/json',
                                 'Authorization': exec_token}


        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)


        self.add_actor = {"name": "Kiki Nkunku",
                          "age": 25,
                          "gender": "Female"}
        self.edit_actor = {"name": "PATCHED Kiki Nkunku",
                          "age": 99,
                          "gender": "Male"}
        self.add_link = {
                          "movie_id": 1,
                          "actor_id": 1
                        }
        self.add_movie = {
                            "title": "Malukani Junbulukeni",
                            "releasedate": 1983
                          }
        self.edit_movie = {
                            "title": "PATCHED Malukani Junbulukeni",
                            "releasedate": 9999
                          }

    def tearDown(self):
        """Executed after each test"""
        pass


    # TEST 1: TEST ACCESS TO ADD ACTORS WITHOUT AUTH
    def test_01_add_actor_no_auth(self):
        response = self.client().post('/actors', json=self.add_actor)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')

    # TEST 2: TEST ACCESS TO ADD ACTORS WITH insufficient PERMISSION (AS CAST ASSISTANT)
    def test_02_add_actor_no_perm(self):
        response = self.client().post('/actors', json=self.add_actor, headers=self.headers_asst)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # TEST 3: TEST ACCESS TO ADD ACTORS WITH SUFFICIENT PERMISSION (AS CAST DIRECTOR)
    def test_03_add_actor_with_perm(self):
        response = self.client().post('/actors', json=self.add_actor, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor'], 'Kiki Nkunku')

    # TEST 4: TEST ACCESS TO VIEW ACTORS WITHOUT AUTH
    def test_04_view_actors_no_auth(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')

    # TEST 5: TEST ACCESS TO VIEW ACTORS WITH SUFFICIENT PERMISSION (AS CAST ASSISTANT)
    def test_05_view_actors_with_perm(self):
        res = self.client().get('/actors', headers=self.headers_asst)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['actors'][0]['__name'], 'Kiki Nkunku')

    # TEST 6: TEST ACCESS TO ADD MOVIES WITH INSUFFICIENT PERMISSION (AS CAST DIRECTOR)
    def test_06_add_movie_no_perm(self):
        response = self.client().post('/movies', json=self.add_movie , headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # TEST 7: TEST ACCESS TO ADD MOVIES WITH SUFFICIENT PERMISSION (AS EXECUTIVE PRODUCER)
    def test_07_add_movie_with_perm(self):
        response = self.client().post('/movies', json=self.add_movie , headers=self.headers_exec)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie'], 'Malukani Junbulukeni')

    # TEST 8: TEST ACCESS TO VIEW MOVIES
    def test_08_view_movies(self):
      res = self.client().get('/movies', headers=self.headers_dir)
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertEqual(data['movies'][0]['__title'], 'Malukani Junbulukeni')

    # TEST 9: TEST ACCESS TO LINK MOVIES TO ACTORS (AS EXECUTIVE PRODUCER)
    def test_09_actor_movie_link(self):
        response = self.client().post('/link', json=self.add_link, headers=self.headers_exec)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['linked_actor'], 'Kiki Nkunku')
        self.assertEqual(data['linked_movie'], 'Malukani Junbulukeni')

    # TEST 10: TEST ACCESS TO EDIT ACTOR (AS CAST DIRECTOR)
    def test_10_edit_actor(self):
        response = self.client().patch('/actors/1', json=self.edit_actor, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_name'], 'PATCHED Kiki Nkunku')

    # TEST 11: TEST ACCESS TO EDIT MOVIE (AS CAST DIRECTOR)
    def test_11_edit_movie(self):
        response = self.client().patch('/movies/1', json=self.edit_movie, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie_title'], 'PATCHED Malukani Junbulukeni')

    # TEST 12: TEST ACCESS TO DELETE ACTOR (AS CAST DIRECTOR) [WITH PERMISSION]
    def test_12_delete_actor_with_perm(self):
        response = self.client().delete('/actors/1', headers=self.headers_dir)
        data = response.json
        actor = Actor.query.filter(Actor.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor'], 'PATCHED Kiki Nkunku')
        self.assertEqual(actor, None)

    # TEST 13: TEST ACCESS TO DELETE MOVIE (AS CAST DIRECTOR) [NO PERMISSION]
    def test_13_delete_movie_no_perm(self):
        response = self.client().delete('/movies/1', headers=self.headers_dir)
        data = response.json
        actor = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # TEST 14: TEST ACCESS TO DELETE MOVIE (AS EXECUTIVE PRODUCER) [with PERMISSION]
    def test_13_delete_movie_no_perm(self):
      response = self.client().delete('/movies/1', headers=self.headers_exec)
      data = response.json
      actor = Movie.query.filter(Movie.id == 1).one_or_none()
      self.assertEqual(response.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['deleted_movie'], 'PATCHED Malukani Junbulukeni')
      self.assertEqual(actor, None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()