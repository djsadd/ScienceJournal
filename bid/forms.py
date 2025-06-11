from django import forms
from .models import Bid, BidStatus, Review
from ckeditor.widgets import CKEditorWidget


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["ai_usage_details", "exclusive_submission", "no_plagiarism", "authors_confirmed", "manuscript",
                  "authors_file", "cover_letter"]
        labels = {
            "ai_usage_details": "Сведения о применении генеративного ИИ",
            "exclusive_submission": "Статья ранее не публиковалась и не рассматривается другим журналом",
            "no_plagiarism": "В статье отсутствует плагиат",
            "authors_confirmed": "Все авторы подтверждают согласие с поданной версией",
            "manuscript": "Рукопись (*.doc, *.docx)",
            "authors_file": "Файл со сведениями об авторах (*.doc, *.docx)",
            "cover_letter": "Сопроводительное письмо (*.pdf)",
        }
        widgets = {
            "ai_usage_details": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "exclusive_submission": forms.CheckboxInput(),
            "no_plagiarism": forms.CheckboxInput(),
            "authors_confirmed": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True


class CommentBid(forms.Form):
    comment = forms.CharField(
        widget=CKEditorWidget(attrs={
            'placeholder': 'Введите комментарий',
            'class': 'form-control',
            'rows': 5,
            'cols': 40
        }),
        label='Комментарий',
    )


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            "plagiarism",
            "novelty",
            "originality",
            "innovation",
            "significance",
            "structuredness",
            "literary_level",
            "design_quality",
            "conclusion",
        ]

        labels = {
            "plagiarism": "Важность, полезность и/или применимость идей, методов, технологий",
            "novelty": "Новое освещение, применение в той или иной отрасли",
            "originality": "Идеи, методы, способы, решения и результаты поставленных задач исследования ранее не были известны или апробированы",
            "innovation": "Новый процесс, услуга, продукт, основанные на новых, неизвестных технологиях, методах или методологиях, определение новых для потребителей услуг",
            "significance": "Изложение результатов, теоретическая и практическая значимость, выводы, научно-практическое значение",
            "structuredness": "Логичность, последовательность, связность изложения",
            "literary_level": "Коммуникативная ценность, соответствие научному стилю, языковым и стилистическим нормам",
            "design_quality": "Соответствие требованиям редакции, использование терминологической лексики. Наличие аннотаций, пристатейного аппарата, ключевых слов, соблюдение определенных параметров страницы, библиографического списка",
            "conclusion": "",
        }