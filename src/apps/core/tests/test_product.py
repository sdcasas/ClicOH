import json

import pytest

from rest_framework.test import APIClient

from core.models import Product


def get_client():
    client = APIClient()
    client.login(username='admin', password='asdf1234')
    return client

@pytest.mark.django_db()
def test_product_create(user_admin_create):

    URL = "/api/product/"
    product_name = "Notebook Asus"

    data = {
        "name": product_name,
        "price": 350000,
        "stock": 5,
    }

    client = get_client()
    response = client.post(URL, data=data)

    p1 = Product.objects.last()

    assert response.status_code == 201
    assert response.status_text == "Created"
    assert response.json().get("data").get("attributes").get("name") == product_name
    assert p1.name == product_name


@pytest.mark.django_db()
def test_product_list(user_admin_create, product_create_multiple):

    URL = "/api/product/"

    client = get_client()

    response = client.get(URL)

    data_json = response.json().get("data")
    assert response.status_code == 200
    assert len(data_json) == 3
    assert data_json[0]["attributes"]["name"] == 'Notebook Bangho'
    assert data_json[1]["attributes"]["name"] == 'Notebook HP'
    assert data_json[2]["attributes"]["name"] == 'Notebook Lenovo'


@pytest.mark.django_db()
def test_product_update(user_admin_create, product_create_multiple):

    product = Product.objects.get(name='Notebook HP')
    URL = f"/api/product/{product.id}/"
    data_new = {
        "data": {
            "type": "Product",
            "id": product.id,
            "attributes": {
                "name": 'Notebook HP Pavilon'
            }
        }
    }
    client = get_client()
    response = client.put(URL, data=json.dumps(data_new))

    product.refresh_from_db()
    assert response.status_code == 301
    assert product.name == "Notebook HP Pavilon"
