from unittest import TestCase
from unittest.mock import patch
import json
from utils.constants import YOUTUBE

from utils.request import check_youtube_user

class UtilsTests(TestCase):
    
    def setUp(self):
        self.channel_info = {
            "items": [
                {
                    "snippet": {
                        "title": "live test title",
                    },
                    "channelTitle":  "channel test name",
                }
            ],
        }
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.user_name = self.channel_info["items"][0]["channelTitle"]
        self.platform = YOUTUBE
            
    @patch("requests.get")
    def test_check_youtube_user(self, mock_requests_get):
        """
            Test for get check youtube user mocking request youtube api
        """
        mock_requests_get.return_value = json.dumps(self.channel_info)
        data = check_youtube_user("channel test name", "test_id", "test_key")
        
        self.assertEqual(self.title, data["title"])
        self.assertEqual(self.platform, data["platform"])
        self.assertEqual(self.user_name, data["user_name"])
