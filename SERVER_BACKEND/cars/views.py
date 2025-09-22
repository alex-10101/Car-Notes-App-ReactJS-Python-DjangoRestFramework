from rest_framework import permissions
from .models import Car
from .serializers import CarSerializer, CreateUpdateCarSerializer
from rest_framework import generics
from django.db.models import Q

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

    # def __car_contains_filter(self, filter, car):
    #     """
    #     Helper method to check if a car contains the given filter
    #     """
    #     contains_filter=False
    #     filter_values = filter.split("-")
    #     for filter_value in filter_values:
    #         if filter_value in car.brand or filter_value in car.motor:
    #             contains_filter=True
    #             break
    #     return contains_filter

    # def get_queryset(self):
    #     all_cars_of_the_request_user=Car.objects.filter(user= self.request.user).order_by("-createdAt")

    #     # Filtering based on query parameters
    #     filters = self.request.query_params

    #     filtered_cars = []

    #     for car in all_cars_of_the_request_user:
    #         is_valid_filter = True

    #         brand = filters.get('brand')
    #         if brand:
    #             is_valid_filter = is_valid_filter and self.__car_contains_filter(filter=brand, car=car)
            
    #         motor = filters.get('motor')
    #         if motor:
    #             is_valid_filter = is_valid_filter and self.__car_contains_filter(filter=motor, car=car)
            
    #         if is_valid_filter:
    #             filtered_cars.append(car)

    #     return filtered_cars


    def get_queryset(self):
        """
        Get all cars belonging to the current request user,
        optionally filtered by query parameters.

        Supported query parameters:
        - brand: one or more brand names separated by "-" (OR logic within brand).
                Example: "Volkswagen-Hyundai-Aston Martin"
                → matches cars whose brand is Volkswagen OR Hyundai OR Aston Martin.
        - motor: one or more motor types separated by "-" (OR logic within motor).
                Example: "Diesel-Electric"
                → matches cars whose motor is Diesel OR Electric.

        The method filters all cars of the request user with the given brands AND the given motors

        Filtering logic:
        - brand group and motor group are each optional.
        - If both are provided, results must satisfy BOTH (AND logic).
        - Filtering is case-insensitive (iexact).
        - Always restricted to cars owned by the current request user.
        - Results are ordered by createdAt descending.
        """
        brand_queries = Q()
        motor_queries = Q()

        # Filtering based on query parameters
        params = self.request.query_params

        brand = params.get('brand')
        if brand:
            for brand_value in brand.split('-'):
                brand_value = brand_value.strip() # remove white spaces
                if brand_value:
                    # brand_queries |= Q(brand__iexact=brand_value) # OR queries (exact match, case-sensitive)
                    brand_queries |= Q(brand__icontains=brand_value) # OR queries (substring match, case-sensitive)

        motor = params.get('motor')
        if motor:
            for motor_value in motor.split('-'):
                motor_value = motor_value.strip()  # remove white spaces
                if motor_value:
                    # motor_queries |= Q(motor__iexact=motor_value) # OR queries (exact match, case-sensitive)
                    motor_queries |= Q(motor__icontains=motor_value) # OR queries (substring match, case-sensitive)

        # filter cars belonging only to the request user
        filters = Q(user=self.request.user) & brand_queries & motor_queries

        return Car.objects.filter(filters).order_by('-createdAt') # AND queries

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
    
    # def __car_contains_filter(self, filter, car):
    #     """
    #     Helper method to check if a car contains the given filter
    #     """
    #     contains_filter=False
    #     filter_values = filter.split("-")
    #     for filter_value in filter_values:
    #         if filter_value in car.brand or filter_value in car.motor:
    #             contains_filter=True
    #             break
    #     return contains_filter

    # def get_queryset(self):
    #     all_cars_of_all_users=Car.objects.all().order_by("-createdAt")

    #     # Filtering based on query parameters
    #     filters = self.request.query_params

    #     filtered_cars = []

    #     for car in all_cars_of_all_users:
    #         is_valid_filter = True

    #         brand = filters.get('brand')
    #         if brand:
    #             is_valid_filter = is_valid_filter and self.__car_contains_filter(filter=brand, car=car)
            
    #         motor = filters.get('motor')
    #         if motor:
    #             is_valid_filter = is_valid_filter and self.__car_contains_filter(filter=motor, car=car)
            
    #         if is_valid_filter:
    #             filtered_cars.append(car)

    #     return filtered_cars

    def get_queryset(self):
        """
        Get all cars belonging to all users,
        optionally filtered by query parameters.

        Supported query parameters:
        - brand: one or more brand names separated by "-" (OR logic within brand).
                Example: "Volkswagen-Hyundai-Aston Martin"
                → matches cars whose brand is Volkswagen OR Hyundai OR Aston Martin.
        - motor: one or more motor types separated by "-" (OR logic within motor).
                Example: "Diesel-Electric"
                → matches cars whose motor is Diesel OR Electric.

        The method filters all cars of all users with the given brands AND the given motors

        Filtering logic:
        - brand group and motor group are each optional.
        - If both are provided, results must satisfy BOTH (AND logic).
        - Filtering is case-insensitive (iexact).
        - Always restricted to cars owned by all users.
        - Results are ordered by createdAt descending.
        """
        brand_queries = Q()
        motor_queries = Q()

        # Filtering based on query parameters
        params = self.request.query_params

        brand = params.get('brand')
        if brand:
            for brand_value in brand.split('-'):
                brand_value = brand_value.strip() # remove white spaces
                if brand_value:
                    # brand_queries |= Q(brand__iexact=brand_value) # OR queries (exact match, case-sensitive)
                    brand_queries |= Q(brand__icontains=brand_value) # OR queries (substring match, case-sensitive)

        motor = params.get('motor')
        if motor:
            for motor_value in motor.split('-'):
                motor_value = motor_value.strip()  # remove white spaces
                if motor_value:
                    print(motor_value)
                    # motor_queries |= Q(motor__iexact=motor_value) # OR queries (exact match, case-sensitive)
                    motor_queries |= Q(motor__icontains=motor_value) # OR queries (substring match, case-sensitive)

        # cars belong to all users
        filters = brand_queries & motor_queries # AND queries

        return Car.objects.filter(filters).order_by('-createdAt')

class CarDetailApiViewAdminPriviledge(generics.DestroyAPIView):
    """
    View for removing a particular car note from the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        return Car.objects.all()

    lookup_field="id"


