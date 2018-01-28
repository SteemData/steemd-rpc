## A basic http steemd proxy
Distribute a load over different steemd nodes (prototype).

### Run
```
docker run --name steemd-proxy -p 80:80 \
    -v /home/user/GitHub/SteemData/steemd-rpc/proxy/nginx.conf:/etc/nginx/nginx.conf \
    -d nginx
```