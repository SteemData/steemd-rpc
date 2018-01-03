**Install dependencies:**
```
apt update && apt upgrade -y
apt install -y tmux vim htop docker.io
```

**Setup required directories:**
```
cd /home
mkdir -p steem_shm
mkdir -p steem_rpc_data
```

**Copy configs**
```
scp fullnode.config.ini root@${SERVER_IP}:/home
```


                  
**Run it**    
```            
docker run -v /home/steem_rpc_data:/witness_node_data_dir \
           -v /home/fullnode.config.ini:/witness_node_data_dir/config.ini \
           -v /home/steem_shm:/home/steem_shm \
           -p 8090:8090 -d \
    furion/steemr
```