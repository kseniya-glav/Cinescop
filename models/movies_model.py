from pydantic import BaseModel, Field
from typing import Optional, Union
from constants.locations import Locations

class BaseMovie(BaseModel):
    name: str
    imageUrl: Optional[str] = Field(default= None, description="Сслыка на изображение")
    price: int = Field(gt = 0, description="Стоимость билета")
    description: str = Field(max_length=500, description="Описание фильма")
    location: Locations = Field(description=f"Локация только из списка {list(Locations)}")
    published: bool = Field(description= "Видимость")
    genreId: int = Field(description= "Идентификатор жанра")
    
    class Config:
        use_enum_values = True 
    
class Movie(BaseMovie):
    id: int = Field(description= "Идентификатор фильма")

class Genre(BaseModel):
    name: str

class MovieSchema(Movie):
    genre: Genre
    createdAt: str
    rating: float

class AllMovies(BaseModel):
    movies: list[MovieSchema]
    count: int
    page: int
    pageSize: int
    pageCount: int
    
class User(BaseModel):
    fullName: str
    
class Review(BaseModel):
    userId: str
    rating: int
    text: str
    hidden: bool
    createdAt: str
    user: User
    
class MovieGetId(MovieSchema):
    reviews: list[Review]

class Reviews(BaseModel):
    data: Union[list[Review], Review, None]