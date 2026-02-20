from rest_framework import permissions
from .models import Car
from .serializers import GetCarSerializer, CreateUpdateCarSerializer, GetProductFilterOptionsSerializer
from rest_framework import generics
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

class CarNotesPagination(PageNumberPagination):
    page_query_param = "page"

    # Default number of items returned per page
    # Example: GET /items/  -> returns 9 items
    page_size = 9

    # Name of the query parameter that allows the client
    # to override `page_size` dynamically.
    # Example: GET /items/?page_size=5
    page_size_query_param = "page_size"

    # Maximum number of items the client is allowed to request per page,
    # even if a larger `page_size` is provided in the query params.
    # This prevents clients from requesting too much data at once.
    max_page_size = 20


    def paginate_queryset(self, queryset, request, view=None):
        """
        Implements the SAME behavior as the manual Django Paginator approach:
        - If the page is missing / not an int -->  return data at page 1
        - If the page is out of range --> return data at the last page
        - If there are 0 pages (empty queryset) --> return data at page 1 (returns empty qeryset)
        """
        # store request so get_paginated_response / links can use it if needed
        self.request = request
        
        # Determine the page size that was actually used.
        # If the client passed ?page_size=... use that,
        # otherwise fall back to the default page_size.
        page_size = self.get_page_size(request) or self.page_size

        # Use Django's Paginator directly (same as your manual code)
        paginator = Paginator(object_list=queryset, per_page=page_size)
        
        # store it, so that it can be used in the get_paginated_response method
        self._paginator = paginator  

        page_param = request.query_params.get(self.page_query_param)

        try:
            # Attempt to return the requested page.
            # If page="2", this returns the 2nd chunk of 9 items.
            self.page = paginator.page(page_param)
        except PageNotAnInteger:
            # If 'page' is not an integer (e.g. "abc" or None),
            # fall back to the first page.               
            page_param = 1
            self.page = paginator.page(page_param)
        except EmptyPage:
            # if there are no pages at all, fallback to page 1
            if paginator.num_pages == 0:
                self.page = paginator.page(1)
            else:
                # If the requested page number is larger than the total number of pages
                # (e.g. page=10 but only 3 pages exist),
                # return the *last valid page* instead.        
                self.page = paginator.page(paginator.num_pages)
        # except EmptyPage:
        #     # If the requested page number is larger than the total number of pages
        #     # (e.g. page=10 but only 3 pages exist),
        #     # return the *last valid page* instead.      
        #     # If there are no items in the dataset (no pages), 
        #     # this will still return an empty page without returning an error,
        #     # because  Django’s Paginator has allow_empty_first_page=True by default.    
        #     self.page = paginator.page(paginator.num_pages)


        # Normalize the page number that will be returned to the client.
        # If the client did not provide a page parameter, we are effectively on page 1.
        # if page_param is None:
        #     page_param = 1
        # page_param = int(page_param)


        # DRF expects a list/iterable of objects for the serializer
        # return list(self.page)
        return self.page.object_list

    def get_paginated_response(self, data):
        paginator = getattr(self, "_paginator", None)

        # this does not fix the problem
        # If something went wrong, still return a safe structure
        # if paginator is None:
        #     return Response(
        #         {"count": 0, "pages": 1, "data": [], "page": 1, "page_size": self.page_size}
        #     )

        return Response({
            # Total number of filtered objects in the database.
            # Useful for UI summaries like: "57 results found".
            "count": paginator.count,

            # Total number of pages.
            # "pages": paginator.num_pages if paginator.num_pages > 0 else 1,  
            "pages": paginator.num_pages,  
            
            # The actual serialized objects for the current page.
            "data": data,

            # Current page number. Useful for displaying: "Page 2 of 6".
            # "page": self.page.number if getattr(self, "page", None) else 1,
            "page": self.page.number,

            # Page size actually used.
            "page_size": paginator.per_page,
        })

class CarListCreateApiView(generics.ListCreateAPIView):
    """
    View for listing the car notes of the current user or for creating a new car note.
    """
    permission_classes=[permissions.IsAuthenticated]
    pagination_class = CarNotesPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCarSerializer
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
                --> matches cars whose brand is Volkswagen OR Hyundai OR Aston Martin.
        - motor: one or more motor types separated by "-" (OR logic within motor).
                Example: "Diesel-Electric"
                --> matches cars whose motor is Diesel OR Electric.

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
            return GetCarSerializer
        return  CreateUpdateCarSerializer
    
    def get_queryset(self):
        return Car.objects.filter(user=self.request.user)    

    lookup_field="id"


class CarListCreateApiViewAdminPriviledge(generics.ListAPIView):
    """
    View for listing all the notes in the database.
    """

    permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class=GetCarSerializer
    
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




class ProductFilterOptionsView(APIView):
    """
    Class Based View for retrieving all distinct product brands and categories.
    """
    permission_classes = [permissions.IsAuthenticated]

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