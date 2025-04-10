from django import forms

# Models
from .models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["file", "title", "annotation", "authors"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'id': 'title',
            'placeholder': 'Введите название статьи',
            'class': 'form-control',
            'required': 'required'
        })

        self.fields['annotation'].widget.attrs.update({
            'id': 'annotation',
            'placeholder': 'Введите аннотацию',
            'class': 'form-control',
            'required': 'required'
        })

        self.fields['authors'].widget.attrs.update({
            'id': 'title',
            'placeholder': 'Введите название статьи',
            'class': 'form-control',
            'required': 'required'
        })
        self.fields['file'].widget.attrs.update({
            'id': 'file',
            'class': 'form-control',
            'required': 'required'
        })
