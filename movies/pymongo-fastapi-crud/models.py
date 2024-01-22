import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
import datetime


PyObjectId = Annotated[str, BeforeValidator(str)]

class Movie(BaseModel):
    
    id: PyObjectId = Field(alias="_id", default=None)
    title: str = Field(...)
    plot: Optional[str] = Field(None, alias="plot")
    genres : List[str] = Field(...)
    runtime: Optional[int] = Field(...)
    cast: List[str] = Field(...)
    poster: Optional[str] = Field(None, alias="poster")
    fullplot: Optional[str] = Field(None, alias="fullplot")
    languages: List[str] = Field(None, alias="languages")
    # released: datetime = Field(None, alias="released")
    directors: List[str] = Field(None, alias="directors")
    rated: Optional[str] = Field(None, alias="rated")
    awards: Optional[dict] = Field(None, alias="awards")
    # lastupdated: datetime = Field(None, alias="lastupdated")
    year: Optional[int] = Field(None, alias="year")
    imdb: Optional[dict] = Field(None, alias="imdb")
    countries: List[str] = Field(None, alias="countries")
    type: Optional[str] = Field(None, alias="type")
    tomatoes: Optional[dict] = Field(None, alias="tomatoes")
    num_mflix_comments: Optional[int] = Field(None, alias="num_mflix_comments")

    @validator("plot", pre=True)
    def validate_plot(cls, plot: Optional[str]):
        if plot is None:
            return "No plot information available."
        return plot
    
    @validator("poster", pre=True)
    def validate_poster(cls, poster: Optional[str]):
        if poster is None:
            return "No poster associated."
        return poster
    
    @validator("fullplot", pre=True)
    def validate_fullplot(cls, fullplot: Optional[str]):
        if fullplot is None:
            return "No fullplot associated."
        return fullplot
    
    @validator("languages", pre=True)
    def validate_fullplot(cls, languages: List[str]):
        if languages is None:
            return "No languages associated."
        return languages
    
    # @validator("released", pre=True)
    # def validate_released_time(cls, released: datetime):
    #     if released is None:
    #         return "No release date specified."
    #     return released

    @validator("directors", pre=True)
    def validate_directors(cls, directors: List[str]):
        if not directors:
            return "No directors specified."
        return directors

    @validator("rated", pre=True)
    def validate_rated(cls, rated: Optional[str]):
        if rated is None:
            return "No rating specified."
        return rated

    @validator("awards", pre=True)
    def validate_awards(cls, awards: Optional[dict]):
        if awards is None:
            return "No awards specified."
        return awards

    # @validator("lastupdated", pre=True)
    # def validate_lastupdated(cls, lastupdated: datetime):
    #     if lastupdated is None:
    #         return "No last updated information."
    #     return lastupdated

    @validator("year", pre=True)
    def validate_year(cls, year: Optional[int]):
        if year is None:
            return "No year specified."
        return year

    @validator("imdb", pre=True)
    def validate_imdb(cls, imdb: Optional[dict]):
        if imdb is None:
            return "No IMDb information specified."
        return imdb

    @validator("countries", pre=True)
    def validate_countries(cls, countries: List[str]):
        if not countries:
            return "No countries specified."
        return countries

    @validator("type", pre=True)
    def validate_type(cls, movie_type: Optional[str]):
        if movie_type is None:
            return "No type specified."
        return movie_type

    @validator("tomatoes", pre=True)
    def validate_tomatoes(cls, tomatoes: Optional[dict]):
        if tomatoes is None:
            return "No Tomatoes information specified."
        return tomatoes

    @validator("num_mflix_comments", pre=True)
    def validate_num_mflix_comments(cls, num_mflix_comments: Optional[int]):
        if num_mflix_comments is None:
            return "No comments specified."
        return num_mflix_comments

    class Config:
        allow_population_by_field_name = True
        

class MovieUpdate(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    title: str = Field(...)
    plot: Optional[str] = Field(None, alias="plot")
    genres : List[str] = Field(...)
    runtime: Optional[int] = Field(...)
    cast: List[str] = Field(...)
    poster: Optional[str] = Field(None, alias="poster")
    fullplot: Optional[str] = Field(None, alias="fullplot")
    languages: List[str] = Field(None, alias="languages")
    # released: datetime = Field(None, alias="released")
    directors: List[str] = Field(None, alias="directors")
    rated: Optional[str] = Field(None, alias="rated")
    awards: Optional[dict] = Field(None, alias="awards")
    # lastupdated: datetime = Field(None, alias="lastupdated")
    year: Optional[int] = Field(None, alias="year")
    imdb: Optional[dict] = Field(None, alias="imdb")
    countries: List[str] = Field(None, alias="countries")
    type: Optional[str] = Field(None, alias="type")
    tomatoes: Optional[dict] = Field(None, alias="tomatoes")
    num_mflix_comments: Optional[int] = Field(None, alias="num_mflix_comments")

    class Config:
        allow_population_by_field_name = True
