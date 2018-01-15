import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager, suppress
from prettytable import PrettyTable

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
def benchmark_vops(ctx, node_url, num_of_requests):
    print("Getting %d random virtual-blocks from %s" % (num_of_requests, node_url))
    request_bodies = [
        get_random_vops_body() for _ in range(num_of_requests)
    ]
    with timeit():
        run_benchmark(
            node_url,
            request_bodies,
            max_workers=ctx.obj['threads'])

@cli.command('auto')
@click.argument('node-url', default="https://api.steemit.com")
@click.argument('num-of-requests', default=10000)
def benchmark_auto(node_url, num_of_requests):
    t = PrettyTable(["Host", "Bench", "Requests", "Threads", "Time"])
    t.align = "l"

    for bench_fn in [get_random_block_body, get_random_vops_body]:
        for threads in [10, 50, 100, 250, 500, 1000]:
            click.echo("Making %d requests to %s [%s threads]"
                % (num_of_requests, node_url, threads))
            request_bodies = [
                bench_fn() for _ in range(num_of_requests)
            ]
            start = time.time()
            run_benchmark(
                node_url,
                request_bodies,
                max_workers=threads)
            end = time.time()
            diff = "%.2fs" % (end - start)
            t.add_row([
                node_url,
                bench_fn.__name__,
                num_of_requests,
                threads,
                diff,
            ])

    click.echo("\n>Results:")
    click.echo(t)

if __name__ == '__main__':
    cli(obj={})
