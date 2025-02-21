from django.urls import path
from users import views

app_name = "user"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("users_cart", views.UserCartView.as_view(), name="users_cart"),
]


