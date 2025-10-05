from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import UserPreferences
from .forms import UserPreferencesForm


class UserPreferencesUpdateView(LoginRequiredMixin, UpdateView):
    model = UserPreferences
    form_class = UserPreferencesForm
    template_name = "preferences/preferences_form.html"
    success_url = reverse_lazy("preferences_view")

    def get_object(self, queryset=None):
        # Отримуємо або створюємо об’єкт налаштувань для поточного користувача
        obj, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return obj