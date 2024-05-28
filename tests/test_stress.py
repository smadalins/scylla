import dataclasses

import pytest

import stress
import test_stress_data


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "Op rate                   :   12,522 op/s  [WRITE: 12,523 op/s]",
            12522,
        ),
        ("Latency mean              :    0.7 ms [WRITE: 0.8 ms] ", 0.7),
        ("Latency 99th percentile   :    2.3 ms [WRITE: 2.4 ms] ", 2.3),
        (" Latency max               :   24.2 ms [WRITE: 23.2 ms] ", 24.2),
    ],
)
def test_parse_result_line(line, expected):
    result = stress.StressResult()
    stress.parse_result_line(result, line)
    for field in dataclasses.fields(result):
        try:
            assert getattr(result, field.name) == expected
            break
        except AssertionError:
            continue
    else:
        assert False, f"Parsed value ({expected}) not found in line: {line}"


def test_parse_output():
    output = test_stress_data.STRESS_OUTPUT
    result = stress.parse_output(output)
    assert result is not None
    assert result.op_rate == 30679
    assert result.latency_mean == 0.3
    assert result.latency_99th == 2.0
    assert result.latency_max == 23.8


@pytest.mark.parametrize(
    "line, type, expected",
    [
        ("", int, 0),
        ("test", int, 0),
        ("", float, 0.0),
        ("test", float, 0.0),
        (": 2", int, 2),
        (": 2,000", int, 2000),
        (": 2.0", int, 0),
        (": 2,000.0", int, 0),
        (": 23,232", int, 23232),
        (": 2,000.0", float, 2000.0),
        (": 2,000", float, 2000.0),
        (": 2.0", float, 2.0),
        (": 2", float, 2.0),
        (": 23,232.3", float, 23232.3),
        (": 23.2", float, 23.2),
        (": 23,232.3", float, 23232.3),
        (": 23.2", float, 23.2),
        (": 999,999,999.9999", float, 999999999.9999),
        (": 0.0", int, 0),
        (": 0.0", float, 0.0),
    ],
)
def test_parse_numeric_value(line, type, expected):
    assert stress.parse_numeric_value(line, type) == expected


def test_run_command():
    cmd = "echo 'hello test'"
    stdout, stderr = stress.run_command(cmd, 0)
    assert stdout == "hello test\n"
    assert stderr == ""


def test_run_command_error():
    cmd = "echo 'hello test' && exit 1"
    stdout, stderr = stress.run_command(cmd, 0)
    assert stdout == "hello test\n"
    assert stderr == ""


@pytest.mark.parametrize(
    "result_list, expected",
    [
        (
            [
                stress.StressResult(),
                stress.StressResult(),
                stress.StressResult(),
            ],
            stress.AggregatedResult(0, 0, 0, 0),
        ),
        (
            [
                stress.StressResult(op_rate=1),
                stress.StressResult(op_rate=2),
                stress.StressResult(op_rate=3),
            ],
            stress.AggregatedResult(6, 0, 0, 0),
        ),
        (
            [
                stress.StressResult(latency_mean=1),
                stress.StressResult(latency_mean=2),
                stress.StressResult(latency_mean=3),
            ],
            stress.AggregatedResult(0, 2, 0, 0),
        ),
        (
            [
                stress.StressResult(latency_99th=1),
                stress.StressResult(latency_99th=2),
                stress.StressResult(latency_99th=3),
            ],
            stress.AggregatedResult(0, 0, 2, 0),
        ),
        (
            [
                stress.StressResult(latency_max=2),
                stress.StressResult(latency_max=2),
                stress.StressResult(latency_max=2),
            ],
            stress.AggregatedResult(0, 0, 0, 0.0),
        ),
        (
            [
                stress.StressResult(latency_max=1.99),
                stress.StressResult(latency_max=2),
                stress.StressResult(latency_max=2),
            ],
            stress.AggregatedResult(0, 0, 0, 0.005773502691896263),
        ),
    ],
)
def test_analze_results(result_list, expected):
    result = stress.analyze_results(result_list)
    assert result == expected
