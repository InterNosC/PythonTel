from django import forms

from .models import Profile
from .models import Message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {
            'external_id',
            'name',
        }
        widgets = {
            'name': forms.TextInput,
        }
