import aiohttp
from fastapi import APIRouter, Depends

from src.auth.auth_router import get_user_from_token
from src.auth.user_model import StoredUser
from src.breweries.brewerie_models import BreweriesList
from src.breweries.order_model import Order

router = APIRouter(prefix="/breweries")


@router.post("/")
async def post_order(
        order: Order, request_user: StoredUser = Depends(get_user_from_token)
):
    """
    Implements the second assignment of the test.
    :param order: a Order model
    :param request_user: Used for authorization
    :return: a Order Model
    """
    return order


@router.get("/")
async def get_all_breweries(request_user: StoredUser = Depends(get_user_from_token)):
    """
    Implements the third assignment of test.
    :param request_user: Used for authorization
    :return:
    """
    url = "https://api.openbrewerydb.org/breweries/"
    async with aiohttp.request("GET", url=url) as response:
        response_data = await response.json()
    all_breweries = list({b_data["name"] for b_data in response_data})
    return BreweriesList(breweries=all_breweries)
