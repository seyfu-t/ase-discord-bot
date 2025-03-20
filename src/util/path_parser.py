import aiohttp
import logging


logger = logging.getLogger("Util")


def read_file_bytes(uri: str) -> bytes:
    with open(uri, "rb") as f:
        return f.read()


async def read_url_bytes(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        logger.info(f"Grabbing resource from {url}")
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()


async def get_bytes_from_uri(uri: str) -> bytes:
    if uri.startswith("http://") or uri.startswith("https://"):
        return await read_url_bytes(uri)

    elif uri.startswith("file://"):
        local_path = uri[len("file://"):]
    else:
        local_path = uri

    return read_file_bytes(local_path)
