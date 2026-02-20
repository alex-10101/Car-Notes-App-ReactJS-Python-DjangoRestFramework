from django.urls import path
# from .views_generic_class_based_views  import CarListCreateApiView, CarDetailApiView, CarListCreateApiViewAdminPriviledge, CarDetailApiViewAdminPriviledge, ProductFilterOptionsView
from .views_api_class_based_views  import CarListCreateApiView, CarDetailApiView, CarListCreateApiViewAdminPriviledge, CarDetailApiViewAdminPriviledge, ProductFilterOptionsView



urlpatterns = [
    path('', CarListCreateApiView.as_view(), name="car_list_create"),
    path("filters/", ProductFilterOptionsView.as_view(), name="prpduct_filters"),
    path('admin/', CarListCreateApiViewAdminPriviledge.as_view(), name="car_list_create_admin"),
    path('<int:id>/', CarDetailApiView.as_view(), name="car_detail"),
    path('admin/<int:id>/', CarDetailApiViewAdminPriviledge.as_view(), name="car_detail_admin"),
]
