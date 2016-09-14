import json
import random
import redis
import time
import uuid

from settings import APP_SECRET, AUTH_USERNAME, AUTH_PASSWORD, REDIS, THROTTLE

from bottle import route, request, response, run, redirect, view

@route('/')
@view('page')
def index():
    if not request.get_cookie('sess', secret=APP_SECRET): response.set_cookie('sess', str(uuid.uuid4()), secret=APP_SECRET)
    msg = "You are logged in" if request.get_cookie('auth', secret=APP_SECRET) else "You are not logged in"
    return {
        'title': 'Index', 
        'message': msg, 
        'content': index_content(),
        'cookies': json.dumps(dict(request.cookies), indent=2),
        'ip': request.environ.get('REMOTE_ADDR')
    }

@route('/login', method='get')
@view('login')
def login_form():
    if not request.get_cookie('sess', secret=APP_SECRET): response.set_cookie('sess', str(uuid.uuid4()), secret=APP_SECRET)
    response.set_cookie('auth', str(uuid.uuid4()), expires=0)
    return {
        'title': 'Login', 
        'message': 'Please Log In', 
        'cookies': json.dumps(dict(request.cookies), indent=2),
        'ip': request.environ.get('REMOTE_ADDR')
    }

@route('/login', method='post')
def do_login():
    if not request.get_cookie('sess', secret=APP_SECRET): response.set_cookie('sess', str(uuid.uuid4()), secret=APP_SECRET)
    if authenticate(request.forms.get('username'), request.forms.get('password')):
        response.set_cookie('auth', str(uuid.uuid4()), secret=APP_SECRET)
        redirect('/')
    else:
        response.set_cookie('auth', str(uuid.uuid4()), expires=0)
        redirect('/login')

@route('/page/<id>')
@view('page')
def page(id):
    if not request.get_cookie('sess', secret=APP_SECRET): response.set_cookie('sess', str(uuid.uuid4()), secret=APP_SECRET)
    msg = "You are logged in" if request.get_cookie('auth', secret=APP_SECRET) else "You are not logged in"
    return {
        'title': 'Page {id}'.format(id=id), 
        'message':  msg, 
        'content': page_content(id),
        'cookies': json.dumps(dict(request.cookies), indent=2),
        'ip': request.environ.get('REMOTE_ADDR')
    }

@route('/throttled')
def throttled():
    usage_data = get_usage_data()
    response.set_header('X-App-Usage', json.dumps(usage_data))
    response.content_type = 'application/json'
    return json.dumps({'status': 'ok', 'usage_data': usage_data})

def get_usage_data():
    _redis = redis.Redis(**REDIS)
    now = int(time.time() * 1000)
    cutoff = now - THROTTLE['window']
    _redis.zremrangebyscore(THROTTLE['key'], 0, cutoff)
    reqs = _redis.zcard(THROTTLE['key'])
    if reqs >= THROTTLE['limit']:
        raise Exception('Limit Exceeded')
    _redis.zadd(THROTTLE['key'], str(now), now)
    usage = int((reqs / float(THROTTLE['limit'])) * 100)
    usage_data = {
        'foo': 0,
        'bar': 0,
        'baz': usage,
    }
    return usage_data

def index_content():
    links = []
    ids = random.sample(range(1, 1000), 20)
    for id in ids:
        links.append("<p><a href='/page/{id}'>{id}</a></li></p>".format(id=id))
    return "\n".join(links)


def page_content(id):
    return "This is page {id}".format(id=id)

def authenticate(username, password):
    return username == AUTH_USERNAME and password == AUTH_PASSWORD
    
run(host='0.0.0.0', port=8080, debug=True, reloader=True)
