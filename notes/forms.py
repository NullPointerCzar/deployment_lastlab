from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'name': 'description', 'rows': 4}),
        }
