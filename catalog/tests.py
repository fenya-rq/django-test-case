# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Responsible for testing `catalog` module."""
import requests
import pytest
from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APIClient


from .models import Goods, Images, Parameters


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def load_fixture(db):
    """
    Fixture to load a JSON fixture into the database.

    :param db: *pytest fixture*: Ensures that the test
     interacts with the database.
    :return: Callable function that loads a fixture by name
     from the 'catalog/fixtures' directory.
    """
    def _load_fixture(fixture_name):
        """
        Load a specific fixture file into the test database.

        :param fixture_name: str: The name of the fixture file
         (without '.json' extension).
        """
        call_command('loaddata', f'catalog/fixtures/{fixture_name}.json')
    return _load_fixture


@pytest.fixture
def goods_instance():
    """
    Fixture to create a `Goods` instance along with its related
    `Images` and `Parameters`.

    :return: A `Goods` object with associated `Images` and
     `Parameters` objects.
    """
    good = Goods.objects.create(name='test1',
                                info='test info',
                                base_cost='50.00',
                                sort_order='ASC')
    Images.objects.create(good=good,
                          file='image1.jpg',
                          sign='test sign',
                          sort_order='ASC')
    Parameters.objects.create(good=good,
                              name='image1.jpg',
                              value='test sign',
                              cost='100.00',
                              sort_order='ASC')
    yield good
    good.delete()


@pytest.mark.django_db
class TestModelsWriting:
    """
    Test class for writing operations related to `Goods` and
    linked models.
    """

    def test_create_good(self):
        """
        Test the creation of a `Goods` object.

        :assert: Verifies that the created object is
         an instance of the `Goods` model.
        """
        good = Goods.objects.create(name='test1',
                                    info='test info',
                                    base_cost='50.00',
                                    sort_order='ASC')
        assert isinstance(good, Goods)

    def test_create_linked_good(self, goods_instance):
        """
        Test the creation of a `Goods` object with linked `Images` and
        `Parameters`.

        :param goods_instance: Goods: Fixture providing
         a `Goods` instance with linked data.
        :assert: Verifies that the related `Images` and `Parameters`
         are correctly associated with `Goods`.
        """
        good_with_relations = (Goods.objects.prefetch_related('images', 'parameters')
                               .get(pk=goods_instance.id))
        good_image = good_with_relations.images.get(pk=1)
        good_parameter = good_with_relations.parameters.get(pk=1)
        assert isinstance(good_image, Images) and isinstance(good_parameter, Parameters)


@pytest.mark.django_db
class TestModelsReading:
    """
    Test class for reading data from the database using fixtures.
    """

    def test_goods_fixtures_data(self, load_fixture):
        """
        Test the loading and existence of `Goods` objects from a fixture.

        :param load_fixture: *Callable*: Fixture used to load data from
         the JSON fixture.
        :assert: Ensures that `Goods` objects are successfully loaded
         into the database.
        """
        load_fixture('goods')
        objects = Goods.objects.count()
        assert objects > 0

    def test_images_fixtures_data(self, load_fixture):
        """
        Test the loading and existence of `Images` objects from
        a fixture.

        :param load_fixture: *Callable*: Fixture used to load data
         from the JSON fixture.
        :assert: Ensures that `Images` objects are successfully loaded
         into the database.
        """
        load_fixture('goods')
        load_fixture('images')
        objects = Images.objects.count()
        assert objects > 0

    def test_parameters_fixtures_data(self, load_fixture):
        """
        Test the loading and existence of `Parameters` objects
        from a fixture.

        :param load_fixture: *Callable*: Fixture used to load data
         from the JSON fixture.
        :assert: Ensures that `Parameters` objects are successfully
         loaded into the database.
        """
        load_fixture('goods')
        load_fixture('parameters')
        objects = Parameters.objects.count()
        assert objects > 0


@pytest.mark.django_db
class TestViews:

    def test_catalog_list_view(self, api_client, goods_instance):
        """
        Test the catalog list view endpoint.

        This test ensures that the catalog list view correctly returns a
        200 OK response when accessed with a GET request. It checks that
        the API endpoint for listing goods is functioning and returning
        the expected status code.

        :param api_client: The API client fixture to send requests.
        :param goods_instance: A fixture for creating a Goods instance.
        """
        url = reverse('goods-list')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_catalog_good_view(self, api_client, goods_instance):
        """
        Test the catalog detail view endpoint for a specific good.

        This test ensures that the catalog detail view correctly
        returns a 200 OK response when accessed with a GET request
        for a specific good item. It verifies that the detail view
        endpoint for a specific good item is functioning and returning
        the expected status code.

        :param api_client: The API client fixture to send requests.
        :param goods_instance: A fixture for creating a Goods instance.
        """
        url = reverse('goods-detail', kwargs={'pk': goods_instance.pk})
        response = api_client.get(url)
        assert response.status_code == 200
