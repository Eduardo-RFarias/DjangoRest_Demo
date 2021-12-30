from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers

from .views import LoginView, UserView

router = routers.DefaultRouter()
router.register(r"user", UserView)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"login/", LoginView.as_view(), name="knox_login"),
    path(r"logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path(r"logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]
