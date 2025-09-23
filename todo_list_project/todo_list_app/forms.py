from django import forms 
from django.contrib.auth import authenticate
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

class LoginForm(forms.Form):
    """ Represents a Login Form with username and password. 
    
    Attributes: 
        username(CharField): A character field to represent the created username by the user.
        password(CharField): A character field to represet the user's password.
    """

    username = forms.CharField(max_length=64)
    password = forms.CharField(widget= forms.PasswordInput)

    def clean(self): 
        """
        Brief: A method that validate and authenticates a user's login.

        Details: The method authenticates the entered login data,
                 and raises a validation error in case of failure.

        Args:
            self
        """
        cleaned_data = super().clean()                 # returns a dictionary 

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Check if username and password were provided
        if not username or not password: 
            return cleaned_data

        # Authenticate User 
        user = authenticate(username= username, password=password )

        # If authenticate returns nothing then it could not authenticate 
        if user is None:
            raise forms.ValidationError(" Wrong username or password! ")

        # We can add the user object to the form for easy access in the views
        self.user = user 

        return cleaned_data

class AddListForm(forms.Form):
    """ Represents an AddList form with a list name.
    
    Attributes: 
        list_name(CharField): A character field to represent the created username by the user.
    """
    list_name = forms.CharField(max_length=100)


 


