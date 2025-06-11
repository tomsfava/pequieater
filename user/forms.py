from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Nome de usuário",
            "email": "E-mail",
            "password1": "Senha",
            "password2": "Confirme a senha",
        }
        help_texts = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        error_messages = {
            "username": {
                "unique": "Este nome de usuário já está em uso.",
                "required": "O nome de usuário é obrigatório.",
            },
            "email": {
                "invalid": "Informe um e-mail válido.",
                "required": "O e-mail é obrigatório.",
            },
            "password2": {
                "password_mismatch": "As senhas não coincidem.",
            },
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio']
        labels = {
            "username": "Nome de usuário",
            "email": "E-mail",
            "bio": "Biografia"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Conte um pouco sobre você..."
            }),
        }