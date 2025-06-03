from django import forms

# Models
from .models import Article
from ckeditor.widgets import CKEditorWidget


class ArticleCreateForm(forms.ModelForm):
    annotation = forms.CharField(widget=CKEditorWidget())
    annotation_kk = forms.CharField(widget=CKEditorWidget())
    annotation_ru = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ["category", "file", "title", "title_kk", "title_ru", "annotation", "annotation_kk", "annotation_ru",
                  "authors"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_text_input_attrs = {
            'class': 'form-control',
            'required': 'required',
        }
        self.fields['category'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите категорию статьи'})
        self.fields['title'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите название статьи'})
        self.fields['title_kk'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите название статьи'})
        self.fields['title_ru'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите название статьи'})
        self.fields['authors'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Авторы статьи'})
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'required': 'required'})


class ArticleUpdateForm(forms.ModelForm):
    annotation = forms.CharField(widget=CKEditorWidget())
    annotation_kk = forms.CharField(widget=CKEditorWidget())
    annotation_ru = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ["category", "title", "title_kk", "title_ru", "annotation", "annotation_kk", "annotation_ru", "authors"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_text_input_attrs = {
            'class': 'form-control',
            'required': 'required',
        }
        self.fields['category'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите категорию статьи'})
        self.fields['title'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите название статьи'})
        self.fields['title_kk'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите название статьи'})
        self.fields['title_ru'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Введите название статьи'})
        self.fields['authors'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Авторы статьи'})
