"""Clean trash"""

import os

from env.default_env import RESPONSE_TEMP_DIR


def del_temp_files():
    """Clean files saved as temp files as response data"""
    try:
        files_to_remove_list = os.listdir(RESPONSE_TEMP_DIR)
    except OSError as err:
        files_to_remove_list = []
        print(err)

    for file in files_to_remove_list:
        try:
            os.unlink(os.path.join(RESPONSE_TEMP_DIR, file))
            print(f"temp file {file} removed.")
        except OSError as err:
            print(err)
