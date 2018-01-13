# Original: https://github.com/steemit/jussi/blob/master/contrib/perf/batch_size_perf.py
#
# MIT License
#
# Copyright (c) 2017
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# -*- coding: utf-8 -*-
# pylint: skip-file
import logging
import os
import sys
import time

import requests

s = requests.Session()

sys.path.append(os.path.dirname(__file__))
logger = logging.getLogger(__name__)


def chunkify(iterable, chunksize=10000):
    i = 0
    chunk = []
    for item in iterable:
        chunk.append(item)
        i += 1
        if i == chunksize:
            yield chunk
            i = 0
            chunk = []
    if len(chunk) > 0:
        yield chunk


def make_batch_request(rpc_url, batch):
    resp = s.post(rpc_url, json=batch)
    return resp


def show_results(results, total=2000):
    for batch_size, start, end, resp_time in results:
        elapsed = end - start
        rps = batch_size / elapsed
        print(
            'batch size: %s '
            'elapsed: %.2fs '
            '(%.2f requests/s) '
            % (batch_size, elapsed, rps))


if __name__ == '__main__':
    bench_size = 2000
    block_nums = list(range(18_000_000, 18_000_000+bench_size))
    rpc_reqs = [
        {
            "method": "get_block", "params": [block_num],
            "jsonrpc": "2.0", "id": 0
        } for block_num in block_nums]
    results = []
    for batch_size in range(1, 500, 50):
        print('Making JSONRPC requests in batch of %s' % batch_size)

        # print(resp)
        for test in range(1, 3):
            batches = list(chunkify(rpc_reqs, batch_size))
            resp = make_batch_request('https://api.steemit.com', batches[0])
            start = time.perf_counter()
            resp = make_batch_request('https://api.steemit.com', batches[0])
            end = time.perf_counter()
            results.append((batch_size, start, end, resp.elapsed))
    show_results(results)
