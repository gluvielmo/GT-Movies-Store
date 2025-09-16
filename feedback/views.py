from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Feedback
from .forms import FeedbackForm
from cart.models import Order

def submit_feedback(request):
    """Handle feedback submission via AJAX"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            
            # Try to get the most recent order for this user if they're logged in
            if request.user.is_authenticated:
                try:
                    latest_order = Order.objects.filter(user=request.user).order_by('-date').first()
                    if latest_order:
                        feedback.order = latest_order
                except Order.DoesNotExist:
                    pass
            
            feedback.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your feedback! Your input helps us improve the GT Movie Store.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def view_feedback(request):
    """Display all feedback submissions"""
    feedback_list = Feedback.objects.all().order_by('-created_at')
    template_data = {
        'title': 'Customer Feedback',
        'feedback_list': feedback_list
    }
    return render(request, 'feedback/view_feedback.html', {'template_data': template_data})