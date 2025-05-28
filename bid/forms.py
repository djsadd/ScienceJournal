from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["ai_usage_details", "exclusive_submission", "no_plagiarism", "authors_confirmed", "manuscript", "authors_file", "cover_letter"]
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
        # Устанавливаем required=True для всех полей
        for field_name, field in self.fields.items():
            field.required = True