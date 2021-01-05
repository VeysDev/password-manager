from django import forms


class PasswordForm(forms.Form):
    
    # custom form password
    CF_password = forms.CharField(label='Your Password', max_length=100, widget=forms.PasswordInput)

class GoldbarForm(forms.Form):

    CFG_website = forms.CharField(label='Website URL', max_length=100)
    CFG_username = forms.CharField(label='Username', max_length=15)
    CFG_password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
    CFG_masterpassword = forms.CharField(label='Confirm Your Master Password', max_length=100, widget=forms.PasswordInput)

    # could've added meta class to specify the corresponding model but
    # we'll get the owner object from the request and use constructor of goldbar