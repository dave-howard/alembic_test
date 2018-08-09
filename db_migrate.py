from Simple_Flask import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run() # run(commands="db init")?

"""
Usage:
python db_migrate.py db init  =  create migrations folder/content
python db_migrate.py db migrate -m "description" = create a new version script in migrations/versions folder
python db_migrate.py db upgrade = upgrade the database to last version
python db_migrate.py db downgrade = downgrade database to previous version

run 'init' once for a database
run migrate after sqlalchemy models have been updated
run upgrade to actually change the the database (add tables, relationships or columns)
beware: if you remove a field, or change a table name data will be dropped and lost
"""

