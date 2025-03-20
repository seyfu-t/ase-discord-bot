import logging
from config import Config
from util.path_parser import get_bytes_from_uri

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
    async def hello(context):
        await context.respond("Hello!")

    bot.run(cfg.DISCORD_TOKEN)
