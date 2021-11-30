import aiohttp
from fastapi import APIRouter, Depends

from src.auth.auth_router import get_user_from_token
from src.breweries.brewerie_models import BreweriesList
from src.breweries.order_model import Order

router = APIRouter(
    prefix="/breweries",
    dependencies=[
        Depends(get_user_from_token)
    ]
)


@router.post("")
async def post_order(order: Order) -> Order:
    """
    Implements the second assignment of the test.
    :param order: a Order model
    :return: a Order Model
    """
    return order


@router.get("")
async def get_all_breweries() -> BreweriesList:
    """
    Implements the third assignment of test.
    :return: A list of breweries names
    """
    url = "https://api.openbrewerydb.org/breweries/"
    async with aiohttp.request("GET", url=url) as response:
        response_data = await response.json()
    all_breweries = list({b_data["name"] for b_data in response_data})
    return BreweriesList(breweries=all_breweries)
