from httpx import AsyncClient, Response


class RestClientConfig:
    """Base config - does nothing by default"""

    def apply(self, client: AsyncClient) -> None:
        pass


class RestClient:
    def __init__(
        self, client: AsyncClient, config: RestClientConfig | None = None
    ) -> None:
        if config:
            config.apply(client)
        self._client = client

    async def _get(self, url: str, *args, **kwargs) -> "Response":
        response = await self._client.get(url, *args, **kwargs)
        return response

    async def _post(self, url: str, *args, **kwargs) -> "Response":
        response = await self._client.post(url, *args, **kwargs)
        return response
