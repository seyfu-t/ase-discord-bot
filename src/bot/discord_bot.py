import logging

logger = logging.getLogger("Dc-Bot")


def run_bot(token: str, guild_id: int):
    import discord

    bot = discord.Bot()

    @bot.event
    async def on_ready():
        logger.info(f"Bot logged in as {bot.user}")

    @bot.slash_command(guild_ids=[guild_id])
    async def hello(context):
        await context.respond("Hello!")

    bot.run(token)
