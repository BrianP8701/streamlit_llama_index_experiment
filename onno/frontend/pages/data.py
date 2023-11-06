import streamlit as st
from onno.shared.utils.database_utils import retrieve_user_info, save_user_info
from onno.frontend.helpers.user_utils import initialize_user_info, create_new_empty_library

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
            if st.text_input('Select Library'):
                pass
            st.write("")
            
            
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