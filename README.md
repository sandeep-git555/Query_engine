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

Vector Embedding Script:
This script ('vector_embedding_inserter.py') processes a CSV file to create vector embeddings for product-related fields and inserts the data into a Qdrant collection.

Usage
Ensure 'bigBasketProducts.csv' is placed in the root directory of the project.
Run the script using the command: python vector_embedding_inserter.py

This FastAPI application provides a '/query-search' endpoint that accepts natural language queries about products and returns the most relevant product names.

Usage
Start the FastAPI server: uvicorn main:app --reload

Send a POST request to '/query-search' with a JSON body containing a query field.

Configuration:
Configure your OpenAI API key in the FastAPI application script.
Ensure the CSV file is formatted correctly and includes the required fields for the embedding script.
Adjust the vector_embedding_inserter.py script if the fields differ from those expected.

API Reference
POST '/query-search': Accepts a JSON body with a 'query' string and returns the names of the top three products matching the query.




