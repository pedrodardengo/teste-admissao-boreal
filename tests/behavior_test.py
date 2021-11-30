USER_PAYLOAD = {
    'username': 'test@test.com',
    'password': '1!aAaaaa'
}

ORDER_PAYLOAD = {
    'user': 'AUser',
    'order': 12.13,
    'previous_order': False
}


def sign_test_user_and_get_auth_headers(client) -> dict:
    client.post('/auth/signup', json=USER_PAYLOAD)
    token = client.post('/auth/token', data=USER_PAYLOAD).json().get('access_token')
    return {"Authorization": f"Bearer {token}"}


def test_should_return_unauthorized_when_request_breweries_without_token(client):
    response = client.get('/breweries').json()
    assert response == {'detail': 'Not authenticated'}
    response = client.post('/breweries', json=ORDER_PAYLOAD).json()
    assert response == {'detail': 'Not authenticated'}


def test_should_return_same_order_when_post_breweries(client):
    headers = sign_test_user_and_get_auth_headers(client)
    order = client.post("/breweries", headers=headers, json=ORDER_PAYLOAD).json()
    assert order == ORDER_PAYLOAD


def test_should_return_breweries_list_when_get_breweries(client, mock_aio_responses):
    headers = sign_test_user_and_get_auth_headers(client)
    breweries = set(client.get("/breweries", headers=headers).json()['breweries'])
    assert breweries == {
        '12 West Brewing Company',
        '12 West Brewing Company - Production Facility'
    }
