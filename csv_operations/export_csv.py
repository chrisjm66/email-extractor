import csv
from pathlib import Path


def next_available_filename(base_filename):
    base_path = Path(base_filename)
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent

    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def write_to_csv(records, filename="results.csv"):
    output_path = next_available_filename(filename)
    columns = ["email", "contact_name", "source_url", "page_title", "context_snippet"]
    unique_records = {}

    for record in records:
        key = (record.get("email", "").lower(), record.get("source_url", ""))
        if not key[0]:
            continue
        if key not in unique_records:
            unique_records[key] = record

    with open(output_path, "w", newline="") as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(columns)
        sorted_records = sorted(
            unique_records.values(),
            key=lambda row: (row.get("email", ""), row.get("source_url", "")),
        )
        for record in sorted_records:
            writer.writerow([record.get(column, "") for column in columns])

    print(f"Wrote {len(unique_records)} records to {output_path}")
