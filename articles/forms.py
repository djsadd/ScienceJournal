from django import forms
from django.utils.translation import gettext_lazy as _

# Models
from .models import Article, Tag
from ckeditor.widgets import CKEditorWidget


class ArticleCreateForm(forms.ModelForm):
    annotation_en = forms.CharField(widget=CKEditorWidget())
    annotation_kk = forms.CharField(widget=CKEditorWidget())
    annotation_ru = forms.CharField(widget=CKEditorWidget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    new_tags = forms.CharField(
        required=False,
        label=_('Добавить ключевые слова'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Новые ключевые слова через запятую'),
        })
    )

    class Meta:
        model = Article
        fields = [
            "category",
            "tags",
            "new_tags",
            "file",
            "plagiarism",
            "title_en",
            "title_kk",
            "title_ru",
            "annotation_en",
            "annotation_kk",
            "annotation_ru",
            "authors_en",
            "authors_kk",
            "authors_ru"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_text_input_attrs = {
            'class': 'form-control',
            'required': 'required',
        }
        self.fields['category'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Название кафедры или раздела'})
        self.fields['title_en'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Заголовок на английском'})
        self.fields['title_kk'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Заголовок на казахском'})
        self.fields['title_ru'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Заголовок на русском'})
        self.fields['authors_en'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Авторы на английском'})
        self.fields['authors_kk'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Авторы на казахском'})
        self.fields['authors_ru'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Авторы на русском'})
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['plagiarism'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['new_tags'].widget.attrs.update({'list': 'tagList'})

    def save(self, commit=True):
        article = super().save(commit=False)
        if commit:
            article.save()
            self.save_m2m()
            new_tags = self.cleaned_data.get('new_tags')
            if new_tags:
                names = [name.strip() for name in new_tags.split(',') if name.strip()]
                for name in names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    article.tags.add(tag)
        return article

    def attach_new_tags(self, article):
        new_tags = self.cleaned_data.get('new_tags')
        if not new_tags:
            return
        names = [name.strip() for name in new_tags.split(',') if name.strip()]
        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            article.tags.add(tag)

class ArticleUpdateForm(forms.ModelForm):
    annotation = forms.CharField(widget=CKEditorWidget())
    annotation_kk = forms.CharField(widget=CKEditorWidget())
    annotation_ru = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = [
            "category",
            "title",
            "title_kk",
            "title_ru",
            "annotation",
            "annotation_kk",
            "annotation_ru",
            "authors",
            "authors_en",
            "authors_kk",
            "authors_ru",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_text_input_attrs = {
            'class': 'form-control',
            'required': 'required',
        }
        self.fields['category'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Название кафедры или раздела'})
        self.fields['title'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Заголовок'})
        self.fields['title_kk'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Заголовок на казахском'})
        self.fields['title_ru'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Заголовок на русском'})
        self.fields['authors'].widget.attrs.update({**common_text_input_attrs, 'placeholder': 'Авторы'})
        self.fields['authors_en'].widget.attrs.update({**common_text_input_attrs, 'placeholder': '������ �� ����������'})
        self.fields['authors_kk'].widget.attrs.update({**common_text_input_attrs, 'placeholder': '������ �� ���������'})
        self.fields['authors_ru'].widget.attrs.update({**common_text_input_attrs, 'placeholder': '������ �� �������'})
