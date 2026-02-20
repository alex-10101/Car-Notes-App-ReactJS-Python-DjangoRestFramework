import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Car
from .serializers import GetCarSerializer, CreateUpdateCarSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# # NOT USED ANYMORE. 
# # THIS THROWS AN INVALID PAGE ERROR, IF A REQUEST
# # IS MADE WITH A PAGE PARAM GREATER THAN THE TOTLA NUMBER OF PAGES.
# # A VERSION OF THIS CLASS WHICH SOLVES THIS ISSUE CAN BE FOUND IN 
# views_generic_class_based_views.py.
# # --> IN THIS FILE ANOTHER APPROACH IS USED.
# class CarsPagination(PageNumberPagination):

#     # Default number of items returned per page
#     # Example: GET /items/  -> returns 9 items
#     page_size = 9

#     # Name of the query parameter that allows the client
#     # to override `page_size` dynamically.
#     # Example: GET /items/?page_size=5
#     page_size_query_param = "page_size"

#     # Maximum number of items the client is allowed to request per page,
#     # even if a larger `page_size` is provided in the query params.
#     # This prevents clients from requesting too much data at once.
#     max_page_size = 20


#     def get_paginated_response(self, data):
#         # Determine the page size that was actually used.
#         # If the client passed ?page_size=...  use that,
#         # otherwise fall back to the default page_size.
#         page_size = self.get_page_size(self.request) or self.page_size

#         # Total number of records AFTER filtering (before pagination).
#         # Example: 57 total items matching filters.
#         count = self.page.paginator.count

#         # Compute total number of pages.
#         # Needed by frontend to render pagination buttons.
#         # Example: 57 items, page_size=10 --> 57/10=5.7 --> rounds up to 6 pages.
#         pages = math.ceil(count / page_size) if page_size else 1

#         return Response({
#             # Total number of filtered objects in the database.
#             # Useful for UI summaries like: "57 results found".
#             "count": count,

#             # Total number of pages.
#             "pages": pages,

#             # Absolute URL of the next or previous page (or None).
#             # DRF automatically generates it.
#             # Useful if you ever switch to "Next/Previous" only.
#             "next": self.get_next_link(),
#             "previous": self.get_previous_link(),

#             # The actual serialized objects for the current page.
#             "data": data,

#             # Current page number. Useful for displaying: "Page 2 of 6".
#             "page": self.page.number,

#             # Page size actually used.
#             "page_size": page_size,
#         })


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

        # Filter cars belonging only to the request user
        # If brand_queries or motor_queries are empty, these queries are ignored. 
        # For example, if both brand_queries and motor_queries are empty, 
        # the query returns all cars of the request user.
        filters = Q(user=self.request.user) & brand_queries & motor_queries

        filtered_cars = Car.objects.filter(filters).order_by('-createdAt') # AND queries

        # serializer = GetCarSerializer(filtered_cars, many=True, context={"request": request})
        #
        # return Response(serializer.data, status=status.HTTP_200_OK)

        # PAGINATION

        # Read the requested page number from the query parameters (?page=2, ?page=5, etc.)
        # If the client does not send a page parameter, this will be None.        
        page = request.query_params.get("page")

        page_size = 9  # page size = 9 items per page

        # Create a paginator over the *already filtered* queryset.
        # This splits the queryset into chunks ("pages") of 9 items each (9 items per page, because page_size=9):
        #       page 1 -> items[0:8]
        #       page 2 -> items[9:17]
        #       page 3 -> items[18:26]
        #               ...
        paginator = Paginator(object_list=filtered_cars, per_page=page_size) 

        try:
            # Attempt to return the requested page.
            # If page="2", this returns the 2nd chunk of 9 items.
            cars_page = paginator.page(page)
        except PageNotAnInteger:
            # If 'page' is not an integer (e.g. "abc" or None),
            # fall back to the first page.            
            cars_page = paginator.page(1)
        except EmptyPage:
            # If the requested page number is larger than the total number of pages
            # (e.g. page=10 but only 3 pages exist),
            # return the *last valid page* instead.    
            # If there are no items in the dataset (no pages), 
            # this will still return an empty page without returning an error,
            # because  Django’s Paginator has allow_empty_first_page=True by default.    
            cars_page = paginator.page(paginator.num_pages)

        # Normalize the page number that will be returned to the client.
        # If the client did not provide a page parameter, we are effectively on page 1.
        # if page is None:
        #     page = 1
        # page = int(page)

        # serializer = GetCarSerializer(cars_page, many=True, context={"request": request})
        serializer = GetCarSerializer(cars_page.object_list, many=True, context={"request": request})

        return Response({
            # Total number of filtered objects in the database.
            # Useful for UI summaries like: "57 results found".
            "count": paginator.count,

            # Total number of pages.
            "pages": paginator.num_pages,

            # The actual serialized objects for the current page.
            "data": serializer.data,

            # Current page number. Useful for displaying: "Page 2 of 6".
            "page": cars_page.number,

            # Page size actually used.
            "page_size": paginator.per_page,
        })

    def post(self, request):
        """
        Create a new car note
        """
        serializer = CreateUpdateCarSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


class CarDetailApiView(APIView):
    """
    View for retrieving, updating or deleting a particular car note of the current user.
    """

    permission_classes=[permissions.IsAuthenticated]

    # def __get_car_note(self, carId, userId):
    #     """
    #     Private method to get the car note with given car id and user id
    #     """
    #     try:
    #         return Car.objects.get(id=carId, user__id = userId)
    #     except Car.DoesNotExist:
    #         return None

    def __get_car_note(self, carId, requestUser):
        """
        Private method to get the car note with given car id and user id
        """
        try:
            return Car.objects.get(id=carId, user = requestUser)
        except Car.DoesNotExist:
            return None


    def get(self, request, id):
        """
        Get the car note with the given car id and user id.
        The id is a request parameter.
        """
        # car = self.__get_car_note(carId=id, userId=request.user.id)
        car = self.__get_car_note(carId=id, requestUser=request.user)


        if car is None:
            return Response(
                {"detail": "Car note with the given car id and user id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GetCarSerializer(car, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
 
    
    def put(self, request, id):
        """
        Update the car note with the given car id and user id.
        The id is a request parameter.
        """

        # car = self.__get_car_note(carId=id, userId=request.user.id)
        car = self.__get_car_note(carId=id, requestUser=request.user)

        if car is None:
            return Response(
                {"detail": "Car note with the given car id and user id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        # serializer = CarSerializer(instance=car, data=data, partial=True)
        serializer = CreateUpdateCarSerializer(instance=car, data=request.data, context={"request": request})

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
        # car = self.__get_car_note(carId=id, userId=request.user.id)
        car = self.__get_car_note(carId=id, requestUser=request.user)

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
        serializer = GetCarSerializer(filtered_cars, many=True)
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

class ProductFilterOptionsView(APIView):
    """
    Class Based View for retrieving all distinct product brands and categories.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Retrieve all distinct car brands and motors when the user makes a GET request to this endpoint.    
        """
        brands = (
            Car.objects
            .values_list("brand", flat=True)
            .distinct()
            .order_by("brand")
        )

        categories = (
            Car.objects
            .values_list("motor", flat=True)
            .distinct()
            .order_by("motor")
        )

        return Response({
            "brands": list(brands),
            "motors": list(categories),
        }, status=status.HTTP_200_OK)