from django import forms
# from .models import KhabarName
# from captcha.fields import CaptchaField

# class khabarnameForm(forms.ModelForm):
#     class Meta:
#         model = KhabarName
#         fields = "__all__"

# class ContactUsForm(forms.Form):
#     name = forms.CharField(max_length=300)
#     email = forms.EmailField(max_length=254)
#     subject = forms.CharField(max_length=300)
#     message = forms.CharField(widget=forms.Textarea())
#     captcha =CaptchaField()

class SearchForm(forms.Form):
    mag = forms.CharField(max_length=300)
    
class CommentForm(forms.Form):
    name= forms.CharField(max_length=200)
    Email_address = forms.EmailField(max_length=254)
    massage = forms.CharField(widget=forms.Textarea())
    
class CommentFormReplay(forms.Form):
    name= forms.CharField(max_length=200)
    Email_address = forms.EmailField(max_length=254)
    massage = forms.CharField()