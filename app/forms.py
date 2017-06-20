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

class FormMovie(forms.Form):
    users = forms.CharField(label='Usuário', max_length=100, widget=forms.Select(attrs={'id':'users_id', 'class':'aa', 'onchange':'get_whatched_movies()'}))
    movies = forms.CharField(label='Usuário', max_length=100)

    def __init__(self, *args, **kwargs):
        super(FormMovie, self).__init__(*args,**kwargs)
        self.fields['users'] = forms.ModelChoiceField(required=True, queryset=User.objects.all(), widget=forms.Select())
        self.fields['movies'] = forms.ModelChoiceField(required=True, queryset=Movie.objects.all(), widget=forms.Select())
        self.fields['users'].widget.attrs['onchange'] = 'get_whatched_movies()'
        self.fields['users'].widget.attrs['id'] = 'users_id'
        self.fields['movies'].widget.attrs['id'] = 'movies_id'
        self.fields['movies'].widget.attrs['disabled'] = 'disabled'