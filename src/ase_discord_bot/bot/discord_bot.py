import logging

from typing import Optional
from discord import Bot, ApplicationContext, AutocompleteContext, OptionChoice, errors, option
from ase_discord_bot.api_util.api_calls import get_recommended_movie, get_recommended_tvshow
from ase_discord_bot.api_util.model.filters import MovieFilter, TVShowFilter
from ase_discord_bot.api_util.model.genres import MovieGenre, TVShowGenre
from ase_discord_bot.api_util.model.languages import Language
from ase_discord_bot.bot.msg_format import format_recommendation, help_command
from ase_discord_bot.config_registry import get_config
from ase_discord_bot.util.path_parser import get_bytes_from_uri
from ase_discord_bot.util.type_checks import is_list_of_movies, is_list_of_tvshows

logger = logging.getLogger("Dc-Bot")


def run_bot():
    """
    Run the Discord bot.

    This function creates a Discord bot, sets up event handlers and slash commands,
    and starts the bot using the configured token.
    """
    bot = Bot()
    cfg = get_config()

    @bot.event
    async def on_ready():
        """
        Event handler for when the bot is ready.

        It updates the bot's avatar, banner, and username based on the configuration.
        """
        avatar_bytes = await get_bytes_from_uri(cfg.DISCORD_AVATAR)
        banner_bytes = await get_bytes_from_uri(cfg.DISCORD_BANNER)

        if bot.user is None:
            logger.error("Logging in has failed.")
            return

        try:
            if cfg.DISCORD_USERNAME != bot.user.name:
                await bot.user.edit(username=cfg.DISCORD_USERNAME)

            await bot.user.edit(avatar=avatar_bytes, banner=banner_bytes)
        except errors.HTTPException:
            logger.error("Rate limit: couldn't change username/avatar/banner.")

        logger.info(f"Bot logged in as {bot.user}")

    async def autocomplete_language(context: AutocompleteContext):
        """
        Autocomplete language options based on user input.

        Parameters
        ----------
        context : AutocompleteContext
            The context containing the user's input for language autocomplete.

        Returns
        -------
        list[OptionChoice]
            A list of language choices, limited to the configured size.
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

    @bot.slash_command(guild_ids=[cfg.DISCORD_GUILD_ID], description="Recommand Movies")
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
        """
        Recommend a movie based on user-specified criteria.

        Validates year inputs, builds a movie filter, retrieves recommendations,
        and sends formatted results back to the user.

        Parameters
        ----------
        context : ApplicationContext
            The context of the slash command.
        genre : int
            The selected movie genre.
        year : Optional[int]
            A specific release year for the movie.
        min_year : Optional[int]
            The minimum release year in a range.
        max_year : Optional[int]
            The maximum release year in a range.
        original_language : Optional[str]
            The original language filter for the movie.
        """
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

    @bot.slash_command(guild_ids=[cfg.DISCORD_GUILD_ID], description="Recommand TV Shows")
    @option("genre",
            type=int,
            description="🍿 Choose a tv show genre",
            choices=TVShowGenre.as_choices())
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
            description="🌐 Choose the original tv show language",
            autocomplete=autocomplete_language,
            required=False)
    async def recommend_tvshow(
        context: ApplicationContext,
        genre: int,
        year: Optional[int],
        min_year: Optional[int],
        max_year: Optional[int],
        original_language: Optional[str],
    ):
        """
        Recommend a TV show based on user-specified criteria.

        Validates year inputs, builds a TV show filter, retrieves recommendations,
        and sends formatted results back to the user.

        Parameters
        ----------
        context : ApplicationContext
            The context of the slash command.
        genre : int
            The selected TV show genre.
        year : Optional[int]
            A specific release year for the TV show.
        min_year : Optional[int]
            The minimum release year in a range.
        max_year : Optional[int]
            The maximum release year in a range.
        original_language : Optional[str]
            The original language filter for the TV show.
        """
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

        tvshow_filter: TVShowFilter = TVShowFilter(genre, year, min_year, max_year, language)
        recommendations = get_recommended_tvshow(tvshow_filter)

        if len(recommendations) == 0:
            await context.respond("🚫 **No Matches found.**")
            return

        # Check what type of list got returned
        if isinstance(recommendations, list):
            if isinstance(recommendations[0], int):
                logger.error(f"All api requests failed. {recommendations}")
                msg = f"An unexpected error has occured. Status codes: {recommendations}"
                await context.respond(msg)
            elif is_list_of_tvshows(recommendations):
                await context.defer()
                for msg in format_recommendation(recommendations):
                    await context.followup.send(msg)
            else:
                logger.error("An error occurred. Unexpected list contents.")
                await context.respond("🚫 **A fatal error has occured**")
        else:
            logger.error(f"An error occurred. Unexpected type: {type(recommendations)}")
            await context.respond("🚫 **A fatal error has occured**")

    @bot.slash_command(guild_ids=[cfg.DISCORD_GUILD_ID], description="List all Commands")
    async def help(context: ApplicationContext):
        """
        Display the help message for available commands.

        Responds with the help text generated by help_command().

        Parameters
        ----------
        context : ApplicationContext
            The context of the slash command.
        """
        await context.respond(help_command())

    bot.run(cfg.DISCORD_TOKEN)
