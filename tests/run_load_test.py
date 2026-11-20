"""
Standalone load test runner for PulseCare HMS using Python threading.
Simulates concurrent users hitting multiple endpoints and reports statistics.

Usage:
    python tests/run_load_test.py
"""
import threading
import time
import json
import statistics
import urllib.request
import urllib.error
from datetime import datetime

BASE_URL = "http://localhost:5000"
ENDPOINTS = [
    "/health",
    "/metrics",
    "/login",
    "/health",   # weight /health more
]

results_lock = threading.Lock()
all_results = {ep: {"success": 0, "fail": 0, "times": [], "errors": []} for ep in ENDPOINTS}
total_success = 0
total_fail = 0


def make_request(endpoint):
    global total_success, total_fail
    url = BASE_URL + endpoint
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HMS-LoadTest/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            _ = resp.read()
            elapsed = (time.perf_counter() - start) * 1000  # ms
            with results_lock:
                all_results[endpoint]["success"] += 1
                all_results[endpoint]["times"].append(elapsed)
                total_success += 1
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        with results_lock:
            all_results[endpoint]["fail"] += 1
            all_results[endpoint]["errors"].append(str(e)[:60])
            total_fail += 1


def run_wave(num_users, endpoints):
    """Simulate one wave of concurrent users."""
    threads = []
    for i in range(num_users):
        ep = endpoints[i % len(endpoints)]
        t = threading.Thread(target=make_request, args=(ep,), daemon=True)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)


def main():
    print("=" * 60)
    print("PulseCare HMS — Load Test Report")
    print(f"Target: {BASE_URL}")
    print(f"Endpoints: {', '.join(ENDPOINTS)}")
    print("=" * 60)

    # Warmup
    print("\n[Phase 0] Warmup (5 requests)...")
    run_wave(5, ENDPOINTS)
    time.sleep(1)

    # Reset after warmup
    for ep in ENDPOINTS:
        all_results[ep] = {"success": 0, "fail": 0, "times": [], "errors": []}
    global total_success, total_fail
    total_success = 0
    total_fail = 0

    test_start = time.perf_counter()

    # Phase 1: Light load (10 concurrent)
    print("\n[Phase 1] Light load — 10 concurrent users × 3 waves...")
    for wave in range(3):
        run_wave(10, ENDPOINTS)
        time.sleep(0.5)

    # Phase 2: Medium load (20 concurrent)
    print("[Phase 2] Medium load — 20 concurrent users × 3 waves...")
    for wave in range(3):
        run_wave(20, ENDPOINTS)
        time.sleep(0.5)

    # Phase 3: Peak load (50 concurrent)
    print("[Phase 3] Peak load — 50 concurrent users × 2 waves...")
    for wave in range(2):
        run_wave(50, ENDPOINTS)
        time.sleep(1)

    total_duration = time.perf_counter() - test_start

    # ── Print Summary ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("LOAD TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"{'Endpoint':<25} {'Reqs':>5} {'OK':>5} {'Fail':>5} {'Avg(ms)':>9} {'P95(ms)':>9} {'Min':>7} {'Max':>7}")
    print("-" * 70)

    grand_times = []
    for ep in ENDPOINTS:
        r = all_results[ep]
        reqs = r["success"] + r["fail"]
        times = r["times"]
        if times:
            avg = statistics.mean(times)
            p95 = sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else times[0]
            mn = min(times)
            mx = max(times)
            grand_times.extend(times)
        else:
            avg = p95 = mn = mx = 0
        print(f"{ep:<25} {reqs:>5} {r['success']:>5} {r['fail']:>5} {avg:>9.1f} {p95:>9.1f} {mn:>7.1f} {mx:>7.1f}")

    print("-" * 70)
    total_reqs = total_success + total_fail
    rps = total_reqs / total_duration if total_duration > 0 else 0
    if grand_times:
        overall_avg = statistics.mean(grand_times)
        overall_p95 = sorted(grand_times)[int(len(grand_times) * 0.95)]
    else:
        overall_avg = overall_p95 = 0

    print(f"\n{'Total Requests:':<30} {total_reqs}")
    print(f"{'Successful:':<30} {total_success}")
    print(f"{'Failed:':<30} {total_fail}")
    print(f"{'Error Rate:':<30} {(total_fail/total_reqs*100) if total_reqs else 0:.1f}%")
    print(f"{'Test Duration:':<30} {total_duration:.2f}s")
    print(f"{'Throughput (RPS):':<30} {rps:.1f}")
    print(f"{'Avg Response Time:':<30} {overall_avg:.1f} ms")
    print(f"{'95th Percentile:':<30} {overall_p95:.1f} ms")
    print("=" * 60)
    print("✅ Load test completed successfully")

    # Save JSON results
    import os
    os.makedirs("security/reports", exist_ok=True)
    summary = {
        "timestamp": datetime.now().isoformat(),
        "target": BASE_URL,
        "total_requests": total_reqs,
        "total_success": total_success,
        "total_fail": total_fail,
        "error_rate_pct": round((total_fail / total_reqs * 100) if total_reqs else 0, 2),
        "duration_seconds": round(total_duration, 2),
        "rps": round(rps, 1),
        "avg_response_ms": round(overall_avg, 1),
        "p95_response_ms": round(overall_p95, 1),
        "per_endpoint": {
            ep: {
                "requests": all_results[ep]["success"] + all_results[ep]["fail"],
                "success": all_results[ep]["success"],
                "fail": all_results[ep]["fail"],
                "avg_ms": round(statistics.mean(all_results[ep]["times"]), 1) if all_results[ep]["times"] else 0,
            }
            for ep in ENDPOINTS
        }
    }
    with open("security/reports/load_test_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved → security/reports/load_test_results.json")
    return summary


if __name__ == "__main__":
    main()
