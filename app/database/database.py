from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('URI')

class Database:
    def __init__(self,uri):
        self.uri = uri
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client['cv-reviewer']  # Replace with your actual database name
        self.collection = self.db['cvs']
        self.insert_id_list = []

    def insert_data(self, data):
        result = self.collection.insert_one(data)
        self.insert_id_list.append(result.inserted_id)
        return result.inserted_id
    
    def update_one(self, query, update_data):
        result = self.collection.update_one(query, {"$set": update_data})
        return result.modified_count

    def update_many(self, query, update_data):
        result = self.collection.update_many(query, {"$set": update_data})
        return result.modified_count
    
    def update_structured_results(self, pdf_bytes, structured_results):
        result = self.collection.update_one(
            {"pdf": pdf_bytes},
            {"$set": {"structured_results": structured_results}}
        )
        return result.modified_count

    def update_analysis_results(self, pdf_bytes,analysis_results):
        result = self.collection.update_one(
            {'pdf': pdf_bytes},
            {'$set': {'analysis_results': analysis_results}},
            upsert=True
        )
        return result.upserted_id or result.modified_count > 0




    def insert_many(self, data_list):
        result = self.collection.insert_many(data_list)
        self.insert_id_list.extend(result.inserted_ids)
        return result.inserted_ids

    def find_one(self, query):
        return self.collection.find_one(query)

    def find_many(self, query, limit=0):
        return list(self.collection.find(query).limit(limit))

    

    def delete_one(self, query):
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, query):
        result = self.collection.delete_many(query)
        return result.deleted_count

    def count_documents(self, query={}):
        return self.collection.count_documents(query)

    def aggregate(self, pipeline):
        return list(self.collection.aggregate(pipeline))

    def create_index(self, keys, **kwargs):
        return self.collection.create_index(keys, **kwargs)

    def close_connection(self):
        self.client.close()
    
    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
