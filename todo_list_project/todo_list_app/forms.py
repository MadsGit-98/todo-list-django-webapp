from tkinter import Widget
from django import forms 
from django.contrib.auth.models import User

class RegisterForm(forms.Form): 
    """ Represents a Registeration Form with username, email, password, confirm_password 
    
    Attributes: 
        username(CharField): A character field to represent the created username by the user.
        email(EmailField): An e-mail field to represent the User's email address. 
        password(CharField): A character field to represet the user's password.
        confirm_password(CharField): A character field to represet the user's password confirmation.
    """

    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget= forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget= forms.PasswordInput, min_length=8)

    def clean_username(self):
        """
        Brief: A method that validates the username field.

        Details: The method vlidates the entered e-mail during registeration
                 is not already in use by an other user.

        Args:
            self
        """
        username = self.cleaned_data.get("username")

        does_exist = User.objects.filter(username=username).exists()

        if does_exist: 
            raise forms.ValidationError("User is already in use!")
        
        return username 

    def clean_email(self): 
        """
        Brief: A method that validates the email field.

        Details: The method vlidates the entered e-mail during registeration
                 is not already in use by an other user.

        Args:
            self
        """
        email = self.cleaned_data.get("email")
        does_exist = User.objects.filter(email=email).exists()

        if does_exist: 
            raise forms.ValidationError("Email is already in use!")

        return email

    def clean(self):
        """
        Brief: A method that validates the password field.

        Details: The method vlidates the password field by checking if it matches 
                 the password confirmation field. If both fields do not match a 
                 validation error is raised.

        Args:
            self
        """
        cleaned_data = super().clean()    # Returns a dictionary 
        
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Validate that the password and the confirm_password are matching 
        if password != confirm_password: 
            raise forms.ValidationError("Password Fields Not Matching!")

        return cleaned_data 