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
python3 [blocks|vops] <steemd_url> <number_of_requests>
```


### Benchmark Random Block Fetching
```
python3 bench.py blocks http://localhost:8090 10000
```
_10000_ is the number of random blocks to fetch.

### Benchmark Random Virtual-Ops Fetching
```
python3 bench.py vops http://localhost:8090 10000
```

### Changing number of threads
Global threads max can be set with the `--threads` flag.
The default is `100`.

Increasing the number of threads _may_ improve performance.
```
python3 bench.py --threads 200 blocks http://localhost:8090 10000
```
