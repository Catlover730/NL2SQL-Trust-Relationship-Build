# NL2SQL Trust Relationship Build

## Overview
This project focuses on visualizing SQL queries using Graphviz. It includes a Python script for parsing SQL queries and generating corresponding visual representations. The project is beneficial for understanding and demonstrating the structure and flow of SQL queries.

## Files in the Project
- `sqlvis.py`: Contains the `SQLVisualization` class, which generates visualizations for SQL queries.
- `sqlparser.py`: A script for parsing SQL queries into components like SELECT, FROM, WHERE, etc.
- `Demo1.ipynb` : Demonstrating how to apply encoder, decoder and attention to output sql executing process step by step. (Incomplete)
- `Demo2.ipynb`: Demonstrating the how to generate a graph of sql executing process.
- `training_set.json`: A JSON file that provides a set of SQL queries and corresponding parsed components for training or demonstration purposes.

## How to Use
1. **Parsing SQL Queries**: Use `sqlparser.py` to parse a SQL query into its constituent components.
2. **Generating Visualization**: Pass the parsed components to the `SQLVisualization` class in `sqlvis.py` to generate a visual representation of the query.

## Dependencies
- Python 3.7.4
- Graphviz 0.20.1
- sqlparse 0.4.4

## Example Usage
```python
from sqlparser import parse_sql
from sqlvis import SQLVisualization

# Example SQL query
sql_query = "SELECT column1 FROM table1 WHERE column2 = 'value' GROUP BY column3 HAVING count(column1) > 5"

# Parse the SQL query
parsed_components = parse_sql(sql_query)

# Create and render the visualization
visualizer = SQLVisualization(parsed_components)
visualizer.create_graph()