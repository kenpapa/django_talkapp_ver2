from django import forms
from django.contrib.auth.models import User
from .models import Post

class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

class PostForm(forms.ModelForm):
    message = forms.CharField(required=True)

    class Meta:
        model = Post
        fields = ['message']
