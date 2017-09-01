import requests
import time
from multiprocessing import Manager, Process
import math
import numpy as np

from common import *

def test_func(iter_range, url, payload):
    delay = 0
    for i in iter_range:
        begin_time = time.time()
        resp = requests.post(url, json=payload)
        end_time = time.time()
        assert resp.status_code == 200
        delay += end_time - begin_time
    delay /= (iter_range[-1] - iter_range[0])
    return delay


worker_num = 4
iter_num = 5000
# Test empty API
args_list = []
url = "http://132.239.10.165:8080/test/2"
data = {
    'query': {
        'min_lat': 50,
        'min_lng': 100,
        'max_lat': 60,
        'max_lng': 150
    }
}
for i in range(worker_num):
    args_list.append((range(0, math.ceil(iter_num/worker_num)), url, data))
#res = benchmark_one(test_func, args_list, worker_num, iter_num)

# Test real data query
args_list = []
url = "http://132.239.10.165:8080/api/querydata/simplebbox"
data = {
    'query': {
        'min_lat': 32,
        'min_lng': -118,
        'max_lat': 34,
        'max_lng': -117
    }
}
for i in range(worker_num):
    args_list.append((range(0, math.ceil(iter_num/worker_num)), url, data))
res = benchmark_one(test_func, args_list, worker_num, iter_num)

print('REAL DATA QUERY DELAY: {0}'.format(res))
