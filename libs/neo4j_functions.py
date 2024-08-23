import os
from neo4j import GraphDatabase
from typing import Any, Dict


URI = "neo4j://"+os.environ.get('NEO4J_URI',"localhost:7687")
AUTH = (os.environ.get('NEO4J_USERNAME'),os.environ.get('NEO4J_PASSWORD'))


driver = GraphDatabase.driver(uri=URI, auth=AUTH)



def value_sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize the input dictionary.

    Sanitizes the input dictionary by removing embedding-like values,
    lists with more than 128 elements, that are mostly irrelevant for
    generating answers in a LLM context. These properties, if left in
    results, can occupy significant context space and detract from
    the LLM's performance by introducing unnecessary noise and cost.
    """
    LIST_LIMIT = 128
    # Create a new dictionary to avoid changing size during iteration
    new_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            # Recurse to handle nested dictionaries
            new_dict[key] = value_sanitize(value)
        elif isinstance(value, list):
            # check if it has less than LIST_LIMIT values
            if len(value) < LIST_LIMIT:
                # if value is a list, check if it contains dictionaries to clean
                cleaned_list = []
                for item in value:
                    if isinstance(item, dict):
                        cleaned_list.append(value_sanitize(item))
                    else:
                        cleaned_list.append(item)
                new_dict[key] = cleaned_list  # type: ignore[assignment]
        else:
            new_dict[key] = value
    return new_dict

def run_query(query: str ,params: dict ={}, sanitize=True):
    from neo4j import Query
    from neo4j.exceptions import CypherSyntaxError, DriverError, Neo4jError

    with driver.session() as session:
        try:
            data = session.run(Query(text=query, timeout=10), params)
            json_data = [r.data() for r in data]
            if sanitize:
                json_data = [value_sanitize(el) for el in json_data]
            # print(json_data)
            return json_data
        
        except DriverError as exception:
            return f"DriverError: raised an error: \n{exception}"

        except Neo4jError as exception:
            return f"Neo4jError raised an error: \n{exception}"
        
        except CypherSyntaxError as e:
            return f"Generated Cypher Statement is not valid\n{e}"