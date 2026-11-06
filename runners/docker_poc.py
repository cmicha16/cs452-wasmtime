import subprocess
import time
import statistics

IMAGE = "cs452-benchmark:docker"
COMMAND = ["docker", "run", "--rm", "-i", IMAGE]


def launch():
    start = time.perf_counter_ns()

    process = subprocess.Popen(
        COMMAND,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    ready = process.stdout.readline().strip()

    if ready != "READY":
        raise RuntimeError(f"Unexpected startup: {ready}")

    startup_ms = (time.perf_counter_ns() - start) / 1_000_000

    return process, start, startup_ms


def request(process):
    start = time.perf_counter_ns()

    process.stdin.write("RUN 10000\n")
    process.stdin.flush()

    result = process.stdout.readline().strip()

    latency_ms = (time.perf_counter_ns() - start) / 1_000_000

    if result != "RESULT 1229":
        raise RuntimeError(f"Unexpected result: {result}")

    return latency_ms


def stop(process):
    process.stdin.write("QUIT\n")
    process.stdin.flush()
    process.stdin.close()
    process.wait(timeout=10)


print("=== COLD START ===")

for trial in range(1, 4):
    process, start, startup_ms = launch()

    request(process)

    total_ms = (time.perf_counter_ns() - start) / 1_000_000

    stop(process)

    print(
        f"Trial {trial}: "
        f"Startup={startup_ms:.3f} ms, "
        f"Cold Total={total_ms:.3f} ms"
    )


print("\n=== WARM EXECUTION ===")

process, _, _ = launch()

# Warm-up requests (not measured)
for _ in range(3):
    request(process)

# Measured warm requests
latencies = []

for _ in range(10):
    latency = request(process)
    latencies.append(latency)

stop(process)

print(f"Warm requests: {len(latencies)}")
print(f"Mean latency: {statistics.mean(latencies):.3f} ms")
print(f"Median latency: {statistics.median(latencies):.3f} ms")

print("\nBenchmark completed successfully!")