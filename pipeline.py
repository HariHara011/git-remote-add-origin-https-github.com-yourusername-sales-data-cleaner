import csv


# 1. Skip rows where name is empty
# 2. Capitalize name properly
# 3. Capitalize region properly
# 4. Skip rows where sales is not a valid number
# 5. Skip rows where sales is negative or zero
# 6. Remove duplicate rows

def clean_row(row):

    # Remove extra spaces
    name = row['name'].strip()
    sales = row['sales'].strip()
    region = row['region'].strip()
    month = row['month'].strip()

    # Skip empty name
    if name == "":
        return None, "empty name"

    # Capitalize properly
    name = name.capitalize()
    region = region.capitalize()

    # Check valid sales number
    try:
        sales = int(sales)
    except ValueError:
        return None, "invalid sales"

    # Skip negative or zero sales
    if sales <= 0:
        return None, "negative or zero sales"

    # Return cleaned row
    return {
        "name": name,
        "sales": sales,
        "region": region,
        "month": month
    }, None


def load_data(filepath, verbose=False):

    rows = []
    seen = set()
    skipped = []

    with open(filepath, 'r') as f:

        reader = csv.DictReader(f)

        for row in reader:
            if verbose:
                print(f"READ: {row}")

            cleaned, reason = clean_row(row)

            # Skip invalid rows
            if cleaned is None:
                skipped.append((row, reason))
                if verbose:
                    print(f"  SKIP ({reason})")
                continue

            # Create duplicate key
            key = (
                cleaned['name'],
                cleaned['sales'],
                cleaned['month']
            )

            # Skip duplicates
            if key in seen:
                skipped.append((row, "duplicate"))
                if verbose:
                    print(f"  SKIP (duplicate)")
                continue

            # Add key to seen set
            seen.add(key)

            # Add cleaned row
            rows.append(cleaned)
            if verbose:
                print(f"  KEEP: {cleaned}")

    if verbose:
        print(f"\nSummary: {len(rows)} kept, {len(skipped)} skipped out of {len(rows) + len(skipped)} rows read\n")

    return rows


def save_clean(rows, filepath):
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "sales", "region", "month"])
        writer.writeheader()
        writer.writerows(rows)


def save_report(rows):
    total_sales = sum(row['sales'] for row in rows)

    by_name = {}
    for row in rows:
        by_name[row['name']] = by_name.get(row['name'], 0) + row['sales']
    top_earner = max(by_name, key=by_name.get)

    by_region = {}
    for row in rows:
        by_region[row['region']] = by_region.get(row['region'], 0) + row['sales']
    sorted_regions = sorted(by_region.items(), key=lambda x: x[1], reverse=True)

    by_month = {}
    for row in rows:
        by_month[row['month']] = by_month.get(row['month'], 0) + row['sales']
    best_month = max(by_month, key=by_month.get)

    with open('report.txt', 'w') as f:
        f.write("=== SALES REPORT ===\n\n")
        f.write(f"Total Sales: ${total_sales}\n")
        f.write(f"Top Earner: {top_earner} (${by_name[top_earner]})\n\n")
        f.write("Sales by Region:\n")
        for region, amount in sorted_regions:
            f.write(f"  {region}: ${amount}\n")
        f.write(f"\nBest Month: {best_month} (${by_month[best_month]})\n")


if __name__ == '__main__':
    rows = load_data('sales.csv.txt', verbose=True)
    print(f"Loaded {len(rows)} clean rows")
    save_clean(rows, 'sales_clean.csv')
    save_report(rows)
    print("Done. Check sales_clean.csv and report.txt")