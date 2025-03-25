import logging
from typing import Optional
from discord import ApplicationContext, option
from ase_discord_bot.config import Config
from ase_discord_bot.util.path_parser import get_bytes_from_uri

logger = logging.getLogger("Dc-Bot")


def run_bot(cfg: Config):
    import discord

    bot = discord.Bot()

    @bot.event
    async def on_ready():
        avatar_bytes = await get_bytes_from_uri(cfg.DISCORD_AVATAR)
        banner_bytes = await get_bytes_from_uri(cfg.DISCORD_BANNER)

        if bot.user is None:
            logger.error("Logging in has failed.")
            return

        if cfg.DISCORD_USERNAME != bot.user.name:
            await bot.user.edit(username=cfg.DISCORD_USERNAME)

        await bot.user.edit(avatar=avatar_bytes, banner=banner_bytes)

        logger.info(f"Bot logged in as {bot.user}")

    @bot.slash_command(guild_ids=[cfg.DISCORD_GUILD_ID])
    @option("genre",
            type=int,
            description="Choose a movie genre")
    @option("year",
            type=int,
            description="Choose a release year",
            min_value=1990,
            max_value=2025,
            required=False)
    @option("max_year",
            type=int,
            description="Choose a maximum release year",
            min_value=1990,
            max_value=2025,
            required=False)
    @option("min_year",
            type=int,
            description="Choose a minumum release year",
            min_value=1990,
            max_value=2025,
            required=False)
    @option("original_language",
            type=str,
            description="Choose the original movie language",
            required=False)
    async def recommend_movie(
        context: ApplicationContext,
        genre: int,
        year: Optional[int],
        min_year: Optional[int],
        max_year: Optional[int],
        original_language: Optional[str],
    ):
        await context.respond(f"{genre}, {year}, {min_year}, {max_year}, {original_language}")

    bot.run(cfg.DISCORD_TOKEN)
