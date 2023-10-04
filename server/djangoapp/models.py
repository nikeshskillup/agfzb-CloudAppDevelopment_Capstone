from django.db import models
from django.utils.timezone import now
import json
import uuid


# Create your models here.

# Create a Car Make model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default='Make')
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name

# Create a Car Model model
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=100, default='Car')

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    MINIVAN = 'Minivan'
    
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (MINIVAN, 'Minivan')
    ]

    type = models.CharField(
        null=False,
        max_length=50,
        choices=CAR_TYPES,
        default=SEDAN
    )
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name

class CarDealer(models.Model):

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    st = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return "Dealer name: " + self.full_name

# class DealerReview(models.Model):

#     dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     purchase = models.BooleanField()
#     review = models.TextField()
#     purchase_date = models.DateField(null=True)
#     car_make = models.CharField(max_length=100, null=True)
#     car_model = models.CharField(max_length=100, null=True)
#     car_year = models.CharField(max_length=4, null=True)
#     sentiment = models.CharField(max_length=10, null=True)

#     def __str__(self):
#         return "Review: " + self.review
