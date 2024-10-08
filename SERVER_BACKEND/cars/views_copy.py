from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Car
from .serializers import CarSerializer, CreateUpdateCarSerializer
import nh3

# Create your views here.

class CarListCreateApiView(APIView):
    """
    View for listing the car notes of the current user or for creating a new car note.
    """

    permission_classes=[permissions.IsAuthenticated]

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


    def get(self, request):
        """
        Get all the car notes for given requested user
        """
        # Filtering based on query parameters
        filters = request.query_params

        all_cars_of_the_request_user = Car.objects.filter(user = request.user).order_by("-createdAt")
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
        car = self.get_car_note(id, request.user.id)

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
        car = self.get_car_note(id, request.user.id)

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


    def get(self, request):
        """
        Get all car notes of all users.
        """

        # Filtering based on query parameters
        filters = request.query_params

        all_cars_of_all_users = Car.objects.all().order_by("-createdAt")
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

