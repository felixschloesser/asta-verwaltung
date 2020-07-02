from django.urls import path

from . import views


app_name = 'keys' # Namespace: keys:detail, keys:results

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # ex: /keys/
]
