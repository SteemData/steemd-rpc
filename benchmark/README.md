## Steemd RPC Benchmark Tool
This tool will bechmark _steemd_ nodes for random block access performance.

### Installation (Ubuntu 16.04+)

Install dependencies:
```
sudo apt install -y python3 python3-pip
sudo pip3 install -r requirements.txt
```

## Usage
```
python3 bench.py [auto|blocks|vops] <steemd_url> <number_of_requests>
```

## Run the benchmark (Auto)
```
python3 bench.py auto http://localhost:8090
```

It should output something like this:
```
+-----------------------+-----------------------+----------+---------+---------+
| Host                  | Bench                 | Requests | Threads | Time    |
+-----------------------+-----------------------+----------+---------+---------+
| http://localhost:8090 | get_random_block_body | 1000     | 10      | 133.20s |
| http://localhost:8090 | get_random_block_body | 1000     | 50      | 51.01s  |
| http://localhost:8090 | get_random_block_body | 1000     | 100     | 55.63s  |
| http://localhost:8090 | get_random_block_body | 1000     | 250     | 50.77s  |
| http://localhost:8090 | get_random_vops_body  | 1000     | 10      | 2.87s   |
| http://localhost:8090 | get_random_vops_body  | 1000     | 50      | 1.87s   |
| http://localhost:8090 | get_random_vops_body  | 1000     | 100     | 2.19s   |
| http://localhost:8090 | get_random_vops_body  | 1000     | 250     | 1.79s   |
+-----------------------+-----------------------+----------+---------+---------+
```
_Note: Due to the random block selection, some variance is expected between each batch.
To reduce the variance, increase the number of requests as well as run the bench. multiple times._

### Benchmark Random Block Fetching
```
python3 bench.py blocks http://localhost:8090 1000
```
_10000_ is the number of random blocks to fetch.

### Benchmark Random Virtual-Ops Fetching
```
python3 bench.py vops http://localhost:8090 1000
```

### Changing number of threads
Global threads max can be set with the `--threads` flag.
The default is `100`.

Increasing the number of threads _may_ improve performance.
```
python3 bench.py --threads 200 blocks http://localhost:8090 1000
```
