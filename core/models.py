from django.db import models
import uuid

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, related_name='medicines', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    total_days = models.IntegerField(default=1)
    start_date = models.DateField(auto_now_add=True)
    times = models.JSONField(default=list) # List of HH:MM strings

    def __str__(self):
        return f"{self.name} for {self.person.name}"
