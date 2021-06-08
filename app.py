import flask 
import os
import sys
import logging
import logging.handlers

from flask import Flask
print(sys.path)
from front.front import front_end
from back.users.UserServices import users_page
from back.matchs.MatchServices import matchs_page
from back.bets.BetsServices import bets_page
from back.tools.Tools import tools_page


application = Flask(__name__, static_url_path='', static_folder="")
application.secret_key = u'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT#BB'

application.register_blueprint(front_end, url_prefix="/front", template_folder='templates')
application.register_blueprint(users_page, url_prefix="/back/users", template_folder='templates')
application.register_blueprint(matchs_page, url_prefix="/back/matchs", template_folder='templates')
application.register_blueprint(tools_page, url_prefix="/back/tools", template_folder='templates')
application.register_blueprint(bets_page, url_prefix="/back/bets", template_folder='templates')


print(sys.path)

application.logger.warning('Started')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logging.basicConfig(filename='bet.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

logger = logging.getLogger(__name__)
logger.addHandler(ch)


logger.info('Started')

# Get application version from env
app_version = os.environ.get('APP_VERSION')

# Get cool new feature flag from env
enable_cool_new_feature = os.environ.get('ENABLE_COOL_NEW_FEATURE') in ['true', 'True']

@application.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0, no-cache, no-store, must-revalidate'
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    #logger.info(u'response.headers={}'.format(response.headers))
    return response

@application.route("/")
def hello_world():
    logger.info("application.static_folder={}".format(str(application.static_folder)))
    logger.info("before lauch index")
    return application.send_static_file('index.html')

@application.route('/yeah')
def yo():
    return 'yooooooooooooooooooooooooo'

@application.route('/hello')
def yeah():
    return 'Hello, World'


@application.errorhandler(404)
def ma_page_404(error):
	return u"Page not found !<br/> <h1>404 error code !</h1> <h1>Where do you really want to go ?</h1>", 404

if __name__ == '__main__':
    print("main app.py application.run")
    application.run(host='0.0.0.0', port=os.environ.get('OPENSHIFT_PYTHON_PORT', 5000))