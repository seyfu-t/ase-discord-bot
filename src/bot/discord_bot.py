import logging
from config import Config

logger = logging.getLogger("Dc-Bot")


def run_bot(cfg: Config):
    import discord

    bot = discord.Bot()

    @bot.event
    async def on_ready():
        with open(cfg.DISCORD_AVATAR, "rb") as avatar_file:
            avatar_bytes = avatar_file.read()

        with open(cfg.DISCORD_BANNER, "rb") as banner_file:
            banner_bytes = banner_file.read()

        if (user := bot.user):
            await user.edit(username=cfg.DISCORD_USERNAME, avatar=avatar_bytes, banner=banner_bytes)

        logger.info(f"Bot logged in as {bot.user}")

    @bot.slash_command(guild_ids=[cfg.DISCORD_GUILD_ID])
    async def hello(context):
        await context.respond("Hello!")

    bot.run(cfg.DISCORD_TOKEN)
