import logging

from openai import OpenAI
from ase_discord_bot.api_util.model.responses import Movie, TVShow
from ase_discord_bot.config_registry import get_config

logger = logging.getLogger("Ai")


def summarize(media: Movie | TVShow) -> str:
    """
    Generate a concise summary for a media item.

    The function attempts to create a new summary using an OpenAI model.
    If the API call fails or returns no content, it falls back to the original overview.

    Parameters
    ----------
    media : Movie | TVShow
        The media item (movie or TV show) to summarize.

    Returns
    -------
    str
        The generated summary or the original media overview.
    """
    cfg = get_config()

    client = OpenAI(
        base_url=cfg.OPEN_ROUTER_BASE_URL.human_repr(),
        api_key=cfg.OPEN_ROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-thinking-exp:free",
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": _get_text(media)
            }]
        }]
    )
    content = None
    try:
        content = completion.choices[0].message.content
    except TypeError:
        logger.error("Ai has failed, probably a rate-limit by the api.")
        content = None

    if content is not None:
        return content
    else:
        return media.overview


def _get_text(media: Movie | TVShow) -> str:
    """
    Build the input text for the summarization API call.

    The text includes the media title and its original overview, along with instructions
    for rewriting the summary.

    Parameters
    ----------
    media : Movie | TVShow
        The media item to be summarized.

    Returns
    -------
    str
        The formatted text prompt.
    """
    if isinstance(media, Movie):
        media_type = "movie"
        title = media.title
    elif isinstance(media, TVShow):
        media_type = "tvshow"
        title = media.name

    return (
        f"Given the title of a {media_type} and an existing summary, rewrite the summary "
        "into a new, concise version that accurately captures the plot. The output should be 2 to "
        "3 sentences long. The output must be a standalone summary with no introductory or "
        "explanatory text. Do not include any conversational phrases or metadata — only the "
        f"revised summary itself.\nTitle: {title}\nSummary: {media.overview}"
    )
