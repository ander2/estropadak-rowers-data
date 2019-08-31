# Parse for rower data

## Parsers
Every league has it's own parser located in the parser folder

## Utils
Once we have the parsers, we have some utilities to use the parsed data:
*`analize.py`: Uses the parsers to parse all the data and create a pickle file
*`create_csv.py`:  Uses the parsers to parse all the data and creates a CSV file
*`export_data_to_couchdb.py`: Reads values from couchdb and Uses the generated pickle file to update the data in the couchdb database