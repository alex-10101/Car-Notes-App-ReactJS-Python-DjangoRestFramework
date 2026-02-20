# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# import json 
# import time

# # Create your tests here.

# User = get_user_model()

# class RegistrationTests(TestCase):
#     """
#     Unit Tests to check the registration view. This tests only work if recaptcha is disabled.
#     """

#     def setUp(self):
#         # Create a test user for duplicate username/email tests
#         self.existing_user = User.objects.create_user(
#             username='existinguser', 
#             email='existinguser@example.com', 
#             password='password123'
#         )

#     def test_registration_success(self):
#         """
#         Test that a user can register successfully with valid data
#         """
#         registration_data = {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password': 'StrongPassword123',
#             'confirmPassword': 'StrongPassword123'
#         }

#         response = self.client.post(
#             reverse('register'), 
#             data=json.dumps(registration_data), 
#             content_type='application/json')

#         # Ensure registration was successful 
#         self.assertEqual(response.status_code, 201)
#         # Check that the new user exists in the database
#         self.assertTrue(User.objects.filter(username='newuser').exists())
#         self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

#     def test_registration_password_mismatch(self):
#         """
#         Test that registration fails when passwords do not match
#         """
#         registration_data = {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password': 'StrongPassword123',
#             'confirmPassword': 'DifferentPassword123'
#         }

#         response = self.client.post(
#             reverse('register'), 
#             data=json.dumps(registration_data), 
#             content_type='application/json')

#         # Ensure registration failed
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user was not created
#         self.assertFalse(User.objects.filter(username = "newuser").exists())


#     def test_registration_duplicate_username(self):
#         """
#         Test that registration fails when username is already taken
#         """
#         registration_data = {
#             'username': 'existinguser',  # This username already exists
#             'email': 'newuser@example.com',
#             'password': 'StrongPassword123',
#             'confirmPassword': 'StrongPassword123'
#         }
#         response = self.client.post(
#             reverse('register'), 
#             data=json.dumps(registration_data), 
#             content_type='application/json')

#         # Ensure registration failed 
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user was not created
#         self.assertFalse(User.objects.filter(username = "existinguser", email = "newuser@example.com").exists())

#     def test_registration_duplicate_email(self):
#         """
#         Test that registration fails when email is already in use
#         """
#         registration_data = {
#             'username': 'newuser',
#             'email': 'existinguser@example.com',  # This email is already taken
#             'password': 'StrongPassword123',
#             'confirmPassword': 'StrongPassword123'
#         }
#         response = self.client.post(
#             reverse('register'), 
#             data=json.dumps(registration_data), 
#             content_type='application/json')

#         # Ensure registration failed 
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user was not created
#         self.assertFalse(User.objects.filter(username = "newuser", email = "existinguser@example.com").exists())

#     def test_registration_invalid_email(self):
#         """
#         Test that registration fails when an invalid email format is provided
#         """
#         registration_data = {
#             'username': 'newuser',
#             'email': 'invalid-email-format',  # Invalid email format
#             'password': 'StrongPassword123',
#             'confirmPassword': 'StrongPassword123'
#         }
#         response = self.client.post(
#             reverse('register'), 
#             data=json.dumps(registration_data), 
#             content_type='application/json')


#         # Ensure registration failed 
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user was not created
#         self.assertFalse(User.objects.filter(email='invalid-email-format').exists())


#     def test_registration_missing_fields(self):
#         """
#         Test that registration fails when required fields are missing
#         """
#         registration_data = {
#             'username': '',
#             'email': 'newuser@example.com',
#             'password': 'StrongPassword123',
#             'confirmPassword': 'StrongPassword123'
#         }
#         response = self.client.post(
#             reverse('register'), 
#             data=json.dumps(registration_data), 
#             content_type='application/json')

#         # Ensure registration failed 
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user was not created
#         self.assertFalse(User.objects.filter(email='newuser@example.com').exists())


#     def test_registration_weak_password(self):
#         """
#         Test that registration fails when a weak password is provided
#         """
#         registration_data = {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password': 'weak',
#             'confirmPassword': 'weak'
#         }
#         response = self.client.post(reverse('register'), registration_data)

#         # Ensure registration failed 
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user was not created
#         self.assertFalse(User.objects.filter(username='newuser').exists())


# class SessionAuthTests(TestCase):
#     """
#     Unit Tests to check the authentication and logout views. This tests only work if recaptcha is disabled.
#     """

#     def setUp(self):
#         # Create a test user
#         self.username = 'testuser'
#         self.email = 'testemail@gmail.com'
#         self.password = 'testpassword123'
#         self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)


#     def test_login_success(self):
#         """
#         Test that a user can log in successfully with valid credentials
#         """
#         login_data = {
#             'email': "testemail@gmail.com",
#             'password': "testpassword123"
#         }
#         response = self.client.post(
#             reverse('login'), 
#             data=json.dumps(login_data), 
#             content_type='application/json')

#         # Ensure login was successful 
#         self.assertEqual(response.status_code, 204)
#         # Ensure the user is authenticated
#         self.assertTrue(response.wsgi_request.user.is_authenticated)


#     def test_login_failure(self):
#         """
#         Test that a user cannot log in with invalid credentials
#         """
#         login_data = {
#             'email': "testemail@gmail.com",
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(
#             reverse('login'), 
#             data=json.dumps(login_data), 
#             content_type='application/json')

#         # Ensure login failed
#         self.assertEqual(response.status_code, 400)
#         # Ensure the user is not authenticated
#         self.assertFalse(response.wsgi_request.user.is_authenticated)


#     def test_session_exists_after_login(self):
#         """
#         Test that session data is set after login
#         """
#         login_data = {
#             'email': "testemail@gmail.com",
#             'password': "testpassword123"
#         }
#         response = self.client.post(
#             reverse('login'), 
#             data=json.dumps(login_data), 
#             content_type='application/json')

#         self.assertEqual(response.status_code, 204)
#         # Check that session key is set (logged-in session)
#         session = self.client.session
#         self.assertIn('_auth_user_id', session)
#         # Ensure the session user is correct
#         self.assertEqual(int(session['_auth_user_id']), self.user.pk)


#     def test_logout_clears_session(self):
#         """
#         Test that logging out clears the session
#         """
#         # First, log in the user
#         login_data = {
#             'email': "testemail@gmail.com",
#             'password': "testpassword123"
#         }
#         response = self.client.post(
#             reverse('login'), 
#             data=json.dumps(login_data), 
#             content_type='application/json')

#         self.assertEqual(response.status_code, 204)
#         # Now, log the user out
#         response = self.client.post(reverse('logout'))
#         # Ensure logout was successful 
#         self.assertEqual(response.status_code, 204)
#         # Check that session is cleared
#         session = self.client.session
#         self.assertNotIn('_auth_user_id', session)


#     def test_session_expiry(self):
#         """
#         Test that a session expires after a set time (for example, 0 to force expiry)
#         """
#         # Login user
#         login_data = {
#             'email': "testemail@gmail.com",
#             'password': "testpassword123"
#         }
#         response = self.client.post(
#             reverse('login'), 
#             data=json.dumps(login_data), 
#             content_type='application/json')

#         self.assertEqual(response.status_code, 204)

#         # Force session to expire the session in 1 second
#         session = self.client.session
#         session.set_expiry(1)  
#         session.save()

#         # Wait for 2 seconds to ensure the session has expired
#         time.sleep(2)  

#         # Try to access a restricted view after forcing session expiry
#         response = self.client.get(reverse('car_list_create'))
#         # Check if user was logged out due to session expiry
#         self.assertEqual(response.status_code, 403)  
#         self.assertNotIn('_auth_user_id', self.client.session)




