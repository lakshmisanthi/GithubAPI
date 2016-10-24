#!/usr/bin/python
import sys
import requests
import json
import pprint
from threading import Thread
import time
import Queue

# Get argvs from command line
q = sys.argv[1]
sort = sys.argv[2]
order = sys.argv[3]

# Get repositoires
def get_repos(arg, queue):
    r = requests.get('https://api.github.com/search/repositories?'+q+'&'+sort+'&'+order+'&per_page=100&page='+arg)
    if(r.ok):
        repoItem = json.loads(r.text or r.content) # Load data in json format
        queue.put({arg: repoItem})


def api_call():
    arguments = ('1', '2', '3', '4', '5')
    q = Queue.Queue()
    threads = []

    # Multiple calls
    for argument in arguments:
        t = Thread(target=get_repos, args=(argument, q)) # thread creating
        t.start() # thread started
        threads.append(t)

    for t in threads:
        t.join()

    # return all repositories data
    return [q.get() for _ in xrange(len(arguments))]

# printed data
pprint.pprint(api_call())

