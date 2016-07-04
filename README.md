[![CircleCI](https://circleci.com/gh/fieldaware/liveprofiler_sampler.svg?style=svg)](https://circleci.com/gh/fieldaware/liveprofiler_sampler)
[![PyPI version](https://badge.fury.io/py/liveprofiler_sampler.svg)](https://badge.fury.io/py/liveprofiler_sampler)

# Object and middleware for profiling live services

This is a package that should be used to profile python services on production. This is fallow up work based on https://github.com/nylas/nylas-perftools. So most of the credit goes to: nylas.com

To really understand what is going on here check this great blog post: https://www.nylas.com/blog/performance

# Usage

For wsgi applications you can this library as any other middleware. Here we have a little flask example:

```
from flask import Flask
app = Flask(__name__)

import liveprofiler_sampler
app.wsgi_app = liveprofiler_sampler.ProfilingMiddleware(app, interval=0.05, secret_header='secret')
app.run()


> curl -v localhost:5000/liveprofiler
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /liveprofiler HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.43.0
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 403 YOU SHALL NOT PASS!!!!!!!!!!!!1111oneoneonelephant
< Connection: close
< Server: Werkzeug/0.11.10 Python/2.7.8
< Date: Thu, 30 Jun 2016 15:30:21 GMT
<
* Closing connection 0

```

Our tiny app denied the request, because we should not expose our profiling data to anyone. The `secret_header` param passed to `ProfilingMiddleware` constructor is the secret value that protects our stacks. Passing the secret token will return a json ready to consume and visualise.

```
> curl curl --header "PROFILER_TOKEN: secret" -v localhost:5000/liveprofiler
* Rebuilt URL to: curl/
* Could not resolve host: curl
* Closing connection 0
curl: (6) Could not resolve host: curl
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 5000 (#1)
> GET /liveprofiler HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.43.0
> Accept: */*
> PROFILER_TOKEN: secret
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Connection: close
< Server: Werkzeug/0.11.10 Python/2.7.8
< Date: Thu, 30 Jun 2016 15:31:39 GMT
<
{"granularity": 0.05, "stacks": [{"count": 9, "frame": "<module>(__main__);start_ipython(IPython);launch_instance(traitlets.config.application);
start(IPython.terminal.ipapp);mainloop(IPython.terminal.interactiveshell);
interact(IPython.terminal.interactiveshell);run_cell(IPrt(IP...........
```

To visualize the data please check: https://github.com/fieldaware/liveprofiler
# Installation

To install the package simply type:

```
pip install liveprofiler_sampler
```

# uWSGI integration

Because sampler is implemented based on signals, you have to be aware of that when running your service under uWSGI.
In order to gather any samples you need to add following configuration to your uwsgi.ini
```
py-call-osafterfork = true  # enable child processes running cpython to trap OS signals
lazy-apps = true  # load apps in each worker instead of the master

```
