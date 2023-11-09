import streamlit as st
from onno.frontend.utils.user_utils import create_new_empty_library
from onno.frontend.data_loaders.pdf_loader import PDFLoader
from onno.frontend.data_loaders.web_loader import WebScraper
from onno.frontend.data_loaders.github_loader import RepoScraper

class Data:
    def __init__(self):
        pass
    
    def display(self):
        st.title("Data")
        
        user_libraries = st.session_state['user_info']['libraries']
        library = st.selectbox('Which library?', user_libraries.keys())
        
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
                    st.session_state['DATABASE'].save_user_info(st.session_state['username'], user_info)
                    st.session_state['user_info'] = user_info
                    create_new_empty_library(st.session_state['username'], new_library_name)
                    st.success(f'Created new library: {new_library_name}')
                    st.rerun()
            st.divider()
            
        with upload_pdf:
            st.write("Upload a PDF to a library. For now, we extract the text and only use that in the rest of the application. In the near future we will be able to simply pass the entire pdf with images, graphs and charts into the model.")
            st.divider()
            if library:
                uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
                document_name = st.text_input('Document Name', key='document_name').rstrip('.pdf')
                if len(document_name) > 100:
                    st.error('Please keep the document name under 100 characters')
                document_metadata = st.text_input('Can you provide a concise description of the document? (Optional)')
                if len(document_metadata) > 1000:
                    st.error('Please keep the description under 1000 characters')
                if uploaded_file:
                    if st.button("Upload and load data"):
                        if document_name == '':
                            st.error('Please enter a document name')
                        elif document_name in st.session_state['user_info']['libraries'][library]:
                            st.error(f'Document name already exists in library: {library}')
                        elif st.session_state['DATABASE'].does_file_exists_in_gcs(f'users/{st.session_state["username"]}/libraries/{library}/text/{document_name.replace(" ", "_")}.txt'):
                            st.error(f'File already exists in library: {library}')
                        else:
                            with st.spinner(f'Extracting and uploading {uploaded_file.name}, please wait...'):
                                st.session_state['DATABASE'].save_uploaded_file_to_gcs(uploaded_file, f'users/{st.session_state["username"]}/libraries/{library}/raw/{document_name.replace(" ", "_")}.pdf')
                                pdfloader = PDFLoader(st.secrets['OPENAI_KEY'])
                                extracted_text = pdfloader.pypdf2_scraper(uploaded_file)
                                st.session_state['DATABASE'].save_string_to_gcs(''.join(extracted_text), f'users/{st.session_state["username"]}/libraries/{library}/text/{document_name.replace(" ", "_")}.txt')
                                user_info = st.session_state['user_info']
                                user_info['libraries'][library].append({
                                    'name': document_name,
                                    'type': 'pdf',
                                    'metadata': document_metadata
                                })
                                st.session_state['DATABASE'].save_user_info(st.session_state['username'], user_info)
                                st.success(f'Uploaded {uploaded_file.name} to {library}')
            else:
                st.error('Please select a library first')
            
        with scrape_website:
            st.write('Write the root link of a URL, and APIFY will scrape the website and all of its subpages. This can take a while, so please be patient. This also costs me money, so please be considerate.')
            st.divider()
            if library:
                url = st.text_input('URL', key='website_url')
                website_metadata = st.text_input('Can you provide a concise description of what this website is? (Optional)')
                if len(website_metadata) > 1000:
                    st.error('Please keep the description under 1000 characters')
                if url:
                    if st.button('Load data'):
                        with st.spinner(f'Scraping {url}, please wait...'):
                            webloader = WebScraper(st.secrets['APIFY_KEY'])
                            extracted_text = webloader.scrape(url)
                            st.session_state['DATABASE'].save_string_to_gcs(''.join(extracted_text), f'users/{st.session_state["username"]}/libraries/{library}/text/{url.replace(" ", "_").replace("/", "_")}.json')
                            user_info = st.session_state['user_info']
                            user_info['libraries'][library].append({
                                'name': url,
                                'type': 'website',
                                'metadata': website_metadata
                            })
                            st.session_state['DATABASE'].save_user_info(st.session_state['username'], user_info)
                            st.success(f'Scraped {url} to {library}')
            else:
                st.error('Please select a library first')

        with scrape_github_repo:
            st.write('Write the root link of a GitHub repository, and we will scrape the repository and all of its subpages. This is free and fast, but it only works for public repositories.')
            st.divider()
            if library:
                url = st.text_input('URL', key='github_url')
                document_metadata = st.text_input('Can you provide a concise description of what this repository is? (Optional)')
                if len(document_metadata) > 1000:
                    st.error('Please keep the description under 1000 characters')
                if url:
                    if st.button('Load data'):
                        with st.spinner(f'Scraping {url}, please wait...'):
                            webloader = RepoScraper()
                            extracted_text = webloader.scrape(url)
                            st.session_state['DATABASE'].save_string_to_gcs(''.join(extracted_text), f'users/{st.session_state["username"]}/libraries/{library}/text/{url.replace(" ", "_").replace("/", "_")}.json')
                            user_info = st.session_state['user_info']
                            user_info['libraries'][library].append({
                                'name': url,
                                'type': 'github',
                                'metadata': document_metadata
                            })
                            st.session_state['DATABASE'].save_user_info(st.session_state['username'], user_info)
                            st.success(f'Scraped {url} to {library}')
            else:
                st.error('Please select a library first')
        
            
