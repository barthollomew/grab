import json
import os
import requests
import yt_dlp
from bs4 import BeautifulSoup

def load_cookies(cookie_file):
    """
    Loads cookies from a JSON file and returns them as a dictionary.
    
    :param cookie_file: Path to the cookie JSON file.
    :return: Dictionary of cookie names and values.
    """
    with open(cookie_file, "r") as file:
        cookie_data = json.load(file)
    cookies = {cookie["name"]: cookie["value"] for cookie in cookie_data["cookies"]}
    return cookies


def get_final_redirect_url(initial_url, session):
    """
    Follows redirects to obtain the final URL from the initial request.
    
    :param initial_url: URL to follow redirects from.
    :param session: Requests session object.
    :return: Final URL after redirects or None if an error occurs.
    """
    try:
        response = session.get(initial_url, allow_redirects=True)
        response.raise_for_status()
        return response.url
    except Exception as e:
        print(f"Error following redirects: {e}")
        return None


def extract_redirect_url_from_script(soup, session):
    """
    Extracts the media source URL from script tags in the page.

    :param soup: BeautifulSoup object of the HTML page.
    :param session: Requests session object.
    :return: Final video URL or None if not found.
    """
    try:
        for script in soup.find_all("script"):
            if "media_sources" in script.text:
                media_sources = script.text
                for part in media_sources.split("{"):
                    if '"src":' in part and '"bitrate":' in part:
                        src_url = part.split('"src":"')[1].split('"')[0].replace("\\", "")
                        return get_final_redirect_url(src_url, session)
        return None
    except Exception as e:
        print(f"Error extracting redirect URL: {e}")
        return None


def get_video_url(video_title, video_url, session):
    """
    Retrieves the final video URL from the page.

    :param video_title: Title of the video.
    :param video_url: URL of the page containing the video.
    :param session: Requests session object.
    :return: Final video URL or None if an error occurs.
    """
    try:
        response = session.get(video_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        final_url = extract_redirect_url_from_script(soup, session)

        if not final_url:
            for iframe in soup.find_all('iframe'):
                if 'media_attachments' in iframe.get('src', ''):
                    return get_final_redirect_url(iframe['src'], session)
        return final_url
    except Exception as e:
        print(f"An error occurred while processing {video_title}: {e}")
        return None


def download_video(url, video_title, cookies):
    """
    Downloads the video using yt-dlp.

    :param url: Direct URL to the video.
    :param video_title: Title of the video.
    :param cookies: Dictionary of cookies.
    """
    try:
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)
        ydl_opts = {
            "outtmpl": os.path.join(download_dir, f"{video_title}.mp4"),
            "format": "best",
            "cookies": "cookies.txt",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Failed to download {video_title}: {e}")


def process_video_links(video_title, video_url, session, cookies):
    """
    Processes video links from a file and attempts to download them.

    :param video_title: Title of the video.
    :param video_url: URL of the page containing the video.
    :param session: Requests session object.
    :param cookies: Dictionary of cookies.
    :return: True if a video is successfully downloaded, False otherwise.
    """
    final_video_url = get_video_url(video_title.replace(" ", "_"), video_url, session)
    if final_video_url:
        download_video(final_video_url, video_title.replace(" ", "_"), cookies)
        return True
    return False
