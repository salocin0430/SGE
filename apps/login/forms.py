from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegistroForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
	    model = User
	    fields=('first_name', 'last_name', 'email', 'is_superuser', 'username',  'password1', 'password2')

	def save(self, commit=True):
	    User= super(RegistroForm, self).save(commit=False)
	    User.email = self.cleaned_data["email"]
	    
	    if commit:
	        User.save()

	    return User