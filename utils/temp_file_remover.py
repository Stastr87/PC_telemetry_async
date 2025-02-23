import os
from env.default_env import RESPONSE_TEMP_DIR

def del_temp_files():
    files_to_remove_list = os.listdir(RESPONSE_TEMP_DIR)
    for file in files_to_remove_list:
        try:
            os.unlink(os.path.join(RESPONSE_TEMP_DIR, file))
            print(f'temp file {file} removed.')
        except Exception as err:
                print(err)

