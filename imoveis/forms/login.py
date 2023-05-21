from django import forms


class FormLogin(forms.Form):
    usuario = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'usuário',
            }
        ),
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'senha',
            }
        )
    )
