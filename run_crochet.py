from flask import Flask
from app import app
"""
If Twisted's WSGI server is not desired in favor for solutions like uwsgi or gunicorn or anything similar,
the `crochet` library can execute Twisted code in an isolated thread. Be EXTREMELY careful with this solution!
Python's WSGI servers generally use threads, as does `crochet`, and/or processes which means there might be
situations where one thread may spawn multiple threads. It's up to the developers to account for intricacies
hen dealing with multi threaded/process applications.
Local usage:
    python flask_crochet.py
Gunicorn usage:
    gunicorn -b 0.0.0.0:9000 flask_crochet:app
"""

# @app.route('/greeting')
# @app.route('/greeting/<name>')
# def greeting(name='World'):
#    return 'Hello %s!' % (name)


#if __name__ == '__main__':
app.run('0.0.0.0', 9000)
