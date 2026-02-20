from rest_framework import serializers
from .models import Car
from utils.sanitizeUserInput import sanitize_user_input

class GetCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class CreateUpdateCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["brand", "motor", "model"]
        read_only_fields = ["user"]

        # override the default error messages:
        extra_kwargs = {
            "brand": {
                "error_messages": {
                    'required': 'Car brand is required.', 
                    'null': 'Car brand is required.', 
                    'invalid': 'Car brand is invalid.', 
                    'blank': 'Car brand is required.', 
                    'max_length': 'Car brand is too long.', 
                    'min_length': 'Car brand is too short.'
                }
            },
            "motor": {
                "error_messages": {
                    'required': 'Car motor is required.', 
                    'null': 'Car motor is required.', 
                    'invalid': 'Car motor is invalid.', 
                    'blank': 'Car motor is required.', 
                    'max_length': 'Car motor is too long.', 
                    'min_length': 'Car motor is too short.'
                }
            },
            "model": {
                "error_messages": {
                    'required': 'Car model is required.', 
                    'null': 'Car model is required.', 
                    'invalid': 'Car model is invalid.', 
                    'blank': 'Car model is required.', 
                    'max_length': 'Car model is too long.', 
                    'min_length': 'Car model is too short.'
                }
            }
        }

    # def __init__(self, *args, **kwargs):
    #     super(CreateUpdateCarSerializer, self).__init__(*args, **kwargs)     

    #     # the default error_messages for these fields (in models.py all these fields are CharFields of max_lenghth = 255 characters)

    #     # {'required': 'This field is required.', 
    #     #  'null': 'This field may not be null.', 
    #     #  'invalid': 'Not a valid string.', 
    #     #  'blank': 'This field may not be blank.', 
    #     #  'max_length': 'Ensure this field has no more than {max_length} characters.', 
    #     #  'min_length': 'Ensure this field has at least {min_length} characters.'}
    #     print(self.fields['brand'].error_messages)

    #     # {'required': 'This field is required.', 
    #     #  'null': 'This field may not be null.', 
    #     #  'invalid': 'Not a valid string.', 
    #     #  'blank': 'This field may not be blank.', 
    #     #  'max_length': 'Ensure this field has no more than {max_length} characters.', 
    #     #  'min_length': 'Ensure this field has at least {min_length} characters.'}
    #     print(self.fields['motor'].error_messages)

    #     # {'required': 'This field is required.', 
    #     #  'null': 'This field may not be null.', 
    #     #  'invalid': 'Not a valid string.', 
    #     #  'blank': 'This field may not be blank.', 
    #     #  'max_length': 'Ensure this field has no more than {max_length} characters.', 
    #     #  'min_length': 'Ensure this field has at least {min_length} characters.'}
    #     print(self.fields['model'].error_messages)

    def validate(self, data):
        return sanitize_user_input(data)



class GetProductFilterOptionsSerializer(serializers.Serializer):
    brands = serializers.ListField(child=serializers.CharField())
    motors = serializers.ListField(child=serializers.CharField())

