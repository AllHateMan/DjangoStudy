from django import forms

class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    required_delivery_address = forms.BooleanField(required=False)
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.BooleanField(required=False)

    
