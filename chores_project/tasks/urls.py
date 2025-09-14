from django.urls import path
from .views import (
    TaskCategoryListView,
    TaskCategoryDetailView,
    TaskCategoryCreateView,
    TaskCategoryUpdateView,
    TaskCategoryDeleteView,
)

urlpatterns = [
    path("tasks/", TaskCategoryListView.as_view(), name="category_list"),
    path("tasks/", TaskCategoryDetailView.as_view(), name="category_detail"),
    path("tasks/", TaskCategoryCreateView.as_view(), name="category_create"),
    path("tasks/", TaskCategoryUpdateView.as_view(), name="category_update"),
    path("tasks/", TaskCategoryDeleteView.as_view(), name="category_delete"),
]