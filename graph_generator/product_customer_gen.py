import random
from faker import Faker

# Initialize the Faker library
fake = Faker()

# Generate a list of random categories
categories = [
    "Electronics", "Books", "Clothing", "Home & Kitchen", "Sports & Outdoors",
    "Toys & Games", "Health & Personal Care", "Automotive", "Baby", "Beauty"
]

# Function to generate random products
def generate_products(n):
    products = []
    for _ in range(n):
        product = {
            "asin": fake.bothify(text='B#########'),
            "name": fake.catch_phrase(),
            "category": random.sample(categories, k=random.randint(1, 3))
        }
        products.append(product)
    return products

# Function to generate random customers with reviews
def generate_customers(n, products):
    customers = []
    for _ in range(n):
        customer = {
            "id": fake.uuid4(),
            "name": fake.name(),
            "reviews": []
        }
        # Each customer writes between 1 and 5 reviews
        for _ in range(random.randint(1, 5)):
            product = random.choice(products)
            review = {
                "id": fake.uuid4(),
                "product_asin": product["asin"],
                "text": fake.text(max_nb_chars=200),
                "rating": random.uniform(1, 5),
                "summary": fake.sentence()
            }
            customer["reviews"].append(review)
        customers.append(customer)
    return customers

# Generate random products and customers
num_products = 10
num_customers = 5

products = generate_products(num_products)
customers = generate_customers(num_customers, products)

