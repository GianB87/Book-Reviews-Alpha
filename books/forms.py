from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'authors', 'rate', 'image_link',
        'youtube_link','review', 'summary']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
 
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


