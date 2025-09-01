from django.db import models
from django.core.exceptions import ValidationError
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

class Shop(models.Model):
    shop_id = models.AutoField(primary_key = True)
    shop_unique_id = models.CharField(max_length=25, blank=True, null=True)
    district = models.ForeignKey(District, on_delete = models.CASCADE,related_name="shops")
    shop_name = models.CharField(max_length=150)
    address = models.TextField()
    # unique_id = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length = 8,
        choices = [('active','Active'),('inactive','Inactive')],
        default='active'
    )

    def save(self, *args, **kwargs):
        if not self.shop_id:
            district_code = self.district.district_name.upper()
            shop_count = Shop.objects.filter(district=self.district).count()+1
            self.shop_unique_id = f"{district_code}_SHOP_{shop_count:03d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.shop_name} ({self.shop_unique_id})"



class ShopAdmin(models.Model):
    admin_id = models.CharField(max_length=100,unique=True,editable=False)
    admin_name = models.CharField(max_length = 100,blank=False,null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100,blank=False,null=False)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name="admins")
    region = models.CharField(max_length=100,blank=False,null=False)
    
    def save(self, *args, **kwargs):
        districts = {
            "Erode":"ER",
            "Coimbatore":"CBE",
            "Tiruppur":"TPR",
            "Karur":"KRR",
            "Namakkal":"NKL",
            "Salem":"SLM"
        }
        if not self.admin_id:
            district_code = districts[self.shop.district.district_name]
            print(f"{self.shop.district.district_name}")
            shop_number = self.shop.shop_unique_id.split("_")[-1]
            admin_count = ShopAdmin.objects.filter(shop=self.shop).count() + 1
            if admin_count > 2:
                raise ValidationError("A shop can only have 2 admins.")
            self.admin_id = f"{district_code}_SH{shop_number}_{admin_count:03d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.admin_name} ({self.admin_id})"

class Product(models.Model):
    product_id = models.AutoField(primary_key = True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    product_unique_id = models.CharField(max_length=100,unique=True,blank=True)
    category = models.CharField(max_length=100,blank=False,null=False)
    name = models.CharField(max_length=200,blank=False,null=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    manufactured_date = models.DateField(auto_now=True)
    description = models.TextField(blank=False,null=False)
    image = models.ImageField(upload_to="product_images/")
    # stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.product_unique_id:
            shop_name = self.shop.shop_name.upper().replace(" ","_")
            category_name = self.category.upper().replace(" ","_")
            nth_number = Product.objects.filter(shop=self.shop,category=self.category).count()+1
            self.product_unique_id = f"{shop_name}_{category_name}_{nth_number}"
        super(Product,self).save(*args,**kwargs)
    def __str__(self):
        return f"{self.name} ({self.product_unique_id})"





