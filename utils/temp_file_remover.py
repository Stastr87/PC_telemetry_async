"""Clean trash"""

import os

from env.default_env import RESPONSE_TEMP_DIR


def del_temp_files():
    """Clean files saved as temp files as response data"""
    removed_files = []
    remove_file_error = []
    try:
        files_to_remove_list = os.listdir(RESPONSE_TEMP_DIR)
    except OSError as err:
        return [], remove_file_error.append(err)

    for file in files_to_remove_list:
        try:
            os.unlink(os.path.join(RESPONSE_TEMP_DIR, file))
            removed_files.append(file)
        except OSError as err:
            remove_file_error.append(f"{file} {err}")

    return removed_files, remove_file_error
