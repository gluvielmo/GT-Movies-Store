from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Leave empty to remain anonymous")
    thoughts = models.TextField(help_text="Your thoughts about the checkout process")
    order = models.ForeignKey('cart.Order', on_delete=models.CASCADE, null=True, blank=True, help_text="Associated order")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text="User who submitted feedback")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        display_name = self.name if self.name else "Anonymous"
        return f"Feedback from {display_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']