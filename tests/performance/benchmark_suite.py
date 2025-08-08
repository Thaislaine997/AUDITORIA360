"""
Performance Benchmarking Tool for AUDITORIA360
Phase 3 Performance Optimization Testing
"""

import asyncio
import json
import logging
import statistics
import time
from datetime import datetime
from typing import Dict, List

import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceBenchmark:
    """Performance benchmarking tool for API endpoints"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}

    async def benchmark_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict = None,
        headers: dict = None,
        concurrent_requests: int = 10,
        total_requests: int = 100,
    ) -> Dict:
        """Benchmark a specific endpoint with concurrent requests"""

        if headers is None:
            headers = {"Content-Type": "application/json"}

        async def make_request(session: aiohttp.ClientSession) -> Dict:
            """Make a single request and measure performance"""
            start_time = time.time()

            try:
                if method.upper() == "GET":
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        content = await response.text()
                        status = response.status
                elif method.upper() == "POST":
                    async with session.post(
                        f"{self.base_url}{endpoint}", json=data, headers=headers
                    ) as response:
                        content = await response.text()
                        status = response.status
                else:
                    raise ValueError(f"Unsupported method: {method}")

                end_time = time.time()
                response_time = (
                    end_time - start_time
                ) * 1000  # Convert to milliseconds

                return {
                    "response_time": response_time,
                    "status_code": status,
                    "success": 200 <= status < 300,
                    "content_length": len(content),
                }

            except Exception as e:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000

                return {
                    "response_time": response_time,
                    "status_code": 0,
                    "success": False,
                    "error": str(e),
                    "content_length": 0,
                }

        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrent_requests)

        async def limited_request(session: aiohttp.ClientSession):
            async with semaphore:
                return await make_request(session)

        # Execute benchmark
        logger.info(
            f"Benchmarking {endpoint} with {total_requests} requests ({concurrent_requests} concurrent)"
        )

        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [limited_request(session) for _ in range(total_requests)]
            results = await asyncio.gather(*tasks)

        end_time = time.time()
        total_time = end_time - start_time

        # Calculate statistics
        response_times = [r["response_time"] for r in results]
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]

        stats = {
            "endpoint": endpoint,
            "method": method,
            "total_requests": total_requests,
            "concurrent_requests": concurrent_requests,
            "total_time": total_time,
            "requests_per_second": total_requests / total_time,
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / total_requests * 100,
            "response_times": {
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0,
                "mean": statistics.mean(response_times) if response_times else 0,
                "median": statistics.median(response_times) if response_times else 0,
                "p95": self._percentile(response_times, 95) if response_times else 0,
                "p99": self._percentile(response_times, 99) if response_times else 0,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.results[endpoint] = stats
        return stats

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of a list"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]

    async def run_payroll_benchmark_suite(self) -> Dict:
        """Run comprehensive benchmark suite for payroll endpoints"""

        logger.info("Starting payroll performance benchmark suite...")

        # Test endpoints with different loads
        endpoints_to_test = [
            {"endpoint": "/health", "method": "GET", "concurrent": 20, "total": 200},
            {
                "endpoint": "/api/v1/payroll/employees",
                "method": "GET",
                "concurrent": 10,
                "total": 100,
            },
            {
                "endpoint": "/api/v1/payroll/competencies",
                "method": "GET",
                "concurrent": 10,
                "total": 100,
            },
            # Add authenticated endpoints with mock data
        ]

        results = {}

        for test_config in endpoints_to_test:
            try:
                result = await self.benchmark_endpoint(
                    endpoint=test_config["endpoint"],
                    method=test_config["method"],
                    concurrent_requests=test_config["concurrent"],
                    total_requests=test_config["total"],
                )
                results[test_config["endpoint"]] = result

                # Log results
                logger.info(f"Endpoint: {test_config['endpoint']}")
                logger.info(f"  RPS: {result['requests_per_second']:.2f}")
                logger.info(
                    f"  Mean Response Time: {result['response_times']['mean']:.2f}ms"
                )
                logger.info(
                    f"  95th Percentile: {result['response_times']['p95']:.2f}ms"
                )
                logger.info(f"  Success Rate: {result['success_rate']:.2f}%")
                logger.info("---")

            except Exception as e:
                logger.error(f"Error benchmarking {test_config['endpoint']}: {e}")

        return results

    def generate_report(self, output_file: str = None) -> str:
        """Generate a performance report"""

        report = {
            "benchmark_results": self.results,
            "summary": {
                "total_endpoints_tested": len(self.results),
                "overall_performance_score": self._calculate_performance_score(),
                "recommendations": self._generate_recommendations(),
            },
            "generated_at": datetime.utcnow().isoformat(),
        }

        if output_file:
            with open(output_file, "w") as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {output_file}")

        return json.dumps(report, indent=2)

    def _calculate_performance_score(self) -> int:
        """Calculate overall performance score (0-100)"""
        if not self.results:
            return 0

        scores = []
        for endpoint, stats in self.results.items():
            # Score based on RPS, response time, and success rate
            rps_score = (
                min(stats["requests_per_second"] / 10, 10) * 10
            )  # Max 100 for 100+ RPS
            response_time_score = max(
                0, 100 - stats["response_times"]["mean"] / 10
            )  # Penalty for slow responses
            success_rate_score = stats["success_rate"]

            endpoint_score = (rps_score + response_time_score + success_rate_score) / 3
            scores.append(endpoint_score)

        return int(statistics.mean(scores))

    def _generate_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []

        for endpoint, stats in self.results.items():
            if stats["response_times"]["mean"] > 1000:  # More than 1 second
                recommendations.append(
                    f"High response time on {endpoint}: Consider caching or query optimization"
                )

            if stats["success_rate"] < 95:
                recommendations.append(
                    f"Low success rate on {endpoint}: Check error handling and stability"
                )

            if stats["requests_per_second"] < 10:
                recommendations.append(
                    f"Low throughput on {endpoint}: Consider async optimization"
                )

        if not recommendations:
            recommendations.append(
                "All endpoints performing within acceptable parameters"
            )

        return recommendations


class CachePerformanceTest:
    """Test cache performance and hit rates"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def test_cache_effectiveness(self) -> Dict:
        """Test cache hit rates and performance improvement"""

        # Test endpoint with caching
        endpoint = "/api/v1/payroll/employees"

        logger.info("Testing cache effectiveness...")

        # First request (cache miss)
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                first_response_time = time.time() - start_time
                await response.text()

        # Second request (cache hit)
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                second_response_time = time.time() - start_time
                await response.text()

        # Calculate improvement
        improvement_percentage = (
            (first_response_time - second_response_time) / first_response_time
        ) * 100

        return {
            "endpoint": endpoint,
            "first_request_time": first_response_time * 1000,  # ms
            "second_request_time": second_response_time * 1000,  # ms
            "cache_improvement_percentage": improvement_percentage,
            "cache_working": improvement_percentage
            > 10,  # At least 10% improvement expected
        }


async def main():
    """Run comprehensive performance benchmarks"""

    benchmark = PerformanceBenchmark()
    cache_test = CachePerformanceTest()

    # Run main benchmark suite
    logger.info("=== AUDITORIA360 Performance Benchmark Suite ===")
    results = await benchmark.run_payroll_benchmark_suite()

    # Test cache performance
    logger.info("=== Cache Performance Test ===")
    cache_results = await cache_test.test_cache_effectiveness()
    logger.info(
        f"Cache improvement: {cache_results['cache_improvement_percentage']:.2f}%"
    )

    # Generate report
    report = benchmark.generate_report("performance_report.json")

    # Print summary
    performance_score = benchmark._calculate_performance_score()
    logger.info(f"=== PERFORMANCE SUMMARY ===")
    logger.info(f"Overall Performance Score: {performance_score}/100")

    if performance_score >= 80:
        logger.info("✅ Excellent performance! Target exceeded.")
    elif performance_score >= 60:
        logger.info("✅ Good performance! Target achieved.")
    else:
        logger.info("⚠️  Performance below target. Optimization needed.")

    return results


if __name__ == "__main__":
    asyncio.run(main())
