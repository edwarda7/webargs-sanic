import os
import argparse
import yaml
from pathlib import Path
from dotenv import load_dotenv
import logging.config
from sanic import Sanic

from extentions.exceptions import blueprint as ext_exceptions
from extentions.middlewares import blueprint as ext_middlewares

from app import blueprint as app_blueprint


# Command line parser options & setup default values
parser = argparse.ArgumentParser()
parser.add_argument('--host', help='Setup host ip to listen up, default to 0.0.0.0', default='0.0.0.0')
parser.add_argument('--port', help='Setup port to attach, default to 8080', default='8080')
parser.add_argument('--workers', help='Setup workers to run, default to 1', type=int, default=1)
parser.add_argument('--debug', help='Enable or disable debugging', action='store_true')
parser.add_argument('--accesslog', help='Enable or disable access log', action='store_true')
args = parser.parse_args()

env_path = Path(__file__).absolute().parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure Sanic apps
app = Sanic(__name__, load_env=os.environ.get("ENV_PREFIX", "SANIC_"))

# Config logging system
with open(app.config['LOG_CFG']) as fobj:
    logging.config.dictConfig(yaml.safe_load(fobj))

# Install extentions
app.blueprint(ext_exceptions)
app.blueprint(ext_middlewares)

# Install app
app.blueprint(app_blueprint, url_prefix='/')

# Running sanic, we need to make sure directly run by interpreter
# ref: http://sanic.readthedocs.io/en/latest/sanic/deploying.html#running-via-command
if __name__ == '__main__':
    app.run(
        host=args.host,
        port=args.port,
        workers=args.workers,
        debug=args.debug,
        access_log=args.accesslog
    )