import requests
import time
from multiprocessing import Manager, Process
from math import floor
import numpy as np

def parallel_func(orig_func, return_idx, return_dict, *args):
    return_dict[return_idx] = orig_func(*args)

def test_func(iter_range, url, payload):
    delay = 0
    #url = "http://132.239.10.165:8080/test/2"
    for i in iter_range:
        begin_time = time.time()
        resp = requests.post(url, json=payload)
        end_time = time.time()
        assert resp.status_code == 200
        delay += end_time - begin_time
    delay /= (iter_range[-1] - iter_range[0])
    return delay

def benchmark_one(func, args_list, worker_num=4, iter_num=5000):
    assert len(args_list) == worker_num
    manager = Manager()
    result_dict = manager.dict()

    p_list = list()
    for i in range(0, worker_num):
        #iter_range = range(0, floor(iter_num / worker_num))
        #args = (iter_range, url, data)
        args = args_list[i]
        p = Process(target=parallel_func, args=(test_func, i, result_dict, *args))
        p_list.append(p)
    for p in p_list:
        p.start()

    for p in p_list:
        p.join()

    tot_delay = np.mean(result_dict.values())

    print(tot_delay)
    return {
        'avg_delay': tot_delay
    }
