import os
import pytest
from django.contrib.auth.models import User

from core.models import Product


@pytest.fixture
def user_admin_create():
    admin = User.objects.create(username="admin", is_staff=True, is_active=True)
    admin.set_password("asdf1234")
    admin.save()
    return admin


@pytest.fixture
def product_create_multiple():
    p1, _ = Product.objects.get_or_create(name="Notebook HP", price=220000, stock=7)
    p2, _ = Product.objects.get_or_create(name="Notebook Lenovo", price=180000, stock=3)
    p3, _ = Product.objects.get_or_create(name="Notebook Bangho", price=120000, stock=15)
    return p1, p2, p3


@pytest.fixture
def product_create():
    return Product.objects.create(name="Notebook HP", price=220000, stock=7)