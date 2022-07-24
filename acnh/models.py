from django.db import models

class Shadow(models.Model):
    # Unique Fields
    size = models.CharField(max_length=45)

    # Relationships
    # fishes
    # sea_creatures

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hour(models.Model):
    # Unique Fields
    time = models.IntegerField()
    @property
    def time_12hr(self):
        time_int = self.time % 12
        if time_int == 0:
            time_int = 12
        return str(time_int)
    @property
    def time_am_pm(self):
        if self.time < 12:
            return self.time_12hr + " AM"
        else:
            return self.time_12hr + " PM"

    # Relationships
    # bugs
    # fishes
    # sea_creatures

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Month(models.Model):
    # Unique Fields
    number = models.IntegerField()
    name = models.CharField(max_length=45)
    @property
    def short_name(self):
        return self.name[0:3]
    @property
    def initial(self):
        return self.name[0]

    # Relationships
    # Same table one-to-one relationship. For use in getting southern hemisphere month ranges.
    @property
    def southern(self):
        try:
            southern_month = Month.objects.get(number=(self.number+5)%12+1)
        except:
            return None
        return southern_month
    # bugs
    # fishes
    # sea_creatures

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Manager
    # objects = MonthMgr()

class Bug(models.Model):
    # Unique Fields
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    price = models.IntegerField()
    @property
    def img_name(self):
        return str(self.id) + "-bug-img.png"

    # Relationships
    hours = models.ManyToManyField(Hour, related_name="bugs")
    months = models.ManyToManyField(Month, related_name="bugs")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Fish(models.Model):
    # Unique Fields
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    price = models.IntegerField()
    fin = models.BooleanField(default=False)
    @property
    def img_name(self):
        return str(self.id) + "-fish-img.png"

    # Relationships
    shadow = models.ForeignKey(Shadow, related_name="fishes", on_delete=models.CASCADE)
    hours = models.ManyToManyField(Hour, related_name="fishes")
    months = models.ManyToManyField(Month, related_name="fishes")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SeaCreature(models.Model):
    # Unique Fields
    name = models.CharField(max_length=45)
    price = models.IntegerField()
    @property
    def img_name(self):
        return str(self.id) + "-sea-img.png"

    # Relationships
    shadow = models.ForeignKey(Shadow, related_name="sea_creatures", on_delete=models.CASCADE)
    hours = models.ManyToManyField(Hour, related_name="sea_creatures")
    months = models.ManyToManyField(Month, related_name="sea_creatures")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
