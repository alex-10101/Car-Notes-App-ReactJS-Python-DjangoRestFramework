from django.urls import path
# from .views  import CarListCreateApiView, CarDetailApiView, CarListCreateApiViewAdminPriviledge, CarDetailApiViewAdminPriviledge
from .views_copy  import CarListCreateApiView, CarDetailApiView, CarListCreateApiViewAdminPriviledge, CarDetailApiViewAdminPriviledge



urlpatterns = [
    path('', CarListCreateApiView.as_view(), name="car_list_create"),
    path('admin/', CarListCreateApiViewAdminPriviledge.as_view(), name="car_list_create_admin"),
    path('<int:id>/', CarDetailApiView.as_view(), name="car_detail"),
    path('admin/<int:id>/', CarDetailApiViewAdminPriviledge.as_view(), name="car_detail_admin"),
]
