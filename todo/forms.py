from django.forms import ModelForm
from .models import Todo

class TodoForms(ModelForm):
    class Meta:
        model = Todo
        fields=['title','memo','important']