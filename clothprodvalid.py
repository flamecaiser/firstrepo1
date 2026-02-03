import pandas as pd
from datetime import datetime

print("----- Welcome to XYZ Fashions -----")

# ================= PRODUCT MASTER =================
PRODUCTS = {
    1: {"name": "Saree", "cost": 1200, "price": 2000, "stock": 10},
    2: {"name": "Kurta", "cost": 800, "price": 1400, "stock": 15},
    3: {"name": "Denims", "cost": 900, "price": 1600, "stock": 12},
    4: {"name": "Night Suit", "cost": 700, "price": 1300, "stock": 8},
    5: {"name": "Tops", "cost": 400, "price": 900, "stock": 20},
}

GST_RATE = 0.18  # 18% GST


def show_products():
    print("\nAvailable Products:")
    print("-" * 60)
    print("ID  Product       Price   Stock")
    print("-" * 60)
    for k, v in PRODUCTS.items():
        print(f"{k:<3} {v['name']:<12} ₹{v['price']:<7} {v['stock']}")
    print("-" * 60)


while True:

    print("""
Offers:
1. Flat discount on bill
2. Buy 1 Get 1 Free
3. Buy above ₹5000 & get 50% off
4. Buy 3 or more (same product) & get discount
5. Exit
""")

    try:
        choice = int(input("Select offer (1–5): "))
    except ValueError:
        print("❌ Invalid input")
        continue

    if choice == 5:
        print("Thank you! System closed.")
        break

    bill_data = []

    n = int(input("How many different products customer is buying? "))

    for i in range(n):

        while True:
            show_products()
            pid = int(input(f"Select product {i+1} (ID): "))

            if pid not in PRODUCTS:
                print("❌ Invalid product ID")
                continue

            product = PRODUCTS[pid]

            qty = int(input(f"Enter quantity for {product['name']}: "))

            if qty > product["stock"]:
                print("❌ Insufficient stock")
            else:
                break

        for _ in range(qty):
            bill_data.append({
                "Product": product["name"],
                "Cost": product["cost"],
                "Price": product["price"]
            })

        PRODUCTS[pid]["stock"] -= qty

    df = pd.DataFrame(bill_data)

    print("\n----- BILL SUMMARY -----")
    print(df)

    subtotal = df["Price"].sum()
    total_cost = df["Cost"].sum()

    # ================= OFFER LOGIC =================

    if choice == 1:
        disc = float(input("Enter discount %: ")) / 100
        discounted_amount = subtotal * (1 - disc)

    elif choice == 2:
        print(df[["Product", "Price"]])
        p = int(input("Primary item row number: ")) - 1
        f = int(input("Free item row number: ")) - 1
        discounted_amount = df.iloc[p]["Price"]

    elif choice == 3:
        discounted_amount = subtotal * 0.5 if subtotal >= 5000 else subtotal

    elif choice == 4:
        disc = float(input("Enter discount % for Buy 3: ")) / 100
        discounted_amount = 0

        for product, group in df.groupby("Product"):
            if len(group) >= 3:
                discounted_amount += (group["Price"] * (1 - disc)).sum()
            else:
                discounted_amount += group["Price"].sum()

    # ================= GST CALCULATION =================

    gst_amount = round(discounted_amount * GST_RATE, 2)
    final_amount = round(discounted_amount + gst_amount, 2)
    profit = round(discounted_amount - total_cost, 2)

    print("\n----- GST INVOICE -----")
    print(f"Subtotal        : ₹{subtotal}")
    print(f"After Discount  : ₹{round(discounted_amount,2)}")
    print(f"GST (18%)       : ₹{gst_amount}")
    print(f"Total Payable   : ₹{final_amount}")

    if profit > 0:
        print(f"✔ Profit Earned : ₹{profit}")
    elif profit == 0:
        print("✔ No Profit No Loss")
    else:
        print("❌ Loss detected")

    # ================= EXPORT BILL =================

    bill_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    df["GST"] = gst_amount / len(df)
    df["FinalPrice"] = final_amount / len(df)

    csv_name = f"bill_{bill_time}.csv"
    excel_name = f"bill_{bill_time}.xlsx"

    df.to_csv(csv_name, index=False)
    df.to_excel(excel_name, index=False)

    print("\n📁 Bill exported successfully:")
    print(f"✔ CSV  : {csv_name}")
    print(f"✔ Excel: {excel_name}")

    again = input("\nDo you want to continue billing? (y/n): ").lower()
    if again != "y":
        print("Thank you! Visit Again.")
        break