import pandas as pd

print("----- Welcome to XYZ Fashions -----")

# Product master
PRODUCTS = {
    1: "Saree",
    2: "Kurta",
    3: "Denims",
    4: "Night Suit",
    5: "Tops"
}

def show_products():
    print("\nSelect Product:")
    for k, v in PRODUCTS.items():
        print(f"{k}. {v}")

while True:

    print("""
Offers:
1. Discount on USER-SELECTED items
2. Buy 1 and get 1 free
3. Buy Products above 5000 & get 50% discount
4. Buy 3 or more (same product) & get discount
5. Exit
""")

    try:
        choice = int(input("Select offer (1–5): "))
    except ValueError:
        print("❌ Invalid input")
        continue

    if choice == 5:
        print("Thank you! Billing exited.")
        break

    data = {"Name": [], "Cost": [], "Price": []}

    try:
        n = int(input("How many different products customer is buying? "))
    except ValueError:
        print("❌ Invalid number")
        continue

    for i in range(n):

        # ---------- PRODUCT MENU ----------
        while True:
            show_products()
            try:
                p_choice = int(input(f"Choose product {i+1} (1–5): "))
                if p_choice in PRODUCTS:
                    name = PRODUCTS[p_choice]
                    break
                else:
                    print("❌ Invalid product selection")
            except ValueError:
                print("❌ Enter a number")

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

    # ================= OFFER LOGIC =================

    if choice == 1:
        discount = float(input("Enter discount percentage: ")) / 100
        df["FinalPrice"] = df["Price"] * (1 - discount)
        final_price = round(df["FinalPrice"].sum(), 2)
        profit = round(final_price - df["Cost"].sum(), 2)

    elif choice == 2:
        print(df[["Name", "Price"]])
        p = int(input("Select primary item row number: ")) - 1
        o = int(input("Select free item row number: ")) - 1

        primary = df.iloc[p]
        free = df.iloc[o]

        final_price = primary["Price"]
        profit = final_price - (primary["Cost"] + free["Cost"])

    elif choice == 3:
        bill = df["Price"].sum()
        print(f"Current Bill: ₹{bill}")

        while bill < 5000:
            print("Bill < 5000, add more items")

            show_products()
            p_choice = int(input("Select product (1–5): "))
            name = PRODUCTS[p_choice]

            qty = int(input(f"How many {name}s? "))

            for j in range(qty):
                cost = float(input(f"Enter cost price for {name}: ₹"))
                price = float(input(f"Enter selling price for {name}: ₹"))

                df.loc[len(df)] = [name, cost, price]
                bill += price

            print(f"Updated Bill: ₹{bill}")

        final_price = round(bill * 0.5, 2)
        profit = 0

    elif choice == 4:
        discount = float(input("Enter discount percentage: ")) / 100
        final_price = 0
        total_cost = df["Cost"].sum()

        for product, group in df.groupby("Name"):
            if len(group) >= 3:
                final_price += (group["Price"] * (1 - discount)).sum()
            else:
                final_price += group["Price"].sum()

        final_price = round(final_price, 2)
        profit = round(final_price - total_cost, 2)

    # ================= RESULT =================

    if profit < 0:
        print("❌ Loss detected – offer not allowed")
    elif profit == 0:
        print(f"Customer Pays: ₹{final_price}")
        print("✔ No Profit, No Loss")
    else:
        print(f"Customer Pays: ₹{final_price}")
        print(f"✔ Profit Earned: ₹{profit}")

    print("✔ Business strategy satisfied")

    again = input("\nDo you want to continue billing? (y/n): ").lower()
    if again != "y":
        print("Thank you! Billing completed.")
        break