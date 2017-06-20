from django import forms
from django.forms import ModelForm, Select, TextInput, EmailInput, ChoiceField, CharField, EmailInput,RadioSelect, ModelMultipleChoiceField, SelectMultiple
from .models import *

class FormUser(ModelForm):
   
    class Meta:
        model = User
        fields = ['name']
        widgets = {
           'name': Select(attrs={'class':'dropdown'}) 
        }    
    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args,**kwargs)
        self.fields['name'] = forms.ModelChoiceField(required=True, queryset=User.objects.all(), widget=forms.Select())
          
