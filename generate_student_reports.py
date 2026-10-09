"""Create one Lab/KC completion report per student from a Canvas grades CSV."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Iterable


def module_columns(fieldnames: Iterable[str]) -> list[str]:
    """Return only module columns whose names identify a Lab or Knowledge Check."""
    return [
        field
        for field in fieldnames
        if field and (field.startswith("KC - ") or "]-Lab - " in field)
    ]


def safe_filename(student_name: str, student_id: str) -> str:
    """Build a filesystem-safe, unique report filename."""
    base_name = re.sub(r"[^\w.-]+", "_", student_name, flags=re.UNICODE).strip("._")
    return f"{base_name or 'student'}_{student_id or 'unknown'}.md"


def display_module_name(column_name: str) -> str:
    """Remove the Canvas item ID while retaining the readable module name."""
    name = re.sub(r"\s*\(\d+\)\s*$", "", column_name)
    return name.replace("]-Lab - ", "] Lab - ")


def module_category(column_name: str) -> str:
    """Return the report category for a module column."""
    return "KC" if column_name.startswith("KC - ") else "Lab"


def is_unscored(value: str | None) -> bool:
    """Treat an empty or whitespace-only grade as not scored."""
    return value is None or not value.strip()


def is_test_student(student_name: str) -> bool:
    """Recognize the test account regardless of Canvas name ordering."""
    normalized = re.sub(r"\s+", " ", student_name.casefold()).strip()
    return normalized in {"test student", "student, test"}


def table_rows(modules: list[tuple[str, str, str]]) -> list[str]:
    """Format module results as a Markdown table."""
    rows = [
        (
            name.replace("|", r"\|"),
            score or "-",
            "Not scored" if is_unscored(score) else "Completed",
        )
        for _, name, score in modules
    ]
    return [
        "| Module | Score | Status |",
        "| --- | ---: | --- |",
        *(f"| {name} | {score} | {status} |" for name, score, status in rows),
    ]


def write_student_report(
    row: dict[str, str],
    module_fields: list[str],
    output_directory: Path,
) -> Path:
    student_name = row.get("Student", "").strip()
    student_id = row.get("ID", "").strip()
    modules = [
        (module_category(field), display_module_name(field), row.get(field, "").strip())
        for field in module_fields
    ]
    unscored = [(category, name) for category, name, score in modules if is_unscored(score)]
    report_path = output_directory / safe_filename(student_name, student_id)

    lines = [
        f"# Student Report: {student_name or 'Unknown'}",
        "",
        f"- **ID:** {student_id or 'Unknown'}",
        f"- **Current Score:** {row.get('Current Score', '').strip() or 'Not available'}",
        f"- **Final Score:** {row.get('Final Score', '').strip() or 'Not available'}",
        "",
        "> **Note:** The Final Score includes all modules in the complete "
        "curriculum, including modules that have not yet been covered.",
        "",
        "## Modules Not Scored (Not Completed)",
    ]
    if unscored:
        lines.extend(f"- [{category}] {name}" for category, name in unscored)
    else:
        lines.append("- None")

    for category in ("KC", "Lab"):
        category_modules = [
            (module_category, name, score)
            for module_category, name, score in modules
            if module_category == category
        ]
        lines.extend(["", f"## {category} Results", "", *table_rows(category_modules)])
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def generate_reports(input_csv: Path, output_directory: Path) -> int:
    """Generate reports and return the number of student reports written."""
    output_directory.mkdir(parents=True, exist_ok=True)
    with input_csv.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("The CSV file does not contain a header row.")

        modules = module_columns(reader.fieldnames)
        if not modules:
            raise ValueError("The CSV file contains no KC or Lab module columns.")

        report_count = 0
        for row in reader:
            student_name = row.get("Student", "").strip()
            if (
                not student_name
                or student_name == "Points Possible"
                or is_test_student(student_name)
            ):
                continue
            write_student_report(row, modules, output_directory)
            report_count += 1
    return report_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one Lab/KC completion report per student."
    )
    parser.add_argument("input_csv", type=Path, help="Path to the grades CSV file.")
    parser.add_argument(
        "-o",
        "--output-directory",
        type=Path,
        default=Path("student_reports"),
        help="Directory for generated reports (default: student_reports).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report_count = generate_reports(args.input_csv, args.output_directory)
    print(f"Created {report_count} student report(s) in {args.output_directory}.")


if __name__ == "__main__":
    main()
