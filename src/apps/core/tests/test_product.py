import json
import pytest

from core.models import Product
from .conftest import get_client


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
def test_product_detail(user_admin_create, product_create_multiple):

    product = Product.objects.get(name='Notebook HP')

    assert Product.objects.count() == 3

    URL = f"/api/product/{product.id}/"
    client = get_client()
    response = client.get(URL)

    data = response.json()["data"]["attributes"]
    assert response.status_code == 200
    assert response.json()["data"]["id"] == str(product.id)
    assert data["name"] == product.name
    assert data["price"] == product.price
    assert data["stock"] == product.stock


@pytest.mark.django_db()
def test_product_update(user_admin_create, product_create_multiple):

    product = Product.objects.get(name='Notebook HP')
    URL = f"/api/product/{product.id}/"
    data_new = {"name": "Notebook HP Pavilon"}
    client = get_client()
    response = client.patch(URL, data=data_new)

    product.refresh_from_db()
    assert response.status_code == 200
    assert response.status_text == "OK"
    assert product.name == "Notebook HP Pavilon"


@pytest.mark.django_db()
def test_product_stock_update(user_admin_create, product_create_multiple):

    product = Product.objects.get(name='Notebook HP')

    assert product.stock == 7

    URL = f"/api/product/{product.id}/"
    data_new = {"stock": 20}
    client = get_client()
    response = client.patch(URL, data=data_new)

    product.refresh_from_db()
    assert response.status_code == 200
    assert product.stock == 20


@pytest.mark.django_db()
def test_product_delete(user_admin_create, product_create_multiple):

    product = Product.objects.get(name='Notebook HP')

    assert Product.objects.count() == 3

    URL = f"/api/product/{product.id}/"
    client = get_client()
    response = client.delete(URL)

    assert response.status_code == 204
    assert Product.objects.count() == 2
    assert Product.objects.filter(id=product.id).exists() == False
