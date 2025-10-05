from django import forms
from .models import UserPreferences

class UserPreferencesForm(Modelform):

    class Meta:
        model = UserPreferences
        fields = ["liked_categories",
               "disliked_categories",
                "availability",
                "experience_levels",
                "physical_limitations"]
        
        widgets = {}

    

liked_categories: список із чекбоксів (CheckboxSelectMultiple)

disliked_categories: список із чекбоксів (CheckboxSelectMultiple)

availability: багаторядкове текстове поле (textarea) з CSS-класом "form-control"
+ підказка (help_text) = "Введіть у форматі JSON. Напр.: {'monday': ['09:00-12:00']}"

experience_levels: багаторядкове текстове поле (textarea) з CSS-класом "form-control"
help_text = "Введіть у форматі JSON. Напр.: {'cooking': 3}"

physical_limitations: багаторядкове поле (textarea) з CSS-класом "form-control"