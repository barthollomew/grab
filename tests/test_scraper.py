import requests
from unittest.mock import Mock, patch
from grab.utils.scraper import load_cookies, get_video_url

def test_load_cookies():
    mock_cookies = {
        "cookies": [
            {"name": "cookie1", "value": "value1"},
            {"name": "cookie2", "value": "value2"}
        ]
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_cookies))):
        cookies = load_cookies("mock_cookies.json")
        assert cookies == {"cookie1": "value1", "cookie2": "value2"}

def test_get_video_url():
    mock_response = Mock()
    mock_response.content = b"<html><body><script>var media_sources = '{\"src\":\"https://example.com/video.mp4\",\"bitrate\":1000}'</script></body></html>"
    
    session = requests.Session()
    with patch.object(session, 'get', return_value=mock_response):
        soup = BeautifulSoup(mock_response.content, "html.parser")
        video_url = get_video_url("Test Video", "https://example.com", session)
        assert video_url == "https://example.com/video.mp4"
