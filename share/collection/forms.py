from django import forms
from .models import Collection, Link


class CollectionForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Board Name'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-input',
     'placeholder': 'Small Descriptiono (Optional)', 'rows': 2, 'cols': 100}), required=False)
    privacy = forms.BooleanField(label='Make it a private board.', required=False)
    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "privacy",
        ]


class LinkForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title (Optional)'}))
    link = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'http://'}), required=True)
    class Meta:
        model = Link
        fields = [
            "title",
            "link",
            "tags",
        ]