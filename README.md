# Ws Server

## General

As default, the app will serve as a websocket server.

## Http Server

If run the app with following commands, the app will act as the http server to output text generation.

``` Bash
    python3 app.py
```

## Dev
```
    docker run -it -d --name dev-ws-server -v /etc/localtime:/etc/localtime:ro -v $(pwd)/ws_server:/workspace -w /workspace --net host ws-server/base:v1.0.0 bash
```
