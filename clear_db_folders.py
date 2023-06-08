import os
import shutil


def clear_folder_contents(folder):
    """
    Removes all files and directories in the specified folder.

    :param folder: Path to the folder to clear.
    """
    # Loop over all files in the folder
    for filename in os.listdir(folder):
        # Create absolute file path
        file_path = os.path.join(folder, filename)
        # Remove file or directory
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


# Usage:
clear_folder_contents('./db/data')
clear_folder_contents('./db/log')
clear_folder_contents('./db/secrets')
