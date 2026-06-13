import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from bot.services.marzban import MarzbanAPI

class TestMarzbanAPI(unittest.IsolatedAsyncioTestCase):
    @patch("httpx.AsyncClient.post")
    async def test_get_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_token"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        api = MarzbanAPI()
        token = await api._get_token()
        self.assertEqual(token, "test_token")

    @patch("httpx.AsyncClient.get")
    async def test_get_user(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"username": "test_user"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        api = MarzbanAPI()
        api.token = "test_token"
        user = await api.get_user("test_user")
        self.assertEqual(user["username"], "test_user")

if __name__ == "__main__":
    unittest.main()
