from onno.frontend.utils.database_utils import save_user_info, create_folder

def initialize_user_info(username: str, hashed_password: str, email: str):
    user_info = {
        'username': username,
        'password': hashed_password,
        'email': email,
        'libraries': {}
    }
    save_user_info(username, user_info)
    create_folder(f'users/{username}/libraries/')
    return user_info

def create_new_empty_library(username: str, library_name: str):
    create_folder(f'users/{username}/libraries/{library_name}/raw/')
    create_folder(f'users/{username}/libraries/{library_name}/text/')
    