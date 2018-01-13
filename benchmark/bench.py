import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager, suppress

import click
import requests

session = requests.Session()


@contextmanager
def timeit():
    t1 = time.time()
    yield
    print("Time Elapsed: %.2f" % (time.time() - t1))


def get_random_block_body():
    million = 1000000
    block_num = random.randint(15 * million, 18 * million)
    body = {
        'jsonrpc': '2.0', 'id': block_num, 'method': 'call',
        'params': ['database_api', 'get_block', (block_num,)]
    }
    return json.dumps(body)


def get_random_block(steemd_url):
    with suppress(Exception):
        return session.post(
            steemd_url,
            data=get_random_block_body()).text


def benchmark_get_blocks(steemd_url, num_of_requests, max_workers=100):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = (executor.submit(get_random_block, steemd_url)
                   for _ in range(num_of_requests))
        for _ in as_completed(futures):
            continue


@click.command()
@click.argument('node-url', default="https://api.steemit.com")
@click.argument('num-of-requests', default=1000)
def benchmark(node_url, num_of_requests):
    print("Getting %d random blocks from %s" % (num_of_requests, node_url))
    with timeit():
        benchmark_get_blocks(node_url, num_of_requests)


if __name__ == '__main__':
    benchmark()
