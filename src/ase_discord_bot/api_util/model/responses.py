from typing import Optional
from pydantic import BaseModel


class MediaBase(BaseModel):
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
    original_title: str
    release_date: str
    title: str
    video: bool


class TVShow(MediaBase):
    origin_country: list[str]
    original_name: str
    first_air_date: str
    name: str


class MovieResponse(BaseModel):
    page: int
    results: list[Movie]
    total_pages: int
    total_results: int


class TVShowResponse(BaseModel):
    page: int
    results: list[TVShow]
    total_pages: int
    total_results: int
