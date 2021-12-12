from django import forms
from .models import Conversation


# class ChatUploadForm(forms.Form):
    # chat = forms.FileField()

class ChatUploadForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ["name", "chat"]


