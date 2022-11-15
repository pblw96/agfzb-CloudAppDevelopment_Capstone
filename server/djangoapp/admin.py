from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.StackedInline):
  model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
  list_display = ['name','car_make', 'type', 'year', 'seats', 'transmission', 'fuel', 'engine', 'drive_type', 'price']
  list_filter = ['car_make', 'type', 'year', 'seats', 'transmission', 'fuel', 'drive_type']
  search_fields = ['name','car_make', 'type', 'year']
  date_hierarchy = 'year'
  ordering = ['name']



# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
  inlines = [CarModelInline]
  list_display = ['name', 'description']
  list_filter = ['name']
  search_fields = ['name', 'description']
  ordering = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
