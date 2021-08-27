from django.db.models.base import Model
from django.forms import fields
from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    number = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)