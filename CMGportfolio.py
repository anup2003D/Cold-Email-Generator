import pandas as pd
import chromadb
import uuid


import os
import pandas as pd

class Portfolio:
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        self.data = pd.read_csv(file_path)

        required_columns = {"Techstack", "Links"}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        base_dir = os.getcwd()
        vectorstore_path = os.path.join(base_dir, "vectorstore")
        os.makedirs(vectorstore_path, exist_ok=True)

        try:
            self.chroma_client = chromadb.PersistentClient(path=vectorstore_path)
            self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize chroma client: {e}")

        self.load_portfolio()



    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])