Configuration and Environment Variables
=========================================

All available settings are defined in :file:`src/ase_discord_bot/config.py`. Configure the bot by setting environment variables. You can use a ``.env`` file, and optionally a ``.env.dev`` or ``.env.prod`` file (depending on the MODE).

Required Environment Variables
------------------------------

- **TMDB_READ_ACCESS_TOKEN**: TMDB API read access token.
- **DISCORD_TOKEN**: Discord bot token.
- **DISCORD_GUILD_ID**: Discord Guild ID.
- **OPEN_ROUTER_API_KEY**: Open Router API key.

Optional Environment Variables
------------------------------

- **DISCORD_AVATAR**: URL or path to the bot avatar image (defaults to `assets/avatar.jpg`).
- **DISCORD_BANNER**: URL or path to the bot banner image (defaults to `assets/banner.jpg`).
- **DISCORD_USERNAME**: Desired username for the bot (defaults to `DHBW-ASE`).
- **MODE**: Operating mode (`prod` or `dev`, default is `dev`).
- **MAX_API_PAGES_COUNT**: Maximum number of pages for API queries (defaults to `15`).
- **MIN_VOTE_COUNT**: Minimum vote count for filtering recommendations (defaults to `4000`).
