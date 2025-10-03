from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Petition, Vote
from .forms import PetitionForm, VoteForm

def petition_list(request):
    """Display all active petitions"""
    petitions = Petition.objects.filter(is_active=True)
    context = {
        'template_data': {'title': 'Movie Petitions - StealthCut'},
        'petitions': petitions
    }
    return render(request, 'petitions/list.html', context)

@login_required
def create_petition(request):
    """Create a new petition"""
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petitions.detail', petition_id=petition.id)
    else:
        form = PetitionForm()
    
    context = {
        'template_data': {'title': 'Create Petition - StealthCut'},
        'form': form
    }
    return render(request, 'petitions/create.html', context)

def petition_detail(request, petition_id):
    """Display petition details and voting interface"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    
    # Check if user has already voted
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(petition=petition, user=request.user)
        except Vote.DoesNotExist:
            user_vote = None
    
    # Create vote form if user hasn't voted
    vote_form = None
    if request.user.is_authenticated and not user_vote:
        vote_form = VoteForm()
    
    context = {
        'template_data': {'title': f'{petition.title} - StealthCut'},
        'petition': petition,
        'user_vote': user_vote,
        'vote_form': vote_form
    }
    return render(request, 'petitions/detail.html', context)

@login_required
@require_POST
def vote_petition(request, petition_id):
    """Handle voting on a petition"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    
    # Check if user has already voted
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        messages.warning(request, 'You have already voted on this petition.')
        return redirect('petitions.detail', petition_id=petition.id)
    
    vote_type = request.POST.get('vote_type')
    if vote_type not in ['yes', 'no']:
        messages.error(request, 'Invalid vote type.')
        return redirect('petitions.detail', petition_id=petition.id)
    
    # Create the vote
    Vote.objects.create(
        petition=petition,
        user=request.user,
        vote_type=vote_type
    )
    
    messages.success(request, f'Your {vote_type} vote has been recorded!')
    return redirect('petitions.detail', petition_id=petition.id)

@login_required
def my_petitions(request):
    """Display petitions created by the current user"""
    petitions = Petition.objects.filter(created_by=request.user, is_active=True)
    context = {
        'template_data': {'title': 'My Petitions - StealthCut'},
        'petitions': petitions
    }
    return render(request, 'petitions/my_petitions.html', context)
