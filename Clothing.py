import pandas as pd

print("----- Welcome to XYZ Fashions -----")

print("""
Products available in our shop:
• Saree
• Kurta
• Denims
• Night Suit
• Tops
""")

while True:

    print("""
Offers:
1. Discount on USER-SELECTED items
2. Buy 1 and get 1 free
3. Buy Products above 5000 & get 50% discount
4. Buy 3 or more (same product) & get discount
""")

    choice = int(input("Select offer (1–4): "))

    data = {"Name": [], "Cost": [], "Price": []}
    n = int(input("How many different product customer is buying? "))

    for i in range(n):
        name = input(f"\nEnter name of product {i+1}: ")
        qty = int(input(f"How many {name}s? "))

        for j in range(qty):
            cost = float(input(f"Enter cost price for {name} unit {j+1}: ₹"))
            price = float(input(f"Enter selling price for {name} unit {j+1}: ₹"))

            data["Name"].append(name)
            data["Cost"].append(cost)
            data["Price"].append(price)

    df = pd.DataFrame(data)

    print("\n----- Billing Summary -----")
    print(df[["Name", "Price"]])

    if choice == 1:
        discount_percent = float(input("Enter discount percentage: "))
        discount_rate = discount_percent / 100

        df["FinalPrice"] = df["Price"] * (1 - discount_rate)

        final_price = round(df["FinalPrice"].sum(), 2)
        total_cost = df["Cost"].sum()
        profit = round(final_price - total_cost, 2)

    elif choice == 2:
        print("\nSelect Primary Item:")
        print(df[["Name", "Price"]])

        p = int(input("Enter row number: ")) - 1
        primary_item = df.iloc[p]

        print("\nSelect Offer Item:")
        print(df[["Name", "Price"]])

        o = int(input("Enter row number: ")) - 1
        offer_item = df.iloc[o]

        final_price = primary_item["Price"]
        profit = final_price - (primary_item["Cost"] + offer_item["Cost"])

    elif choice == 3:
        bill_amount = df["Price"].sum()
        print(f"\nCurrent total bill: ₹{bill_amount}")

        while bill_amount < 5000:
            print("\nBill amount less than 5000 – please add more items")
            n_add = int(input("How many different items to add? "))

            for i in range(n_add):
                name = input(f"\nEnter name of item {i+1}: ")
                qty = int(input(f"How many {name}s? "))

                for j in range(qty):
                    cost = float(input(f"Enter cost price for {name} unit {j+1}: ₹"))
                    price = float(input(f"Enter selling price for {name} unit {j+1}: ₹"))

                    df.loc[len(df)] = [name, cost, price]
                    bill_amount += price

            print(f"Current total bill: ₹{bill_amount}")

        final_price = round(bill_amount * 0.5, 2)
        profit = 0

    elif choice == 4:
        discount_percent = float(input("Enter discount percentage for Buy 3 offer: "))
        discount_rate = discount_percent / 100

        final_price = 0
        total_cost = df["Cost"].sum()

        grouped = df.groupby("Name")

        print("\nOffer Evaluation:")

        for product, group in grouped:
            unit_count = len(group)

            if unit_count < 3:
                print(f"{product}: Quantity {unit_count} — offer not applied")
                final_price += group["Price"].sum()
            else:
                print(f"{product}: Quantity {unit_count} — discount applied")
                final_price += (group["Price"] * (1 - discount_rate)).sum()

        final_price = round(final_price, 2)
        profit = round(final_price - total_cost, 2)

    else:
        print("Invalid choice")
        continue

    if profit < 0:
        print(" Loss detected – offer not allowed")
    elif profit == 0:
        print(f"Customer Pays: ₹{final_price}")
        print("✔ No Profit, No Loss")
        print("✔ Inventory cleared")
    else:
        print(f"Customer Pays: ₹{final_price}")
        print(f"✔ Profit Earned: ₹{profit}")

    print("✔ Business strategy satisfied")

    again = input("\nDo you want to apply another offer? (y/n): ").lower()
    if again != "y":
        print("Thank you! Billing completed.")
        break
