from django import forms 
from django.core.exceptions import ValidationError


class InfoForm(forms.Form):
    city = forms.CharField(max_length=100,required=False)
    province = forms.CharField(max_length=200,required=False)
    address = forms.CharField(widget=forms.Textarea,required=False)
    code_posty = forms.IntegerField(required=False)
    receiver_name= forms.CharField(max_length=250,required=False)
    code_meli = forms.IntegerField(required=False)

class PhoneNumber(forms.Form):
    phone = forms.CharField()


    def clean(self):
        cleaned_data = super().clean()
        phone = str(cleaned_data.get('phone'))
        print(phone)
        if len(phone) != 11:
            raise ValidationError('11 nist')
        if phone[0] != '0' and phone[1] != '9':
            raise ValidationError('09 nist')