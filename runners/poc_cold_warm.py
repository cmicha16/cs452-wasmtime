import subprocess
import sys
import time

CMD = sys.argv[1:]
N = 10000
EXPECTED = "RESULT 1229"


def start():
    t0 = time.perf_counter_ns()
    p = subprocess.Popen(CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
    ready = p.stdout.readline().strip()
    t1 = time.perf_counter_ns()
    assert ready == "READY", ready
    return p, t0, t1


def run(p, n):
    s = time.perf_counter_ns()
    p.stdin.write(f"RUN {n}\n")
    p.stdin.flush()
    reply = p.stdout.readline().strip()
    e = time.perf_counter_ns()
    return reply, (e - s) / 1e6


def stop(p):
    p.stdin.write("QUIT\n")
    p.stdin.flush()
    p.wait()


print("COLD")
for i in range(5):
    p, t0, t1 = start()
    reply, _ = run(p, N)
    t2 = time.perf_counter_ns()
    stop(p)
    assert reply == EXPECTED, reply
    print(f"trial {i}: startup_ms={(t1 - t0) / 1e6:.2f} cold_total_ms={(t2 - t0) / 1e6:.2f}")

print("WARM")
p, _, _ = start()
for _ in range(3):
    run(p, N)
for i in range(10):
    reply, ms = run(p, N)
    assert reply == EXPECTED, reply
    print(f"request {i}: latency_ms={ms:.3f}")
stop(p)
