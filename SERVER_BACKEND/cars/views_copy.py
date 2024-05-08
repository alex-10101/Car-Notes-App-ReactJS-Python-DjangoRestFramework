from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Car
from .serializers import CarSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.html import escape
import nh3
from rest_framework.throttling import UserRateThrottle

# Create your views here.

@method_decorator(csrf_protect, name="dispatch") 
class CarListCreateApiView(APIView):
    """
    View for listing the car notes of the current user or for creating a new car note.
    """

    permission_classes=[permissions.IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get(self, request):
        """
        Get all the car notes for given requested user
        """
        try:

            # Filtering based on query parameters
            filters = request.query_params

            all_cars = Car.objects.filter(user = request.user).order_by("-createdAt")
            filtered_cars = []

            for car in all_cars:
                is_valid_filter = True

                brand = filters.get('brand')
                if brand:
                    car_contains_brand = False
                    brand_values = brand.split("-")
                    for brand_value in brand_values:
                        if car.brand == brand_value:
                            car_contains_brand = True
                            break
                    is_valid_filter = is_valid_filter and car_contains_brand
                
                motor = filters.get('motor')
                if motor:
                    car_contains_motor = False
                    motor_values = motor.split("-")
                    for motor_value in motor_values:
                        if motor_value in car.motor:
                            car_contains_motor = True
                            break
                    is_valid_filter = is_valid_filter and car_contains_motor

                if is_valid_filter:
                    filtered_cars.append(car)


            serializer = CarSerializer(filtered_cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        """
        Create a new car note
        """
        try:

            data = {
                "brand": nh3.clean(request.data["brand"]), 
                "model": nh3.clean(request.data["model"]), 
                "motor": nh3.clean(request.data["motor"]),
                "user": request.user.id
            }

            serializer = CarSerializer(data=data, partial = True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                {"detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_protect, name="dispatch") 
class CarDetailApiView(APIView):
    """
    View for retrieving, updating or deleting a particular car note of the current user.
    """

    permission_classes=[permissions.IsAuthenticated]

    def get_car_note(self, carId, userId):
        """
        Helper method to get the car note with given car id and user id
        """
        try:
            return Car.objects.get(id=carId, user = userId)
        except Car.DoesNotExist:
            return None
        
    def get(self, request, id):
        """
        Get the car note with the given car id and user id.
        The id is a request parameter.
        """
        try:
            car = self.get_car_note(id, request.user.id)

            if car is None:
                return Response(
                    {"detail": "Car note with the given car id and user id does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = CarSerializer(car)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    
    def put(self, request, id):
        """
        Update the car note with the given car id and user id.
        The id is a request parameter.
        """

        try:
            car = self.get_car_note(id, request.user.id)

            if car is None:
                return Response(
                    {"detail": "Car note with the given car id and user id does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            data = {
                "brand": nh3.clean(request.data["brand"]), 
                "model": nh3.clean(request.data["model"]), 
                "motor": nh3.clean(request.data["motor"]),
                "user": request.user.id
            }

            serializer = CarSerializer(instance=car, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
                
            return Response(
                {"detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id):
        """
        Delete the car note with the given car id and user id.
        The id is a request parameter.
        """

        try:
            car = self.get_car_note(id, request.user.id)

            if car is None:
                return Response(
                    {"detail": "Car note with the given car id and user id does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            car.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_protect, name="dispatch") 
class CarListCreateApiViewAdminPriviledge(APIView):
    """
    View for listing all the notes in the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    # throttle_classes = [UserRateThrottle]

    def get(self, request):
        """
        Get all car notes of all users.
        """
        try:

            # Filtering based on query parameters
            filters = request.query_params

            all_cars_of_all_users = Car.objects.all().order_by("-createdAt")
            filtered_cars = []

            for car in all_cars_of_all_users:
                is_valid_filter = True

                brand = filters.get('brand')
                if brand:
                    car_contains_brand = False
                    brand_values = brand.split("-")
                    for brand_value in brand_values:
                        if car.brand == brand_value:
                            car_contains_brand = True
                            break
                    is_valid_filter = is_valid_filter and car_contains_brand
                
                motor = filters.get('motor')
                if motor:
                    car_contains_motor = False
                    motor_values = motor.split("-")
                    for motor_value in motor_values:
                        if motor_value in car.motor:
                            car_contains_motor = True
                            break
                    is_valid_filter = is_valid_filter and car_contains_motor

                if is_valid_filter:
                    filtered_cars.append(car)

            serializer = CarSerializer(filtered_cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_protect, name="dispatch") 
class CarDetailApiViewAdminPriviledge(APIView):
    """
    View for removing a particular car note from the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]

    def delete(self, request, id):
        """
        Delete the car note with the given car id.
        The id is a request parameter.
        """

        try:
            car = None
            try:
                car = Car.objects.get(id=id)
            except Car.DoesNotExist:
                return Response(
                    {"detail": "Car note with the given car id does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

            car.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
