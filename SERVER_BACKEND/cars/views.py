from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Car
from .serializers import CarSerializer, CreateUpdateCarSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.html import escape
import nh3
from rest_framework.throttling import UserRateThrottle
from rest_framework import generics

# Create your views here.

@method_decorator(csrf_protect, name="dispatch") 
class CarListCreateApiView(generics.ListCreateAPIView):
    """
    View for listing the car notes of the current user or for creating a new car note.
    """
    permission_classes=[permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarSerializer
        return  CreateUpdateCarSerializer
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        all_cars=Car.objects.filter(user= self.request.user).order_by("-createdAt")

        # Filtering based on query parameters
        filters = self.request.query_params

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
                car_contains_motor= False
                motor_values = motor.split("-")
                for motor_value in motor_values:
                    if motor_value in car.motor:
                        car_contains_motor = True
                        break
                is_valid_filter = is_valid_filter and car_contains_motor

            if is_valid_filter:
                filtered_cars.append(car)

        return filtered_cars

@method_decorator(csrf_protect, name="dispatch") 
class CarDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating or deleting a particular car note of the current user.
    """

    permission_classes=[permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarSerializer
        return  CreateUpdateCarSerializer
    
    def get_queryset(self):
        return Car.objects.filter(user=self.request.user)    

    lookup_field="id"


@method_decorator(csrf_protect, name="dispatch") 
class CarListCreateApiViewAdminPriviledge(generics.ListAPIView):
    """
    View for listing all the notes in the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class=CarSerializer
    # throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        all_cars=Car.objects.all().order_by("-createdAt")

        # Filtering based on query parameters
        filters = self.request.query_params

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

        return filtered_cars


@method_decorator(csrf_protect, name="dispatch") 
class CarDetailApiViewAdminPriviledge(generics.DestroyAPIView):
    """
    View for removing a particular car note from the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        return Car.objects.all()

    lookup_field="id"


