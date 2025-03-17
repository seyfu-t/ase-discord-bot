import discord


class BotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')


def run_bot(token: str):
    intents = discord.Intents.default()
    intents.message_content = True
    client = BotClient(intents=intents)
    client.run(token)
