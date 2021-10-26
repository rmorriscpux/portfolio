from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Count
from .models import Bug, Fish, SeaCreature, Month, Hour, Shadow

# Wrap function for getting the hours available range(s) for critters.
def hour_range(critter):
    # For all hours, return an "All Day" string.
    if len(critter.hours.all()) == 24:
        return "All Day"

    # Get the first range.
    start = critter.hours.all()[0]
    end = Hour.objects.get(time=(start.time+1)%24)
    count = 1
    # Count the amount of consecutive hours.
    while end in critter.hours.all():
        end = Hour.objects.get(time=(end.time+1)%24)
        count += 1
    
    temp_count = count # There may be two consecutive ranges, so we may need this amount later.

    # Overnight Wraparound Check
    if start.time == 0 and critter.hours.all()[len(critter.hours.all())-1].time == 23:
        start = Hour.objects.get(time=23)
        count += 1
        while Hour.objects.get(time=(start.time-1)%24) in critter.hours.all() and count < len(critter.hours.all()):
            start = Hour.objects.get(time=(start.time-1)%24)
            count += 1

    out_str = f"{start.time_am_pm}-{end.time_am_pm}"

    # Second Range Check
    if count < len(critter.hours.all()):
        start = critter.hours.all()[temp_count]
        end = Hour.objects.get(time=(start.time+1)%24)
        # Count the amount of consecutive hours.
        while (end in critter.hours.all()) and count < len(critter.hours.all()):
            end = Hour.objects.get(time=(end.time+1)%24)
            count += 1

        out_str = out_str + f", {start.time_am_pm}-{end.time_am_pm}"

    return out_str

# Wrap function for getting the months available range(s) for critters.
def month_range(critter, is_southern=False):
    # For all months, return an "All Year" string.
    if len(critter.months.all()) == 12:
        return "All Year"

    # Get the first range.
    start = critter.months.all()[0]
    end = start
    count = 1
    while Month.objects.get(number=(end.number%12)+1) in critter.months.all():
        end = Month.objects.get(number=(end.number%12)+1)
        count += 1

    temp_count = count # There may be two consecutive ranges, so we may need this amount later.

    # Year Wraparound Check
    if start.name == "January" and critter.months.all()[len(critter.months.all())-1].name == "December":
        start = Month.objects.get(name="December")
        count += 1
        while Month.objects.get(number=(start.number-1)) in critter.months.all() and count < len(critter.months.all()):
            start = Month.objects.get(number=(start.number-1))
            count += 1

    if start == end:
        out_str = f"{start.southern.short_name}" if is_southern else f"{start.short_name}"
    else:
        out_str = f"{start.southern.short_name}-{end.southern.short_name}" if is_southern else f"{start.short_name}-{end.short_name}"

    # Second Range Check
    if count < len(critter.months.all()):
        start = critter.months.all()[temp_count]
        end = start
        count += 1
        while Month.objects.get(number=(end.number%12)+1) in critter.months.all() and count < len(critter.months.all()):
            end = Month.objects.get(number=(end.number%12)+1)
            count += 1
        
        if start == end:
            out_str = out_str + f", {start.southern.short_name}" if is_southern else out_str + f", {start.short_name}"
        else:
            out_str = out_str + f", {start.southern.short_name}-{end.southern.short_name}" if is_southern else out_str + f", {start.short_name}-{end.short_name}"

    return out_str

# index
# Path: /
# Main Page
def index(request):
    return render(request, "acnh/index.html")

# bugs
# Path: /bugs/
# Bug List Page
def bugs(request):
    context = {}
    if request.method == "POST":
        hemisphere = "southern" if "southern" in request.POST else "northern"
        # Get all the bugs for a selected month, or all if no month was selected.
        if 'selected_month' in request.POST:
            selected_month = Month.objects.filter(name=request.POST['selected_month'])
            if selected_month:
                if hemisphere == "northern":
                    month_bugs = selected_month[0].bugs.all()
                else: # Southern
                    month_bugs = selected_month[0].southern.bugs.all()
                context['current_month'] = request.POST['selected_month']
            else:
                month_bugs = Bug.objects.all()
                context['current_month'] = ""
        else:
            month_bugs = Bug.objects.all()
        # Get all the bugs for a selected hour, or all if no hour was selected.
        if 'selected_hour' in request.POST:
            selected_hour = Hour.objects.filter(time=request.POST['selected_hour'])
            if selected_hour:
                hour_bugs = selected_hour[0].bugs.all()
                context['current_hour'] = selected_hour[0].time_am_pm
            else:
                hour_bugs = Bug.objects.all()
                context['current_hour'] = ""
        else:
            hour_bugs = Bug.objects.all()
        # Put them together.
        context['bugs'] = month_bugs.intersection(hour_bugs)
        context['hemisphere'] = hemisphere
    else: # Grab all the bugs in the list.
        context['bugs'] = Bug.objects.all()
        context['hemisphere'] = "northern"
        context['current_month'] = ""
        context['current_hour'] = ""
    context['months'] = Month.objects.all()
    context['hours'] = Hour.objects.all()
    context['all_bugs'] = Bug.objects.all()
    return render(request, "acnh/bugs.html", context)
    
# fish
# Path: /fish/
# Fish List Page
def fish(request):
    context = {}
    if request.method == "POST":
        hemisphere = "southern" if "southern" in request.POST else "northern"
        # Get all the fish for a selected shadow, or all if no shadow was selected.
        if 'selected_shadow' in request.POST:
            selected_shadow = Shadow.objects.filter(size=request.POST['selected_shadow'])
            if selected_shadow:
                shadow_fishes = selected_shadow[0].fishes.all()
                context['current_shadow'] = request.POST['selected_shadow']
            else:
                shadow_fishes = Fish.objects.all()
                context['current_shadow'] = ""
        else:
            shadow_fishes = Fish.objects.all()
        # Get all the fish for a selected month, or all if no month was selected.
        if 'selected_month' in request.POST:
            selected_month = Month.objects.filter(name=request.POST['selected_month'])
            if selected_month:
                if hemisphere == "northern":
                    month_fishes = selected_month[0].fishes.all()
                else: # Southern
                    month_fishes = selected_month[0].southern.fishes.all()
                context['current_month'] = request.POST['selected_month']
            else:
                month_fishes = Fish.objects.all()
                context['current_month'] = ""
        else:
            month_fishes = Fish.objects.all()
        # Get all the fish for a selected hour, or all if no hour was selected.
        if 'selected_hour' in request.POST:
            selected_hour = Hour.objects.filter(time=request.POST['selected_hour'])
            if selected_hour:
                hour_fishes = selected_hour[0].fishes.all()
                context['current_hour'] = selected_hour[0].time_am_pm
            else:
                hour_fishes = Fish.objects.all()
                context['current_hour'] = ""
        else:
            hour_fishes = Fish.objects.all()
        # Put them together.
        context['fishes'] = month_fishes.intersection(hour_fishes, shadow_fishes)
        context['hemisphere'] = hemisphere
    else: # Grab all the fish in the list.
        context['fishes'] = Fish.objects.all()
        context['hemisphere'] = "northern"
        context['current_month'] = ""
        context['current_hour'] = ""
    context['months'] = Month.objects.all()
    context['hours'] = Hour.objects.all()
    context['shadows'] = Shadow.objects.all()
    context['all_fishes'] = Fish.objects.all()
    return render(request, "acnh/fish.html", context)
    
# sea_creatures
# Path: /sea_creatures/
# Sea Creatures List Page
def sea_creatures(request):
    context = {}
    if request.method == "POST":
        hemisphere = "southern" if "southern" in request.POST else "northern"
        # Get all the sea creatures for a selected shadow, or all if no shadow was selected.
        if 'selected_shadow' in request.POST:
            selected_shadow = Shadow.objects.filter(size=request.POST['selected_shadow'])
            if selected_shadow:
                shadow_creatures = selected_shadow[0].sea_creatures.all()
                context['current_shadow'] = request.POST['selected_shadow']
            else:
                shadow_creatures = SeaCreature.objects.all()
                context['current_shadow'] = ""
        else:
            shadow_creatures = SeaCreature.objects.all()
        # Get all the sea creatures for a selected month, or all if no month was selected.
        if 'selected_month' in request.POST:
            selected_month = Month.objects.filter(name=request.POST['selected_month'])
            if selected_month:
                if hemisphere == "northern":
                    month_creatures = selected_month[0].sea_creatures.all()
                else: # Southern
                    month_creatures = selected_month[0].southern.sea_creatures.all()
                context['current_month'] = request.POST['selected_month']
            else:
                month_creatures = SeaCreature.objects.all()
                context['current_month'] = ""
        else:
            month_creatures = SeaCreature.objects.all()
        # Get all the sea creatures for a selected hour, or all if no hour was selected.
        if 'selected_hour' in request.POST:
            selected_hour = Hour.objects.filter(time=request.POST['selected_hour'])
            if selected_hour:
                hour_creatures = selected_hour[0].sea_creatures.all()
                context['current_hour'] = selected_hour[0].time_am_pm
            else:
                hour_creatures = SeaCreature.objects.all()
                context['current_hour'] = ""
        else:
            hour_creatures = SeaCreature.objects.all()
        # Put them together.
        context['sea_creatures'] = month_creatures.intersection(hour_creatures, shadow_creatures)
        context['hemisphere'] = hemisphere
    else: # Grab all the sea creatures in the list.
        context['sea_creatures'] = SeaCreature.objects.all()
        context['hemisphere'] = "northern"
        context['current_month'] = ""
        context['current_hour'] = ""
    context['months'] = Month.objects.all()
    context['hours'] = Hour.objects.all()
    context['shadows'] = Shadow.objects.annotate(Count('sea_creatures')).filter(sea_creatures__count__gt=0)
    context['all_sea_creatures'] = SeaCreature.objects.all()
    return render(request, "acnh/sea_creatures.html", context)

# bugs_info
# Path: /bugs/critter_info/
# AJAX Get information for a specific bug.
def bugs_info(request):
    if request.method != "POST":
        return redirect('../')
    if 'name' not in request.POST:
        return redirect('../')

    try:
        selected_bug = Bug.objects.get(name=request.POST['name'])
    except:
        return HttpResponse("Bug Not Found.")

    is_southern =  request.POST['hemisphere'] == "southern"

    out_html = f'''
    <table class="critter_info">
        <tr>
            <th colspan="2">{selected_bug.name}</th>
        </tr>
        <tr>
            <td class="category">Location</td>
            <td class="value">{selected_bug.location}</td>
        </tr>
        <tr>
            <td class="category">Value</td>
            <td class="value">{selected_bug.price}</td>
        </tr>
        <tr>
            <td class="category">Hours</td>
            <td class="value">{hour_range(selected_bug)}</td>
        </tr>
        <tr>
            <td class="category">Months</td>
            <td class="value">{month_range(selected_bug, is_southern)}</td>
        </tr>
    </table>
    '''

    return HttpResponse(out_html)

# fish_info
# Path: /fish/critter_info/
# AJAX Get information for a specific fish.
def fish_info(request):
    if request.method != "POST":
        return redirect('../')
    if 'name' not in request.POST:
        return redirect('../')

    try:
        selected_fish = Fish.objects.get(name=request.POST['name'])
    except:
        return HttpResponse("Fish Not Found.")

    is_southern = request.POST['hemisphere'] == "southern"
    fin_text = " (Fin)" if selected_fish.fin else ""

    out_html = f'''
    <table class="critter_info">
        <tr>
            <th colspan="2">{selected_fish.name}</th>
        </tr>
        <tr>
            <td class="category">Location</td>
            <td class="value">{selected_fish.location}</td>
        </tr>
        <tr>
            <td class="category">Shadow</td>
            <td class="value">{selected_fish.shadow.size}{fin_text}</td>
        </tr>
        <tr>
            <td class="category">Value</td>
            <td class="value">{selected_fish.price}</td>
        </tr>
        <tr>
            <td class="category">Hours</td>
            <td class="value">{hour_range(selected_fish)}</td>
        </tr>
        <tr>
            <td class="category">Months</td>
            <td class="value">{month_range(selected_fish, is_southern)}</td>
        </tr>
    </table>
    '''

    return HttpResponse(out_html)

# sea_creatues_info
# Path: /sea_creatures/critter_info/
# AJAX Get information for a specific sea creature.
def sea_creatures_info(request):
    if request.method != "POST":
        return redirect('../')
    if 'name' not in request.POST:
        return redirect('../')

    try:
        selected_creature = SeaCreature.objects.get(name=request.POST['name'])
    except:
        return HttpResponse("Sea Creature Not Found.")

    is_southern = request.POST['hemisphere'] == "southern"

    out_html = f'''
    <table class="critter_info">
        <tr>
            <th colspan="2">{selected_creature.name}</th>
        </tr>
        <tr>
            <td class="category">Shadow</td>
            <td class="value">{selected_creature.shadow.size}</td>
        </tr>
        <tr>
            <td class="category">Value</td>
            <td class="value">{selected_creature.price}</td>
        </tr>
        <tr>
            <td class="category">Hours</td>
            <td class="value">{hour_range(selected_creature)}</td>
        </tr>
        <tr>
            <td class="category">Months</td>
            <td class="value">{month_range(selected_creature, is_southern)}</td>
        </tr>
    </table>
    '''

    return HttpResponse(out_html)