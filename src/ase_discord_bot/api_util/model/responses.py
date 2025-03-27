from typing import Optional
from pydantic import BaseModel


class MediaBase(BaseModel):
    """
    Base model for media items.

    Attributes
    ----------
    adult : bool
        Indicates if the media is adult content.
    backdrop_path : Optional[str]
        Path to the backdrop image.
    genre_ids : list[int]
        List of genre identifiers.
    id : int
        Unique identifier for the media.
    original_language : str
        ISO code of the original language.
    overview : str
        Summary of the media content.
    popularity : float
        Popularity score.
    poster_path : Optional[str]
        Path to the poster image.
    vote_average : float
        Average vote score.
    vote_count : int
        Total vote count.
    """
    adult: bool
    backdrop_path: Optional[str]
    genre_ids: list[int]
    id: int
    original_language: str
    overview: str
    popularity: float
    poster_path: Optional[str]
    vote_average: float
    vote_count: int


class Movie(MediaBase):
    """
    Model representing a movie.

    Attributes
    ----------
    original_title : str
        The original title of the movie.
    release_date : str
        Release date in ISO format.
    title : str
        The display title of the movie.
    video : bool
        Indicates if a video is available.
    """
    original_title: str
    release_date: str
    title: str
    video: bool


class TVShow(MediaBase):
    """
    Model representing a TV show.

    Attributes
    ----------
    origin_country : list[str]
        List of countries of origin.
    original_name : str
        The original name of the TV show.
    first_air_date : str
        First air date in ISO format.
    name : str
        The display name of the TV show.
    """
    origin_country: list[str]
    original_name: str
    first_air_date: str
    name: str


class MovieResponse(BaseModel):
    """
    Response model for movie queries.

    Attributes
    ----------
    page : int
        Current page number.
    results : list[Movie]
        List of movie results.
    total_pages : int
        Total number of pages.
    total_results : int
        Total number of results.
    """
    page: int
    results: list[Movie]
    total_pages: int
    total_results: int


class TVShowResponse(BaseModel):
    """
    Response model for TV show queries.

    Attributes
    ----------
    page : int
        Current page number.
    results : list[TVShow]
        List of TV show results.
    total_pages : int
        Total number of pages.
    total_results : int
        Total number of results.
    """
    page: int
    results: list[TVShow]
    total_pages: int
    total_results: int
