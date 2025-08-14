from django.db import models

# Create your models here.
class District(models.Model):
    district_id = models.AutoField(primary_key = True)
    district_name = models.CharField(max_length = 100)
    district_state = models.CharField(max_length = 100,default = "TamilNadu")
    country_name = models.CharField(max_length = 100, default = "India")
    created_at = models.DateTimeField(auto_now_add=True) # "auto_now_add=True" -> Value is set only once — when the object is first created. It never changes automatically after that.
    updated_at = models.DateTimeField(auto_now = True) # "auto_now = True" -> Value is updated every time the object is saved (updated).
    status = models.CharField(
        max_length = 8,
        choices = [('active','Active'),('inactive','Inactive')],
        # The list contains tuples:
        # First value → actual value stored in the database ('active', 'inactive')
        # Second value → human-readable label shown in Django Admin/forms ('Active', 'Inactive')
        default = 'active'
    )
    def __str__(self):
        return self.district_name

# python manage.py makemigrations - This command generates a migration file (SQL instructions for your DB).
# python manage.py migrate - This will create the District table with all fields in your database.
# After migrating, Django automatically names your database table based on: <app_name>_<model_name_lowercase>, Eg:store_district. 