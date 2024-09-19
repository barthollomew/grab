from unittest.mock import Mock, patch
from grab.utils.selenium_extractor import extract_video_url_selenium_logs

def test_extract_video_url_selenium_logs():
    mock_driver = Mock()
    mock_driver.get_log.return_value = [{
        "message": '{"message":{"method":"Network.responseReceived","params":{"response":{"url":"https://example.com/video.mp4"}}}}'
    }]

    with patch("selenium.webdriver.Chrome") as MockWebDriver:
        MockWebDriver.return_value = mock_driver
        video_url = extract_video_url_selenium_logs("https://example.com", "/path/to/chromedriver")
        assert video_url == "https://example.com/video.mp4"
