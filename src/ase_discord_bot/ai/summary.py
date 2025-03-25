from openai import OpenAI
from ase_discord_bot.api_util.model.responses import Movie
from ase_discord_bot.config import Config


def summarize(cfg: Config, movie: Movie) -> str:
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
                "text": ("Given the title of a movie and an existing summary,"
                         "rewrite the summary into a new, concise version that"
                         "accurately captures the plot. The output must be a"
                         "standalone summary with no introductory or explanatory"
                         "text. Do not include any conversational phrases or "
                         "metadata — only the revised summary itself.\nTitle:"
                         f"{movie.title}\nSummary: {movie.overview}")
            }]
        }]
    )

    content = completion.choices[0].message.content

    if content is not None:
        return content
    else:
        return movie.overview
