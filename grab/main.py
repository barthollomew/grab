import os
import click
import requests
from grab.utils.file_check import check_required_files, validate_file_format
from grab.utils.scraper import load_cookies, process_video_links as html_process
from grab.utils.selenium_extractor import process_video_links as selenium_process


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
    cookies_data = load_cookies(cookies)
    session.cookies.update(cookies_data)

    with open("cookies.txt", "w") as f:
        for name, value in cookies_data.items():
            f.write(f"{name}\tTRUE\t/\tFALSE\t0\t{name}\t{value}\n")

    with open(file, "r") as video_links_file:
        lines = video_links_file.readlines()

    for i in range(0, len(lines), 2):
        video_title = lines[i].strip()
        video_url = lines[i + 1].strip()

        if video_title and video_url:
            if not html_process(video_title, video_url, session, cookies_data):
                print(f"HTML scraper failed for {video_title}, trying Selenium...")
                selenium_process(video_title, video_url, driver)


if __name__ == "__main__":
    main()
