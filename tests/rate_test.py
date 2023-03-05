from web import app

def test_rates():
    client = app.test_client()
    test_cases = [
        {
            "name": "empty_date_from",
            "url": "/rates?&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main",
            "code": 400,
        },
        {
            "name": "empty_date_to",
            "url": "/rates?date_from=2016-01-01&origin=CNSGH&destination=north_europe_main",
            "code": 400,
        },
        {
            "name": "empty_origin",
            "url": "/rates?date_from=2016-01-01&date_to=2016-01-10&destination=north_europe_main",
            "code": 400,
        },
        {
            "name": "empty_destination",
            "url": "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH",
            "code": 400,
        },
        {
            "name": "invalid_date_to",
            "url": "/rates?date_from=2016-01-10&date_to=2016&origin=CNSGH&destination=north_europe_main",
            "code": 400,
        },
        {
            "name": "invalid_date_from",
            "url": "/rates?date_from=201601-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main",
            "code": 400,
        },
        {
            "name": "valid",
            "url": "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main",
            "code": 200,
        },

    ]
    for tc in test_cases:      
        response = client.get(tc["url"])    
        assert response.status_code == tc["code"]