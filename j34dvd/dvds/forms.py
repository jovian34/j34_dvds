__author__ = 'carljame'

from flask_wtf import Form
from wtforms.fields import StringField, IntegerField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Regexp

class DVDForm(Form):
    title = StringField('The title of the DVD', validators=[DataRequired()])
    binder = StringField('Binder or Bookcase')
    page = IntegerField('Page in the binder or shelf on bookcase')
    sleeve = IntegerField('Sleeve slot - left to right, top to bottom, front then back,'
                          'or case number on shelf left to right: ')
    imdb_page = URLField('Movie\'s IMDb Page URL', validators=[url()])
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                    message='Tags can only contain letters and numbers')])

    def validate(self):
        if not self.imdb_page.data.startswith('http://') or \
                self.imdb_page.data.startswith('https://'):
            self.imdb_page.data = 'http://' + self.imdb_page.data

        if not Form.validate(self):
            return False

        #filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ','.join(tagset)

        return True

