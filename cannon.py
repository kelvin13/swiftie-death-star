import pytumblr
import time
import datetime
import random

from tumblr_keys import client

_urlchars = set('1234567890abcdefghijklmnopqrstuvwxyz-')

def _op(post):
    source_title = None
    if 'source_title' in post:
        source_title = post['source_title']
    
    try:
    # if source title is nonexistent or website
        if not source_title or not set(source_title) <= _urlchars:
            try:
                source_title = post['trail'][0]['blog']['name']
            except IndexError:
                # if root post
                source_title = post['blog_name']
            except KeyError:
                source_title = post['blog_name']
    except TypeError:
        print (post)
    
    return source_title

def _get_ammo(blog, N):
    if N == -1:
        N = 1989
    PP = []
    offset = 0
    while True:
        posts = client.posts(blog, limit=20, offset=offset, tag='N')['posts']
        if not posts:
            print('DONE')
            break
        PP += posts
        offset += 20
        if offset > N:
            PP = PP[:N]
            break

    return list(enumerate(PP))

def _sample(L, n):
    if n > len(L):
        n = len(L)
    return [ L[i] for i in sorted(random.sample(range(len(L)), n)) ]

def load(N, S, source):
    return _sample(_get_ammo(source, N), S)
    
def fire(POSTS, T1, T2, blog, live=False):
    U1 = T1.timestamp()
    U2 = T2.timestamp()
    for i, P in POSTS:
        print(str(i + 1) + '\t' + _op(P) + ': ' + P['summary'])
        
        key = P['reblog_key']
        I = P['id']
        T = random.randint(U1, U2)
        DATE = datetime.datetime.fromtimestamp(T).strftime('%Y-%m-%dT%H:%M:%S')
        print(datetime.datetime.fromtimestamp(T).strftime('%B %d, %Y at %I:%M %p'))

        if live:
            print(client.reblog(blog, reblog_key=key, id=I, publish_on=DATE))
        else:
            print('(dry run)')

# import deathstar
# import datetime

# P = load(-1, 15, '{BLOGNAME}')
# t1 = datetime.datetime(2016, month=1, day=7, hour=16, minute=59, second=0, microsecond=0)
# t2 = datetime.datetime(2016, month=1, day=7, hour=17, minute=30, second=0, microsecond=0)
# fire(P, t1, t2, '{BLOGNAME}', live=True)
