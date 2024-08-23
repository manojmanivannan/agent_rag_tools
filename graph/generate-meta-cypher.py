import json
import re, sys
import glob
import uuid
from customRotatingHandler import MyLogger

LOG_FILENAME = 'graph/create-meta-nodes.cypher'
EACH_LOG_FILE_SIZE = 500 * 1024 * 1024
NUM_OF_LOGS = 30
logger = MyLogger.get_logger(LOG_FILENAME, EACH_LOG_FILE_SIZE, NUM_OF_LOGS)


meta_files = glob.glob('/home/manoj/Github/AmazonReviewData/*meta-split*.json')
meta_files = sorted(meta_files)
print('//',f'There are a total of {len(meta_files)} files')

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

# each meta looks like this
#    {
#    "category": [
#        "Clothing, Shoes & Jewelry",
#        "Women",
#        "Clothing",
#        "Tops, Tees & Blouses",
#        "Blouses & Button-Down Shirts"
#    ],
#    "tech1": "",
#    "description": [
#        "(=^ ^=) 1.It is made of high quality materials,durable enought for your daily"
#    ],
#    "fit": "",
#    "title": "Women Blouse, Ninasill Hooded Sweatshirt Coat Winter Warm Wool Zipper Pockets Cotton Coat Outwear",
#    "also_buy": [],
#    "image": [
#        "https://images-na.ssl-images-amazon.com/images/I/41FcdYMol2L._SX38_SY50_CR,0,0,38,50_.jpg",
#        "https://images-na.ssl-images-amazon.com/images/I/51ul8a%2B-IjL._SX38_SY50_CR,0,0,38,50_.jpg",
#        "https://images-na.ssl-images-amazon.com/images/I/51zLLlGLEHL._SX38_SY50_CR,0,0,38,50_.jpg",
#        "https://images-na.ssl-images-amazon.com/images/I/515CIhAjPIL._SX38_SY50_CR,0,0,38,50_.jpg"
#    ],
#    "tech2": "",
#    "brand": "Ninasill_Blouse",
#    "feature": [
#        "Import",
#        "Versatile Occasions - "
#    ],
#    "rank": [],
#    "also_view": [],
#    "details": {},
#    "main_cat": "Movies & TV",
#    "similar_item": "",
#    "date": "<div class=\"a-fixed-left-grid a-spacing-none\"><div class=\"a-fixed-left-grid-inner\" style=\"padding-left:280px\"><div class=\"a-fixed-left-grid-col a-col-left\" style=\"width:280px;margin-left:-280px;float:left;\"><span class=\"a-declarative\" data-action=\"reviews:filter-action:push-state\" data-reviews:filter-action:push-state=\"{&quot;scrollToSelector&quot;:&quot;#reviews-filter-info&quot;,&quot;allowLinkDefault&quot;:&quot;1&quot;}\"><table id=\"histogramTable\" class=\"a-normal a-align-middle a-spacing-base\" role=\"presentation\"><tr class=\"a-histogram-row\"><td class=\"aok-nowrap\"><span aria-hidden=\"true\" class=\"a-size-base\">5 star</span><span class=\"a-offscreen\">5 star (0%)</span><span class=\"a-letter-space\"></span>",
#    "price": "$9.99 - $12.50",
#    "asin": "6305121869"
#    }


# for each file 
for meta_file in meta_files:
    file_contents = load_file(meta_file)
    print('//',f'There are a total of {len(file_contents)} products in file {meta_file}')

    # for each line/review in the file
    for line in file_contents:
        try:
            line_json = json.loads(line)
            # print(json.dumps(line_json, indent=4))
            meta_description = line_json.get('description',[])
            if meta_description:
                meta_description = meta_description[0].replace("'", "\\'").replace('"', '\\"')
            else:
                meta_description = ''
            meta_description = re.sub(r'\s+', ' ', meta_description).strip()
            category_list = [s.replace("'", "\\'").replace('"', '\\"') for s in line_json.get("category")]
            category_list = [re.sub(r'\s+', ' ', s).strip() for s in category_list]

            product_category = json.dumps(category_list).replace("'", "\\'")# this is a list
            brand = line_json.get("brand","")
            main_category = line_json.get("main_cat",'')
            price = line_json.get("price",'')
            product_id = line_json.get("asin",'')
            product_name = line_json.get("title",'').replace("'", "\\'").replace('"', '\\"')


            logger.info(f"MERGE (p:Product {{asin: '{product_id}'}}) ON MATCH SET p.name='{product_name}', p.category={product_category};")
        except KeyError as e:
            print(f'// Skipping meta KeyError due to {e}')
        except KeyboardInterrupt:
            print('Stopping..')
            sys.exit(1)
        except Exception as exc:
            print(f'// Skipping meta Exception due to {exc}')


