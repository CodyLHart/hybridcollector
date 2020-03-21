from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User    

APPT_TYPES = (
    ('H', 'Haircut'),
    ('D', 'Dentist'),
    ('L', 'DUI Lawyer'),
    ('V', 'Vajazzle')
)

class Vest(models.Model):
    vest_type = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.vest_type
    
    def get_absolute_url(self):
        return reverse('vests_detail', kwargs={'pk': self.id})

class Hybrid(models.Model):
    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=100)
    produce = models.CharField(max_length=100)
    num_legs = models.IntegerField(default=4)
    vests = models.ManyToManyField(Vest)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'hybrid_id': self.id})
    
    class Meta:
        ordering = ['name']
        
class Appointment(models.Model):
    date = models.DateField()
    appt_type = models.CharField(
        'Appointment Type',
        max_length=1,
        choices=APPT_TYPES,
        default=APPT_TYPES[1][0]
    )
    hybrid = models.ForeignKey(Hybrid, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_appt_type_display()} appointment on {self.date}"
    
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    hybrid=models.ForeignKey(Hybrid, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for hybrid_id: {self.hybrid_id} @{self.url}"