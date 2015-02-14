# -*- coding: utf-8 -*-
import requests
import time
from multiprocessing.pool import ThreadPool

"""
N - liczba wątków
długość pilku
liczba części
"""

def load_data_from_web(website, n=1):
    """
    downloads data from given website as binary file
    :param website: url to be downloaded
    :return: file as binary string
    """
    response = requests.head(website)
    resp_len = int(response.headers['Content-Length'])
    print(resp_len)
    p = ThreadPool(n)
    try:
        step = int(resp_len/n)
        request_ranges = [(ii, min(resp_len, ii+step-1)) for ii in range(0, resp_len, step)]
        print(request_ranges)
        f = make_loader(website)
        data = p.map(f, request_ranges)
    finally:
        p.close()
        p.join()
    return merge_data(data)

def make_loader(website):
    return lambda x: load_fragment(website, x)


def load_fragment(website, request_range):
    response = requests.get(website,
                     headers = {
                        "Range": "bytes={}-{}".format(*request_range)
                    })
    return response

def merge_data(data):
    return b"".join([d.content for d in data])

if __name__ == '__main__':
    import hashlib
    start = time.monotonic()
    collected = load_data_from_web('http://db.fizyka.pw.edu.pl/pwzn-data/zaj7/rand-data-a', n=4)
    hash = hashlib.md5()
    hash.update(collected)
    print(hash.hexdigest(), '')
    print('czas pobierania mniejszego pliku:', time.monotonic()-start, 's')
    start = time.monotonic()
    collected = load_data_from_web('http://db.fizyka.pw.edu.pl/pwzn-data/zaj7/rand-data-b', n=4)
    hash = hashlib.md5()
    hash.update(collected)
    print(hash.hexdigest(), '')
    print('czas pobierania większego pliku:', time.monotonic()-start, 's')