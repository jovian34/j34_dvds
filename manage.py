#! C:\Users\carljame\Envs python

import os

from j34dvd import create_app, db

from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('prod')
manager = Manager(app)


migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
