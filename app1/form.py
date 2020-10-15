from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, PasswordChangeForm


help_text1 = """
                <ul>
                    <li>
                        Your password must contain at least 8 characters. <input type="checkbox" id="check_length" disabled>
                    </li>
                    <li>
                        Your password should contain special character. <input type="checkbox" id="check_special" disabled>
                    </li>
                    <li>
                        Your password should contain number. <input type="checkbox" id="check_number" disabled>
                    </li>
                </ul>
             """
help_text2 = """
                <ul>
                    <li>
                        Enter the same password as before, for verification.
                    </li>
                </ul>
             """

class PasswordSet(SetPasswordForm):
    new_password1 = forms.CharField(required=True, label='Password', help_text=help_text1, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'title': 'Enter password', 'autofocus': 'on', 'oninput': 'check();'}))
    new_password2 = forms.CharField(required=True, label='Password (again)', help_text=help_text2, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'title': 'Enter password again', 'oninput': 'check();'}))

class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'title': 'Enter Email', 'autofocus': 'on'}))