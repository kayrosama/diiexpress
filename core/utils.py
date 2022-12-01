from django.db.models import Prefetch, F

from config import wsgi
import json
import random
import string
from random import randint

from core.erp.models import *
from core.homepage.models import Comments
from core.security.models import *

numbers = list(string.digits)
letters = list(string.ascii_letters)
alphanumeric = numbers + letters


def insert_entities():
    company = Company()
    company.name = 'Socio Express'
    company.ruc = ''.join(random.choices(numbers, k=13))
    company.email = 'socioexpress_2219@hotmail.com'
    company.phone = ''.join(random.choices(numbers, k=7))
    company.mobile = ''.join(random.choices(numbers, k=10))
    company.desc = 'Somos la solución al courier tradicional, recepción y entrega en el mismo día y en el menor tiempo posible.'
    company.website = 'https://socio.express/'
    company.address = 'Calle Sucre y Comercio junto al Club Olimpia'
    company.iva = 12.00
    company.save()

    names_cities = ['Azuay', 'Cuenca', 'Gualaceo', 'Paute', 'Sigsig', 'Girón', 'San Fernando', 'Santa Isabel', 'Pucará', 'Nabón', 'Galápagos', 'Isabela', 'Santa Cruz', 'Puerto Baquerizo Moreno', 'Puerto Ayora', 'Cañar', 'Cañar', 'Biblián', 'Azogue', 'La Troncal', 'Bolivar', 'Guaranda', 'San Miguel de Bolívar', 'Caluma', 'Chillanes', 'Echeandía', 'Chimbo', 'La Asunción', 'La Magdalena', 'CARCHI',
                    'Mira', 'Bolívar', 'Tulcán', 'El Angel', 'Huaca',
                    'Julio Andrade', 'La Paz', 'San Gabriel', 'Chimborazo', 'Riobamba', 'Guano', 'Chambo', 'Colta', 'Penipe', 'Guamote', 'Pallatanga', 'Alausí', 'Chunchi', 'Cumandá', 'Cajabamba', 'Huigra', 'San Andrés', 'San Juan', 'Cotopaxi', 'Saquisilí', 'Latacunga', 'Pujilí', 'Salcedo', 'Sigchos', 'La Maná', 'Chantillin', 'El Corazón', 'Guaytacama', 'Lasso',
                    'Pastocalle', 'Poalo', 'Tanicuchi', 'Toacaso', 'Mulalo', 'El Oro', 'El Guabo', 'Huaquillas', 'Machala', 'Pasaje', 'Piñas', 'Puerto Bolivar', 'Santa Rosa', 'Zaruma', 'Portovelo', 'Arenillas', 'Atahualpa', 'Balsas', 'Chilla', 'Marcabeli', 'Esmeraldas', 'Guayaquil', 'Daule', 'Duran', 'El Empalme', 'SANTA ELENA', 'Santa Elena', 'La Libertad', 'Salinas', 'LOJA', 'Loja', 'Macara',
                    'Catamayo', 'Cariamanga', 'Celica', 'Macas',
                    'Gualaquiza', 'Limon Indanza', 'Santiago', 'Sucua', 'IMBABURA', 'Ibarra', 'Ambuqui', 'Atuntaqui', 'Cotacachi', 'Otavalo', 'LOS RIOS', 'Babahoyo', 'Buena Fe', 'Puebloviejo', 'Quevedo', 'Ventanas', 'Portoviejo', 'Bahia De Caraquez', 'Chone', 'El Carmen', 'Jipijapa', 'Tena', 'Archidona', 'Baeza', 'El Chaco', 'Carlos Julio Arosemena Tola', 'ORELLANA',
                    'Francisco De Orellana', 'La Joya De Los Sachas', 'Loreto', 'Nuevo Rocafuerte', 'PASTAZA', 'Puyo', 'Mera', 'Palora', 'Shell', 'Arajuno', 'Santo Domingo', 'Alluriquin', 'Luz De América', 'Valle Hermoso', 'Quito', 'Cayambe', 'Conocoto', 'Cumbaya', 'Machachi', 'Nueva Loja', 'Gonzalo Pizarro', 'Putumayo', 'Shushufindi', 'Sucumbios', 'Ambato', 'Baños', 'Cevallos', 'Izamba', 'Mocha',
                    'Zamora', 'Chinchipe', 'Nangaritza', 'Yacuambi',
                    'Yantzaza']

    for i in names_cities:
        if not City.objects.filter(name=i.upper()).exists():
            City(name=i.upper()).save()

    for i in ['GRANDE', 'MEDIANO', 'PEQUEÑO', 'EXTRAGRANDE']:
        Size(name=i).save()

    for i in ['FRAGIL', 'BLANDO', 'RESISTENTE']:
        Condition(name=i).save()

    for i in City.objects.all():
        Tariff(city_id=i.id, minimum_weight=1.00, maximum_weight=3.00, price=random.randint(1, 3)).save()
        Tariff(city_id=i.id, minimum_weight=4.00, maximum_weight=7.00, price=random.randint(4, 7)).save()
        Tariff(city_id=i.id, minimum_weight=8.00, maximum_weight=11.00, price=random.randint(8, 11)).save()

    client = Client()
    client.names = 'William Jair Dávila Vargas'
    client.dni = '0928363993'
    client.mobile = '0979014551'
    client.email = 'williamjair94@hotmail.com'
    client.address = 'Milagro, Guayas Ecuador'
    client.save()


def insert_products():
    Category(name='SERVICIOS').save()
    Product(name='LIMPIEZA DE CASA', category_id=1, code=''.join(random.choices(alphanumeric, k=8)).upper(), type=TYPE_PRODUCT[1][0], pvp=25.00).save()
    Product(name='LIMPIEZA DE MUEBLES', category_id=1, code=''.join(random.choices(alphanumeric, k=8)).upper(), type=TYPE_PRODUCT[1][0], pvp=15.00).save()
    Product(name='LIMPIEZA DE CASA', category_id=1, code=''.join(random.choices(alphanumeric, k=8)).upper(), type=TYPE_PRODUCT[2][0], pvp=5.00).save()
    Product(name='LIMPIEZA DE OFICINA', category_id=1, code=''.join(random.choices(alphanumeric, k=8)).upper(), type=TYPE_PRODUCT[1][0], pvp=20.00).save()
    Product(name='LIMPIEZA DE ESCRITORIOS', category_id=1, code=''.join(random.choices(alphanumeric, k=8)).upper(), type=TYPE_PRODUCT[1][0], pvp=18.00).save()
    Product(name='LIMPIEZA DE OFICINA', category_id=1, code=''.join(random.choices(alphanumeric, k=8)).upper(), type=TYPE_PRODUCT[2][0], pvp=6.00).save()
    with open(f'{settings.BASE_DIR}/deploy/products.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for i in data['rows'][0:80]:
            row = i['value']
            product = Product()
            product.name = row['nombre']
            product.code = ''.join(random.choices(alphanumeric, k=8)).upper()
            product.description = 's/n'
            product.category = product.get_or_create_category(name=row['marca'])
            product.price = randint(1, 10)
            product.pvp = (float(product.price) * 0.12) + float(product.price)
            product.save()
            print(product.name)


def insert_purchase():
    provider = Provider()
    provider.name = 'EXPALSA S.A.'
    provider.ruc = ''.join(random.choices(numbers, k=13))
    provider.email = 'expalsa@gmail.com'
    provider.mobile = ''.join(random.choices(numbers, k=10))
    provider.address = 'Duran'
    provider.save()

    for i in range(1, 5):
        purchase = Purchase()
        purchase.number = ''.join(random.choices(numbers, k=8))
        purchase.provider_id = 1
        purchase.save()

        for d in range(1, 20):
            purchasedetail = PurchaseDetail()
            purchasedetail.purchase_id = purchase.id
            products = Product.objects.filter(type=TYPE_PRODUCT[0][0]).values_list('id', flat=True)
            purchasedetail.product_id = random.choices(products, k=1)[0]
            while purchase.purchasedetail_set.filter(product_id=purchasedetail.product_id).exists():
                purchasedetail.product_id = random.choices(products, k=1)[0]
            purchasedetail.cant = randint(1, 50)
            purchasedetail.price = purchasedetail.product.pvp
            purchasedetail.subtotal = float(purchasedetail.price) * purchasedetail.cant
            purchasedetail.save()
            purchasedetail.product.stock += purchasedetail.cant
            purchasedetail.product.save()

        purchase.calculate_invoice()
        print(i)


# for employee in Employee.objects.all():
#     for day in range(1, 32):
#         date_joined = datetime(2022, 7, day)
#         assistance = Assistance()
#         assistance.employee_id = employee.id
#         assistance.state = random.randint(0, 1)
#         assistance.date_joined = date_joined
#         assistance.save()
#         print(assistance.id)

# insert_entities()
# insert_products()
# insert_purchase()
for i in Sale.objects.filter(type=TYPE_SALE[0][0]):
    i.date_attention = i.date_joined
    i.employee_id = random.randint(1, Employee.objects.count())
    i.save()
    print(i.id)
