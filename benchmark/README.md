## Steemd RPC Benchmark Tool
This tool will bechmark _steemd_ nodes for random block access performance.

### Installation (Ubuntu 16.04+)

Install dependencies:
```
sudo apt install -y python3 python3-pip
sudo pip3 install -r requirements.txt
```

### Run the script
```
python3 bench.py http://localhost:8090 10000
```
_10000_ is the number of random blocks to fetch.

