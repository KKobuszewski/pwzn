# -*- coding: utf-8 -*-
import requests
import hashlib
from multiprocessing.pool import ThreadPool
from multiprocessing import Queue, Process
import numpy as np
import bs4
import sys

adress = "http://localhost:4444/"
res = requests.post(adress + "login", {"uname": "foo", "password": "bar"}, allow_redirects=False)


def process(q_out, q_in):
    while True:
        item = q_in.get()
        print(item)
        data = requests.get(adress + item[0], cookies=res.cookies)
        bs = bs4.BeautifulSoup(data.text)
        for href in bs.findAll('a'):
            q_out.put((href.text, item[1] - 1))
"""
if __name__ == '__main__':
    q_in, q_out = Queue(), Queue()
    q_out.put(("2516972517", 5))
    processes = []
    for ii in range(4):
        p = Process(target=process, args=(q_in, q_out))
        p.start()
        processes.append(p)
    result = []
    links = []
    while True:
        try:
            item = q_in.get()
            if item[1] > 0:
                q_out.put(item)
            else:
                links.append(item[0])
        except:
            for p in processes:
                p.terminate()
            print(links)
            exit()
"""

def getLinks(queue_out, queue_in, session, address):
    ii = 0
    while True:
        if ii==0:
            sys.stdout.write("\ \r")
            sys.stdout.flush()
        elif ii==1:
            sys.stdout.write("/ \r")
            sys.stdout.flush()
        else:
            sys.stdout.write("- \r")
            sys.stdout.flush()
        ii = (ii+1)%3
        i, to_explore = queue_in.get()
        resp = session.get(address+"/237931237970/"+to_explore)
        links = [ link['href'] for link in bs4.BeautifulSoup(resp.text).findAll('a') ]
        queue_out.put((i+1, links))

if __name__ == '__main__':
    #address = "http://194.29.175.134:4444"
    address = "http://127.0.0.1:4444"
    headers = {
    "uname": "foo",
    "password":"bar"
    }
    levels = 4
    queue_in, queue_out = Queue(), Queue()
    session = requests.session()
    session.post(address+"/login", params=headers, allow_redirects=False)
    resp = session.get(address+"/237931237970")
    links = [ link['href'] for link in bs4.BeautifulSoup(resp.text).findAll('a') ]
    result = []

    for i in range(levels+1):
        result.append(['level '+str(i)])
        result[0]+=links
        processes = []

    for i in range(4):
        p = Process(target=getLinks, args=(queue_in, queue_out, session, address))
        p.start()
        processes.append(p)

    for link in links:
        queue_out.put((0, link))

    while True:
        try:
            level, links = queue_in.get(timeout=1)
        except Exception:
            break
        result[level]+=links
        if level < levels:
            for link in links:
                queue_out.put((level, link))

    for pr in processes:
        pr.terminate()
    for elem in result:
        print(len(elem)-1)
        print(elem)
