#! C:\Users\carljame\Envs python

from flask import url_for
from flask.ext.testing import TestCase

import j34dvd
from j34dvd.models import User, Dvds

class J34dvdTestCase(TestCase):

    def create_app(self):
        return j34dvd.create_app('test')

    def setUp(self):
        self.db = j34dvd.db
        self.db.create_all()
        self.client = self.app.test_client()

        u = User(username='test', email='test@example.com', password='testpassword')
        dvd = Dvds(user=u, title="Jurasic World", binder="leather", page="24", sleeve="2",
                   imdb_page="http://www.imdb.com/title/tt0369610/",
                   tags="live action,kids,sci-fi")
        self.db.session.add(u)
        self.db.session.add(dvd)
        self.db.session.commit()

        self.client.post(url_for('auth.login'),
                         data = dict(username='test', password='testpassword'))

    def tearDown(self):
        j34dvd.db.session.remove()
        j34dvd.db.drop_all()

    def test_delete_all_tags(self):
        response = self.client.post(
            url_for('dvds.edit_dvd', dvd_id=1),
            data = dict(
                title="Jurasic World",
                tags="Changed",
                binder="leather",
                page="24",
                sleeve="2",
                imdb_page="http://www.imdb.com/title/tt0369610/"
            ),
            follow_redirects = True
        )

        assert response.status_code == 200
        dvd = Dvds.query.first()
        assert not dvd._tags
