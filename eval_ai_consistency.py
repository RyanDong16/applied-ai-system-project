from pprint import pprint

from logic_utils import evaluate_ai_consistency


def main():
    report = evaluate_ai_consistency(
        secret=50,
        history=[10, 25, 30],
        low=1,
        high=100,
        attempt_limit=8,
        runs_per_case=10,
    )

    print("AI CONSISTENCY REPORT")
    print("=" * 50)
    print(f"Average consistency: {report['average_consistency']:.2f}")
    print(f"Total guardrail violations: {report['total_guardrail_violations']}")
    print(f"Overall status: {report['overall_status']}")
    print("-" * 50)

    for case in report["cases"]:
        pprint(case)
        print("-" * 50)


if __name__ == "__main__":
    main()