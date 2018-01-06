**Install dependencies**
```
apt update && apt upgrade -y
apt install -y tmux vim htop docker.io
```

**Setup required directories**
```
mkdir -p /home/steem_rpc_data
```

**Create a swapfile**
```
fallocate -l 450G /home/swapfile
chmod 600 /home/swapfile
mkswap /home/swapfile
swapon /home/swapfile
```

**tmpfs**
```
mount -o remount,size=510G /dev/shm
```
_Make sure this is slightly more than the shm in fullnode.config.ini
Also, assuming 128GB ram and 450GB swap. Leave a bit for other apps/leaks._

**Copy configs**
```
scp fullnode.config.ini root@${SERVER_IP}:/home
```
                 
**Run it**    
```            
docker run -v /home/steem_rpc_data:/witness_node_data_dir \
           -v /home/fullnode.config.ini:/witness_node_data_dir/config.ini \
           -v /dev/shm:/steem_shm \
           -p 8090:8090 -d \
    furion/steemr
```

For replay, add: `/usr/local/bin/steemd --replay-blockchain`