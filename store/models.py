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

class WebAppAdmin(models.Model):
    DISTRICT_CHOICES = [
        ('ER','Erode'),
        ('CBE','Coimbatore'),
        ('TPR','Tiruppur'),
        ('SLM','Salem'),
        ('NKL','Namakkal'),
        ('KRR','Karur')
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    district = models.CharField(max_length=3, choices=DISTRICT_CHOICES) # when district is choosen, the corresponding DT code will be saved in this district variable.
    unique_id = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            district_code = self.district # gets the district value(which was the code already stored)
            count = WebAppAdmin.objects.filter(district=self.district).count()+1
            count_str = str(count).zfill(3) #Formats the count with leading zeros. Example: 5 → "005".
            self.unique_id = f"{district_code}_WAA_{count_str}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name}({self.unique_id})"




