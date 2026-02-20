# # NOT USED ANYMORE

# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six  

# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
#     """
#     Class which extends Django's built in PasswordTokenGenerator class.
    
#     This class helps generate tokens for activating users' accounts 
#     or for changing the users' forgotten passwords.

#     This token can be used more than once. 
#     """
    
#     def _make_hash_value(self, user, timestamp):
#         """
#         Override the _make_hash_value method to customize the token's unique hash.
#         Generate a hash based on the user's primary key, the timestamp, and their activation status
#         """
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active)
#         )

# # Instantiate an instance of the custom token generator
# account_activation_token = AccountActivationTokenGenerator()

# # The _make_hash_value method in AccountActivationTokenGenerator 
# # is called internally by the PasswordResetTokenGenerator class 
# # whenever you use methods like make_token or check_token on an instance of the token generator.
# # (See for example authentication/views_OLD_with_recaptcha.py RegisterWithSendingEmailView or RequestChangeForgottenPasswordView)


# # The make_token method is used to create a token for a specific user. 
# # When you call account_activation_token.make_token(user), 
# # Django internally calls _make_hash_value(user, timestamp) 
# # to generate a unique hash based on the user's data and a timestamp.
# # Django combines this hash with other data to create the final token, 
# # which is then returned by make_token


# # The check_token method is used to verify if a token is valid for a specific user.
# # When you call account_activation_token.check_token(user, token), 
# # Django regenerates the hash by calling _make_hash_value(user, timestamp) 
# # using the current timestamp and compares it with the one stored in the provided token.
# # If the generated hash matches the token's hash and the token hasn’t expired, 
# # check_token returns True; otherwise, it returns False

## If I use this class, then the activation token can be used only once.
## But I do not really need to add this requirement, since the ActivateAccountView() 
## only sets user.is_active = True, without making any other changes.