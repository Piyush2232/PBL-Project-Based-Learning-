import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('en_IN')

# Broader categories with both specific brands and generic descriptions
financial_categories = {
    "Food": ["Swiggy Delivery", "Zomato", "McDonalds", "Burger King", "Local Cafe", "KFC", "Dominos", "Subway", "Starbucks", "Bake Shop", "Diner", "Restaurant", "Street Food", "Tea Stall", "Coffee Shop", "Pizza", "Bakery"],
    "Travel": ["Uber Ride", "Ola Cabs", "IRCTC Train", "Metro Recharge", "HP Petrol Pump", "Indian Oil", "Rapido", "Flight Ticket", "Toll", "Parking", "Bus Ticket", "Auto Rickshaw", "Fuel", "Ferry", "Car Rental"],
    "Shopping": ["Amazon Order", "Flipkart", "Myntra", "Ajio", "Decathlon", "Zara", "H&M", "Reliance Digital", "Croma", "Mall", "Apparel Store", "Electronics", "Shoe Store", "Boutique", "Hardware Store"],
    "Bills": ["Jio Recharge", "Airtel Broadband", "Electricity Bill", "Water Bill", "Gas Cylinder", "Maintenance", "Property Tax", "Internet", "Mobile Postpaid", "DTH Recharge"],
    "Subscriptions": ["Netflix", "Spotify Premium", "Amazon Prime", "YouTube Premium", "Hotstar", "Gym", "Cloud Storage", "Software", "Magazine", "News", "Fitness App"],
    "Groceries": ["Blinkit", "Zepto", "Swiggy Instamart", "BigBasket", "Dmart", "Reliance Smart", "Local Kirana", "Supermarket", "Fruits and Veg", "Meat Shop", "Dairy", "Provisions"],
    "Others": ["Pharmacy", "Movie Ticket", "Haircut", "Gift", "Stationery", "Gym Membership", "Doctor", "Hospital", "Donation", "Pet Supplies", "Laundry", "Saloon"]
}

start_date = datetime(2025, 1, 1)

with open('large_transactions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Description', 'Amount'])
    
    # Generate 500 completely random transactions
    for i in range(500):
        # Random date within the last year
        current_date = start_date + timedelta(days=random.randint(0, 365))
        
        # Pick a random category
        category = random.choice(list(financial_categories.keys()))
        
        # Determine the base description context
        desc_base = random.choice(financial_categories[category])
        
        # Introduce significant variations to make each entry truly unique
        variation_type = random.random()
        if variation_type > 0.8:
            # 20% chance: Random company prefix/suffix using Faker
            desc = f"{fake.company()} - {desc_base}"
        elif variation_type > 0.6:
            # 20% chance: Random UPI ID format
            desc = f"UPI/{desc_base}/{fake.bban()[-6:]}"
        elif variation_type > 0.4:
            # 20% chance: POS terminal format
            desc = f"POS/{desc_base}/{fake.city()}"
        elif variation_type > 0.2:
            # 20% chance: Online gateway format
            desc = f"PGWY/{desc_base}/{fake.ean8()}"
        else:
            # 20% chance: Just standard with some random ID
            desc = f"{desc_base} #{fake.random_int(min=1000, max=99999)}"
            
        # Generate amount based on category (negative amounts for expenses)
        if category == "Food":
            amt = -random.randint(50, 2500)
        elif category == "Travel":
            amt = -random.randint(20, 5000)
        elif category == "Shopping":
            amt = -random.randint(200, 15000)
        elif category == "Bills":
            amt = -random.randint(100, 5000)
        elif category == "Subscriptions":
            amt = -random.choice([99, 149, 199, 299, 499, 999, 1499])
        elif category == "Groceries":
            amt = -random.randint(100, 6000)
        else:
            amt = -random.randint(50, 4000)
            
        # Add a random decimal portion to make amounts look organic (e.g., 450.50)
        amt = float(amt) - round(random.uniform(0.01, 0.99), 2)
            
        # Occasionally add an income (positive amount)
        if random.random() > 0.95:
            income_sources = ["Salary/Credit", f"Transfer from {fake.name()}", "Freelance Init", "Dividend", "Refund"]
            desc = random.choice(income_sources)
            amt = float(random.randint(15000, 95000)) + round(random.uniform(0.01, 0.99), 2)
            
        writer.writerow([current_date.strftime("%Y-%m-%d"), desc, round(amt, 2)])

print("Successfully generated a completely unique 'large_transactions.csv' with 500 records using Faker!")
