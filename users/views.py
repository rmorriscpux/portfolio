from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from datetime import date
from .forms import Login, Register, Modify
from .models import User
import bcrypt

def user_profile(request):
    if 'user_id' not in request.session: # Not logged in.
        return redirect("/user/login/")

    try:
        current_user = User.objects.get(id=request.session['user_id'])
    except:
        # Something weird happened, session contains an invalid user ID. Dump and go to login.
        messages.error(request, f"User ID not found: {request.session['user_id']}")
        request.session.flush()
        return redirect("/user/login/")

    context = {
        'username' : current_user.username,
        'user_first_name' : current_user.first_name,
        'user_last_name' : current_user.last_name,
        'user_email' : current_user.email,
        'user_credit_balance' : current_user.credit_balance,
        'user_games_played' : current_user.games_played,
        'user_credits_played' : current_user.credits_played,
        'user_credits_won' : current_user.credits_won,
    }
    
    return render(request, "user.html", context)

def register_page(request):
    if 'user_id' in request.session: # Already logged in. Go to user profile page.
        messages.error(request, "Already logged in.")
        return redirect("/user/")

    context = {
        'registration_form' : Register(),
        'today' : date.today(),
    }
    return render(request, "register.html", context)

def create(request):
    if request.method != "POST": # Not from form.
        return redirect("/user/register/")

    if 'user_id' in request.session: # Already logged in. Go to user profile page.
        return redirect("/user/")

    new_user_form = Register(request.POST)
    # Check form input for any errors.
    # Did birthdate validation through the model manager because Django forms date widget is inadequate.
    all_errors = {}
    for err, msgs in new_user_form.errors:
        all_errors.setdefault(err, msgs[0])
    for err, msg in User.objects.register_validation(request.POST):
        all_errors.setdefault(err, msg)

    # Set error messages and go to register page if there are any problems.
    if all_errors:
        for msg in all_errors.values():
            messages.error(request, msg)
        return redirect("/user/register/")
    
    # No problems, create new user.
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        username = request.POST['username'],
        email = request.POST['email'],
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode(),
        birthday = request.POST['birthdate'] # Model converts to date object.
    )

    # Start session and finish up.
    request.session.flush()
    request.session['user_id'] = new_user.id
    messages.success(request, "Registration successful!")
    return redirect("/user/")

def login_page(request):
    if 'user_id' in request.session: # Already logged in. Go to user profile page.
        messages.error(request, "Already logged in.")
        return redirect("/user/")

    context = {
        'login_form' : Login(),
    }

    return render(request, "login.html", context)

def login_verify(request):
    if request.method != "POST":
        return redirect("/user/")

    request.session.flush()
    # Start session and go to user page if credentials are valid. Otherwise go to login page.
    if User.objects.credentials_valid(request.POST['username'], request.POST['password']):
        request.session['user_id'] = User.objects.get(username=request.POST['username']).id
        messages.success(request, "Login successful!")
        return redirect("/user/")
    else:
        messages.error(request, "Invalid Credentials")
        return redirect("/user/login/")

def logout(request):
    if 'user_id' in request.session:
        messages.success(request, "Logout successful!")
    request.session.flush()
    return redirect("/user/login/")

def add_credit(request):
    if 'user_id' not in request.session: # Not logged in.
        return redirect("/user/login/")

    try:
        current_user = User.objects.get(id=request.session['user_id'])
    except:
        # Something weird happened, session contains an invalid user ID. Dump and go to login.
        messages.error(request, f"User ID not found: {request.session['user_id']}")
        request.session.flush()
        return redirect("/user/login/")

    if request.method != "POST": # Didn't get here from form.
        return redirect("/user/")

    if request.POST['credits'] > 0 and request.POST['credits'] <= 100:
        current_user.credit_balance += request.POST['credits']
        current_user.save()
        messages.success(request, "Credits added successfully!")
    else:
        messages.error(request, "Invalid add credits.")

    return redirect("/user/")

def modify(request):
    if 'user_id' not in request.session: # Not logged in.
        return redirect("/user/login/")

    try:
        current_user = User.objects.get(id=request.session['user_id'])
    except:
        # Something weird happened, session contains an invalid user ID. Dump and go to login.
        messages.error(request, f"User ID not found: {request.session['user_id']}")
        request.session.flush()
        return redirect("/user/login/")

    # Setup form
    mod_form = Modify(initial={
        'email' : current_user.email,
        'first_name' : current_user.first_name,
        'last_name' : current_user.last_name,
    })

    # Setup context (may not need it all)
    context = {
        'username' : current_user.username,
        'user_first_name' : current_user.first_name,
        'user_last_name' : current_user.last_name,
        'user_email' : current_user.email,
        'mod_form' : mod_form,
    }
    
    return render(request, "modify.html", context)

def update(request):
    if 'user_id' not in request.session: # Not logged in.
        return redirect("/user/login/")

    if request.method != "POST": # Didn't get here via form submission.
        return redirect("/user/edit/")

    try:
        current_user = User.objects.get(id=request.session['user_id'])
    except:
        # Something weird happened, session contains an invalid user ID. Dump and go to login.
        messages.error(request, f"User ID not found: {request.session['user_id']}")
        request.session.flush()
        return redirect("/user/login/")

    mod_form = Modify(request.POST)
    errors = {}

    if mod_form.is_valid(): # Form submission contains all valid fields, which may or may not include a password change.
        # Look at the password change first. This way if there is a mismatch or other issue, nothing else changes.
        if mod_form.cleaned_data['new_password']:
            # A new password was entered, and it was validated against the confirm pw in the form. Now check the old password.
            if User.objects.credentials_valid(current_user.username, mod_form.cleaned_data['old_password']):
                current_user.pw_hash = bcrypt.hashpw(mod_form.cleaned_data['new_password'].encode(), bcrypt.gensalt()).decode()
                current_user.save()
            else:
                errors['old_password'] = "Invalid password."

        if not errors: # Either no password change requested, or password successfully changed.
            current_user.email = mod_form.cleaned_data['email']
            current_user.first_name = mod_form.cleaned_data['first_name']
            current_user.last_name = mod_form.cleaned_data['last_name']
            current_user.save()

    # Compile errors.
    for field, msgs in mod_form.errors.items():
        errors.setdefault(field, msgs[0])

    # If errors, convert to messages and go to modify. Otherwise success and go to user page.
    if errors:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect("/user/edit/")
    else:
        messages.success(request, "Profile updated successfully!")
        return redirect("/user/")

def destroy(request):
    if 'user_id' not in request.session: # Not logged in.
        return redirect("/user/login/")

    if request.method != "POST": # Didn't get here via form submission.
        return redirect("/user/edit/")

    try:
        current_user = User.objects.get(id=request.session['user_id'])
    except:
        # Something weird happened, session contains an invalid user ID. Dump and go to login.
        messages.error(request, f"User ID not found: {request.session['user_id']}")
        request.session.flush()
        return redirect("/user/login/")

    if User.objects.credentials_valid(current_user.username, request.POST['password']):
        current_user.delete()
        request.session.flush()
        messages.success(request, "Profile deleted successfully.")
        return redirect("/user/login/")
    else:
        messages.error(request, "Invalid password.")
        return redirect("/user/edit")

if settings.DEBUG:
    def test(request):
        context = {
            'login_form' : Login(),
            'registration_form' : Register(),
            'today' : date.today(),
        }
        return render(request, "test.html", context)

    def test_post(request):
        if request.method == "POST":
            if request.POST['form_type'] == "register":
                user_form = Register(request.POST)
            else:
                user_form = Login(request.POST)
            print(f"Valid: {user_form.is_valid()}")
            print(f"Clean Data: {user_form.cleaned_data}")
            print(user_form.errors.as_text())
            context = {
                'submit_data' : request.POST
            }
            return render(request, "test_post.html", context)
        else:
            return redirect("/user/test/")