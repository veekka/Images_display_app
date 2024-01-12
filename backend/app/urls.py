from .views import *
from django.urls import path

urlpatterns = [
    path('upload_images/', upload_images, name="add_image"),
    path('<int:pk>/update/', UpdateImage.as_view(), name='image_edit'),
    path('<int:pk>/delete/', DeleteImage.as_view(), name='image_delete'),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name="register"),
    path('password_change/', UserPasswordChange.as_view(), name='password_change'),
    path('', ImagesApp.as_view(), name='home'),
]