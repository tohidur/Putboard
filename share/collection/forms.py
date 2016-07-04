from django import forms
from .models import Collection, Link


class CollectionForm(forms.ModelForm):
    privacy = forms.BooleanField(label='Make it public', required=False)

    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "privacy",
        ]


class LinkForm(forms.ModelForm):
    link = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 1}))
    class Meta:
        model = Link
        fields = [
            "title",
            "link",
            "tags",
        ]