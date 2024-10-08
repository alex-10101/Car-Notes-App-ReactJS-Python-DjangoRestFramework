from rest_framework import permissions
from .models import Car
from .serializers import CarSerializer, CreateUpdateCarSerializer
from rest_framework import generics

# Create your views here.

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

    def car_contains_filter(self, filter, car):
        """
        Helper method to check if a car contains the given filter
        """
        contains_filter=False
        filter_values = filter.split("-")
        for filter_value in filter_values:
            if filter_value in car.brand or filter_value in car.motor:
                contains_filter=True
                break
        return contains_filter

    def get_queryset(self):
        all_cars_of_the_request_user=Car.objects.filter(user= self.request.user).order_by("-createdAt")

        # Filtering based on query parameters
        filters = self.request.query_params

        filtered_cars = []

        for car in all_cars_of_the_request_user:
            is_valid_filter = True

            brand = filters.get('brand')
            if brand:
                is_valid_filter = is_valid_filter and self.car_contains_filter(filter=brand, car=car)
            
            motor = filters.get('motor')
            if motor:
                is_valid_filter = is_valid_filter and self.car_contains_filter(filter=motor, car=car)
            
            if is_valid_filter:
                filtered_cars.append(car)

        return filtered_cars

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


class CarListCreateApiViewAdminPriviledge(generics.ListAPIView):
    """
    View for listing all the notes in the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class=CarSerializer
    
    def car_contains_filter(self, filter, car):
        """
        Helper method to check if a car contains the given filter
        """
        contains_filter=False
        filter_values = filter.split("-")
        for filter_value in filter_values:
            if filter_value in car.brand or filter_value in car.motor:
                contains_filter=True
                break
        return contains_filter

    def get_queryset(self):
        all_cars_of_all_users=Car.objects.all().order_by("-createdAt")

        # Filtering based on query parameters
        filters = self.request.query_params

        filtered_cars = []

        for car in all_cars_of_all_users:
            is_valid_filter = True

            brand = filters.get('brand')
            if brand:
                is_valid_filter = is_valid_filter and self.car_contains_filter(filter=brand, car=car)
            
            motor = filters.get('motor')
            if motor:
                is_valid_filter = is_valid_filter and self.car_contains_filter(filter=motor, car=car)
            
            if is_valid_filter:
                filtered_cars.append(car)

        return filtered_cars


class CarDetailApiViewAdminPriviledge(generics.DestroyAPIView):
    """
    View for removing a particular car note from the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        return Car.objects.all()

    lookup_field="id"


