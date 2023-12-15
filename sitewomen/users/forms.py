from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-input'})
                               )
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'})
                               )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль")
    repeated_password = forms.CharField(label="Повторите пароль")

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "password", "repeated_password"]
        labels = {
            "email": "Почтовый ящик",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def clean_repeated_password(self):
        cd = self.cleaned_data
        if cd["password"] != cd["repeated_password"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd["password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется!")

        return email
