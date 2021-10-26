from django.shortcuts import render
from users.models import User

def index(request):
    context = {}
    # Grab username for display.
    if 'user_id' in request.session:
        try:
            context['username'] = User.objects.get(id=request.session['user_id']).username
        except:
            context = {}

    return render(request, "index.html", context)
