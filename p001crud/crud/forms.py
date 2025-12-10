from django import forms
from .models import task

class TaskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ["title", "description"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-800 text-white rounded-lg',
                'placeholder': 'Título de la tarea',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 bg-gray-800 text-white rounded-lg',
                'placeholder': 'Descripción',
                'rows': 3,
            }),
        }
