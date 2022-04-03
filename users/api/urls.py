from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('my-invites', views.api_invites, name="api-invites"),
    path('', views.api_overview, name='api-overview')
]