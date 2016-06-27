import webtest
import pytest
import flask
import liveprofiler_sampler

SAMPLER_INTERVAL = 1
PROFILING_SECRET = 'secret'

application = flask.Flask(__name__)

@application.route('/')
def index():
    return 'app_endpoint'

@application.route('/post_test', methods=['POST'])
def post_test():
    return 'app_endpoint'

@pytest.fixture()
def simple_app(request):
    with_middleware = liveprofiler_sampler.ProfilingMiddleware(application, SAMPLER_INTERVAL, PROFILING_SECRET)
    return webtest.TestApp(with_middleware)

@pytest.fixture()
def sampler(request):
    return liveprofiler_sampler.Sampler(0.001)
