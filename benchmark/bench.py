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


def get_random_block_num():
    million = 1000000
    return random.randint(15 * million, 18 * million)


def get_random_block_body():
    block_num = get_random_block_num()
    body = {
        'jsonrpc': '2.0', 'id': block_num, 'method': 'call',
        'params': ['database_api', 'get_block', (block_num,)]
    }
    return json.dumps(body)


def get_random_vops_body():
    block_num = get_random_block_num()
    body = {
        'jsonrpc': '2.0', 'id': block_num, 'method': 'call',
        'params': ['database_api', 'get_ops_in_block', (block_num, True)]
    }
    return json.dumps(body)


def make_request(steemd_url, data):
    with suppress(Exception):
        return session.post(steemd_url, data=data).text


def run_benchmark(steemd_url, request_bodies, max_workers=100):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = (executor.submit(make_request, steemd_url, data)
                   for data in request_bodies)
        for _ in as_completed(futures):
            continue


@click.group(chain=True)
@click.option('--threads', default=100)
@click.pass_context
def cli(ctx, threads):
    ctx.obj['threads'] = threads


@cli.command('blocks')
@click.argument('node-url', default="https://api.steemit.com")
@click.argument('num-of-requests', default=1000)
@click.pass_context
def benchmark_blocks(ctx, node_url, num_of_requests):
    print("Getting %d random blocks from %s" % (num_of_requests, node_url))
    request_bodies = [
        get_random_block_body() for _ in range(num_of_requests)
    ]
    with timeit():
        run_benchmark(
            node_url,
            request_bodies,
            max_workers=ctx.obj['threads'])


@cli.command('vops')
@click.argument('node-url', default="https://api.steemit.com")
@click.argument('num-of-requests', default=1000)
@click.pass_context
def benchmark_blocks(ctx, node_url, num_of_requests):
    print("Getting %d random virtual-blocks from %s" % (num_of_requests, node_url))
    request_bodies = [
        get_random_vops_body() for _ in range(num_of_requests)
    ]
    with timeit():
        run_benchmark(
            node_url,
            request_bodies,
            max_workers=ctx.obj['threads'])


if __name__ == '__main__':
    cli(obj={})
