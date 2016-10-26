from django.conf.urls import url, include
from rest_framework import routers

from ovp_nonprofits import views


router = routers.DefaultRouter()
router.register(r'nonprofits', views.NonprofitResourceViewSet, 'public-profile')

urlpatterns = [
  url(r'^', include(router.urls)),
]
