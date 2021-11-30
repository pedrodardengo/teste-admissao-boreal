import aioresponses
import pytest

BREWERIES_DATA = [
    {
        "id": "12-west-brewing-company-gilbert",
        "name": "12 West Brewing Company",
        "brewery_type": "micro",
        "street": "3000 E Ray Rd Bldg 6",
        "address_2": None,
        "address_3": None,
        "city": "Gilbert",
        "state": "Arizona",
        "county_province": None,
        "postal_code": "85296-7832",
        "country": "United States",
        "longitude": None,
        "latitude": None,
        "phone": "6023395014",
        "website_url": "http://www.12westbrewing.com",
        "updated_at": "2021-10-23T02:24:55.243Z",
        "created_at": "2021-10-23T02:24:55.243Z"
    },
    {
        "id": "12-west-brewing-company-production-facility-mesa",
        "name": "12 West Brewing Company - Production Facility",
        "brewery_type": "micro",
        "street": None,
        "address_2": None,
        "address_3": None,
        "city": "Mesa",
        "state": "Arizona",
        "county_province": None,
        "postal_code": "85207",
        "country": "United States",
        "longitude": "-111.5860662",
        "latitude": "33.436188",
        "phone": None,
        "website_url": None,
        "updated_at": "2021-10-23T02:24:55.243Z",
        "created_at": "2021-10-23T02:24:55.243Z"
    }
]


@pytest.fixture()
def mock_aio_responses():
    with aioresponses.aioresponses() as mock:
        # Mocking: GET https://api.openbrewerydb.org/breweries/ response --------------------------
        mock.get(
            url="https://api.openbrewerydb.org/breweries/",
            status=200,
            payload=BREWERIES_DATA,
        )
        yield mock
