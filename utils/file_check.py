import os

def validate_file_format(file_path):
    """
    Validates the format of the video_links.txt file.
    Ensures that the file alternates between a title line and a link line.

    :param file_path: Path to the video links file.
    :return: True if the file format is valid, False otherwise.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if len(lines) % 2 != 0:
        print(f"Error: {file_path} should contain an even number of lines (pairs of titles and links).")
        return False

    for i in range(0, len(lines), 2):
        if not lines[i].strip() or not lines[i + 1].strip():
            print(f"Error: Each title should be followed by a non-empty link (line {i + 1} and {i + 2}).")
            return False

    return True


def check_required_files(file_path, cookies_file):
    """
    Checks if the required files exist and are accessible.

    :param file_path: Path to the video links file.
    :param cookies_file: Path to the cookies JSON file.
    :return: True if all files exist, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return False

    if not os.path.exists(cookies_file):
        print(f"Error: The file '{cookies_file}' was not found.")
        return False

    return True
