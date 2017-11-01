from ..citadel_helper import *

from uuid import uuid4
import json
import random
import pdb
import math
import time
from ..common import benchmark_one
from copy import deepcopy

def gen_uuid():
    return str(uuid4())

# Configuration
tot_num = 10000
worker_num = 4
gen_point_types_flag = False
gen_unit_flag = False
gen_point_flag = True
point_creation_flag = True
query_by_name_flag = True
query_by_pointtype_flag = True

# Dummy point hierarchy define
if gen_point_types_flag:
    span = 4
    depth = 3
    curr_layer = []
    subclass_dict = dict()
    point_types = []
    if not curr_layer:
        curr_layer = [gen_uuid() for _ in range(0, span)]
        point_types += curr_layer
    for _ in range(0, depth):
        prev_layer = curr_layer
        curr_layer = []
        for point_type in prev_layer:
            for _ in range(0, span):
                new_point_type = gen_uuid()
                point_types.append(new_point_type)
                subclass_dict[point_type] = new_point_type
                curr_layer.append(new_point_type)
    with open('temp/point_types.json', 'w') as fp:
        json.dump(point_types, fp, indent=2)
    with open('temp/subclass_dict.json', 'w') as fp:
        json.dump(subclass_dict, fp, indent=2)
else:
    with open('temp/point_types.json', 'r') as fp:
        point_types = json.load(fp)
    with open('temp/subclass_dict.json', 'r') as fp:
        subclass_dict = json.load(fp)

if gen_unit_flag:
    unit_num = 50
    units = [gen_uuid() for _ in range(0, unit_num)]
    with open('temp/unit.json', 'w') as fp:
        json.dump(units, fp, indent=2)
else:
    with open('temp/unit.json', 'r') as fp:
        units = json.load(fp)

# Generate multiple points
if gen_point_flag:
    points = []
    for i in range(0, tot_num):
        point = {
            'pointType': random.sample(point_types, 1)[0],
            'unit': random.sample(units, 1)[0],
            'name': gen_uuid()
        }
        points.append(point)
    with open('temp/points.json', 'w') as fp:
        json.dump(points, fp, indent=2)
else:
    with open('temp/points.json', 'r') as fp:
        points = json.load(fp)
    assert len(points) == tot_num


################### Point creation benchmark
if point_creation_flag:
    print('Start running point creation')
    def point_create_test_func(points):
        delay = 0
        cnt = 0
        for point in points:
            begin_time = time.time()
            res = create_point(point)
            end_time = time.time()
            if not res:
                print('Cannot create point')
            delay += end_time - begin_time
            cnt += 1
        delay /= cnt
        return delay


    args_list = [(points[math.floor(tot_num/worker_num*i):
                        math.floor(tot_num/worker_num*(i+1))], )
                 for i in range(0, worker_num)]
    res = benchmark_one(point_create_test_func, args_list, worker_num)
    print('Point Creation Latency: {0} seconds.'.format(res['avg_delay']))
    #res = point_create_test_func(points)


################### Point query by name
if query_by_name_flag :
    print('Start querying point by name')
    iter_num = 10000
    def query_by_name_test_func(names, iter_num):
        delay = 0
        cnt = 0
        for i in range(0, iter_num):
            try:
                name = random.sample(names, 1)[0]
                begin_time = time.time()
                res = find_points({'name': name})
                end_time = time.time()
                if not res:
                    print('Cannot create point')
                delay += end_time - begin_time
                cnt += 1
            except:
                continue
        delay /= cnt
        print('actual iteration: {0}'.format(cnt))
        return delay
    names = [point['name'] for point in points]
    args_list = [(deepcopy(names), math.floor(iter_num/worker_num))
                 for _ in range(0, worker_num)]
    res = benchmark_one(query_by_name_test_func, args_list, worker_num)
    print('Point Query by Name Latency: {0} seconds.'.format(res['avg_delay']))


################### Query by point type

if query_by_pointtype_flag:
    print('Start querying point by point type')
    iter_num = 10000
    def query_by_pointtype_test_func(point_types, iter_num):
        delay = 0
        cnt = 0
        for i in range(0, iter_num):
            try:
                pointtype = random.sample(point_types, 1)[0]
                begin_time = time.time()
                res = find_points({'pointType': pointtype})
                end_time = time.time()
                if not res:
                    print('Cannot create point')
                delay += end_time - begin_time
                cnt += 1
            except:
                continue
        delay /= cnt
        print('actual iteration: {0}'.format(cnt))
        return delay
    args_list = [(deepcopy(point_types), math.floor(iter_num/worker_num))
                 for _ in range(0, worker_num)]
    res = benchmark_one(query_by_pointtype_test_func, args_list, worker_num)
    print('Point Query by Name Latency: {0} seconds.'.format(res['avg_delay']))

