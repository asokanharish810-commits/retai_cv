from collections import Counter

def show_summary(journey):

    print("\n==============================")
    print(" RETAIL ANALYTICS SUMMARY")
    print("==============================\n")

    print(f"Total Customers: {len(journey)}\n")

    for cid, path in journey.items():
        print(f"Customer {cid}: {path}")

    # ✅ Count how many customers visited each zone
    zone_visits = Counter()
    for path in journey.values():
        for zone in set(path):  # set() = count each zone once per customer
            zone_visits[zone] += 1

    print("\n------------------------------")
    print(" ZONE ENGAGEMENT REPORT")
    print("------------------------------")

    if zone_visits:
        sorted_zones = zone_visits.most_common()

        most_zone, most_count = sorted_zones[0]
        least_zone, least_count = sorted_zones[-1]

        print(f"\n📊 Zone Visits (by unique customers):\n")
        for zone, count in sorted_zones:
            bar = "█" * count
            print(f"  {zone:<12} {bar} ({count} customers)")

        print(f"\n🔥 Most Visited  : {most_zone} ({most_count} customers)")
        print(f"❄️  Least Visited : {least_zone} ({least_count} customers)")

    else:
        print("No zone data recorded.")

    print("\n==============================")