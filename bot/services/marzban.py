import httpx
import logging
from bot.config import config
from datetime import datetime

logger = logging.getLogger(__name__)

class MarzbanAPI:
    def __init__(self):
        self.base_url = config.MARZBAN_ADDRESS.rstrip("/")
        self.username = config.MARZBAN_USERNAME
        self.password = config.MARZBAN_PASSWORD
        self.verify_ssl = not config.MARZBAN_SKIP_SSL_VERIFY
        self.token = None

    async def _get_token(self):
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            try:
                url = f"{self.base_url}/api/admin/token"
                logger.debug(f"Attempting to get Marzban token from {url}")
                response = await client.post(
                    url,
                    data={
                        "username": self.username,
                        "password": self.password,
                    },
                )
                response.raise_for_status()
                self.token = response.json()["access_token"]
                return self.token
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error getting Marzban token: {e.response.status_code} - {e.response.text}")
                return None
            except Exception as e:
                logger.error(f"Error getting Marzban token from {self.base_url}: {type(e).__name__}: {e}")
                return None

    async def _get_headers(self):
        if not self.token:
            await self._get_token()
        return {"Authorization": f"Bearer {self.token}"}

    async def create_user(self, username: str, expire: int = 0, data_limit: int = 0):
        """
        expire: timestamp of expiration
        data_limit: in bytes
        """
        headers = await self._get_headers()
        if not headers.get("Authorization") or "None" in headers["Authorization"]:
             logger.error("Cannot create user: No Marzban token")
             return None

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            try:
                user_data = {
                    "username": username,
                    "proxies": {"vless": {}},
                    "inbounds": {"vless": ["VLESS Reality"]},
                    "expire": expire,
                    "data_limit": data_limit,
                }
                response = await client.post(
                    f"{self.base_url}/api/user",
                    json=user_data,
                    headers=headers
                )
                if response.status_code == 401: # Token expired
                    await self._get_token()
                    headers = await self._get_headers()
                    response = await client.post(
                        f"{self.base_url}/api/user",
                        json=user_data,
                        headers=headers
                    )

                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error creating user in Marzban: {type(e).__name__}: {e}")
                return None

    async def get_user(self, username: str):
        headers = await self._get_headers()
        if not headers.get("Authorization") or "None" in headers["Authorization"]:
             return None

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/user/{username}",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                logger.error(f"HTTP error getting user from Marzban: {e.response.status_code}")
                return None
            except Exception as e:
                logger.error(f"Error getting user from Marzban: {type(e).__name__}: {e}")
                return None

    async def update_user(self, username: str, expire: int = 0, data_limit: int = 0):
        headers = await self._get_headers()
        if not headers.get("Authorization") or "None" in headers["Authorization"]:
             return None

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            try:
                user_data = {
                    "expire": expire,
                    "data_limit": data_limit,
                }
                response = await client.put(
                    f"{self.base_url}/api/user/{username}",
                    json=user_data,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error updating user in Marzban: {type(e).__name__}: {e}")
                return None

    async def reset_user_data_usage(self, username: str):
        headers = await self._get_headers()
        if not headers.get("Authorization") or "None" in headers["Authorization"]:
             return None

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/user/{username}/reset",
                    headers=headers
                )
                response.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Error resetting user data in Marzban: {type(e).__name__}: {e}")
                return False

    def get_subscription_link(self, username: str):
        return f"{self.base_url}/sub/{username}"
