from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from model_utils import Choices

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'donor'),
    ('1', 'item_code'),
    ('2', 'item_name'),
    ('3', 'item_quantity'),
    ('4', 'acquired_date'),
)

class Volunteer(models.Model):
    vol_number = models.IntegerField(blank=False, null=False)
    lname = models.CharField(max_length=50)
    fname = models.CharField(max_length=50)
    vol_dob = models.DateTimeField(
        default=timezone.now)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    vol_notes = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)


    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.vol_number)


class Inventory(models.Model):
    donor = models.CharField(max_length=50)
    item_code = models.IntegerField(primary_key=True,blank=False, null=False)
    item_name = models.CharField(primary_key=True,max_length=200)
    item_quantity = models.IntegerField(blank=False)
    acquired_date = models.DateField(default=timezone.now)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def query_portfolio_by_args(**kwargs):
        draw = int(kwargs.get('draw', None)[0])
        length = int(kwargs.get('length', None)[0])
        start = int(kwargs.get('start', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        queryset = Inventory.objects.all()
        total = queryset.count()

        if search_value:
            queryset = queryset.filter(Q(donor__icontains=search_value) |
                                        Q(item_code__icontains=search_value) |
                                        Q(item_name__icontains=search_value) |
                                        Q(item_quantity__icontains=search_value) |
                                        Q(acquired_date__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


