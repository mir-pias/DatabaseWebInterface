from django import forms
from django.core.exceptions import ValidationError
import django.core.validators as val
from django.utils.translation import gettext_lazy as _
import re


class InputForm(forms.Form):

    def galois_validation(value):
        if ',' in value:
            input_list = value.split(',')
            if len(input_list) != 2:
                raise ValidationError(
                _('enter two numbers seperated by comma, T or t'),
                params={'value': value},)
        elif 'T' in value:
            input_list = value.split('T')
            if len(input_list) != 2:
                raise ValidationError(
                _('enter two numbers seperated by comma, T or t'),
                params={'value': value},)
        elif 't' in value:
            input_list = value.split('T')
            if len(input_list) != 2:
                raise ValidationError(
                _('enter two numbers seperated by comma, T or t'),
                params={'value': value},)

        
    
    def disc_validation(value):
        if ',' in value:
            input_list = value.split(',')
            if len(input_list) != 2:
                raise ValidationError(
                _('enter maximum two numbers seperated by comma'),
                params={'value': value},
        )

    def sig_validation(value):
        input_list = value.split(',')
        if len(input_list) != 2:
            raise ValidationError(
            _('enter two numbers seperated by comma'),
            params={'value': value},
        )

    degree = forms.CharField(help_text='e.g. 2', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter whole number(s)', code='invalid', allow_negative=False), disc_validation], localize=True)
    
    discriminant = forms.CharField(help_text='e.g. -1000,-1 ', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter whole number(s)', code='invalid', allow_negative=True), disc_validation])
    
    cm = forms.CharField(help_text='e.g. t or f', required=False, 
        validators=[val.RegexValidator(regex=re.compile('t|f|T|F'), message='enter t or f', code = 'invalid')])
    
    signature = forms.CharField(help_text='e.g. 1,1 ', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter positive whole numbers', code='invalid', allow_negative=False), sig_validation])
    
    galois_group = forms.CharField(help_text=' e.g. 2T1 or 2,1', required=False, 
        validators=[val.int_list_validator(sep=',' or 't' or 'T', message='enter whole numbers', code='invalid', allow_negative=False), 
        val.RegexValidator(regex=re.compile('[,|t|T]'), message='enter two numbers seperated by comma, T or t', code = 'invalid'), galois_validation] )
   
    class_group = forms.CharField(help_text='id = 1 or structure = 2,4 ...', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter whole number(s)', code='invalid', allow_negative=False)])

    
    
    def clean(self):
        self.cleaned_data = super().clean()
        degree = self.cleaned_data.get("degree")
        signature = self.cleaned_data.get("signature")

        if degree and signature:
            # Only do something if both fields are valid so far.
            sig = signature.split(',')
            if degree != sig[0] + 2*sig[1]:
                raise forms.ValidationError(
                    "degree and signature do not match (degree = r+2s)"
                )