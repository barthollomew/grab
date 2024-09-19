import os
import click
import requests
from html_cookie_video_scraper import process_video_links as html_process
from selenium_network_video_extractor import process_video_links as selenium_process


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


@click.command()
@click.option(
    '-f', '--file', 
    default="video_links.txt", 
    show_default=True,
    help="Path to the video links file."
)
@click.option(
    '-d', '--driver', 
    default="/usr/local/bin/chromedriver", 
    show_default=True,
    help="Path to the ChromeDriver."
)
@click.option(
    '-c', '--cookies', 
    default="cookies.json", 
    show_default=True,
    help="Path to the cookies JSON file."
)
def main(file, driver, cookies):
    """
    Main function to process video links. It first attempts to use the HTML scraper,
    and if unsuccessful, falls back to using Selenium.

    :param file: Path to the video links file.
    :param driver: Path to the ChromeDriver.
    :param cookies: Path to the cookies JSON file.
    """
    if not check_required_files(file, cookies):
        return

    if not validate_file_format(file):
        return

    session = requests.Session()
    cookies_data = html_process.load_cookies(cookies)
    session.cookies.update(cookies_data)

    with open("cookies.txt", "w") as f:
        for name, value in cookies_data.items():
            f.write(f"{name}\tTRUE\t/\tFALSE\t0\t{name}\t{value}\n")

    if not html_process(file, session, cookies_data):
        print("HTML scraper failed, trying Selenium...")
        selenium_process(file, driver)


if __name__ == "__main__":
    main()
