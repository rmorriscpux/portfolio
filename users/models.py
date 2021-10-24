from django.db import models
from datetime import date
import bcrypt

class UserMgr(models.Manager):
    def register_validation(self, form_data):
        errors = {}

        # Username
        if self.filter(username=form_data['username']):
            errors['username'] = "Username already registered."
        if len(form_data['username']) < 3:
            errors['username'] = "Username must be at least 3 characters."
        # Email
        if self.filter(email=form_data['email']):
            errors['email'] = "Email already registered."
        # Password - Consider removing, validation is present in Register form class.
        if len(form_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if form_data['password'] != form_data['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match."
        # Birthdate
        try:
            # Note: This is done for compatibility with Python versions earlier than 3.8.
            date_arr = form_data['birthdate'].split("-")
            birthdate = date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
        except:
            errors['birthdate'] = "Invalid birthdate."
        else:
            if birthdate > date.today().replace(year=date.today().year-21):
                errors['birthdate'] = "Must be at least 21 years old to register."

        return errors

    # Check username and password credentials. Returns boolean.
    def credentials_valid(self, username, password):
        user_found = self.filter(username=username)
        if not user_found: # username not in database. Invalid credentials.
            return False

        # Return True on correct password, False on incorrect password.
        return bcrypt.checkpw(password.encode(), user_found[0].pw_hash.encode())

class User(models.Model):
    # Unique Fields
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45, unique=True)
    email = models.CharField(max_length=255, unique=True)
    pw_hash = models.CharField(max_length=255)
    birthday = models.DateField()
    credit_balance = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)
    credits_played = models.PositiveIntegerField(default=0)
    credits_won = models.PositiveIntegerField(default=0)

    # Relationships

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Manager
    objects = UserMgr()