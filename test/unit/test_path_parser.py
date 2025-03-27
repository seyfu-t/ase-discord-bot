import pytest

from pathlib import Path
import ase_discord_bot.util.path_parser as pp


def test_read_file_bytes(tmp_path: Path):
    # Create a temporary file with known content.
    content = b"Hello, World!"
    file = tmp_path / "test.txt"
    file.write_bytes(content)

    result = pp.read_file_bytes(str(file))
    assert result == content


@pytest.mark.asyncio
async def test_read_url_bytes(monkeypatch):
    # Create dummy response and session classes.
    class DummyResponse:
        async def read(self):
            return b"Response data"

        def raise_for_status(self):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummySession:
        def get(self, url):
            # Check that the URL is as expected.
            assert url == "http://example.com"
            return DummyResponse()

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    # Monkey patch the aiohttp.ClientSession to use our dummy session.
    monkeypatch.setattr("aiohttp.ClientSession", lambda: DummySession())

    result = await pp.read_url_bytes("http://example.com")
    assert result == b"Response data"


# Test get_bytes_from_uri for a file URI (with "file://" prefix).
@pytest.mark.asyncio
async def test_get_bytes_from_uri_file(tmp_path: Path):
    content = b"File content test"
    file = tmp_path / "test_file.txt"
    file.write_bytes(content)

    uri = "file://" + str(file)
    result = await pp.get_bytes_from_uri(uri)
    assert result == content


# Test get_bytes_from_uri for an HTTP URI by patching read_url_bytes.
@pytest.mark.asyncio
async def test_get_bytes_from_uri_http(monkeypatch):
    async def dummy_read_url_bytes(url: str) -> bytes:
        return b"HTTP content"
    monkeypatch.setattr(pp, "read_url_bytes", dummy_read_url_bytes)

    result = await pp.get_bytes_from_uri("http://dummy")
    assert result == b"HTTP content"


# Test get_bytes_from_uri for a local file path (without "file://" prefix).
@pytest.mark.asyncio
async def test_get_bytes_from_uri_local(tmp_path: Path):
    content = b"Local file content"
    file = tmp_path / "local.txt"
    file.write_bytes(content)

    result = await pp.get_bytes_from_uri(str(file))
    assert result == content
