# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
import sqlite3



class DimSearchInput(BaseModel):
    dimension: str = Field(description="name of the dimension or column")

class MetricsSearchInput(BaseModel):
    metric: str = Field(description="name of the metric or column")
    aggregation_type: str = Field(description="type of aggreation. sum or avg")

@tool("get_unique_dimension_values", args_schema=DimSearchInput, return_direct=False)
def get_unique_dimension_values(dimension: str):
    """
    Retrieves a list of unique items from the specified column (dimension) from 'procedures' table.
    
    Parameters:
    dimension (str): The name of the column from which to retrieve unique values.
    
    Returns:
    str: A comma-separated list of unique values from the specified column.
    """
    print("Running get_unique_dimension_values")
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
        
        return {'response':f'The distinct {dimension}`s are ' + ', '.join(unique_values)}
    except Exception as e:
        return{'response':f"An error occurred: {e}"} 

@tool("get_metric_values", args_schema=MetricsSearchInput, return_direct=False)
def get_metric_values(metric: str, aggregation_type):
    """
    Retrieves an aggregated value of the specified metric from 'procedures' table.
    
    Parameters:
    metric (str): The name of the metric to aggregate.
    aggregation_type (str): The type of aggregation to perform (e.g., 'sum', 'average').
    
    Returns:
    str: The aggregated value of the specified metric.
    """
    print("Running get_metric_values")
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('./database/example.db')
        cursor = conn.cursor()
        
        # Execute the query
        query = f"SELECT {aggregation_type}({metric}) FROM procedures"
        cursor.execute(query)
        
        # Fetch the result
        result = cursor.fetchone()
        aggregated_value = result[0] if result else "No data found"
        
        # Close the connection
        conn.close()
        
        return {'response':str(aggregated_value)}
    except Exception as e:
        return{'response':f"An error occurred: {e}"} 