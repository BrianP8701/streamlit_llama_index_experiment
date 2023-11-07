import streamlit as st
from onno.shared.utils.database_utils import retrieve_user_info, save_user_info, save_uploaded_file_to_gcs, does_file_exists_in_gcs
from onno.frontend.helpers.user_utils import initialize_user_info, create_new_empty_library
from onno.backend.local.data_loaders.pdf_loader import PDFLoader

class Data:
    def __init__(self):
        pass
    
    def display(self):
        
        libraries, upload_pdf, scrape_website, scrape_github_repo = st.tabs(
            ["Libraries", "Upload PDF", "Scrape Website", "Scrape Github Repo"]
        )
            
        with libraries:
            st.write("A library is a collection of text, coming from textbooks, documentation, code etc. Given that you might have seperate projects and datasets, you can create multiple libraries to keep them seperate.")
            st.divider()
            new_library_name = st.text_input('')

            if st.button('Create New Library'):
                if new_library_name == '':
                    st.error('Please enter a library name')
                elif new_library_name in st.session_state['user_info']['libraries']:
                    st.error('Library already exists')
                else: # create new empty library in database
                    user_info = st.session_state['user_info']
                    user_info['libraries'][new_library_name] = []
                    save_user_info(st.session_state['username'], user_info)
                    st.session_state['user_info'] = user_info
                    create_new_empty_library(st.session_state['username'], new_library_name)
                    st.success(f'Created new library: {new_library_name}')
                    
            st.divider()
            
        with upload_pdf:
            libraries = st.session_state['user_info']['libraries'].keys()
            library = st.selectbox('Which library?', libraries)
            if library:
                uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
                if uploaded_file:
                    if st.button("Upload"):
                        if does_file_exists_in_gcs(f'users/{st.session_state["username"]}/libraries/{library}/{uploaded_file.name}'):
                            st.error(f'File already exists in library: {library}')
                        else:
                            save_uploaded_file_to_gcs(uploaded_file, f'users/{st.session_state["username"]}/libraries/{library}/{uploaded_file.name}')
                            st.success(f'Uploaded {uploaded_file.name} to {library}')
                            pdfloader = PDFLoader()
                            extracted_text = pdfloader.scrape(uploaded_file)
                            print(extracted_text)
                            st.write(extracted_text)
            
            
            '''
                Instead of knowledge graph:
                    - Vector database
                    
                    we want seperate vector databases cuz
                    querying a vector database is O(N) with respect to size of database
                    
                    Instead of utiliing reasoning by navigating the graph, 
                    generate a synthetic query to do top k on vector database
                    
                    The embedding models contain reasoning
                    Generating a synthetic prompt is the navigation
                    
                    
                    much simpler to code
                    
                    
                    
                    experiment
            '''