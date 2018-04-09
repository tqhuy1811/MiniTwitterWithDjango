
from django import forms

class SignUpForm(forms.Form):
  username = forms.CharField(min_length=5,max_length=100)
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput())


class ArticleForm(forms.Form):
  title = forms.CharField(min_length=10)
  content = forms.CharField(widget=forms.Textarea())

class ProfileForm(forms.Form):
  birthday = forms.DateField()
  profilePicture = forms.FileField()
  bio = forms.CharField(widget=forms.Textarea())
  

class CommentForm(forms.Form):
  body = forms.CharField(widget=forms.Textarea())
