# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from typing import Dict, Any
from enum import Enum
from langchain.tools import BaseTool, StructuredTool, tool
import sqlite3
import re

def contains_non_alpha(string: str):
    return bool(re.search(r"[^a-zA-Z]", string))


class AggregationType(str, Enum):
    AVG = "avg"
    MAX = "max"
    SUM = "sum"
    COUNT = "count"
    MIN = "min"

class FilterCondition(BaseModel):
    conditions: Dict[str, Any] = {}

    def to_sql(self) -> str:
        if not self.conditions:
            return ""
        
        # Build the SQL WHERE clause with proper formatting
        conditions_sql = []
        for col, val in self.conditions.items():
            try:
                val = int(val)
                conditions_sql.append(f"{col} = {val}")
            except ValueError:
                conditions_sql.append(f"{col} = '{val}'")
        return " WHERE " + " AND ".join(conditions_sql)


@tool("get_available_columns")
def get_available_columns() -> str:
    """
    Retrieves all the available columns from the 'procedures' table.
    """
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('./database/example.db')
        cursor = conn.cursor()
        
        # Execute the query
        query = f"PRAGMA table_info(procedures)"
        cursor.execute(query)
        
        # Fetch the results
        results = cursor.fetchall()
        unique_values = [row[0] for row in results]
        
        # Close the connection
        conn.close()
        
        return {"response": f'The table has ' + ', '.join(unique_values)}
    except Exception as e:
        raise Exception(e)
    
@tool("get_unique_dimension_values", return_direct=False)
def get_unique_dimension_values(dimension: str) -> str:
    """
    Retrieves a list of unique items from the specified column from 'procedures' table.
    
    Parameters:
    dimension (str): The name of the column from which to retrieve unique values.
    
    Returns:
    str: A comma-separated list of unique values from the specified column.
    """
    print("Running get_unique_dimension_values")
    if contains_non_alpha(dimension):
        return f"{dimension} is not well formatted. remove extra quotes"
    
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('./database/example.db')
        cursor = conn.cursor()
        
        # Execute the query
        query = f"SELECT DISTINCT {dimension} FROM procedures"
        cursor.execute(query)
        
        # Fetch the results
        results = cursor.fetchall()
        unique_values = [row[0] for row in results]
        
        # Close the connection
        conn.close()
        
        return {"response": f'The distinct {dimension}\'s are ' + ', '.join(unique_values)}
    except Exception as e:
        raise Exception(e)

@tool("get_metric_values", return_direct=False)
def get_metric_values(metric: str, aggregation_type: AggregationType, filter: FilterCondition) -> str:
    """
    Retrieves an aggregated value of the specified metric from 'procedures' table.
    
    Parameters:
    metric (str): The name of the metric to aggregate.
    aggregation_type (AggregationType): The type of aggregation to perform (e.g., sum, avg, count, min or max).
    filter (FilterCondition): A dictionary of column-value pairs to filter the data.
    
    Returns:
    str: The aggregated value of the specified metric.
    """
    print("Running get_metric_values")
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('./database/example.db')
        cursor = conn.cursor()
        
        # Execute the query
        filter_sql = filter.to_sql()
        query = f"SELECT {aggregation_type.value}({metric}) FROM procedures {filter_sql}"
        print(query)
        cursor.execute(query)
        
        # Fetch the result
        result = cursor.fetchone()
        aggregated_value = result[0] if result else "No data found"
        
        # Close the connection
        conn.close()
        
        return {"response": aggregated_value}
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    


