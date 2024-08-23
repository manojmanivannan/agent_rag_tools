import json
import re, sys
import glob
import uuid
from customRotatingHandler import MyLogger

LOG_FILENAME = 'graph/create-review-nodes.cypher'
EACH_LOG_FILE_SIZE = 500 * 1024 * 1024
NUM_OF_LOGS = 20
logger = MyLogger.get_logger(LOG_FILENAME, EACH_LOG_FILE_SIZE, NUM_OF_LOGS)


review_files = glob.glob('/home/manoj/Github/AmazonReviewData/*review-split*.json')
review_files = sorted(review_files)
print('//',f'There are a total of {len(review_files)} files')

def load_file(file_path):
    """
    Loads and returns the content of a text file as a list of lines.
    
    Parameters:
    file_path (str): Path to the text file.
    
    Returns:
    list: The content of the text file as a list of lines.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

# Generate REVIEW NODES

# each review looks like this
# {
#     "overall": 1.0,
#     "verified": false,
#     "reviewTime": "12 11, 2015",
#     "reviewerID": "A27BTSGLXK2C5K",
#     "asin": "B017O9P72A",
#     "reviewerName": "Jacob M. Wessler",
#     "reviewText": "Alexa is not able to control my lights. If I ask her to tell me what LIFX can do, she will give me an example with one of my group names. If I use that exact same group name in a new request, she'll await that she doesn't recognize the name. This skill is VERY buggy and has not yet worked for me. I even rest Alexa, uninstalled LIFX, and set everything up again.",
#     "summary": "VERY Buggy, doesn't work.",
#     "unixReviewTime": 1449792000
# }

# for each file 
for review_file in review_files[:2]:
    file_contents = load_file(review_file)
    print('//',f'There are a total of {len(file_contents)} reviews in file {review_file}')

    # for each line/review in the file
    for line in file_contents:
        try:
            line_json = json.loads(line)
            # print(json.dumps(line_json, indent=4))
            review_text = line_json.get('reviewText','').replace("'", "\\'").replace('"', '\\"')
            review_text = re.sub(r'\s+', ' ', review_text).strip()

            rating = line_json.get('overall','')
            product_id = line_json['asin']
            summary = line_json.get('summary',"").replace("'", "\\'").replace('"', '\\"')
            customer_id = line_json.get('reviewerID','')
            customer_name = line_json.get('reviewerName','')

            uniq_id = str(uuid.uuid4())

            query = f"""MERGE (c:Customer {{ID: '{customer_id}'}}) ON CREATE SET c.customer_name = '{customer_name}', c.products_bought = [] MERGE (p:Product {{asin: '{product_id}'}}) MERGE (c)-[:BOUGHT]->(p) ON MATCH SET c.products_bought = CASE WHEN NOT '{product_id}' IN c.products_bought THEN c.products_bought + ['{product_id}'] ELSE c.products_bought END MERGE (r:Review {{ID: '{uniq_id}'}}) SET r.text = '{review_text}', r.rating = {rating}, r.summary = '{summary}', r.product_id = '{product_id}' MERGE (r)<-[:WROTE]-(c) MERGE (p)-[:HAS_REVIEW]->(r);"""
            logger.info(query)
            

        except KeyError as e:
            print(f'// Skipping review due to KeyError {e}, {line_json}')
        except KeyboardInterrupt:
            print('Stopping..')
            sys.exit(1)
        except Exception as exc:
            print(f'// Skipping review due to Exception {exc}')

            # finally add command to create index
logger.info("DROP INDEX solution_index IF EXISTS;")
logger.info("CREATE VECTOR INDEX `solution_index` IF NOT EXISTS FOR (c:Review) ON (c.textEmbedding) OPTIONS { indexConfig: {`vector.dimensions`: 384, `vector.similarity_function`: 'cosine'}};")


