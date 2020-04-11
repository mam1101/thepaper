from django import forms
from django.contrib.auth.models import User

from paper.models import PaperItem


class PaperItemForm(forms.ModelForm):
    published = forms.BooleanField(required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = PaperItem
        fields = (
            'body',
            'published',
            'owner',
        )