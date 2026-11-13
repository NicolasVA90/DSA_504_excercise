# Copy everything in THIS cell into sales_report.py in VS Code.
# This combines a function, a list of dictionaries, and a loop --
# everything we covered today.

def total_revenue(sales_list):
    """Return the sum of revenue across a list of sale dictionaries."""
    total = 0
    for record in sales_list:
        total += record["revenue"]
    return total


def top_store(sales_list):
    """Return the store name with the highest revenue."""
    best = sales_list[0]
    for record in sales_list:
        if record["revenue"] > best["revenue"]:
            best = record
    return best["store"]


def main():
    sales = [
        {"store": "Utica",  "units": 138, "revenue": 4521.75},
        {"store": "Albany", "units": 95,  "revenue": 3980.10},
        {"store": "Rome",   "units": 210, "revenue": 5102.00},
    ]

    print("=== DSA 504 Sales Report ===")
    for record in sales:
        print(f"{record['store']}: {record['units']} units, ${record['revenue']:.2f}")

    print(f"\nTotal revenue: ${total_revenue(sales):.2f}")
    print(f"Top store: {top_store(sales)}")


if __name__ == "__main__":
    main()
