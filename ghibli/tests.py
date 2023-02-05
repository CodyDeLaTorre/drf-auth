from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ghibli


class GhibliTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_ghibli = Ghibli.objects.create(
            name="rake",
            creator=testuser1,
            about="Better for collecting leaves than a shovel.",
        )
        test_ghibli.save()

    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_ghibli_model(self):
        ghibli = Ghibli.objects.get(id=1)
        actual_creator = str(ghibli.creator)
        actual_name = str(ghibli.name)
        actual_about = str(ghibli.about)
        self.assertEqual(actual_creator, "testuser1")
        self.assertEqual(actual_name, "rake")
        self.assertEqual(
            actual_about, "Better for collecting leaves than a shovel."
        )

    def test_get_ghibli_list(self):
        url = reverse("ghibli_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ghiblis = response.data
        self.assertEqual(len(ghiblis), 1)
        self.assertEqual(ghiblis[0]["name"], "rake")

    def test_get_ghibli_by_id(self):
        url = reverse("ghibli_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ghibli = response.data
        self.assertEqual(ghibli["name"], "rake")

    def test_create_ghibli(self):
        url = reverse("ghibli_list")
        data = {"creator": 1, "name": "spoon", "about": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ghiblis = Ghibli.objects.all()
        self.assertEqual(len(ghiblis), 2)
        self.assertEqual(Ghibli.objects.get(id=2).name, "spoon")

    def test_update_ghibli(self):
        url = reverse("ghibli_detail", args=(1,))
        data = {
            "creator": 1,
            "name": "rake",
            "about": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ghibli = Ghibli.objects.get(id=1)
        self.assertEqual(ghibli.name, data["name"])
        self.assertEqual(ghibli.creator.id, data["creator"])
        self.assertEqual(ghibli.about, data["about"])

    def test_delete_ghibli(self):
        url = reverse("ghibli_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        ghiblis = Ghibli.objects.all()
        self.assertEqual(len(ghiblis), 0)

    # added to template
    def test_authentication_required(self):
        self.client.logout()
        url = reverse("ghibli_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
