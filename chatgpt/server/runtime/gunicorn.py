bind = '0.0.0.0:5000'
workers = 16
backlog = 2048
worker_class = 'gevent'
max_requests = 1000
max_requests_jitter = 20
timeout = 300
proc_name = 'tmp/gunicorn.proc'
pidfile = 'tmp/gunicorn.pid'
logfile = 'logs/gunicorn.log'
loglevel = 'info'
errorlog = 'logs/gunicorn_error.log'
accesslog = 'logs/gunicorn_access.log'
access_log_format = """
    %(h)s %({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
"""
