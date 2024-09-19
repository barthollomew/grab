import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import subprocess


def extract_video_url_selenium_logs(embed_url, driver_path):
    """
    Extracts the video URL from the browser's performance logs using Selenium.

    :param embed_url: URL of the page containing the video embed.
    :param driver_path: Path to the ChromeDriver.
    :return: Video URL or None if not found.
    """
    options = Options()
    options.add_argument('--enable-logging')
    options.add_argument('--v=1')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(embed_url)
    time.sleep(2)

    logs = driver.get_log('performance')
    video_url = None
    for log in logs:
        message = log['message']
        if '.mp4' in message and '206' in message:
            video_url = message.split('"url":"')[1].split('"')[0]
            break

    driver.quit()
    return video_url


def download_video(video_url, video_name):
    """
    Downloads the video using yt-dlp.

    :param video_url: Direct URL to the video.
    :param video_name: Name to save the video as.
    """
    if not os.path.exists('./downloads'):
        os.makedirs('./downloads')
    download_path = os.path.join('./downloads', f"{video_name}.mp4")
    command = ['yt-dlp', video_url, '-o', download_path]
    subprocess.run(command, check=True)


def process_video_links(video_title, video_url, driver_path):
    """
    Processes video links from a file and attempts to download them using Selenium.

    :param video_title: Title of the video.
    :param video_url: URL of the page containing the video.
    :param driver_path: Path to the ChromeDriver.
    :return: True if a video is successfully downloaded, False otherwise.
    """
    video_url = extract_video_url_selenium_logs(video_url, driver_path)
    if video_url:
        download_video(video_url, video_title)
        return True
    return False
