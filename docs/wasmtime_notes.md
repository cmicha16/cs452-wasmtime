# Wasmtime notes

- Wasmtime version: wasmtime 50.0.1 (c307ec81d 2026-10-29)
- Rust version: rustc 1.99.1 (58cf8f9c3 2026-10-13)
- Python version: Python 3.10.12
- Host: Linux 6.18.54.1-microsoft-standard-WSL2 x86_64 (WSL2)
- Run command: wasmtime run -C cache=n benchmark/target/wasm32-wasip1/release/benchmark.wasm

## Cache setting
Compilation cache appears to be active by default in this Wasmtime version (~/.cache/wasmtime/modules is created after the first run, no config file in ~/.config/wasmtime). Cache can be controlled with -C cache=y|n.

## Cold definition (proposed, to be agreed with Andreas)
Cold = new process per trial with compilation cache disabled (-C cache=n). Cache-enabled cold is recorded as a second condition.

## Pilot results (5 cold trials, 10 warm requests, N=10000, preliminary)
- Cold startup median, cache on: about 18 ms
- Cold startup median, cache off: about 55 ms
- Warm latency median: about 0.24-0.28 ms
- First cold trial with cache on (123 ms) included compilation.
