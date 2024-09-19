import requests
from unittest.mock import patch, mock_open
from grab.main import main

@patch("grab.main.html_process")
@patch("grab.main.selenium_process")
@patch("grab.main.load_cookies", return_value={"cookie1": "value1"})
@patch("builtins.open", new_callable=mock_open, read_data="Title 1\nhttps://example.com/video1\n")
def test_main(mock_open, mock_load_cookies, mock_selenium_process, mock_html_process):
    mock_html_process.return_value = False  # HTML process fails
    mock_selenium_process.return_value = True  # Selenium process succeeds

    # Simulate the CLI command call
    with patch("sys.argv", ["main.py", "--file", "video_links.txt", "--driver", "/path/to/chromedriver", "--cookies", "cookies.json"]):
        main()

    mock_html_process.assert_called_once()
    mock_selenium_process.assert_called_once()
