'''
Created on Sep 28, 2013

@author: anujacharya
'''
from django import forms

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()