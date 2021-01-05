from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Goldbar
from .forms import PasswordForm, GoldbarForm
import hashlib, base64
from cryptography.fernet import Fernet
from django.contrib import messages



# Create your views here.


@login_required
def addGoldbar(request):
    if request.method == 'POST':
        form = GoldbarForm(request.POST)
        if form.is_valid():
            
            # password we got from the form
            password = form.cleaned_data.get('CFG_masterpassword')
            
            # authenticate master password
            if manualAuthenticate(request, password):
                
                # generate encryption key from password
                key = base64.b64encode(hashlib.sha256(password.encode()).digest())
                
                # encrypt message (message = objects password)
                message = form.cleaned_data.get('CFG_password').encode()
                f = Fernet(key)
                encrypted_message = f.encrypt(message)

                # instantiate a goldbar object with the encrypted password and others
                Goldbar(
                    website=form.cleaned_data.get('CFG_website'),
                    username=form.cleaned_data.get('CFG_username'),
                    password=encrypted_message.decode(),
                    owner=request.user
                ).save()

                # slip a succes message to requeest
                messages.success(request, f'Goldbar created for {request.user.username}')
                return redirect('vault-page')
            else:
                messages.warning(request, f'Wrong Master Password for user {request.user.username}')

    else:
        form = GoldbarForm()
    return render(request, 'vault/addGoldbar.html', {'form': form})



@login_required
def vault_auth(request):

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            
            if manualAuthenticate(request, form.cleaned_data.get('CF_password')):
                
                # get a query set of all the items that belongs to logged in user
                temp_query = Goldbar.objects.filter(owner=request.user)
                
                # create the symentric key that we also used to encrypt the data so we can decrypt it
                password_encoded = form.cleaned_data.get('CF_password').encode()
                
                # base64 encode the sha256 hash of our CF_password
                # because Fernet requires fixed size base64 bytes 
                # https://gist.github.com/formido/821003
                key = base64.b64encode(hashlib.sha256(password_encoded).digest())

                for i in temp_query: # storelanan password encrypted oolmayınca fernet hata veriyor, add try catch to the for loop so invalid objects are shown on page
                    # initialize the password we got from the query and turn it into bytes
                    message = i.password.encode()
                    
                    # decryption
                    f = Fernet(key)
                    decrypted_message = f.decrypt(message)
                    
                    # replace the encrypted password in the object with the decrypted one
                    i.password = decrypted_message.decode()
                    
                
                # pass the query to the page as context
                context = {
                    'Goldbars': temp_query,
                    'isim': request.user.username,
                }
                
                return render(request, 'vault/main.html', context)
            else:
                messages.warning(request, f'Wrong Master Password for user {request.user.username}')
    else:
        form = PasswordForm()
    return render(request, 'vault/vault.html', {'form': form})

@login_required
def deleteGoldbar(request, goldbar_id):
    Goldbar.objects.get(id=goldbar_id).delete()
    messages.success(request, f'Goldbar deleted succesfully.')
    return redirect('vault-page')
                    

def about(request):
    return render(request, 'vault/about.html')

def home(request):
    return render(request, 'vault/home.html')

def manualAuthenticate(request, sifre): # checks the hash of the current user against the hash of the entered password
    
    # get the password string django stores and parse it (<algorithm>$<iterations>$<salt>$<hash>)
    storage = request.user.password.split("$")
    
    # distribute parsed values to corresponding variables
    iterations = int(storage[1])
    strd_salt = storage[2].encode()
    strd_hash = storage[3].encode()

    # hash the password we got from the user with the salt we got from the database
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        sifre.encode(), # Convert the password to bytes - formerly form.cleaned_data.get('CF_password').encode(),
        strd_salt, 
        iterations
    )
    
    # hash we obtained is a little weird, this is to get it in shape
    # https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/hashers/#PBKDF2PasswordHasher
    new_key = base64.b64encode(new_key).decode('ascii').strip().encode()
    
    # compare the hash we obtained above with the hash from database
    if new_key == strd_hash:
        return True
    return False

