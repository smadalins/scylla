"""
This program will run a stress test on the ScyllaDB database. Using concurrent
N threads running cassandra-stress tool. Number of threads and test durationcan
be specified by the user.

After the test is complete, the program will analyze the results outputted by
the cassandra-stress tool and output the agregated results to stdout.
"""

import argparse
import ipaddress
import logging
import logging.handlers
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from statistics import mean, stdev

LOGGER = logging.getLogger(__name__)


@dataclass
class StressResult:
    op_rate: int = 0
    latency_mean: float = 0
    latency_99th: float = 0
    latency_max: float = 0


@dataclass
class AggregatedResult:
    op_rate_sum: int | None = None
    latency_mean_avg: float | None = None
    latency_99th_avg: float | None = None
    latency_max_std_deviation: float | None = None


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run a stress test on the ScyllaDB database."
    )
    parser.add_argument(
        "-i",
        "--ip",
        type=validate_ip,
        required=True,
        help="IP address of the ScyllaDB node.",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=1,
        help="Number of threads to use.",
    )
    parser.add_argument(
        "-d",
        "--durations",
        type=int,
        nargs="+",
        default=[10],
        help="Duration list of the tests in seconds.",
    )
    args = parser.parse_args()
    validate_duration(args.durations, args.threads)
    return args


def run_casandra_stress(ip: str, threads: int, durations: list[int]):
    LOGGER.info("Running stress test with %d threads", threads)
    cmd_list = []
    result_list = []
    for duration in durations:
        cmd_list.append(
            f"docker exec some-scylla cassandra-stress write"
            f" duration={duration}s -rate threads=10 -node {ip}"
        )
    with ThreadPoolExecutor(threads) as exe:
        futures = [
            exe.submit(run_command, cmd, i) for i, cmd in enumerate(cmd_list)
        ]
        for i, future in enumerate(as_completed(futures)):
            stdout, stderr = future.result()
            if stderr:
                LOGGER.warning(
                    f"Stress test {i} encounter some errors: {stderr}"
                )
            result_list.append(parse_output(stdout))
            LOGGER.debug(f"Stress test {i} completed")
    return result_list


def run_command(cmd: str, worker_id: int):
    LOGGER.debug(f"Stress test {worker_id} Running command: {cmd}")
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    LOGGER.debug(f"stdout stress test {worker_id}: {stdout.decode()}")
    LOGGER.debug(f"stderr stress test {worker_id}: {stderr.decode()}")
    return stdout.decode(), stderr.decode()


def parse_output(output: str) -> StressResult | None:
    result = StressResult()
    lines = iter(output.split("\n"))
    while True:
        try:
            line = next(lines)
            if "Results:" in line:
                break
        except StopIteration:
            LOGGER.error("No results found in output")
            return None
    for line in lines:
        parse_result_line(result, line)
    return result


def parse_result_line(result: StressResult, line: str):
    if "Op rate" in line:
        result.op_rate = parse_numeric_value(line, int)
    elif "Latency mean" in line:
        result.latency_mean = parse_numeric_value(line, float)
    elif "Latency 99th percentile" in line:
        result.latency_99th = parse_numeric_value(line, float)
    elif "Latency max" in line:
        result.latency_max = parse_numeric_value(line, float)


def parse_numeric_value(line: str, type: type):
    words_list = iter(line.split())
    for word in words_list:
        if word == ":":
            return cast_to_type(next(words_list), type)
    return 0


def cast_to_type(value: str, type: type):
    try:
        return type(value.replace(",", ""))
    except ValueError:
        LOGGER.error(f"Error casting {value} to {type}")
        return 0


def validate_ip(ip: str):
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid IP address")


def validate_duration(duration: list[int], threads: int):
    if len(duration) != threads:
        raise argparse.ArgumentTypeError(
            "Number of durations must match number of threads"
        )
    return duration


def analyze_results(results_list: list[StressResult]):
    aggregated_result = AggregatedResult()
    aggregated_result.op_rate_sum = sum(
        [result.op_rate for result in results_list]
    )
    aggregated_result.latency_mean_avg = mean(
        [result.latency_mean for result in results_list]
    )
    aggregated_result.latency_99th_avg = mean(
        [result.latency_99th for result in results_list]
    )
    aggregated_result.latency_max_std_deviation = stdev(
        [result.latency_max for result in results_list]
    )
    return aggregated_result


def print_resutls(aggregated_result: AggregatedResult, threads: int):
    print(f"Results for {threads} stress test processes:")
    print(f"Op rate sum: {aggregated_result.op_rate_sum}")
    print(f"Latency mean avg: {aggregated_result.latency_mean_avg}")
    print(f"Latency 99th avg: {aggregated_result.latency_99th_avg}")
    print(
        f"Latency max std deviation:"
        f" {aggregated_result.latency_max_std_deviation}"
    )


if __name__ == "__main__":
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(format=log_format, level=logging.ERROR)
    args = parse_args()
    LOGGER.debug(f"Arguments: {args}")
    print_resutls(
        analyze_results(
            run_casandra_stress(args.ip, args.threads, args.durations)
        ),
        args.threads,
    )
