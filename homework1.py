items = int(input("Enter the maximum number of items to be shipped: "))

packages_sent = 0
total_weight_sent = 0
total_unused_capacity = 0
unused_capacity_package = 0
current_package_weight = 0

for element in range(items):
    weight = int(input(f"Enter the weight of item {element+1}: "))

    if current_package_weight + weight > 20:
        packages_sent += 1
        total_weight_sent += current_package_weight
        unused_capacity = 20 - current_package_weight
        if unused_capacity > total_unused_capacity:
            total_unused_capacity = unused_capacity
            unused_capacity_package = packages_sent
        print(f"Package {packages_sent} sent with weight of {current_package_weight} kg.")
        current_package_weight = 0

    if weight == 0:
        break

    if 1 <= weight <= 10:
        current_package_weight += weight
    else:
        print("Item was not added to the package, weight needs to be between 1 kg and 10 kg.")

if current_package_weight > 0:
    packages_sent += 1
    total_weight_sent += current_package_weight
    unused_capacity = 20 - current_package_weight
    if unused_capacity > total_unused_capacity:
        total_unused_capacity = unused_capacity
        unused_capacity_package = packages_sent
    print(f"Package {packages_sent} sent with weight of {current_package_weight} kg.")

unused_capacity_total = (packages_sent * 20) - total_weight_sent

print(f"\nSummary:")
print(f"Total packages sent: {packages_sent}")
print(f"Total weight sent: {total_weight_sent} kg")
print(f"Total unused capacity: {unused_capacity_total} kg")
print(f"Package {unused_capacity_package} had the most unused capacity ({total_unused_capacity} kg).")