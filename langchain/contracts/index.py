from typing import List

from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age")
    hobbies: List[str] = Field(description="List of the person's hobbies")
    occupation: str = Field(description="The person's current job or occupation")
    email: str = Field(description="The person's email address")
    phone: str = Field(description="The person's phone number")
    address: str = Field(description="The person's address")
    city: str = Field(description="The person's city")
    state: str = Field(description="The person's state")
    zip: str = Field(description="The person's zip code")
    country: str = Field(description="The person's country")


class Product(BaseModel):
    name: str = Field(description="The product's name")
    price: float = Field(description="The product's price")
    description: str = Field(description="The product's description")
    image: str = Field(description="The product's image URL")
    category: str = Field(description="The product's category")
    rating: float = Field(description="The product's rating")
