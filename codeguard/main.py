import sys

from codeguard.analyzer import analyze_file

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m codeguard.main <file.py>")
        return

    file_path = sys.argv[1]

    try:
        issues = analyze_file(file_path)
    except OSError as e:
        print(f"Not read file {file_path}: {e}")
        return

    if not issues:
        print("No issues found")
        return

    print(f"Found {len(issues)} issues")

    for issue in issues:
        print(
            f"Line {issue['line']}",
            f"Rule {issue['rule']}",
            f"Message {issue['message']}"
        )

if __name__ == "__main__":
    main()