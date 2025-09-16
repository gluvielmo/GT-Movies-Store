from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Feedback
from cart.models import Order

class FeedbackTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            total=1000
        )
    
    def test_feedback_submission(self):
        """Test that feedback can be submitted successfully"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('feedback.submit'), {
            'name': 'Test User',
            'thoughts': 'Great checkout process!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        
        # Check that feedback was created
        feedback = Feedback.objects.get(thoughts='Great checkout process!')
        self.assertEqual(feedback.name, 'Test User')
        self.assertEqual(feedback.user, self.user)
    
    def test_anonymous_feedback(self):
        """Test that anonymous feedback can be submitted"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('feedback.submit'), {
            'name': '',
            'thoughts': 'Anonymous feedback'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        
        # Check that feedback was created with empty name
        feedback = Feedback.objects.get(thoughts='Anonymous feedback')
        self.assertEqual(feedback.name, '')
        self.assertEqual(feedback.user, self.user)
    
    def test_feedback_view_page(self):
        """Test that feedback view page loads correctly"""
        # Create some test feedback
        Feedback.objects.create(
            name='Test User',
            thoughts='Test feedback',
            user=self.user,
            order=self.order
        )
        
        response = self.client.get(reverse('feedback.view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test feedback')
    
    def test_feedback_validation(self):
        """Test that feedback form validates required fields"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('feedback.submit'), {
            'name': 'Test User',
            'thoughts': ''  # Empty thoughts should fail
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('thoughts', response.json()['errors'])