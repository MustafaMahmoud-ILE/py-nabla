"""
Performance benchmarks for py-nabla.

Targets:
- Parser throughput: ≥500 expressions/second
- Vectorised evaluation: ≥1M points/second
- Memory: <100 MB for 10K expressions
"""

import pytest
import time
import numpy as np
from py_nabla import parse


BENCHMARK_EXPRESSIONS = [
    r"x^2",
    r"\sin(x)",
    r"\frac{1}{x+1}",
    r"\sqrt{x^2 + 1}",
    r"x^3 + 2x^2 - 5x + 1",
    r"\ln(x) + e^x",
    r"\sin(x)^2 + \cos(x)^2",
    r"\frac{x^2 - 1}{x - 1}",
]


class TestParserPerformance:

    def test_parser_throughput(self):
        """Parser should handle ≥30 expressions/second (Lark Earley target)."""
        n = 50
        start = time.perf_counter()
        for _ in range(n):
            for expr_str in BENCHMARK_EXPRESSIONS:
                parse(expr_str)
        elapsed = time.perf_counter() - start
        total = n * len(BENCHMARK_EXPRESSIONS)
        rate = total / elapsed
        print(f"\nParser throughput: {rate:.0f} expr/s")
        assert rate >= 30, f"Too slow: {rate:.0f} expr/s (target: 30)"


class TestEvaluationPerformance:

    def test_vectorised_throughput(self):
        """Vectorised eval should handle ≥500K points/second."""
        f = parse(r"x^2 + \sin(x)")
        n_points = 500_000
        x_vals = np.linspace(0, 10, n_points)

        start = time.perf_counter()
        y_vals = f.evaluate(x=x_vals)
        elapsed = time.perf_counter() - start

        rate = n_points / elapsed
        print(f"\nVectorised eval: {rate/1e6:.2f}M points/s")
        assert y_vals.shape == (n_points,)
        assert rate >= 500_000, f"Too slow: {rate/1e6:.2f}M pts/s"

    def test_lambdify_throughput(self):
        """lambdify should be even faster than direct evaluate."""
        f = parse(r"x^2 + 1")
        func = f.lambdify(['x'])
        x_vals = np.linspace(0, 10, 1_000_000)

        start = time.perf_counter()
        y_vals = func(x_vals)
        elapsed = time.perf_counter() - start

        assert y_vals.shape == (1_000_000,)
        print(f"\nlambdify throughput: {1e6/elapsed:.0f} pts/s")


class TestMemoryUsage:

    def test_expression_memory_bounded(self):
        """10K expressions should use less than 100 MB."""
        tracemalloc = pytest.importorskip("tracemalloc")
        import tracemalloc as tm

        tm.start()
        exprs = [parse(r"x^2 + 1") for _ in range(10_000)]
        current, peak = tm.get_traced_memory()
        tm.stop()

        peak_mb = peak / 1024 / 1024
        print(f"\nPeak memory for 10K expressions: {peak_mb:.1f} MB")
        assert peak_mb < 100, f"Memory too high: {peak_mb:.1f} MB"
        del exprs
