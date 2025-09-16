from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'thoughts']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional - leave empty to remain anonymous)',
                'maxlength': '100'
            }),
            'thoughts': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please share your thoughts about the checkout process...',
                'rows': 4,
                'maxlength': '1000'
            })
        }
        labels = {
            'name': 'Name (Optional)',
            'thoughts': 'Your Thoughts'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thoughts'].required = True
        self.fields['name'].required = False
