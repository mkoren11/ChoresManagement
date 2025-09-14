from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class TaskOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Дозволяє доступ тільки власнику завдання
    """
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user 
        

