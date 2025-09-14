from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.shortcuts import redirect
from django.utils import timezone
from .models import TaskCategory
from .forms import TaskCategoryForm

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from .mixins import TaskOwnerMixin

# Create your views here.
def task_complete(rewquest, pk):
    task = Task.objects.get(pk=pk)
    task.status ="completed"
    task.completed_At = timezone.now()
    task.save()
    return redirect("tasks:task_list")

class TaskCategoryListView(ListView):
    model = TaskCategory
    template_name = "tasks/category_list.html"
    context_object_name = "categories"

class TaskCategoryDetailView(DetailView):
    model = TaskCategory
    template_name = "tasks/category_detail.html"
    context_object_name = "category"

class TaskCategoryCreateView(CreateView):
    model = TaskCategory
    form_class = TaskCategoryForm
    template_name = "tasks/category_create.html"
    success_url = reverse_lazy("category_list")

class TaskCategoryUpdateView(UpdateView):
    model = TaskCategory
    form_class = TaskCategoryForm
    template_name = "tasks/category_update.html"
    success_url = reverse_lazy("category_list")

class TaskCategoryDeleteView(DeleteView):
    model = TaskCategory
    template_name = "tasks/category_delete.html"
    success_url = reverse_lazy("category_list")
