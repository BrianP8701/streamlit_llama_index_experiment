from google.cloud import storage
from llama_index.node_parser import HierarchicalNodeParser
from llama_index import VectorStoreIndex, load_index_from_storage, StorageContext, Document
from llama_index.schema import NodeWithScore
import functions_framework
import gcsfs
import os

@functions_framework.http
def llama_index_handler(request):
    """
    This function processes the HTTP request to interact with a llama index stored on Google Cloud Storage.
    It dispatches the request to various handlers based on the function name specified in the request JSON.

    Functions:
    - "retrieve_context": Retrieves context based on the given messages from the request JSON.
    - "add_documents_to_index": Adds documents to the index from the specified GCS folder.
    
    Args:
        request (flask.Request): The request object. Expected JSON structure:
            {
                "project_name": str,            # GCP project name.
                "bucket_name": str,             # GCS bucket name.
                "llama_index_gcs_path": str,    # GCS path to the llama index folder.
                ...                             # Other fields depending on the function_name.
            }

    Returns:
        flask.Response: A response object with the result of the dispatched function call, or an error message.
    """
    request_json = request.get_json(silent=False)
    project_name = request_json['project_name']
    bucket_name = request_json['bucket_name']
    llama_index_gcs_path = request_json['llama_index_gcs_path']
    
    handler = LLAMA_Index_Retriever(project_name, bucket_name, llama_index_gcs_path)
    try:
        result = handler.retrieve_context(request_json['messages'])
        return result, 200
    except Exception as e:
        return f"Invalid Input: {e}", 500

class LLAMA_Index_Retriever:
    def __init__(self, project_name, bucket_name, llama_index_gcs_path):
        self.client = storage.Client(project_name)
        self.bucket = self.client.bucket(bucket_name)
        self.bucket_name = bucket_name
        self.node_parser = HierarchicalNodeParser.from_defaults()
        self.llama_index_gcs_path = llama_index_gcs_path
        self.gcs = gcsfs.GCSFileSystem()
        if self.check_folder_exists(llama_index_gcs_path):
            self.index = self.retrieve_index_from_gcs()    
            self.retriever = self.index.as_retriever()
        else:
            self.create_new_index()

    def dispatch(self, function_name, *args, **kwargs):
        function_map = {
            'retrieve_context': self.retrieve_context,
            'add_documents_to_index': self.add_documents_to_index,
        }
        if function_name not in function_map:
            raise ValueError(f"Function {function_name} not found.")
        return function_map[function_name](*args, **kwargs)
    
    def create_new_index(self):
        self.index = VectorStoreIndex([])
        self.index.set_index_id(os.path.basename(self.llama_index_gcs_path))
        self.save_index_to_gcs()
        self.retriever = self.index.as_retriever()
        return "Created new index successfully."
            
    def retrieve_context(self, messages):
        retriever = self.retriever
        retrieved_nodes: list[NodeWithScore] = retriever.retrieve(messages[-1]['message'])
        return ' '.join([node.text.replace('\n', ' ') for node in retrieved_nodes])
    
    def save_index_to_gcs(self):
        self.index.storage_context.persist(self.bucket_name + '/' + self.llama_index_gcs_path, fs=self.gcs)
        self.index = self.retrieve_index_from_gcs()
        return "Saved index successfully."

    def check_folder_exists(self, folder_prefix):
        blobs = self.bucket.list_blobs(prefix=folder_prefix)
        for blob in blobs:
            return True  # Folder exists as there are objects with the specified prefix
        return False  # Folder doesn't exist or is empty
    
    def retrieve_index_from_gcs(self):
        sc = StorageContext.from_defaults(persist_dir=self.bucket_name+'/'+self.llama_index_gcs_path, fs=self.gcs)
        return load_index_from_storage(sc, os.path.basename(self.llama_index_gcs_path))
    
    def add_documents_to_index(self, gcs_folder_prefix):
        documents = self.get_documents(gcs_folder_prefix)
        for doc in documents:
            self.index.insert(doc)
        self.save_index_to_gcs()
    
    def get_documents(self, gcs_folder_prefix):
        documents = []
        for blob in self.bucket.list_blobs(prefix=gcs_folder_prefix):
            content = blob.download_as_text()
            content = Document(text=content)
            documents.append(content)
        return documents