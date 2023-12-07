from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
    code = "russian"

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255,
                            min_length=5,
                            label="Заголовок",
                            widget=forms.TextInput(attrs={"class": "form-input"}),
                            validators=[
                                RussianValidator(),
                            ],
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка никак'
                            })

    slug = forms.SlugField(max_length=255,
                           label="URL",
                           validators=[
                               MinLengthValidator(5, message="Min 5 symbols"),
                               MaxLengthValidator(100),
                           ],
                           )

    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), required=False, label="Контент")
    is_published = forms.BooleanField(label="Статус", initial=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Не выбрано")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label="Муж")

    def clean_content(self):
        title = self.cleaned_data["content"]
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел")
