from py2neo import Graph, Node, Relationship

# Connect to the Neo4j database
graph = Graph("neo4j://localhost:7687", auth=("neo4j", "password123"))

from product_customer_gen import products, customers

# Create product nodes
for product in products:
    product_node = Node("Product", asin=product["asin"], name=product["name"], category=product["category"])
    graph.merge(product_node, "Product", "asin")

# Create customer nodes and their relationships with products and reviews
for customer in customers:
    customer_node = Node("Customer", ID=customer["id"], customer_name=customer["name"], products_bought=[])
    graph.merge(customer_node, "Customer", "ID")

    for review in customer["reviews"]:
        # Find the product node for the review
        product_node = graph.nodes.match("Product", asin=review["product_asin"]).first()

        # Create the review node
        review_node = Node("Review", ID=review["id"], text=review["text"], rating=review["rating"], summary=review["summary"], product_id=review["product_asin"])
        graph.create(review_node)

        # Create relationships
        bought_relationship = Relationship(customer_node, "BOUGHT", product_node)
        wrote_relationship = Relationship(customer_node, "WROTE", review_node)
        has_review_relationship = Relationship(product_node, "HAS_REVIEW", review_node)

        graph.merge(bought_relationship, "Customer", "ID")
        graph.merge(wrote_relationship, "Review", "ID")
        graph.merge(has_review_relationship, "Review", "ID")

        # Update the customer's products_bought property
        customer_node["products_bought"].append(review["product_asin"])
        graph.push(customer_node)
