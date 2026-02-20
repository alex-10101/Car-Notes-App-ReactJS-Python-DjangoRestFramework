from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import Car
from django.contrib.auth import get_user_model
from .serializers import GetCarSerializer
import json 

User = get_user_model()

# Django will automatically create a TEST database, and then destroy the database after the tests are completed. 
# Run tests with "python3 manage.py test".

class GetAllCarsTest(TestCase):
    """Test module for GET all cars API (filtered + paginated response)."""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username="u1", email="e1@gmail.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="u2", email="e2@gmail.com", password="password"
        )

        # user1 cars
        self.car1 = Car.objects.create(
            brand="Porsche", model="911 GT3 RS", motor="Petrol", user=self.user1
        )

        # user2 cars
        self.car2 = Car.objects.create(
            brand="Audi", model="A4", motor="Diesel", user=self.user2
        )
        self.car3 = Car.objects.create(
            brand="Audi", model="A5", motor="Hybrid", user=self.user2
        )

        self.url = reverse("car_list_create")

    def login(self, user):
        # DRF-friendly auth shortcut
        self.client.force_authenticate(user=user)

    # def logout(self):
    #     self.client.force_authenticate(user=None)

    def assert_paginated_payload(
        self,
        payload: dict,
        expected_qs,
        *,
        expected_page: int,
        expected_pages: int,
        expected_page_size: int,
        expected_len: int,
    ):
        """Helper to validate the paginated response structure + ordering."""
        self.assertIn("count", payload)
        self.assertIn("pages", payload)
        self.assertIn("data", payload)
        self.assertIn("page", payload)
        self.assertIn("page_size", payload)

        self.assertEqual(payload["count"], expected_qs.count())
        self.assertEqual(payload["pages"], expected_pages)
        self.assertEqual(payload["page"], expected_page)
        self.assertEqual(payload["page_size"], expected_page_size)

        self.assertEqual(len(payload["data"]), expected_len)

        # Ensure ordering by -createdAt (ids should match expected_qs order)
        expected_ids = list(expected_qs.values_list("id", flat=True))[:expected_len]
        response_ids = [item["id"] for item in payload["data"]]
        self.assertEqual(response_ids, expected_ids)

    def test_should_not_get_cars_without_auth(self):
        # self.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user1_should_only_get_cars_of_user1_unfiltered(self):
        self.login(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_qs = Car.objects.filter(user=self.user1).order_by("-createdAt")
        self.assert_paginated_payload(
            response.data,
            expected_qs,
            expected_page=1,
            expected_pages=1,
            expected_page_size=9,
            expected_len=expected_qs.count(),
        )

        # Safety: ensure every returned car belongs to user1
        for car in response.data["data"]:
            self.assertEqual(car["user"], self.user1.id)

    def test_user2_should_only_get_cars_of_user2_unfiltered(self):
        self.login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_qs = Car.objects.filter(user=self.user2).order_by("-createdAt")
        self.assert_paginated_payload(
            response.data,
            expected_qs,
            expected_page=1,
            expected_pages=1,
            expected_page_size=9,
            expected_len=expected_qs.count(),
        )

        for car in response.data["data"]:
            self.assertEqual(car["user"], self.user2.id)

    def test_user1_should_not_get_cars_of_user2(self):
        self.login(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user1 has only 1 car in this fixture
        for car in response.data["data"]:
            self.assertEqual(car["user"], self.user1.id)

        # sanity check: user2 really has cars in DB
        self.assertTrue(Car.objects.filter(user=self.user2).exists())

    def test_filter_brand_or_logic_within_brand_group_and_user_restriction(self):
        # user2 asks for brand=Audi-Porsche -> should match Audi cars of user2 only
        self.login(self.user2)

        response = self.client.get(self.url, {"brand": "Audi-Porsche"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_qs = Car.objects.filter(user=self.user2, brand__icontains="Audi").order_by(
            "-createdAt"
        )
        # (In this fixture, user2 has only Audi brand anyway.)
        self.assert_paginated_payload(
            response.data,
            expected_qs,
            expected_page=1,
            expected_pages=1,
            expected_page_size=9,
            expected_len=expected_qs.count(),
        )

        # user1 asks for brand=Audi -> should return empty (restricted to user1)
        # self.logout()
        self.login(self.user1)
        response2 = self.client.get(self.url, {"brand": "Audi"})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["count"], 0)
        self.assertEqual(response2.data["data"], [])

    def test_filter_motor_or_logic_within_motor_group(self):
        self.login(self.user2)

        response = self.client.get(self.url, {"motor": "Diesel-Hybrid"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # both user2 cars match (Diesel OR Hybrid)
        expected_qs = Car.objects.filter(user=self.user2).order_by("-createdAt")
        self.assert_paginated_payload(
            response.data,
            expected_qs,
            expected_page=1,
            expected_pages=1,
            expected_page_size=9,
            expected_len=expected_qs.count(),
        )

    def test_filter_brand_and_motor_and_logic_across_groups(self):
        """
        brand group AND motor group must both match.
        In this fixture:
          - user2: Audi A4 Diesel, Audi A5 Hybrid
          - user1: Porsche Petrol
        Query for user2: brand=Audi-Porsche AND motor=Diesel
          -> only Audi A4 Diesel (car2)
        """
        self.login(self.user2)

        response = self.client.get(self.url, {"brand": "Audi-Porsche", "motor": "Diesel"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_qs = Car.objects.filter(user=self.user2, motor__icontains="Diesel").order_by(
            "-createdAt"
        )
        self.assert_paginated_payload(
            response.data,
            expected_qs,
            expected_page=1,
            expected_pages=1,
            expected_page_size=9,
            expected_len=expected_qs.count(),
        )

        # Ensure only Diesel cars returned
        for car in response.data["data"]:
            self.assertIn("diesel", car["motor"].lower())

    def test_filter_trims_whitespace_around_hyphen_values(self):
        self.login(self.user2)

        # values have spaces around them; your code does strip()
        response = self.client.get(self.url, {"brand": "  Audi  -   Porsche  "})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # should still match Audi cars for user2
        expected_qs = Car.objects.filter(user=self.user2, brand__icontains="Audi").order_by(
            "-createdAt"
        )
        self.assert_paginated_payload(
            response.data,
            expected_qs,
            expected_page=1,
            expected_pages=1,
            expected_page_size=9,
            expected_len=expected_qs.count(),
        )

    def test_pagination_non_int_page_falls_back_to_page_1_and_out_of_range_to_last_page(self):
        """
        Your pagination behavior:
        - page is missing / not an int => return page 1
        - page out of range => return last page
        """
        # create enough cars for user2 to exceed page_size=9
        for i in range(10):  # user2 already has 2; +10 => 12 total
            Car.objects.create(
                brand="Audi",
                model=f"Extra {i}",
                motor="Diesel",
                user=self.user2,
            )

        self.login(self.user2)

        expected_all = Car.objects.filter(user=self.user2).order_by("-createdAt")
        total = expected_all.count()
        self.assertEqual(total, 12)

        # Non-int page -> page 1
        resp1 = self.client.get(self.url, {"page": "abc"})
        self.assertEqual(resp1.status_code, status.HTTP_200_OK)
        self.assert_paginated_payload(
            resp1.data,
            expected_all,
            expected_page=1,
            expected_pages=2,
            expected_page_size=9,
            expected_len=9,
        )

        # Out-of-range page -> last page (page 2) with remaining 3 items (12 - 9 = 3)
        resp2 = self.client.get(self.url, {"page": 999})
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)

        # For page 2, compare against the slice after the first 9
        expected_page2_qs = expected_all[9:]
        # Our helper expects a queryset-like object with count() + values_list(),
        # so easiest is to materialize expected ids for page 2 and compare directly:
        self.assertEqual(resp2.data["page"], 2)
        self.assertEqual(resp2.data["pages"], 2)
        self.assertEqual(resp2.data["count"], total)
        self.assertEqual(resp2.data["page_size"], 9)
        self.assertEqual(len(resp2.data["data"]), 3)

        expected_ids_page2 = list(expected_page2_qs.values_list("id", flat=True))
        response_ids_page2 = [item["id"] for item in resp2.data["data"]]
        self.assertEqual(response_ids_page2, expected_ids_page2)

class GetSingleCarTest(TestCase):
    """Test module for GET single car API (RetrieveAPIView restricted to request.user)."""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username="u1", email="e1@gmail.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="u2", email="u2@gmail.com", password="password"
        )

        self.car1 = Car.objects.create(
            brand="Porsche", model="911 GT3 RS", motor="Petrol", user=self.user1
        )
        self.car2 = Car.objects.create(
            brand="Audi", model="A4", motor="Diesel", user=self.user2
        )

    def login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)

    def test_should_not_get_valid_single_car_without_auth(self):
        self.logout()
        response = self.client.get(reverse("car_detail", kwargs={"id": self.car1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_get_valid_single_car_of_user1(self):
        self.login(self.user1)

        response = self.client.get(reverse("car_detail", kwargs={"id": self.car1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car = Car.objects.get(id=self.car1.id, user=self.user1)
        serializer = GetCarSerializer(car, context={"request": response.wsgi_request})
        self.assertEqual(response.data, serializer.data)

    def test_should_get_valid_single_car_of_user2(self):
        self.login(self.user2)

        response = self.client.get(reverse("car_detail", kwargs={"id": self.car2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car = Car.objects.get(id=self.car2.id, user=self.user2)
        serializer = GetCarSerializer(car, context={"request": response.wsgi_request})
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_car(self):
        self.login(self.user1)

        # choose an id that does not exist
        invalid_id = max(self.car1.id, self.car2.id) + 999
        response = self.client.get(reverse("car_detail", kwargs={"id": invalid_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user1_should_not_get_car_of_user2(self):
        """
        With get_queryset() restricted to request.user,
        user1 requesting car2.id will behave like "not found" => 404.
        """
        self.login(self.user1)

        response = self.client.get(reverse("car_detail", kwargs={"id": self.car2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user2_should_not_get_car_of_user1(self):
        self.login(self.user2)

        response = self.client.get(reverse("car_detail", kwargs={"id": self.car1.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewCarTest(TestCase):
    """Test module for creating a new car (ListCreateAPIView + perform_create)."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("car_list_create")

        self.user1 = User.objects.create_user(
            username="u1", email="e1@gmail.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="u2", email="e2@gmail.com", password="password"
        )

        # valid payload: no "user" field; server sets user=request.user
        self.valid_payload = {
            "brand": "Porsche",
            "model": "Cayenne",
            "motor": "Petrol",
        }

        # invalid payloads (missing required fields)
        self.invalid_payload1 = {"brand": "", "model": "Cayenne", "motor": "Petrol"}
        self.invalid_payload2 = {"brand": "Porsche", "model": "", "motor": "Petrol"}
        self.invalid_payload3 = {"brand": "Porsche", "model": "Cayenne", "motor": ""}
        self.invalid_payload4 = {"brand": "", "model": "", "motor": ""}

    def login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)

    def test_should_not_create_car_without_auth(self):
        self.logout()
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_valid_car(self):
        self.login(self.user1)

        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify it exists and belongs to request.user
        self.assertTrue(
            Car.objects.filter(
                user=self.user1,
                brand="Porsche",
                model="Cayenne",
                motor="Petrol",
            ).exists()
        )

        # Optional: check returned payload also has the right user
        # (depends on what CreateUpdateCarSerializer returns)
        if isinstance(response.data, dict) and "user" in response.data:
            self.assertEqual(response.data["user"], self.user1.id)

    def test_should_not_create_invalid_car(self):
        self.login(self.user1)

        r1 = self.client.post(self.url, data=self.invalid_payload1, format="json")
        self.assertEqual(r1.status_code, status.HTTP_400_BAD_REQUEST)

        r2 = self.client.post(self.url, data=self.invalid_payload2, format="json")
        self.assertEqual(r2.status_code, status.HTTP_400_BAD_REQUEST)

        r3 = self.client.post(self.url, data=self.invalid_payload3, format="json")
        self.assertEqual(r3.status_code, status.HTTP_400_BAD_REQUEST)

        r4 = self.client.post(self.url, data=self.invalid_payload4, format="json")
        self.assertEqual(r4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_client_cannot_override_user_field(self):
        """
        Even if client sends user=<someone else>,
        perform_create(serializer.save(user=request.user)) must win.
        """
        self.login(self.user1)

        malicious_payload = {
            **self.valid_payload,
            "user": self.user2.id,  # attempt to create a car under user2
        }

        response = self.client.post(self.url, data=malicious_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created = Car.objects.order_by("-id").first()
        self.assertIsNotNone(created)
        self.assertEqual(created.user_id, self.user1.id)  # MUST be user1, not user2

class UpdateCarTest(TestCase):
    """Test module for updating a car (RetrieveUpdateDestroyAPIView restricted to request.user)."""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="u1", email="e1@gmail.com", password="password")
        self.user2 = User.objects.create_user(username="u2", email="e2@gmail.com", password="password")

        self.car1 = Car.objects.create(brand="Porsche", model="Panamera", motor="Petrol", user=self.user1)
        self.car2 = Car.objects.create(brand="Porsche", model="Carrera", motor="Petrol", user=self.user2)

        self.valid_payload = {
            "brand": "Porsche",
            "model": "Cayenne",
            "motor": "Petrol",
        }

        self.invalid_payload1 = {"brand": "", "model": "Cayenne", "motor": "Petrol"}
        self.invalid_payload2 = {"brand": "Porsche", "model": "", "motor": "Petrol"}
        self.invalid_payload3 = {"brand": "Porsche", "model": "Cayenne", "motor": ""}
        self.invalid_payload4 = {"brand": "", "model": "", "motor": ""}

    def login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)

    def test_should_not_update_car_without_auth(self):
        self.logout()
        response = self.client.put(
            reverse("car_detail", kwargs={"id": self.car1.id}),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_car(self):
        self.login(self.user1)

        response = self.client.put(
            reverse("car_detail", kwargs={"id": self.car1.id}),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_car = Car.objects.get(id=self.car1.id)

        # brand stays Porsche, model updated to Cayenne, motor stays Petrol
        self.assertEqual(updated_car.brand, "Porsche")
        self.assertEqual(updated_car.model, "Cayenne")
        self.assertEqual(updated_car.motor, "Petrol")

        # Optional: ensure it still belongs to user1
        self.assertEqual(updated_car.user_id, self.user1.id)

    def test_should_not_update_car_with_invalid_payloads(self):
        self.login(self.user1)

        original = Car.objects.get(id=self.car1.id)
        original_brand, original_model, original_motor = original.brand, original.model, original.motor

        for payload in [self.invalid_payload1, self.invalid_payload2, self.invalid_payload3, self.invalid_payload4]:
            response = self.client.put(
                reverse("car_detail", kwargs={"id": self.car1.id}),
                data=payload,
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # Ensure the object was not changed
            refreshed = Car.objects.get(id=self.car1.id)
            self.assertEqual(refreshed.brand, original_brand)
            self.assertEqual(refreshed.model, original_model)
            self.assertEqual(refreshed.motor, original_motor)

    def test_user1_should_not_update_car_of_user2(self):
        """
        Because get_queryset() filters by request.user, user1 updating car2 returns 404.
        """
        self.login(self.user1)

        response = self.client.put(
            reverse("car_detail", kwargs={"id": self.car2.id}),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Ensure car2 is unchanged in DB
        car2_refreshed = Car.objects.get(id=self.car2.id)
        self.assertEqual(car2_refreshed.model, "Carrera")

class DeleteSingleCarTest(TestCase):
    """Test module for deleting an existing car record."""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="u1", email="e1@gmail.com", password="password")
        self.user2 = User.objects.create_user(username="u2", email="e2@gmail.com", password="password")

        self.car1 = Car.objects.create(brand="Porsche", model="Panamera", motor="Petrol", user=self.user1)
        self.car2 = Car.objects.create(brand="Porsche", model="Carrera", motor="Petrol", user=self.user2)

    def login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)

    def test_should_not_delete_car_without_auth(self):
        self.logout()
        response = self.client.delete(reverse("car_detail", kwargs={"id": self.car1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_delete_car(self):
        self.login(self.user1)

        response = self.client.delete(reverse("car_detail", kwargs={"id": self.car1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(id=self.car1.id).exists())

    def test_invalid_delete_car(self):
        self.login(self.user1)

        invalid_id = max(self.car1.id, self.car2.id) + 999
        response = self.client.delete(reverse("car_detail", kwargs={"id": invalid_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user1_should_not_delete_car_of_user2(self):
        """
        Because get_queryset() filters by request.user, user1 deleting car2 returns 404.
        """
        self.login(self.user1)

        response = self.client.delete(reverse("car_detail", kwargs={"id": self.car2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Ensure car2 still exists
        self.assertTrue(Car.objects.filter(id=self.car2.id).exists())    

class GetAllCarsAdminTest(TestCase):
    """Test module for GET all cars admin API."""

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            username="u1", email="e1@gmail.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="u2", email="e2@gmail.com", password="password"
        )

        self.car1 = Car.objects.create(
            brand="Porsche", model="911 GT3 RS", motor="Petrol", user=self.admin
        )
        self.car2 = Car.objects.create(
            brand="Audi", model="A4", motor="Diesel", user=self.user2
        )
        self.car3 = Car.objects.create(
            brand="Audi", model="A5", motor="Hybrid", user=self.user2
        )

        self.url_admin = reverse("car_list_create_admin")

    def login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)

    def test_should_not_get_admin_cars_without_auth(self):
        self.logout()
        response = self.client.get(self.url_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_should_get_all_cars(self):
        self.login(self.admin)

        response = self.client.get(self.url_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        all_cars = Car.objects.all().order_by("-createdAt")
        serializer = GetCarSerializer(all_cars, many=True, context={"request": response.wsgi_request})

        self.assertEqual(response.data, serializer.data)

    def test_should_not_get_all_cars_if_not_admin(self):
        self.login(self.user2)

        response = self.client.get(self.url_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_filtering_brand_and_motor(self):
        """
        Admin view uses the same filtering approach (icontains, '-' separated values),
        across ALL users.
        """
        self.login(self.admin)

        # brand Audi + motor Diesel => only car2
        response = self.client.get(self.url_admin, {"brand": "Audi", "motor": "Diesel"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_qs = Car.objects.filter(brand__icontains="Audi", motor__icontains="Diesel").order_by("-createdAt")
        serializer = GetCarSerializer(expected_qs, many=True, context={"request": response.wsgi_request})

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car2.id)


class DeleteSingleCarAdminTest(TestCase):
    """Test module for an admin deleting an existing car record."""

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            username="u1", email="e1@gmail.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="u2", email="e2@gmail.com", password="password"
        )

        self.car1 = Car.objects.create(
            brand="Porsche", model="Panamera", motor="Petrol", user=self.admin
        )
        self.car2 = Car.objects.create(
            brand="Porsche", model="Carrera", motor="Petrol", user=self.user2
        )

        self.url_car1_admin = reverse("car_detail_admin", kwargs={"id": self.car1.id})
        self.url_car2_admin = reverse("car_detail_admin", kwargs={"id": self.car2.id})

    def login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)

    def test_should_not_delete_car_without_auth(self):
        self.logout()
        response = self.client.delete(self.url_car1_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_car(self):
        self.login(self.admin)

        # admin deletes own car
        response = self.client.delete(self.url_car1_admin)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(id=self.car1.id).exists())

        # admin deletes another user's car
        response = self.client.delete(self.url_car2_admin)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(id=self.car2.id).exists())

    def test_non_admin_cannot_use_delete_admin_endpoint(self):
        self.login(self.user2)

        # non-admin cannot delete own car via admin endpoint
        response = self.client.delete(self.url_car2_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Car.objects.filter(id=self.car2.id).exists())

        # non-admin cannot delete admin's car via admin endpoint
        response = self.client.delete(self.url_car1_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Car.objects.filter(id=self.car1.id).exists())

    def test_admin_delete_invalid_id(self):
        self.login(self.admin)

        invalid_id = max(self.car1.id, self.car2.id) + 999
        response = self.client.delete(reverse("car_detail_admin", kwargs={"id": invalid_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
