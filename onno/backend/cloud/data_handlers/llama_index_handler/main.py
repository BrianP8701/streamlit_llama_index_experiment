from google.cloud import storage
from llama_index.node_parser import HierarchicalNodeParser
from llama_index import VectorStoreIndex, load_index_from_storage, StorageContext
from llama_index.schema import NodeWithScore
import gcsfs
import json
import os

class CloudLLAMA_Index_Manager:
    '''
    This class manages a llama-index object stored in a JSON file on the cloud.
    Documents are added to the index and context is retrieved directly on the cloud without
    downloading the index to the local file system.
    
    retrieve_context(messages) -> str
    '''
    def __init__(self, project_name, bucket_name, llama_index_gcs_path):
        self.client = storage.Client(project=project_name)
        self.bucket = self.client.bucket(bucket_name)
        self.bucket_name = bucket_name
        self.node_parser = HierarchicalNodeParser.from_defaults()
        self.llama_index_gcs_path = llama_index_gcs_path
        self.gcs = gcsfs.GCSFileSystem(project=project_name, token='secrets/onno-404216-b073f407c6eb.json')
        self.index = self.retrieve_or_create_index()
        
    def retrieve_or_create_index(self):
        if self.check_folder_exists(self.llama_index_gcs_path):
            return self.retrieve_index_from_gcs()
        else:
            return self.create_new_index()

    def create_new_index(self):
        index = VectorStoreIndex([])
        index.set_index_id(os.path.basename(self.llama_index_gcs_path))
        self.save_index_to_gcs(index)
        return index

    def retrieve_index_from_gcs(self):
        sc = StorageContext.from_defaults(persist_dir=self.bucket_name+'/'+self.llama_index_gcs_path, fs=self.gcs)
        return load_index_from_storage(sc, os.path.basename(self.llama_index_gcs_path))
    
    def save_index_to_gcs(self, index):
        index.storage_context.persist(self.bucket_name + '/' + self.llama_index_gcs_path, fs=self.gcs)

    def check_folder_exists(self, folder_prefix):
        blobs = self.bucket.list_blobs(prefix=folder_prefix)
        return any(True for _ in blobs)  # Folder exists if there are objects with the specified prefix

    def add_documents_to_index(self, documents_gcs_paths):
        for gcs_path in documents_gcs_paths:
            # Assuming documents are JSON files and we can use the JSON content as documents
            data = self.gcs.open(gcs_path, 'r').read()
            document = json.loads(data)
            self.index.insert(document)
        # Save the updated index back to GCS
        self.save_index_to_gcs(self.index)

# Cloud function handler
def process_documents_and_update_index(data, context):
    """
    This function is triggered by an event that provides JSON payload with 'data' and 'index_path'.
    """

    documents_gcs_paths = data['onno/users/b/libraries/avalon/text/DL_MIT.pdf']
    

    manager = CloudLLAMA_Index_Manager('onno-404216', 'onno', 'Briansvectoryyyy')
    manager.create_new_index()
    manager.add_documents_to_index(documents_gcs_paths)
    print(f"Updated index with documents from {documents_gcs_paths}")
