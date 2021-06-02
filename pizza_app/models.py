from django.db import models
from django.utils.translation import gettext_lazy as _
import re
import random
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if 'first_name' not in postData or len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters."
        if 'last_name' not in postData or len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        email_usage = self.filter(email = postData['email'])
        if email_usage:
            errors['email'] = "Email already exists"
        if 'password' not in postData or len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "The passwords do not match!"
        return errors

    def updateaccount_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors["firstname"] = " First Name should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['updated_email']):
            errors['updated_email'] = ('Invalid email Address')
        email_check = self.filter(email=postData['updated_email'])
        if email_check:
            errors['updated_email'] = "Email already in use"
        if 'updated_state' not in postData:
            errors['updated_state'] = 'Add a state'
        if len(postData['updated_address']) < 2:
            errors["updated_address"] = "Add a valid address"
        if len(postData['updated_city']) < 2:
            errors["updated_city"] = "Add a valid city"
        return errors

    def pizza_validator(self, postData):
        errors = {}
        if 'method' not in postData:
            errors['method'] = 'Add a method'
        if 'size' not in postData:
            errors['size'] = 'Add a pizza size'
        if 'crust' not in postData:
            errors['crust'] = 'Add crust type'
        if 'qty' not in postData:
            errors['qty'] = 'Add a quantity'
        if 'topping' not in postData:
            errors['topping'] = 'Add toppings'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            address = postData['address'],
            city = postData['city'],
            state = postData['state'],
            password = pw
        )

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Order(models.Model):
    CARRYOUT = "Carryout"
    DELIVERY = "Delivery"
    method_choices = [
        (CARRYOUT,"carryout"),
        (DELIVERY,"delivery")
    ]
    method = models.CharField(max_length=2,choices=method_choices,default=DELIVERY)
    price = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    delivery_price=models.DecimalField(max_digits=6, decimal_places=0, default=0)
    qty = models.IntegerField()
    user = models.ForeignKey(User, related_name="orders", on_delete = models.CASCADE)
    favorite = models.ForeignKey(User, related_name="favorites", on_delete = models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Pizza(models.Model):
    VEGGIE = "VEGETERIAN"
    PEPPERONI= "PEPERONI"
    MARGHERITA = "MARGHERITA"
    BBQ="BARBEQUE"
    HAWAIIAN="HAWAII"
    BUFFALO="BUFFALO"
    SUPREME="SUPREME"
    type_choices = [
        (VEGGIE,"veggie"),
        (PEPPERONI,"pepperoni"),
        (MARGHERITA,"margherita"),
        (BBQ,"bbq"),
        (HAWAIIAN,"hawaiian"),
        (BUFFALO,"buffalo"),
        (SUPREME,"supreme"),
    ]
    types = models.CharField(max_length=2,choices=type_choices,default=VEGGIE)
    LARGE = "LARGE"
    NORMAL= "NORMAL"
    SMALL = "SMALL"
    size_choices= [
        (LARGE,"large"),
        (NORMAL,"normal"),
        (SMALL,"small"),
    ]
    size=models.CharField(max_length=2,choices=size_choices,default=NORMAL)
    THIN_CRUST = "THIN CRUST"
    THICK_CRUST = "THICK CRUST"
    crust_choices=[
        (THIN_CRUST , "thin_crust"),
        (THICK_CRUST , "thick_crust"),
    ]
    crust=models.CharField(max_length=3,choices=crust_choices,default= THIN_CRUST)
    order=models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        null= True,
        related_name="pizza",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    