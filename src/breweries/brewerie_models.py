from pydantic import BaseModel


class BreweriesList(BaseModel):
    breweries: list[str]
