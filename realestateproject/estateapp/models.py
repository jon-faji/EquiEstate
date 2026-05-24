from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Property(BaseModel):
    PROPERTY_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ]
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='residential')
    units = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Tenant(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    property = models.OneToOneField(Property, on_delete=models.SET_NULL, null=True, blank=True)
    lease_start = models.DateField()
    lease_end = models.DateField() 
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Transaction(BaseModel):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.property.name} - {self.tenant.last_name} ({self.status})"
    
class SystemProfile(BaseModel):
    profile_name = models.CharField(max_length=100, default="System Administrator")
    email = models.EmailField(default="admin@equiestate.local")
    avatar = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.profile_name