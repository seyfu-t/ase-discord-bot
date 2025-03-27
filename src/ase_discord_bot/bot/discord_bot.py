import logging

from typing import Optional
from discord import ApplicationContext, AutocompleteContext, OptionChoice, option
from ase_discord_bot.api_util.api_calls import get_recommended_movie
from ase_discord_bot.api_util.model.filters import MovieFilter
from ase_discord_bot.api_util.model.genres import MovieGenre
from ase_discord_bot.api_util.model.languages import Language
from ase_discord_bot.bot.msg_format import format_recommendation
from ase_discord_bot.config_registry import get_config
from ase_discord_bot.util.path_parser import get_bytes_from_uri
from ase_discord_bot.util.type_checks import is_list_of_movies

logger = logging.getLogger("Dc-Bot")


def run_bot():
    import discord
    bot = discord.Bot()
    cfg = get_config()

    @bot.event
    async def on_ready():
        avatar_bytes = await get_bytes_from_uri(cfg.DISCORD_AVATAR)
        banner_bytes = await get_bytes_from_uri(cfg.DISCORD_BANNER)

        if bot.user is None:
            logger.error("Logging in has failed.")
            return

        try:
            if cfg.DISCORD_USERNAME != bot.user.name:
                await bot.user.edit(username=cfg.DISCORD_USERNAME)

            await bot.user.edit(avatar=avatar_bytes, banner=banner_bytes)
        except discord.errors.HTTPException:
            logger.error("Rate limit: couldn't change username/avatar/banner.")

        logger.info(f"Bot logged in as {bot.user}")

    async def autocomplete_language(context: AutocompleteContext):
        """
        Autocompletes language options based on user input.
        Returns a max of 25 results because of api limitations.
        """
        user_input = context.value.lower()

        matches = []

        for lang in Language:
            english = lang.english_name
            # prefer native name but fallback
            local = lang.local_name or english
            code = lang.iso_code

            if user_input in english.lower() or user_input in local.lower():
                matches.append(OptionChoice(name=local, value=code))

        # Discord API limit of 25
        return matches[:cfg.DISCORD_CHOICES_SIZE_LIMIT]

    @bot.slash_command(guild_ids=[cfg.DISCORD_GUILD_ID])
    @option("genre",
            type=int,
            description="🍿 Choose a movie genre",
            choices=MovieGenre.as_choices())
    @option("year",
            type=int,
            description="🗓️ Choose a release year",
            min_value=cfg.ABSOLUTE_MIN_YEAR,
            max_value=cfg.ABSOLUTE_MAX_YEAR,
            required=False)
    @option("max_year",
            type=int,
            description="🗓️ Choose a maximum release year",
            min_value=cfg.ABSOLUTE_MIN_YEAR,
            max_value=cfg.ABSOLUTE_MAX_YEAR,
            required=False)
    @option("min_year",
            type=int,
            description="🗓️ Choose a minumum release year",
            min_value=cfg.ABSOLUTE_MIN_YEAR,
            max_value=cfg.ABSOLUTE_MAX_YEAR,
            required=False)
    @option("original_language",
            type=str,
            description="🌐 Choose the original movie language",
            autocomplete=autocomplete_language,
            required=False)
    async def recommend_movie(
        context: ApplicationContext,
        genre: int,
        year: Optional[int],
        min_year: Optional[int],
        max_year: Optional[int],
        original_language: Optional[str],
    ):
        errors = []

        if year is not None and (min_year is not None or max_year is not None):
            errors.append("⚠️ **Pick either a specific year OR a range, not both.**")

        if min_year is not None and max_year is not None:
            if min_year > max_year:
                errors.append("⚠️ **Minimum year cannot be greater than maximum year.**")
            elif min_year == max_year:
                # Auto-convert to a single year query
                year = min_year
                min_year = max_year = None

        if errors:
            await context.respond("\n".join(errors))
            return

        language = Language.from_fuzzy(original_language)

        movie_filter: MovieFilter = MovieFilter(genre, year, min_year, max_year, language)
        recommendations = get_recommended_movie(movie_filter)

        if len(recommendations) == 0:
            await context.respond("🚫 **No Matches found.**")
            return

        # Check what type of list got returned
        if isinstance(recommendations, list):
            if isinstance(recommendations[0], int):
                logger.error(f"All api requests failed. {recommendations}")
                msg = f"An unexpected error has occured. Status codes: {recommendations}"
                await context.respond(msg)
            elif is_list_of_movies(recommendations):
                await context.defer()
                for msg in format_recommendation(recommendations):
                    await context.followup.send(msg)
            else:
                logger.error("An error occurred. Unexpected list contents.")
                await context.respond("🚫 **A fatal error has occured**")
        else:
            logger.error(f"An error occurred. Unexpected type: {type(recommendations)}")
            await context.respond("🚫 **A fatal error has occured**")

    bot.run(cfg.DISCORD_TOKEN)
