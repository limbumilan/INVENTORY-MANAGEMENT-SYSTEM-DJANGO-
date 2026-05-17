from django import forms
from .models import StockMovement

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        # These are the input fields we want to show the user on the webpage
        fields = ['product', 'movement_type', 'quantity', 'reason']
        
        # We add some clean Bootstrap-friendly styling classes to the form inputs
        widgets = {
            'product': forms.Select(attrs={'class': 'form-input'}),
            'movement_type': forms.Select(attrs={'class': 'form-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'reason': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Customer Order #102'}),
        }