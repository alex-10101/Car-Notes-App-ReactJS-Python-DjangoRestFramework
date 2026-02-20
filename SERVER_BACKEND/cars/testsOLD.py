# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status
# from .models import Car
# from django.contrib.auth import get_user_model
# from .serializers import GetCarSerializer
# import json 

# User = get_user_model()

# # Django will automatically create a TEST database, and then destroy the database after the tests are completed. 
# # Run tests with "python3 manage.py test".

# class GetAllCarsTest(TestCase):
#     """ Test module for GET all cars API."""

#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_user(username='u1', email='e1@gmail.com', password="password")
#         self.user2 = User.objects.create_user(username='u2', email='e2@gmail.com', password="password")
#         self.car1 = Car.objects.create(brand='Porsche', model="911 GT3 RS", motor='Petrol', user = self.user1)
#         self.car2 = Car.objects.create(brand='Audi', model="A4", motor='Diesel', user = self.user2)
#         self.car3 = Car.objects.create(brand='Audi', model="A5", motor='Hybrid', user = self.user2)

#     def login_user1(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def login_user2(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u2')[0])

#     def test_should_not_get_cars_without_auth(self):
#         response = self.client.get(reverse('car_list_create'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_user1_should_only_get_cars_of_user1(self):
#         self.login_user1()
#         response = self.client.get(reverse('car_list_create'))
#         all_cars = Car.objects.filter(user = self.user1.id).order_by("-createdAt")
#         serializer = GetCarSerializer(all_cars, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user2_should_only_get_cars_of_user2(self):
#         self.login_user2()
#         response = self.client.get(reverse('car_list_create'))
#         all_cars = Car.objects.filter(user = self.user2.id).order_by("-createdAt")
#         serializer = GetCarSerializer(all_cars, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user1_should_not_get_cars_of_user2(self):
#         self.login_user1()
#         response = self.client.get(reverse('car_list_create'))

#         # check that all cars in these response.data belong to user 1 (the request user)
#         for car in response.data:
#             self.assertEqual(car["user"], self.user1.id)

#         # check that all cars retrieved retrieved here from the database belong to user 2
#         all_cars_of_user2 = Car.objects.filter(user = self.user2.id).order_by("-createdAt")
#         serializer = GetCarSerializer(all_cars_of_user2, many=True)
#         for car in serializer.data:
#             self.assertEqual(car["user"], self.user2.id)
            
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class GetSingleCarTest(TestCase):
#     """ Test module for GET single car API."""

#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_user(username='u1', email='e1@gmail.com', password="password")
#         self.user2 = User.objects.create_user(username='u2', email='u2@gmail.com', password="password")
#         self.car1 = Car.objects.create(brand='Porsche', model="911 GT3 RS", motor='Petrol', user = self.user1)
#         self.car2 = Car.objects.create(brand='Audi', model="A4", motor='Diesel', user = self.user2)

#     def login_user1(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def login_user2(self):
#         # force_login expects an AbstractUser; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u2')[0])

#     def test_should_not_get_valid_single_car_without_auth(self):
#         response = self.client.get(reverse('car_detail', kwargs={'id': self.car1.id}))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_should_get_valid_single_car_of_user1(self):
#         self.login_user1()
#         response = self.client.get(reverse('car_detail', kwargs={'id': self.car1.id}))
#         car = Car.objects.get(id=self.car1.id, user = self.user1.id)
#         serializer = GetCarSerializer(car)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_should_get_valid_single_car_of_user2(self):
#         self.login_user2()
#         response = self.client.get(reverse('car_detail', kwargs={'id': self.car2.id}))
#         car = Car.objects.get(id=self.car2.id, user = self.user2.id)
#         serializer = GetCarSerializer(car)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_invalid_single_car(self):
#         self.login_user1()
#         # 30 is an id which should hopefully be different from the id of the created car for this test case
#         response = self.client.get(reverse('car_detail', kwargs={'id': 30}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user1_should_not_get_car_of_user2(self):
#         self.login_user1()
#         response = self.client.get(reverse('car_detail', kwargs={'id': self.car1.id}))
#         car = Car.objects.get(user = self.user2.id)
#         serializer = GetCarSerializer(car)
#         self.assertFalse(response.data["user"] == serializer.data["user"])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

# class CreateNewCarTest(TestCase):
#     """ Test module for creating a new car."""

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='u1', email='e1@gmail.com', password="password")

#         self.valid_payload = {
#             'brand': 'Porsche',
#             'model': 'Cayenne',
#             'motor': 'Petrol',
#             'user': self.user.id
#         }
#         self.invalid_payload1 = {
#             'brand': '',
#             'model': 'Cayenne',
#             'motor': 'Petrol',
#             'user': self.user.id
#         }
#         self.invalid_payload2 = {
#             'brand': 'Porsche',
#             'model': '',
#             'motor': 'Petrol',
#             'user': self.user.id
#         }
#         self.invalid_payload3 = {
#             'brand': 'Porsche',
#             'model': 'Cayenne',
#             'motor': '',
#             'user': self.user.id
#         }
#         self.invalid_payload4 = {
#             'brand': '',
#             'model': '',
#             'motor': '',
#             'user': None           
#         }


#     def login_user(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def test_should_not_create_car_without_auth(self):
#         response = self.client.post(
#             reverse('car_list_create'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_valid_car(self):
#         self.login_user()
#         response = self.client.post(
#             reverse('car_list_create'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   

#     def test_should_not_create_invalid_car(self):
#         self.login_user()
#         response = self.client.post(
#             reverse('car_list_create'),
#             data=json.dumps(self.invalid_payload1),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         response = self.client.post(
#             reverse('car_list_create'),
#             data=json.dumps(self.invalid_payload2),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         response = self.client.post(
#             reverse('car_list_create'),
#             data=json.dumps(self.invalid_payload3),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         response = self.client.post(
#             reverse('car_list_create'),
#             data=json.dumps(self.invalid_payload4),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class UpdateCarTest(TestCase):
#     """ Test module for updating a car."""

#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_user(username='u1', email='e1@gmail.com', password="password")
#         self.car1 = Car.objects.create(brand='Porsche', model='Panamera', motor='Petrol', user = self.user1)
#         self.user2 = User.objects.create_user(username='u2', email='e2@gmail.com', password="password")
#         self.car2 = Car.objects.create(brand='Porsche', model='Carrera', motor='Petrol', user = self.user2)

#         self.valid_payload = {
#             'brand': 'Porsche',
#             'model': 'Cayenne',
#             'motor': 'Petrol',
#             'user': self.user1.id
#         }
#         self.invalid_payload1 = {
#             'brand': '',
#             'model': 'Cayenne',
#             'motor': 'Petrol',
#             'user': self.user1.id
#         }
#         self.invalid_payload2 = {
#             'brand': 'Porsche',
#             'model': '',
#             'motor': 'Petrol',
#             'user': self.user1.id
#         }
#         self.invalid_payload3 = {
#             'brand': 'Porsche',
#             'model': 'Cayenne',
#             'motor': '',
#             'user': self.user1.id
#         }
#         self.invalid_payload4 = {
#             'brand': '',
#             'model': '',
#             'motor': '',
#             'user': None           
#         }

#     def login_user1(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def login_user2(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u2')[0])


#     def test_should_not_update_car_without_auth(self):
#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car1.id}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_update_car(self):
#         self.login_user1()
#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car1.id}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )

#         # check the the model property has been updated
#         updated_car = Car.objects.get(id=self.car1.id)
#         self.assertEqual(updated_car.brand, self.car1.brand)
#         self.assertEqual(updated_car.model, "Cayenne")
#         self.assertEqual(updated_car.motor, self.car1.motor)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
   
#     def test_should_not_update_car(self):
#         self.login_user1()
#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car1.id}),
#             data=json.dumps(self.invalid_payload1),
#             content_type='application/json'
#         )

#         # check the the car has not been updated
#         updated_car = Car.objects.get(id=self.car1.id)
#         self.assertEqual(updated_car.brand, self.car1.brand)
#         self.assertEqual(updated_car.model, self.car1.model)
#         self.assertEqual(updated_car.motor, self.car1.motor)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car1.id}),
#             data=json.dumps(self.invalid_payload2),
#             content_type='application/json'
#         )

#         # check the the car has not been updated
#         updated_car = Car.objects.get(id=self.car1.id)
#         self.assertEqual(updated_car.brand, self.car1.brand)
#         self.assertEqual(updated_car.model, self.car1.model)
#         self.assertEqual(updated_car.motor, self.car1.motor)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car1.id}),
#             data=json.dumps(self.invalid_payload3),
#             content_type='application/json'
#         )

#         # check the the car has not been updated
#         updated_car = Car.objects.get(id=self.car1.id)
#         self.assertEqual(updated_car.brand, self.car1.brand)
#         self.assertEqual(updated_car.model, self.car1.model)
#         self.assertEqual(updated_car.motor, self.car1.motor)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car1.id}),
#             data=json.dumps(self.invalid_payload4),
#             content_type='application/json'
#         )

#         # check the the car has not been updated
#         updated_car = Car.objects.get(id=self.car1.id)
#         self.assertEqual(updated_car.brand, self.car1.brand)
#         self.assertEqual(updated_car.model, self.car1.model)
#         self.assertEqual(updated_car.motor, self.car1.motor)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        

#     def test_user1_should_not_update_car_of_user2(self):
#         self.login_user1()
#         response = self.client.put(
#             reverse('car_detail', kwargs={'id': self.car2.id}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         # The original brand of car2 should remain "Carrera", it should not be updated to "Cayenne"
#         self.assertTrue(self.car2.model == "Carrera")
#         self.assertFalse(self.car2.model == "Cayenne")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class DeleteSingleCarTest(TestCase):
#     """ Test module for deleting an existing car record."""

#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_user(username='u1', email='e1@gmail.com', password="password")
#         self.car1 = Car.objects.create(brand='Porsche', model='Panamera', motor='Petrol', user = self.user1)
#         self.user2 = User.objects.create_user(username='u2', email='e2@gmail.com', password="password")
#         self.car2 = Car.objects.create(brand='Porsche', model='Carrera', motor='Petrol', user = self.user2)
   
#     def login_user1(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def login_user2(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u2')[0])

#     def test_should_not_delete_car_without_auth(self):
#         response = self.client.delete(reverse('car_detail', kwargs={'id': self.car1.id}))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_valid_delete_car(self):
#         self.login_user1()
#         response = self.client.delete(reverse('car_detail', kwargs={'id': self.car1.id}))
#         self.assertFalse(Car.objects.filter(id=self.car1.id).exists())
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_invalid_delete_car(self):
#         self.login_user1()
#         # 30 is an id which should hopefully be different from the id of the created car for this test case
#         response = self.client.delete(reverse('car_detail', kwargs={'id': 30}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user1_should_not_delete_car_of_user2(self):
#         self.login_user1()
#         response = self.client.delete(reverse('car_detail', kwargs={'id': self.car2.id}))
#         # Check that car2 still exists
#         self.assertTrue(Car.objects.filter(id=self.car2.id).exists())
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

# class GetAllCarsAdminTest(TestCase):
#     """ Test module for GET all cars admin API."""

#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_superuser(username='u1', email='e1@gmail.com', password="password")
#         self.user2 = User.objects.create_user(username='u2', email='e2@gmail.com', password="password")
#         self.car1 = Car.objects.create(brand='Porsche', model="911 GT3 RS", motor='Petrol', user = self.user1)
#         self.car2 = Car.objects.create(brand='Audi', model="A4", motor='Diesel', user = self.user2)
#         self.car3 = Car.objects.create(brand='Audi', model="A5", motor='Hybrid', user = self.user2)

#     def login_user1(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def login_user2(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u2')[0])

#     def test_should_not_get_cars_without_auth(self):
#         response = self.client.get(reverse('car_list_create'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_should_get_all_cars(self):
#         self.login_user1()
#         response = self.client.get(reverse('car_list_create_admin'))
#         all_cars = Car.objects.all().order_by("-createdAt")
#         serializer = GetCarSerializer(all_cars, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_should_not_get_all_cars_if_not_admin(self):
#         self.login_user2()
#         response = self.client.get(reverse('car_list_create_admin'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# class DeleteSingleCarAdminTest(TestCase):
#     """ Test module for an admin deleting an existing car record."""

#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_superuser(username='u1', email='e1@gmail.com', password="password")
#         self.car1 = Car.objects.create(brand='Porsche', model='Panamera', motor='Petrol', user = self.user1)
#         self.user2 = User.objects.create_user(username='u2', email='e2@gmail.com', password="password")
#         self.car2 = Car.objects.create(brand='Porsche', model='Carrera', motor='Petrol', user = self.user2)
   
#     def login_user1(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u1')[0])

#     def login_user2(self):
#         # force_login expects an AbstractUser as argument; return type of get_or_create is tuple[AbstractUser, bool] 
#         # ---> add "[0]" to choose the AbstractUser from the tuple
#         self.client.force_login(User.objects.get_or_create(username='u2')[0])

#     def test_should_not_delete_car_without_auth(self):
#         response = self.client.delete(reverse('car_detail', kwargs={'id': self.car1.id}))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_admin_can_delete_any_car(self):
#         self.login_user1()

#         # user1 (admin) can delete his/her own car record
#         response = self.client.delete(reverse('car_detail_admin', kwargs={'id': self.car1.id}))
#         self.assertFalse(Car.objects.filter(id=self.car1.id).exists())
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         # user1 (admin) can also delete cars belonging to user2
#         response = self.client.delete(reverse('car_detail_admin', kwargs={'id': self.car2.id}))
#         self.assertFalse(Car.objects.filter(id=self.car2.id).exists())
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_non_admin_can_not_use_the_delete_admin_endpoint(self):
#         self.login_user2()

#         # user2 (not an admin) can delete his/her own car record, but it can not use the "car_detail_admin" endpoint
#         response = self.client.delete(reverse('car_detail_admin', kwargs={'id': self.car2.id}))
#         self.assertTrue(Car.objects.filter(id=self.car2.id).exists())
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#         # user2 (not an admin) can not a car record of user1 
#         response = self.client.delete(reverse('car_detail_admin', kwargs={'id': self.car1.id}))
#         self.assertTrue(Car.objects.filter(id=self.car1.id).exists())
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
