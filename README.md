# Query_engine
LLM Project

# Product Search API with Vector Embedding

This repository provides a suite of tools for creating a semantic search engine for product data. It includes a script for generating vector embeddings from product data and a FastAPI application that serves as a search API using these embeddings. The search is powered by Qdrant and utilizes natural language processing via HuggingFace and OpenAI APIs.

## Overview

The project is composed of two parts:
1. `vector_embedding_inserter.py`: A script for reading product data from a CSV file, generating vector embeddings, and inserting them into a Qdrant database.
2. `main.py`: A FastAPI application that provides an API endpoint to perform a vector-based search on the Qdrant database using natural language queries processed by OpenAI's GPT-3.5 model.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- FastAPI
- Uvicorn (for serving the FastAPI application)
- Qdrant (running on localhost or a remote server)
- An OpenAI API key

### Installation

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>

Install the necessary dependencies : 
pip install -r requirements.txt

Now make sure Qdrant is running and accessible on the configured port.
First, download the latest Qdrant image from Dockerhub:
'docker pull qdrant/qdrant'
Then, run the service:
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

Under the default configuration all data will be stored in the ./qdrant_storage directory. This will also be the only directory that both the Container and the host machine can both see.

SentenceTransformers is a Python framework for state-of-the-art sentence, text and image embeddings. You can use this framework to compute sentence / text embeddings for more than 100 languages. These embeddings can then be compared e.g. with cosine-similarity to find sentences with a similar meaning.

pip install -U sentence-transformers


Vector Embedding Script:
This script ('vector_embedding_inserter.py') processes a CSV file to create vector embeddings for product-related fields and inserts the data into a Qdrant collection.

Usage:
Ensure 'bigBasketProducts.csv' is placed in the root directory of the project.
Run the script using the command: python vector_embedding_inserter.py

Import Statements: The script begins by importing necessary libraries and modules. QdrantClient from qdrant_client is used to interact with a Qdrant database. VectorParams and Distance are used to configure the vector space in which the data will be embedded. Pandas is imported for data manipulation, and HuggingFaceEmbeddings from langchain.embeddings is used to convert text data into vector embeddings.

Embeddings Initialization: An object of HuggingFaceEmbeddings is created. This object will be used to generate vector embeddings for textual data.

Load and Prepare Dataset:

dataset = pd.read_csv("bigBasketProducts.csv"): The CSV file bigBasketProducts.csv is loaded into a pandas DataFrame.
dataset_df = pd.DataFrame(dataset): A new DataFrame is created from the loaded data for further processing.
Embedding Process: For each column of interest (such as 'product', 'category', etc.), the script applies the embed_query method of the embeddings object to each value in the column to generate embeddings. This is done in a loop, and the embeddings for each column are stored in a new column with the suffix _embedding.

Output Embedded Data: After embedding, the DataFrame is saved back to a new CSV file named 'output.csv'.

Qdrant Client Setup: A QdrantClient is initialized to connect to a Qdrant server running locally on the default port 6333.

Vector Space Configuration: The vector size is determined from the length of the embedding of the 'description' field. The script then configures a collection in Qdrant called "Products", setting up the vector space for each field with the cosine distance metric.

Data Insertion into Qdrant:

The DataFrame length is calculated, and a loop is set up to insert the data into the Qdrant collection in batches of 100.
Within the loop, for each batch, a smaller DataFrame mini_dataset_df is created with the current slice of the main DataFrame.
The client.upsert method is called to insert the points into the "Products" collection. Each point represents a product, with its various attributes (like 'product', 'category', etc.) and their respective embeddings.
Each point also includes a payload, which is a dictionary with the product's index and name.
Completion: Once the loop has finished processing all batches, a completion message is printed.

This script essentially reads product information from a CSV, creates vector embeddings for the textual data, and then inserts these embeddings into a Qdrant collection for later retrieval and similarity searching. This is useful for building a semantic search engine where users can query products based on textual similarity rather than exact matches.


The 'main.py' Python code defines a FastAPI application that performs a vector-based search on a Qdrant database using vector embeddings. It leverages the HuggingFace embeddings model to convert text queries into vector embeddings, and then uses those embeddings to find the most similar items in the Qdrant database. It also integrates with the OpenAI GPT-3.5 API to process natural language queries into structured JSON that can be used to perform the search.
This FastAPI application provides a '/query-search' endpoint that accepts natural language queries about products and returns the most relevant product names.

Imports and Initializations:

Union from typing and FastAPI from fastapi are used for type hinting and to define the web API, respectively.
BaseModel from pydantic is used for request body validation.
QdrantClient from qdrant_client is used to interact with the Qdrant database.
HuggingFaceEmbeddings from langchain.embeddings is used to generate vector embeddings from text.
OpenAI from openai is used to interact with the OpenAI API.
json is used for JSON parsing and formatting.
FastAPI App Definition: An instance of FastAPI is created, which is the framework that will handle incoming web requests.

API Endpoint /query-search:

This endpoint accepts POST requests containing a JSON body with a single query string.
It uses the OpenAI API to break down the user's natural language query into structured JSON that represents different attributes of a product (like product, category, rating, etc.).
The JSON structure is predefined in example_json and is used as a template for the AI to fill in with details extracted from the user's query.
After receiving the structured JSON from OpenAI, the script extracts the values and uses them to perform a search in the Qdrant database.
Search Logic:

For each non-null attribute in the JSON, a search is performed in the Qdrant database within the "Products" collection using the query_qdrant function.
It aggregates the scores for products that match multiple attributes, sums these scores, and keeps track of them in product_scores.
product_names stores the actual product names indexed by their unique identifiers.
The script then selects the top three product IDs based on the highest aggregate scores.
The query_qdrant Function:

This function takes a textual query and a vector field name (like product, category, etc.), generates an embedding for the query, and performs a vector search in the Qdrant database.
It returns the search results, which include the product's unique identifier, its score, and its payload (additional data associated with the vector).
Return Value:

The endpoint returns the names of the top three products with the highest aggregated scores.
This application essentially provides a REST API endpoint that allows users to search for products using natural language queries. It uses advanced NLP models to interpret the queries and a vector database for efficient similarity search. It's an example of how modern AI-powered search engines can go beyond keyword matching to understand user intent and context.

Usage:
Start the FastAPI server: uvicorn main:app --reload

Send a POST request to '/query-search' with a JSON body containing a query field.

Configuration:
Configure your OpenAI API key in the FastAPI application script.
Ensure the CSV file is formatted correctly and includes the required fields for the embedding script.
Adjust the vector_embedding_inserter.py script if the fields differ from those expected.

API Reference
POST '/query-search': Accepts a JSON body with a 'query' string and returns the names of the top three products matching the query.




