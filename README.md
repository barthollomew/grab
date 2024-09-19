## Grab

**Grab** is a fast, easy-to-use command-line tool that allows you to download videos in bulk using URLs from a text file. It supports two methods for extracting video URLs: direct HTML scraping and Selenium browser automation, making it versatile for various websites.

### Features

- **Bulk Video Download**: Download multiple videos by simply listing their titles and URLs in a text file.
- **Dual Extraction Methods**: 
  - **HTML Scraping**: Uses `yt-dlp` and `BeautifulSoup` for fast and lightweight URL extraction.
  - **Selenium Automation**: Handles more complex cases where JavaScript or dynamic content needs to be rendered.
- **Support for Cookies**: Use cookies for authenticated sessions if needed.

### Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/grab.git
    cd grab
    ```

2. **Set Up a Virtual Environment:**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Usage

#### Preparing the Input Files

1. **`video_links.txt`**: Create a text file with alternating lines of video titles and URLs. For example:

    ```plaintext
    Lecture Video Title 1
    https://example.com/video1
    Lecture Video Title 2
    https://example.com/video2
    Lecture Video Title 3
    https://example.com/video3
    ```

2. **`cookies.json`**: If needed, place your cookies in a `cookies.json` file. This is useful for downloading videos from sites that require authentication.

#### Running the Tool

You can run Grab from the command line with default settings:

```bash
python main.py
```

Or customize the paths for your files:

```bash
python main.py --file my_video_links.txt --driver /path/to/chromedriver --cookies my_cookies.json
```

#### Command-line Options

- **`-f, --file`**: Path to the video links file (default: `video_links.txt`).
- **`-d, --driver`**: Path to the ChromeDriver executable (default: `/usr/local/bin/chromedriver`).
- **`-c, --cookies`**: Path to the cookies JSON file (default: `cookies.json`).

#### Example

```bash
python main.py --file my_videos.txt --driver /usr/local/bin/chromedriver --cookies my_cookies.json
```
