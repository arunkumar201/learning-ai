from pydantic import BaseModel


class Venue(BaseModel):
    """
    Represents a venue data structure/shape
    """

    name: str
    location: str
    price: str
    capacity: str
    rating: float
    reviews: int
    description: str
