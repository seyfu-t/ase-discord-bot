import aiohttp
import logging


logger = logging.getLogger("Util")


def read_file_bytes(uri: str) -> bytes:
    """
    Read a local file and return its contents as bytes.

    Parameters
    ----------
    uri : str
        The file path to read from.

    Returns
    -------
    bytes
        The content of the file.
    """
    with open(uri, "rb") as f:
        return f.read()


async def read_url_bytes(url: str) -> bytes:
    """
    Asynchronously fetch a URL and return its contents as bytes.

    Parameters
    ----------
    url : str
        The URL to fetch.

    Returns
    -------
    bytes
        The content retrieved from the URL.
    """
    async with aiohttp.ClientSession() as session:
        logger.info(f"Grabbing resource from {url}")
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()


async def get_bytes_from_uri(uri: str) -> bytes:
    """
    Get bytes from a given URI.

    Depending on the URI scheme, this function either fetches data from a URL
    or reads from a local file.

    Parameters
    ----------
    uri : str
        The URI to retrieve data from. It can be an HTTP/HTTPS URL, a file URI,
        or a local file path.

    Returns
    -------
    bytes
        The bytes read from the resource.
    """
    if uri.startswith("http://") or uri.startswith("https://"):
        return await read_url_bytes(uri)

    elif uri.startswith("file://"):
        local_path = uri[len("file://"):]
    else:
        local_path = uri

    return read_file_bytes(local_path)
