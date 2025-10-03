from django import forms
from .models import Petition, Vote

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'movie_title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title for your petition'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe why this movie should be added to our catalog...'
            }),
            'movie_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the movie title'
            })
        }
        labels = {
            'title': 'Petition Title',
            'description': 'Description',
            'movie_title': 'Movie Title'
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote_type']
        widgets = {
            'vote_type': forms.RadioSelect(choices=Vote.VOTE_CHOICES)
        }
        labels = {
            'vote_type': 'Your Vote'
        }
