from django.urls import path
from .views  import CarListCreateApiView, CarDetailApiView, CarListCreateApiViewAdminPriviledge, CarDetailApiViewAdminPriviledge
# from .views_copy  import CarListCreateApiView, CarDetailApiView, CarListCreateApiViewAdminPriviledge, CarDetailApiViewAdminPriviledge



urlpatterns = [
    path('', CarListCreateApiView.as_view()),
    path('admin/', CarListCreateApiViewAdminPriviledge.as_view()),
    path('<int:id>/', CarDetailApiView.as_view()),
    path('admin/<int:id>/', CarDetailApiViewAdminPriviledge.as_view()),
]
