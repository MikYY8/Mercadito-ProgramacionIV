from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(
        label='',
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Escribí tu mensaje...',
            'class': 'form-control'
        })
    )
    photo = forms.ImageField(required=False)
    audio = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': 'audio/*'})
    )