from django import forms

class CreateGroup(forms.Form):
    groupName = forms.CharField(max_length=120)
    groupFile = forms.FileField(required=False)
