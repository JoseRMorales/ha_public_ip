"""Public IP Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class PublicIPClientError(Exception):
    """Exception to indicate a general API error."""


class PublicIPClientCommunicationError(
    PublicIPClientError,
):
    """Exception to indicate a communication error."""


class PublicIPClient:
    """Sample API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(method="get", url="https://ifconfig.me/ip")

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                return await response.text()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise PublicIPClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise PublicIPClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:
            msg = f"Something really wrong happened! - {exception}"
            raise PublicIPClientError(
                msg,
            ) from exception
