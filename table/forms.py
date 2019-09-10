from django import forms
from .models import Post


class CreateField(forms.ModelForm):
    date = forms.CharField(max_length=255,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control datepicker-here', 'data-multiple-dates': '100',
                                      'aria-label': 'Todo', 'data-multiple-dates-separator': ', ',
                                      'data-position': 'top left'}))

    class Meta:
        model = Post
        fields = ['choice', 'text', 'date']