# Docker notes

- Docker version: Docker version 29.1.3, build 29.1.3-0ubuntu3~22.04.2
- Base images: rust:1.99.1-bookworm (build), debian:bookworm-slim (runtime)
- Build command: docker build -f container/Dockerfile -t cs452-benchmark:docker .
- Run command: docker run -i --rm cs452-benchmark:docker
- Host: Linux 6.18.54.1-microsoft-standard-WSL2 x86_64 (WSL2), same machine as the Wasmtime pilot

## Test vector
RUN 10000 -> RESULT 1229, RUN 1000 -> RESULT 168 (identical to native and Wasm builds)

## Pilot results (5 cold trials, 10 warm requests, N=10000, preliminary)
- Cold startup median: about 876 ms (range 812-904 ms)
- Cold total median: about 878 ms
- Warm latency median: about 1.23 ms (range 0.99-1.53 ms)
- Warm requests go through the docker client and daemon, so they include some stdin/stdout forwarding overhead.
