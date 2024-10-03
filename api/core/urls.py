from django.urls import path

from . import views

urlpatterns = [
    path("test",views.test.view1,name="Index")
]