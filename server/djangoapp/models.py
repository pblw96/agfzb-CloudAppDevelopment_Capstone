from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()

  def __str__(self):
    return (self.name)


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

  class Fuel(models.TextChoices):
    GASOLINE = 'Gasoline'
    DIESEL = 'Diesel'
    BIODIESEL = 'Biodiesel'
    BIO_GAS = 'BioGas'
    ELECTRIC = 'Electric'
    FULL_HYBRID = 'Full-Hybrid'
    MILD_HYBRID = 'Mild-Hybrid'
    PLUGIN_HYBRID = 'PlugIn-Hybrid'
  
  class Transmission(models.TextChoices):
    AUTOMATIC = 'Automatic'
    MANUAL = 'Manual'
  
  class DriveType(models.TextChoices):
    FRONT_WHEEL_DRIVE = 'FWD' 'Front-Wheel Drive'
    REAR_WHEEL_DRIVE = 'RWD' 'Rear-Wheel Drive'
    FOUR_WHEEL_DRIVE = '4WD' 'Four-Wheel Drive'
    ALL_WHEEL_DRIVE = 'AWD' 'All-Wheel Drive'

  car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  dealer_id = models.IntegerField()
  type = models.CharField(max_length=100)
  year = models.DateField()
  fuel = models.CharField(choices=Fuel.choices, max_length=20, default=Fuel.GASOLINE)
  engine = models.IntegerField()
  transmission = models.CharField(max_length=20, choices=Transmission.choices, default=Transmission.AUTOMATIC)
  seats = models.IntegerField()
  horse_power = models.IntegerField()
  drive_type = models.CharField(max_length=20, choices=DriveType.choices, default=DriveType.FRONT_WHEEL_DRIVE)
  price = models.IntegerField(default=0)


  def __str__(self):
    return (self.name)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

  def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
    self.address = address
    self.city = city
    self.full_name = full_name
    self.id = id
    self.lat = lat
    self.long = long
    self.short_name = short_name
    self.st = st
    self.zip = zip

  def __str__(self):
    return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

  def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
    self.dealership = dealership
    self.name = name
    self.purchase = purchase
    self.review = review
    self.purchase_date = purchase_date
    self.car_make = car_make
    self.car_model = car_model
    self.car_year = car_year
    self.sentiment = sentiment
    self.id = id

  def __str__(self):
    return 'Reviewer name: ' + self.name