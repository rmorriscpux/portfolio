from django.core.management.color import no_style
from django.db import connection

from .models import *

Shadow.objects.all().delete()
Hour.objects.all().delete()
Month.objects.all().delete()
Bug.objects.all().delete()
Fish.objects.all().delete()
SeaCreature.objects.all().delete()

sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Shadow, Hour, Month, Bug, Fish, SeaCreature])
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)

# Shadows
Shadow.objects.create(size="Smallest")
Shadow.objects.create(size="Small")
Shadow.objects.create(size="Medium")
Shadow.objects.create(size="Large")
Shadow.objects.create(size="Larger")
Shadow.objects.create(size="Largest")
Shadow.objects.create(size="Narrow")

# Hours
Hour.objects.create(time=0)
Hour.objects.create(time=1)
Hour.objects.create(time=2)
Hour.objects.create(time=3)
Hour.objects.create(time=4)
Hour.objects.create(time=5)
Hour.objects.create(time=6)
Hour.objects.create(time=7)
Hour.objects.create(time=8)
Hour.objects.create(time=9)
Hour.objects.create(time=10)
Hour.objects.create(time=11)
Hour.objects.create(time=12)
Hour.objects.create(time=13)
Hour.objects.create(time=14)
Hour.objects.create(time=15)
Hour.objects.create(time=16)
Hour.objects.create(time=17)
Hour.objects.create(time=18)
Hour.objects.create(time=19)
Hour.objects.create(time=20)
Hour.objects.create(time=21)
Hour.objects.create(time=22)
Hour.objects.create(time=23)

# Months
Month.objects.create(number=1, name="January")
Month.objects.create(number=2, name="February")
Month.objects.create(number=3, name="March")
Month.objects.create(number=4, name="April")
Month.objects.create(number=5, name="May")
Month.objects.create(number=6, name="June")
Month.objects.create(number=7, name="July")
Month.objects.create(number=8, name="August")
Month.objects.create(number=9, name="September")
Month.objects.create(number=10, name="October")
Month.objects.create(number=11, name="November")
Month.objects.create(number=12, name="December")

def add_bug(name, location, price, start_hour=0, end_hour=0, start_month=1, end_month=1):
    new_bug = Bug.objects.create(name=name, location=location, price=price)

    if end_hour <= start_hour:
        end_hour += 24
    for i in range(start_hour, end_hour):
        new_bug.hours.add(Hour.objects.get(time=i%24))

    if end_month <= start_month:
        end_month += 12
    for i in range(start_month, end_month):
        new_bug.months.add(Month.objects.get(id=(i-1)%12+1))

    new_bug.save()

    return

def add_fish(name, location, price, shadow_size, has_fin, start_hour=0, end_hour=0, start_month=1, end_month=1):
    new_fish = Fish.objects.create(name=name, location=location, price=price, shadow=Shadow.objects.get(size=shadow_size), fin=has_fin)

    if end_hour <= start_hour:
        end_hour += 24
    for i in range(start_hour, end_hour):
        new_fish.hours.add(Hour.objects.get(time=i%24))

    if end_month <= start_month:
        end_month += 12
    for i in range(start_month, end_month):
        new_fish.months.add(Month.objects.get(id=(i-1)%12+1))

    new_fish.save()

    return

def add_sea_creature(name, price, shadow_size, start_hour=0, end_hour=0, start_month=1, end_month=1):
    new_sea_creature = SeaCreature.objects.create(name=name, price=price, shadow=Shadow.objects.get(size=shadow_size))

    if end_hour <= start_hour:
        end_hour += 24
    for i in range(start_hour, end_hour):
        new_sea_creature.hours.add(Hour.objects.get(time=i%24))

    if end_month <= start_month:
        end_month += 12
    for i in range(start_month, end_month):
        new_sea_creature.months.add(Month.objects.get(id=(i-1)%12+1))

    new_sea_creature.save()

    return

def add_hours(entry, start_hour=0, end_hour=0):
    if end_hour <= start_hour:
        end_hour += 24
    for i in range(start_hour, end_hour):
        entry.hours.add(Hour.objects.get(time=i%24))
    entry.save()
    return

def add_months(entry, start_month=1, end_month=1):
    if end_month <= start_month:
        end_month += 12
    for i in range(start_month, end_month):
        entry.months.add(Month.objects.get(id=(i-1)%12+1))
    entry.save()
    return
    
# BUGS
add_bug("Common Butterfly","Flying",160,4,19,9,7)
add_bug("Yellow Butterfly","Flying",160,4,19,3,7)
add_bug("Tiger Butterfly","Flying",240,4,19,3,10)
add_bug("Peacock Butterfly","Flying by hybrid flowers",2500,4,19,3,7)
add_bug("Common Bluebottle","Flying",300,4,19,4,9)
add_bug("Paper Kite Butterfly","Flying",1000,8,19,1,1)
add_bug("Great Purple Emperor","Flying",3000,4,19,5,9)
add_bug("Monarch Butterfly","Flying",140,4,17,9,12)
add_bug("Emperor Butterfly","Flying",4000,17,8,6,10)
add_bug("Agrias Butterfly","Flying",3000,8,17,4,10)
add_bug("Raja Brooke's Birdwing","Flying by purple flowers",2500,8,17,4,10)
add_bug("Queen Alexandra's Birdwing","Flying",4000,8,16,5,10)
add_bug("Moth","Flying by light",130,19,4,1,1)
add_bug("Atlas Moth","On trees",3000,19,4,4,10)
add_bug("Madagascan Sunset Moth","Flying",2500,8,16,4,10)
add_bug("Long Locust","On ground",200,8,19,4,12)
add_bug("Migratory Locust","On ground",600,8,19,8,12)
add_bug("Rice Grasshopper","On ground",160,8,19,8,12)
add_bug("Grasshopper","On ground",160,8,17,7,10)
add_bug("Cricket","On ground",130,17,8,9,12)
add_bug("Bell Cricket","On ground",430,17,8,9,11)
add_bug("Mantis","On flowers",430,8,17,3,12)
add_bug("Orchid Mantis","On white flowers",2400,8,17,3,12)
add_bug("Honeybee","Flying",200,8,17,3,8)
add_bug("Wasp","Falls from shaking trees",2500,0,0,1,1)
add_bug("Brown Cicada","On trees",250,8,17,7,9)
add_bug("Robust Cicada","On trees",300,8,17,7,9)
add_bug("Giant Cicada","On trees",600,8,17,7,9)
add_bug("Walker Cicada","On trees",400,8,17,8,10)
add_bug("Evening Cicada","On trees",660,4,8,7,9)
add_bug("Cicada Shell","On trees",10,0,0,7,9)
add_bug("Red Dragonfly","Flying",180,8,19,9,11)
add_bug("Darner Dragonfly","Flying",230,8,17,4,11)
add_bug("Banded Dragonfly","Flying",4500,8,17,5,11)
add_bug("Damselfly","Flying",500,0,0,11,3)
add_bug("Firefly","Flying",300,19,4,6,7)
add_bug("Mole Cricket","Underground",500,0,0,11,6)
add_bug("Pondskater","Ponds",130,8,19,5,10)
add_bug("Diving Beetle","Ponds and rivers",800,8,19,5,10)
add_bug("Giant Water Bug","Ponds and rivers",2000,19,8,4,10)
add_bug("Stinkbug","On flowers",120,0,0,3,11)
add_bug("Man-faced Stink Bug","On flowers",1000,19,8,3,11)
add_bug("Ladybug","On flowers",200,8,17,3,7)
add_bug("Tiger Beetle","On ground",1500,0,0,2,12)
add_bug("Jewel Beetle","On tree stumps",2400,0,0,4,9)
add_bug("Violin Beetle","On tree stumps",450,0,0,5,7)
add_bug("Citrus Long-horned Beetle","On tree stumps",350,0,0,1,1)
add_bug("Rosalia Batesi Beetle","On tree stumps",3000,0,0,5,10)
add_bug("Blue Weevil Beetle","On coconut trees",800,0,0,7,9)
add_bug("Dung Beetle","Pushing snowballs",3000,0,0,12,3)
add_bug("Earth-boring Dung Beetle","On ground",300,0,0,7,10)
add_bug("Scarab Beetle","On trees",10000,23,8,7,9)
add_bug("Drone Beetle","On trees",200,0,0,6,9)
add_bug("Goliath Beetle","On coconut trees",8000,17,8,6,10)
add_bug("Saw Stag","On trees",2000,0,0,7,9)
add_bug("Miyama Stag","On trees",1000,0,0,7,9)
add_bug("Giant Stag","On trees",10000,23,8,7,9)
add_bug("Rainbow Stag","On trees",6000,19,8,6,10)
add_bug("Cyclommatus Stag","On coconut trees",8000,17,8,7,9)
add_bug("Golden Stag","On coconut trees",12000,17,8,7,9)
add_bug("Giraffe Stag","On coconut trees",12000,17,8,7,9)
add_bug("Horned Dynastid","On trees",1350,17,8,7,9)
add_bug("Horned Atlas","On coconut trees",8000,17,8,7,9)
add_bug("Horned Elephant","On coconut trees",8000,17,8,7,9)
add_bug("Horned Herucles","On coconut trees",12000,17,8,7,9)
add_bug("Walking Stick","On trees",600,4,8,7,12)
add_bug("Walking Leaf","Near trees, disguised as furniture leaf",600,0,0,7,9)
add_bug("Bagworm","Falls from shaking trees",600,0,0,1,1)
add_bug("Ant","On rotten food",80,0,0,1,1)
add_bug("Hermit Crab","Beach",1000,19,8,1,1)
add_bug("Wharf Roach","On rocks at beach",200,0,0,1,1)
add_bug("Fly","On trash items",60,0,0,1,1)
add_bug("Mosquito","Flying",130,17,4,6,10)
add_bug("Flea","On villagers",70,0,0,4,12)
add_bug("Snail","On rocks (raining)",250,0,0,1,1)
add_bug("Pill Bug","Hit rocks",250,23,16,9,7)
add_bug("Centipede","Hit rocks",300,16,23,9,7)
add_bug("Spider","Falls from shaking trees",480,19,8,1,1)
add_bug("Tarantula","On ground",8000,19,4,11,5)
add_bug("Scorpion","On ground",8000,19,4,5,11) 

add_hours(Bug.objects.get(name="Evening Cicada"), 16, 19)
add_hours(Bug.objects.get(name="Walking Stick"), 17, 19)

add_months(Bug.objects.get(name="Yellow Butterfly"), 9, 11)
add_months(Bug.objects.get(name="Raja Brooke's Birdwing"), 12, 3)
add_months(Bug.objects.get(name="Ladybug"), 10, 11)
add_months(Bug.objects.get(name="Violin Beetle"), 9, 12)

# FISH
add_fish("Bitterling","River",900,"Smallest",False,0,0,11,4)
add_fish("Pale Chub","River",160,"Smallest",False,9,16,1,1)
add_fish("Crucian Carp","River",160,"Small",False,0,0,1,1)
add_fish("Dace","River",240,"Medium",False,16,9,1,1)
add_fish("Carp","Pond",300,"Large",False,0,0,1,1)
add_fish("Koi","Pond",4000,"Large",False,16,9,1,1)
add_fish("Goldfish","Pond",1300,"Smallest",False,0,0,1,1)
add_fish("Pop-eyed Goldfish","Pond",1300,"Smallest",False,9,16,1,1)
add_fish("Ranchu Goldfish","Pond",4500,"Small",False,9,16,1,1)
add_fish("Killifish","Pond",300,"Smallest",False,0,0,4,9)
add_fish("Crawfish","Pond",200,"Small",False,0,0,4,10)
add_fish("Soft-shelled Turtle","River",3750,"Large",False,16,9,8,10)
add_fish("Snapping Turtle","River",5000,"Larger",False,21,4,4,11)
add_fish("Tadpole","Pond",100,"Smallest",False,0,0,3,8)
add_fish("Frog","Pond",120,"Small",False,0,0,5,9)
add_fish("Freshwater Goby","River",400,"Small",False,16,9,1,1)
add_fish("Loach","River",400,"Small",False,0,0,3,6)
add_fish("Catfish","Pond",800,"Large",False,16,9,5,11)
add_fish("Giant Snakehead","Pond",5500,"Larger",False,9,16,6,9)
add_fish("Bluegill","River",180,"Small",False,9,16,1,1)
add_fish("Yellow Perch","River",300,"Medium",False,0,0,10,4)
add_fish("Black Bass","River",400,"Large",False,0,0,1,1)
add_fish("Tilapia","River",800,"Medium",False,0,0,6,11)
add_fish("Pike","River",1800,"Larger",False,0,0,9,1)
add_fish("Pond Smelt","River",500,"Small",False,0,0,12,3)
add_fish("Sweetfish","River",900,"Medium",False,0,0,7,10)
add_fish("Cherry Salmon","River (Clifftop)",1000,"Medium",False,16,9,3,7)
add_fish("Char","River (Clifftop)",3800,"Medium",False,16,9,3,7)
add_fish("Golden Trout","River (Clifftop)",15000,"Medium",False,16,9,3,6)
add_fish("Stringfish","River (Clifftop)",15000,"Larger",False,16,9,12,4)
add_fish("Salmon","River (mouth)",700,"Large",False,0,0,9,10)
add_fish("King Salmon","River (mouth)",1800,"Largest",False,0,0,9,10)
add_fish("Mitten Crab","River",2000,"Small",False,16,9,9,12)
add_fish("Guppy","River",1300,"Smallest",False,9,16,4,12)
add_fish("Nibble Fish","River",1500,"Smallest",False,9,16,5,10)
add_fish("Angelfish","River",3000,"Small",False,16,9,5,11)
add_fish("Betta","River",2500,"Small",False,9,16,5,11)
add_fish("Neon Tetra","River",500,"Smallest",False,9,16,4,12)
add_fish("Rainbowfish","River",800,"Smallest",False,9,16,5,11)
add_fish("Piranha","River",2500,"Small",False,9,16,6,10)
add_fish("Arowana","River",10000,"Large",False,16,9,6,10)
add_fish("Dorado","River",15000,"Larger",False,4,21,6,10)
add_fish("Gar","Pond",6000,"Largest",False,16,9,6,10)
add_fish("Arapaima","River",10000,"Largest",False,16,9,6,10)
add_fish("Saddled Bichir","River",4000,"Large",False,21,4,6,10)
add_fish("Sturgeon","River (mouth)",10000,"Largest",False,0,0,9,4)
add_fish("Sea Butterfly","Sea",1000,"Smallest",False,0,0,12,4)
add_fish("Sea Horse","Sea",1100,"Smallest",False,0,0,4,12)
add_fish("Clown Fish","Sea",650,"Smallest",False,0,0,4,10)
add_fish("Surgeonfish","Sea",1000,"Small",False,0,0,4,10)
add_fish("Butterfly Fish","Sea",1000,"Small",False,0,0,4,10)
add_fish("Napoleonfish","Sea",10000,"Largest",False,4,21,7,9)
add_fish("Zebra Turkeyfish","Sea",500,"Medium",False,0,0,4,12)
add_fish("Blowfish","Sea",5000,"Medium",False,21,4,11,3)
add_fish("Puffer Fish","Sea",250,"Medium",False,0,0,7,10)
add_fish("Anchovy","Sea",200,"Small",False,4,21,1,1)
add_fish("Horse Mackerel","Sea",150,"Small",False,0,0,1,1)
add_fish("Barred Knifejaw","Sea",5000,"Medium",False,0,0,3,12)
add_fish("Sea Bass","Sea",400,"Larger",False,0,0,1,1)
add_fish("Red Snapper","Sea",3000,"Large",False,0,0,1,1)
add_fish("Dab","Sea",300,"Medium",False,0,0,10,5)
add_fish("Olive Flounder","Sea",800,"Large",False,0,0,1,1)
add_fish("Squid","Sea",500,"Medium",False,0,0,12,9)
add_fish("Moray Eel","Sea",2000,"Narrow",False,0,0,8,11)
add_fish("Ribbon Eel","Sea",600,"Narrow",False,0,0,6,11)
add_fish("Tuna","Pier",7000,"Largest",False,0,0,11,5)
add_fish("Blue Marlin","Pier",10000,"Largest",False,0,0,7,10)
add_fish("Giant Trevally","Pier",4500,"Larger",False,0,0,5,11)
add_fish("Mahi-mahi","Pier",6000,"Larger",False,0,0,5,11)
add_fish("Ocean Sunfish","Sea",4000,"Largest",True,4,21,7,10)
add_fish("Ray","Sea",3000,"Larger",False,4,21,8,12)
add_fish("Saw Shark","Sea",12000,"Largest",True,16,9,6,10)
add_fish("Hammerhead Shark","Sea",8000,"Largest",True,16,9,6,10)
add_fish("Great White Shark","Sea",15000,"Largest",True,16,9,6,10)
add_fish("Whale Shark","Sea",13000,"Largest",True,0,0,6,10)
add_fish("Suckerfish","Sea",1500,"Large",True,0,0,6,10)
add_fish("Football Fish","Sea",2500,"Large",False,16,9,11,4)
add_fish("Oarfish","Sea",9000,"Largest",False,0,0,12,6)
add_fish("Barreleye","Sea",15000,"Small",False,21,4,1,1)
add_fish("Coelacanth","Sea (rainy days)",15000,"Largest",False,0,0,1,1)

add_hours(Fish.objects.get(name="Piranha"), 21, 5)

add_months(Fish.objects.get(name="Cherry Salmon"), 9, 12)
add_months(Fish.objects.get(name="Char"), 9, 12)
add_months(Fish.objects.get(name="Golden Trout"), 9, 12)
add_months(Fish.objects.get(name="Blue Marlin"), 11, 5)

# SEA CREATURES
add_sea_creature("Seaweed",600,"Large",0,0,10,8)
add_sea_creature("Sea Grapes",900,"Small",0,0,6,10)
add_sea_creature("Sea Cucumber",500,"Medium",0,0,11,5)
add_sea_creature("Sea Pig",10000,"Small",16,10,11,3)
add_sea_creature("Sea Star",500,"Small",0,0,1,1)
add_sea_creature("Sea Urchin",1700,"Small",0,0,5,10)
add_sea_creature("Slate Pencil urchin",2000,"Medium",16,10,5,10)
add_sea_creature("Sea Anemone",500,"Large",0,0,1,1)
add_sea_creature("Moon Jellyfish",600,"Small",0,0,7,10)
add_sea_creature("Sea Slug",600,"Smallest",0,0,1,1)
add_sea_creature("Pearl Oyster",2800,"Small",0,0,1,1)
add_sea_creature("Mussel",1500,"Small",0,0,6,1)
add_sea_creature("Oyster",1100,"Small",0,0,9,3)
add_sea_creature("Scallop",1200,"Medium",0,0,1,1)
add_sea_creature("Whelk",1000,"Small",0,0,1,1)
add_sea_creature("Turban Shell",1000,"Small",0,0,3,6)
add_sea_creature("Abalone",2000,"Medium",16,10,6,2)
add_sea_creature("Gigas Giant clam",15000,"Largest",0,0,5,10)
add_sea_creature("Chambered Nautilus",1800,"Medium",16,10,3,7)
add_sea_creature("Octopus",1200,"Medium",0,0,1,1)
add_sea_creature("Umbrella Octopus",6000,"Small",0,0,3,6)
add_sea_creature("Vampire Squid",10000,"Medium",17,10,5,9)
add_sea_creature("Firefly Squid",1400,"Smallest",21,5,3,7)
add_sea_creature("Gazami Crab",2200,"Medium",0,0,6,12)
add_sea_creature("Dungeness Crab",1900,"Medium",0,0,11,6)
add_sea_creature("Snow Crab",6000,"Large",0,0,11,5)
add_sea_creature("Red King Crab",8000,"Large",0,0,11,4)
add_sea_creature("Acorn Barnacle",600,"Smallest",0,0,1,1)
add_sea_creature("Spider Crab",12000,"Largest",0,0,3,5)
add_sea_creature("Tiger Prawn",3000,"Small",16,10,6,10)
add_sea_creature("Sweet Shrimp",1400,"Small",16,10,9,3)
add_sea_creature("Mantis Shrimp",2500,"Small",16,10,1,1)
add_sea_creature("Spiny Lobster",5000,"Large",21,5,10,1)
add_sea_creature("Lobster",4500,"Large",0,0,4,7)
add_sea_creature("Giant Isopod",12000,"Medium",9,17,7,11)
add_sea_creature("Horseshoe Crab",2500,"Medium",21,5,7,10)
add_sea_creature("Sea Pineapple",1500,"Small",0,0,4,9)
add_sea_creature("Spotted Garden Eel",1100,"Small",4,22,5,11)
add_sea_creature("Flatworm",700,"Smallest",16,10,8,10)
add_sea_creature("Venus' Flower Basket",5000,"Medium",0,0,10,3)

add_hours(SeaCreature.objects.get(name="Giant Isopod"), 21, 5)

add_months(SeaCreature.objects.get(name="Turban Shell"), 9, 1)
add_months(SeaCreature.objects.get(name="Chambered Nautilus"), 9, 12)
add_months(SeaCreature.objects.get(name="Lobster"), 12, 2)