from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient
from langchain.embeddings import HuggingFaceEmbeddings
from openai import OpenAI
import json

example_json = json.dumps({ 'product' : 'trimmer', 'sale_price' : '200', 'rating': '4', 'description': 'used for body hair also', 'brand' : 'philips', 'type': 'null', 'category' : 'Beauty & Hygiene'})
embeddings = HuggingFaceEmbeddings()
client = QdrantClient(host='localhost', port=6333)
openai_client = OpenAI(api_key = "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")

app = FastAPI()



class SearchBody(BaseModel):
    query: str

@app.post("/query-search")
def query_search(search: SearchBody):
    response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": """Break '{pholder}' into requirements of product, category, rating, sale_price, type, rating, brand. Place rest of the information as description. Respond in json. If query doesn't contain info give null as the value for each key. Strictly answer from the query. Answer category from list of these values 'Beauty & Hygiene','Kitchen, Garden & Pets', 'Cleaning & Household', 'Gourmet & World Food', 'Foodgrains, Oil & Masala', 'Snacks & Branded Foods', 'Beverages', 'Bakery, Cakes & Dairy', 'Baby Care', 'Eggs, Meat & Fish', 'Fruits & Vegetables'. Example for query 'Philips trimmer with price 250 and rating 4 which i could use for body hair' should return '{ex_json}' """.format(pholder = search.query, ex_json = example_json)}
            ]
        )
    query_params = json.loads(response.choices[0].message.content)

    product_ids = []
    product_scores = {}
    product_names = {}
    for k,v in query_params.items():
        if v != "null" :
            query_results = query_qdrant(v , "Products", k, 10 )
            for i, product in enumerate(query_results):
                if product.payload['index'] in product_ids:
                    product_scores[product.payload['index']] += round(product.score, 3)
                else:
                    product_ids.append(product.payload['index'])
                    product_scores[product.payload['index']] = round(product.score, 3)
                    product_names[product.payload['index']] = product.payload['product']

    product_id1 = max(product_scores, key= lambda x: product_scores[x])
    product_id2 = max(product_scores, key= lambda x: product_scores[x] < product_scores[product_id1])
    product_id3 = max(product_scores, key= lambda x: product_scores[x] < product_scores[product_id2])
    
    return [product_names[product_id1], product_names[product_id2], product_names[product_id3] ]



def query_qdrant(query, collection_name, vector_name, top_k=20):
    # Creates embedding vector from user query
    embedded_query = embeddings.embed_query(str(query))

    query_results = client.search(
        collection_name=collection_name,
        query_vector= (vector_name, embedded_query),
        with_payload= True,
        limit=top_k
    )

    return query_results
