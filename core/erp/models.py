import base64
import json
import os
from datetime import datetime

from PIL import Image
from crum import get_current_request
from django.db import models
from django.db.models import Sum, FloatField, Q
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.erp.choices import *


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='Ruc')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=20, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=20, verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, verbose_name='Email')
    website = models.CharField(max_length=250, verbose_name='Página web')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    mission = models.CharField(max_length=500, null=True, blank=True, verbose_name='Misión')
    vision = models.CharField(max_length=500, null=True, blank=True, verbose_name='Visión')
    about_us = models.CharField(max_length=500, null=True, blank=True, verbose_name='Acerca de nosotros')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')
    activate_tax = models.BooleanField(default=True, verbose_name='Estado del IVA')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='IVA')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_iva(self):
        return f'{self.iva:.2f}'

    def get_image_in_base64(self):
        try:
            if self.image:
                src = self.image.path
                file = base64.b64encode(open(src, 'rb').read()).decode('utf-8')
                type = Image.open(src).format.lower()
                return f"data:image/{type};base64,{file}"
        except:
            pass
        return ''

    def toJSONDumps(self):
        return json.dumps(self.toJSON())

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['iva'] = f'{self.iva:.2f}'
        item['image_in_base64'] = self.get_image_in_base64()
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Empresa'),
        )
        ordering = ['-id']


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tamaño'
        verbose_name_plural = 'Tamaños'
        ordering = ['-id']


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['-id']


class Tariff(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Ciudad')
    minimum_weight = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Peso mínimo')
    maximum_weight = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Peso máximo')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio')

    def __str__(self):
        return self.city.name

    def get_full_name(self):
        return f'{self.city} ({self.minimum_weight} KG - {self.maximum_weight} KG) = ${self.price}'

    def get_short_name(self):
        return f'{self.city} ({self.minimum_weight} KG - {self.maximum_weight} KG)'

    def toJSON(self):
        item = model_to_dict(self)
        item['short_name'] = self.get_short_name()
        item['full_name'] = self.get_full_name()
        item['city'] = self.city.toJSON()
        item['minimum_weight'] = f'{self.minimum_weight:.2f}'
        item['maximum_weight'] = f'{self.maximum_weight:.2f}'
        item['price'] = f'{self.price:.2f}'
        return item

    class Meta:
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'
        ordering = ['-id']


class Condition(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Condición'
        verbose_name_plural = 'Condiciones'
        ordering = ['-id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=20, unique=True, verbose_name='Número de cedula')
    mobile = models.CharField(max_length=20, unique=True, verbose_name='Teléfono')
    email = models.CharField(max_length=50, unique=True, verbose_name='Correo electrónico')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class Headings(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    type = models.CharField(max_length=50, choices=TYPE_HEADINGS, default=TYPE_HEADINGS[0][0], verbose_name='Tipo')
    calculation_method = models.CharField(max_length=50, choices=CALCULATION_METHOD, default=CALCULATION_METHOD[0][0], verbose_name='Método de cálculo')
    percent = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Porcentaje')
    valor = models.FloatField(default=0.00, verbose_name='Valor')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['calculation_method'] = {'id': self.calculation_method, 'name': self.get_calculation_method_display()}
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['percent'] = f'{self.percent:.2f}'
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if self.calculation_method == CALCULATION_METHOD[0][0]:
                self.valor = self.percent / 100
            elif self.calculation_method == CALCULATION_METHOD[2][0]:
                self.valor = self.percent
        except:
            pass
        super(Headings, self).save()

    class Meta:
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'
        ordering = ['-id']


class Employee(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=20, unique=True, verbose_name='Número de cedula')
    mobile = models.CharField(max_length=20, unique=True, verbose_name='Teléfono')
    email = models.CharField(max_length=50, unique=True, verbose_name='Correo electrónico')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    rmu = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Salario mensual')
    headings = models.ManyToManyField(Headings, verbose_name='Rubros')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['rmu'] = f'{self.rmu:.2f}'
        item['headings'] = [i.toJSON() for i in self.headings.all()]
        return item

    def calculate_headings(self, rmu, type):
        valor = 0.00
        for i in self.headings.filter(state=True, type=type):
            if i.calculation_method == CALCULATION_METHOD[0][0]:
                valor += float(rmu) * i.valor
        return float(round(valor, 2))

    def get_number(self):
        return f'{self.id:06d}'

    def salary_by_day(self):
        return self.rmu / 24

    def count_worked_days(self, year, month):
        return self.assistance_set.filter(date_joined__year=year, date_joined__month=month, state=True).count()

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-id']


class Assistance(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de asistencia')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado')
    details = models.CharField(max_length=500, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.details

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['employee'] = self.employee.toJSON()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.details is None:
            self.details = 's/n'
        elif len(self.details) == 0:
            self.details = 's/n'
        super(Assistance, self).save()

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['id']


class Salary(models.Model):
    date_joined = models.DateField(default=datetime.now)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS, default=0)
    days_work = models.IntegerField(default=0)
    salary_by_day = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rmu_contract = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rmu_month = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    ingress = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    egress = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    discounts = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.employee.names

    def toJSON(self):
        item = model_to_dict(self)
        item['month'] = f'0{self.month}' if self.month < 10 else self.month
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['employee'] = self.employee.toJSON()
        item['rmu_contract'] = f'{self.rmu_contract:.2f}'
        item['rmu_month'] = f'{self.rmu_month:.2f}'
        item['salary_by_day'] = f'{self.salary_by_day:.2f}'
        item['ingress'] = f'{self.ingress:.2f}'
        item['egress'] = f'{self.egress:.2f}'
        item['discounts'] = f'{self.discounts:.2f}'
        item['total'] = f'{self.total:.2f}'
        return item

    def get_ingress(self):
        return self.salarydetail_set.filter(headings__type=TYPE_HEADINGS[0][0]).filter(Q(valor__gt=0.00) | Q(total__gt=0.00))

    def get_egress(self):
        return self.salarydetail_set.filter(headings__type=TYPE_HEADINGS[1][0]).filter(Q(valor__gt=0.00) | Q(total__gt=0.00))

    class Meta:
        verbose_name = 'Salario'
        verbose_name_plural = 'Salarios'
        ordering = ['-id']


class SalaryDetail(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    headings = models.ForeignKey(Headings, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.FloatField(default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def get_heading_name(self):
        if self.headings.calculation_method in [CALCULATION_METHOD[0][0], CALCULATION_METHOD[2][0]]:
            return f'{self.headings.name} ({self.headings.valor})'
        return self.headings.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['salary'])
        item['heading_name'] = self.get_heading_name()
        item['headings'] = {} if self.headings is None else self.headings.toJSON()
        item['valor'] = self.valor
        item['total'] = f'{self.total:.2f}'
        return item

    class Meta:
        verbose_name = 'Salario Detalle'
        verbose_name_plural = 'Salarios Detalles'
        default_permissions = ()
        ordering = ['-id']


class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    put_assist = models.BooleanField(default=True, verbose_name='¿Poner asistencia?')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipo de Eventos'
        default_permissions = ()
        permissions = (
            ('view_event_type', 'Can view Tipo de Eventos'),
            ('add_event_type', 'Can add Tipo de Eventos'),
            ('change_event_type', 'Can change Tipo de Eventos'),
            ('delete_event_type', 'Can delete Tipo de Eventos'),
        )
        ordering = ['-id']


class Events(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado')
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name='Tipo de Evento')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    start_time = models.TimeField(default=datetime.now, verbose_name='Hora de inicio')
    end_time = models.TimeField(default=datetime.now, verbose_name='Hora de finalización')
    details = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.details

    def get_full_name(self):
        return f"{self.event_type.name} desde el {self.format_start_date()} hasta el {self.format_end_date()}"

    def format_start_date(self):
        return self.start_date.strftime('%Y-%m-%d')

    def format_end_date(self):
        return self.end_date.strftime('%Y-%m-%d')

    def format_start_time(self):
        return self.start_time.strftime('%H-%M')

    def format_end_time(self):
        return self.end_time.strftime('%H-%M')

    def toJSON(self):
        item = model_to_dict(self)
        item['employee'] = self.employee.toJSON()
        item['full_name'] = self.get_full_name()
        item['event_type'] = self.event_type.toJSON()
        item['start_date'] = self.format_start_date()
        item['end_date'] = self.format_end_date()
        item['start_time'] = self.format_start_time()
        item['end_time'] = self.format_end_time()
        return item

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-id']


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=20, unique=True, verbose_name='Ruc')
    mobile = models.CharField(max_length=20, unique=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.ruc})'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    type = models.CharField(max_length=30, choices=TYPE_PRODUCT, default=TYPE_PRODUCT[0][0], verbose_name='Tipo')
    code = models.CharField(max_length=8, unique=True, verbose_name='Código')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Compra')
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Venta')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.code}) ({self.category.name})'

    def get_short_name(self):
        if self.type == TYPE_PRODUCT[0][0]:
            return f'{self.name} ({self.category.name})'
        return f'{self.name} ({self.category.name}) - ({self.get_type_display()})'

    def get_or_create_category(self, name):
        category = Category()
        search = Category.objects.filter(name=name)
        if search.exists():
            category = search[0]
        else:
            category.name = name
            category.save()
        return category

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['category'] = self.category.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['pvp'] = f'{self.pvp:.2f}'
        item['image'] = self.get_image()
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_benefit(self):
        benefit = float(self.pvp) - float(self.price)
        return round(benefit, 2)

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Product, self).delete()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


class Purchase(models.Model):
    number = models.CharField(max_length=8, unique=True, verbose_name='Número de factura')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Proveedor')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.purchasedetail_set.all():
            subtotal += float(i.price) * int(i.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchasedetail_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Purchase, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['provider'] = self.provider.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compra'),
            ('add_purchase', 'Can add Compra'),
            ('delete_purchase', 'Can delete Compra'),
        )
        ordering = ['-id']


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['dscto'] = f'{self.dscto:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        default_permissions = ()
        ordering = ['-id']


class Sale(models.Model):
    number = models.CharField(max_length=20, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empleado')
    date_attention = models.DateTimeField(default=datetime.now, verbose_name='Fecha y hora de atención')
    type = models.CharField(max_length=50, choices=TYPE_SALE, default=TYPE_SALE[0][0], verbose_name='Tipo de Venta')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.number} - {self.client.get_full_name()}'

    def get_employee_date_attention(self):
        if self.type == TYPE_SALE[0][0]:
            if self.employee is not None:
                return f"{self.employee.names} / {self.get_date_attention_format()}"
        return '---'

    def get_date_attention_format(self):
        return self.date_attention.astimezone().strftime('%Y-%m-%d %H:%M %p')

    def get_status(self):
        queryset = self.shippingroute_set.all().order_by('-id')
        if queryset.exists():
            return queryset[0].get_status()
        return {'id': '', 'name': ''}

    def is_sale(self):
        return self.type == TYPE_SALE[0][0]

    def get_products(self):
        return self.saleproducts_set.filter(product__type=TYPE_PRODUCT[0][0])

    def get_subtotal_products(self):
        return self.get_products().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result')

    def get_services(self):
        return self.saleproducts_set.filter(product__type=TYPE_PRODUCT[1][0])

    def get_subtotal_services(self):
        return self.get_services().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result')

    def get_subtotal_packages(self):
        return self.salepackages_set.all().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result')

    def generate_number(self):
        return f'{self.id:010d}'

    def calculate_invoice(self):
        subtotal = 0.00
        if self.type == TYPE_SALE[0][0]:
            for i in self.saleproducts_set.all():
                subtotal += float(i.price) * int(i.cant)
        else:
            for i in self.salepackages_set.all():
                subtotal += float(i.subtotal)
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.saleproducts_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        request = get_current_request()
        if request is not None:
            if self.saleproducts_set.all().exists():
                request.session['product_alert'] = True
        # if self.shippingroute_set.all().exists():
        #     request.session['shipping_alert'] = True
        super(Sale, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['employee'] = {} if self.employee is None else self.employee.toJSON()
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['date_attention'] = self.get_date_attention_format()
        item['client'] = self.client.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['status'] = self.get_status()
        item['employee_date_attention'] = self.get_employee_date_attention()
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Venta'),
            ('add_sale', 'Can add Venta'),
            ('delete_sale', 'Can delete Venta'),
        )
        ordering = ['-id']


class ShippingRoute(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')
    status = models.CharField(max_length=30, choices=STATUS_SENDING, default=STATUS_SENDING[0][0])
    date_joined = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name='Comentario')

    def __str__(self):
        return self.comment

    def get_status(self):
        return {'id': self.status, 'name': self.get_status_display()}

    def get_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d %H:%M:%S')

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        item['status'] = self.get_status()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        request = get_current_request()
        request.session['shipping_alert'] = True
        super(ShippingRoute, self).save()

    class Meta:
        verbose_name = 'Ruta de Envio'
        verbose_name_plural = 'Rutas de Envio'
        default_permissions = ()
        permissions = (
            ('view_shipping_route', 'Can view Ruta de Envio'),
            ('add_shipping_route', 'Can add Ruta de Envio'),
            ('delete_shipping_route', 'Can delete Ruta de Envio'),
        )
        ordering = ['-id']


class SaleProducts(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta Producto'
        verbose_name_plural = 'Detalles de Venta Producto'
        default_permissions = ()
        ordering = ['-id']


class SalePackages(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.condition.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['tariff'] = self.tariff.toJSON()
        item['condition'] = self.condition.toJSON()
        item['size'] = self.size.toJSON()
        item['peso'] = f'{self.peso:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta Paquete'
        verbose_name_plural = 'Detalles de Venta Paquetes'
        default_permissions = ()
        ordering = ['-id']
