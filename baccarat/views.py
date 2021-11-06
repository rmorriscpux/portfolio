from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.contrib import messages
from lib_game.baccarat import Bacc_Table
from users.models import User

def pre_game(request):
    pass

def coup(request):
    # Ensure we came here from AJAX load()
    if request.method != "POST":
        return render(request, "baccarat/table.html", {'state' : "start"})

    # Grab user
    try:
        current_user = User.objects.get(id=request.session['user_id'])
    except:
        messages.error(request, f"User Not Found")
        request.session.flush()
        return redirect("/user/login/")

    # Make dictionary of bets.
    bets = {}
    if int(request.POST['bet_player']) > 0: bets['player'] = int(request.POST['bet_player'])
    if int(request.POST['bet_banker']) > 0: bets['banker'] = int(request.POST['bet_banker'])
    if int(request.POST['bet_tie']) > 0: bets['tie'] = int(request.POST['bet_tie'])
    if int(request.POST['bet_player_pair']) > 0: bets['player_pair'] = int(request.POST['bet_player_pair'])
    if int(request.POST['bet_banker_pair']) > 0: bets['banker_pair'] = int(request.POST['bet_banker_pair'])
    
    # Go back to table if no bets were made (sanity check; button to start game should only activate with non-zero bet placement on page)
    if not bets:
        return render(request, "baccarat/table.html", {'state' : "start"})

    # Ensure user has enough credits to cover bets. Return error if not, otherwise continue.
    total_bet = 0
    for b in bets.values():
        total_bet += b

    if total_bet > current_user.credit_balance:
        messages.error(request, "Not enough credits for bets placed.")
        return render(request, "baccarat/table.html", {'state' : "start"})

    current_user.credit_balance -= total_bet
    current_user.save()

    game_round = Bacc_Table(**bets).reset()
    game_round.burn()
    game_round.coup()

    # Save Baccarat game data.
    request.session['game_data'] = game_round.to_json()

    # Create needed context for page.
    context = {}
    context['player_hand'] = game_round.player
    context['banker_hand'] = game_round.banker
    context['bets'] = game_round.bets
    context['total_bet'] = total_bet
    context['state'] = game_round.state

    return render(request, "baccarat/table.html", context)

def draw(request):
    # Ensure user in session.
    if 'user_id' not in request.session:
        return redirect("/user/login/")

    # Ensure we came here from AJAX load()
    if request.method != "POST":
        return render(request, "baccarat/table.html", {'state' : 'start'})
    
    # Ensure a game is active.
    if 'game_data' not in request.session:
        return render(request, "baccarat/table.html", {'state' : 'start'})

    game_round = Bacc_Table.from_json(request.session['game_data'])

    # Do action based on game state.
    if game_round.state == "player_turn":
        game_round.player_action()
    elif game_round.state == "banker_turn":
        game_round.banker_action()

    # Create needed context for page.
    total_bet = 0
    for b in game_round.bets.values():
        total_bet += b
    context = {}
    context['player_hand'] = game_round.player
    context['banker_hand'] = game_round.banker
    context['bets'] = game_round.bets
    context['total_bet'] = total_bet
    context['state'] = game_round.state

    return render(request, "baccarat/table.html", context)

def end_game(request):
    pass

if settings.DEBUG:
    def test(request):
        if request.method == "POST":
            for b in request.POST.getlist('bets'):
                print(b)

        return render(request, "baccarat/test.html")
