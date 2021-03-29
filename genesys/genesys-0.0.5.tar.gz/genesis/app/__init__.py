from flask import Flask
from . import config
app = Flask('genesis')

from genesis.app.blueprints.project.routes import project
from genesis.app.blueprints.task.routes import task
from genesis.app.blueprints.asset.routes import asset

app.register_blueprint(project)
app.register_blueprint(task)
app.register_blueprint(asset)
app.config.from_object(config)
