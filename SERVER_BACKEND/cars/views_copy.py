from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Car
from .serializers import CarSerializer, CreateUpdateCarSerializer
import nh3
from django.db.models import Q

# Create your views here.

class CarListCreateApiView(APIView):
    """
    View for listing the car notes of the current user or for creating a new car note.
    """

    permission_classes=[permissions.IsAuthenticated]

    # def __car_contains_filter(self, filter, car):
    #     """
    #     Private method to check if a car contains the given filter
    #     """
    #     contains_filter=False
    #     filter_values = filter.split("-")
    #     for filter_value in filter_values:
    #         if filter_value in car.brand or filter_value in car.motor:
    #             contains_filter=True
    #             break
    #     return contains_filter


    # def get(self, request):
    #     """
    #     Get all the car notes for given requested user
    #     """
    #     # Filtering based on query parameters
    #     filters = request.query_params

    #     all_cars_of_the_request_user = Car.objects.filter(user = request.user).order_by("-createdAt")
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

    #     serializer = CarSerializer(filtered_cars, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
    def get(self, request):
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
        
        filtered_cars = Car.objects.filter(filters).order_by('-createdAt') # AND queries
        serializer = CarSerializer(filtered_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def post(self, request):
        """
        Create a new car note
        """
        data = {
            "brand": nh3.clean(request.data["brand"]), 
            "model": nh3.clean(request.data["model"]), 
            "motor": nh3.clean(request.data["motor"]),
            "user": request.user.id
        }

        # serializer = CarSerializer(data=data, partial = True)
        serializer = CreateUpdateCarSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


class CarDetailApiView(APIView):
    """
    View for retrieving, updating or deleting a particular car note of the current user.
    """

    permission_classes=[permissions.IsAuthenticated]

    def __get_car_note(self, carId, userId):
        """
        Private method to get the car note with given car id and user id
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
        car = self.__get_car_note(id, request.user.id)

        if car is None:
            return Response(
                {"detail": "Car note with the given car id and user id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    
    def put(self, request, id):
        """
        Update the car note with the given car id and user id.
        The id is a request parameter.
        """

        car = self.__get_car_note(id, request.user.id)

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

        # serializer = CarSerializer(instance=car, data=data, partial=True)
        serializer = CreateUpdateCarSerializer(instance=car, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
            
        return Response(
            {"detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request, id):
        """
        Delete the car note with the given car id and user id.
        The id is a request parameter.
        """
        car = self.__get_car_note(id, request.user.id)

        if car is None:
            return Response(
                {"detail": "Car note with the given car id and user id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        car.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CarListCreateApiViewAdminPriviledge(APIView):
    """
    View for listing all the notes in the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]

    # def __car_contains_filter(self, filter, car):
    #     """
    #     Private method to check if a car contains the given filter
    #     """
    #     contains_filter=False
    #     filter_values = filter.split("-")
    #     for filter_value in filter_values:
    #         if filter_value in car.brand or filter_value in car.motor:
    #             contains_filter=True
    #             break
    #     return contains_filter


    # def get(self, request):
    #     """
    #     Get all car notes of all users.
    #     """

    #     # Filtering based on query parameters
    #     filters = request.query_params

    #     all_cars_of_all_users = Car.objects.all().order_by("-createdAt")
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


    #     serializer = CarSerializer(filtered_cars, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
    def get(self, request):
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

        # cars belong to all users
        filters = brand_queries & motor_queries
        
        filtered_cars = Car.objects.filter(filters).order_by('-createdAt') # AND queries
        serializer = CarSerializer(filtered_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

