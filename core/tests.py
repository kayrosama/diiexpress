from config.wsgi import *
import string
import random

from core.erp.models import *
from core.homepage.models import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.user.models import User

numbers = list(string.digits)

dashboard = Dashboard()
dashboard.name = 'EXPRESS PN'
dashboard.icon = 'fas fa-fax'
dashboard.layout = 1
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.sidebar = 'sidebar-dark-navy'
dashboard.save()

moduletype = ModuleType()
moduletype.name = 'Adm.Seguridad'
moduletype.icon = 'fas fa-lock'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for i in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for i in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Usuarios'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'S.Paquetería'
moduletype.icon = 'fas fa-file-import'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 2
module.name = 'Compañia'
module.url = '/erp/company/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-building'
module.description = 'Permite gestionar la información de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Company._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Tamaños'
module.url = '/erp/size/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-ruler'
module.description = 'Permite administrar los tamaños de los paquetes'
module.save()
for i in Permission.objects.filter(content_type__model=Size._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Tarifas'
module.url = '/erp/tariff/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe'
module.description = 'Permite administrar las tarifas de los paquetes'
module.save()
for i in Permission.objects.filter(content_type__model=Tariff._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Bodega de Paquetes'
module.url = '/erp/packages/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-dolly'
module.description = 'Permite administrar las bodega de los paquetes'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Ciudades'
module.url = '/erp/city/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-city'
module.description = 'Permite administrar las ciudades para los destinos'
module.save()
for i in Permission.objects.filter(content_type__model=City._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Condiciones'
module.url = '/erp/condition/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-book'
module.description = 'Permite administrar las condiciones de los paquetes'
module.save()
for i in Permission.objects.filter(content_type__model=Condition._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Clientes'
module.url = '/erp/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar los clientes de la empresa'
module.save()
for i in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Talento Humano'
moduletype.icon = 'fas fa-user-check'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 3
module.name = 'Empleados'
module.url = '/erp/employee/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-tie'
module.description = 'Permite administrar los empleados del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Employee._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Tipo de Eventos'
module.url = '/erp/event/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-business-time'
module.description = 'Permite administrar los tipos de eventos de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=EventType._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Eventos'
module.url = '/erp/events/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-business-time'
module.description = 'Permite administrar los eventos de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Events._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Rubros de Rol de pago'
module.url = '/erp/headings/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-invoice-dollar'
module.description = 'Permite administrar los rubros de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Headings._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Control de Asist.'
module.url = '/erp/assistance/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar las asistencias de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Assistance._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Roles de Pago'
module.url = '/erp/salary/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dollar-sign'
module.description = 'Permite administrar los roles de pago de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Salary._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Inventario'
moduletype.icon = 'fa-solid fa-boxes-stacked'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 4
module.name = 'Proveedores'
module.url = '/erp/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-people-carry-box'
module.description = 'Permite administrar a los proveedores de las compras'
module.save()
for i in Permission.objects.filter(content_type__model=Provider._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Categorías'
module.url = '/erp/category/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar las categorías de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Productos'
module.url = '/erp/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los productos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Product._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Compras'
module.url = '/erp/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dolly-flatbed'
module.description = 'Permite administrar las compras de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Purchase._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Página Principal'
moduletype.icon = 'fab fa-buffer'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 5
module.name = 'Comentarios'
module.url = '/comments/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-comments'
module.description = 'Permite administrar los comentarios de los clientes'
module.save()
for i in Permission.objects.filter(content_type__model=Comments._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Servicios'
module.url = '/services/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-broom'
module.description = 'Permite administrar los servicios de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Services._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Preguntas frecuentes'
module.url = '/frequent/questions/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-question-circle'
module.description = 'Permite administrar las preguntas frecuentes de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=FrequentQuestions._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Redes Sociales'
module.url = '/social/networks/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-question-circle'
module.description = 'Permite administrar las redes sociales de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=SocialNetworks._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Testimonios'
module.url = '/testimonials/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comment-alt'
module.description = 'Permite administrar los testimonios de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Testimonials._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Equipo de Trabajo'
module.url = '/team/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-friends'
module.description = 'Permite administrar los equipos de trabajo'
module.save()
for i in Permission.objects.filter(content_type__model=Team._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Facturación'
moduletype.icon = 'fas fa-shopping-cart'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 6
module.name = 'Servicios/Paqueteria'
module.url = '/erp/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-store-alt'
module.description = 'Permite administrar las ventas de la empresa'
module.save()
for i in Permission.objects.filter(content_type__model=Sale._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 6
module.name = 'Control de Ruta/Envio'
module.url = '/erp/shipping/route/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-location-crosshairs'
module.description = 'Permite administrar los controles de ruta de los paquetes'
module.save()
for i in Permission.objects.filter(content_type__model=ShippingRoute._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Informes'
moduletype.icon = 'fas fa-chart-pie'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 7
module.name = 'Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de las ventas'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Empleados'
module.url = '/reports/employee/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de los empleados'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Salarios'
module.url = '/reports/salary/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de los salarios de los empleados'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Compras'
module.url = '/reports/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de las compras de los proveedores'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Respaldo de base'
module.url = '/reports/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de los respaldos de base de datos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Inventarios de Prod.'
module.url = '/reports/inventory/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de los inventarios de los productos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Control de rutas'
module.url = '/reports/shipping/route/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de los controles de ruta de envío'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Gestión de Prod./Serv.'
module.url = '/reports/sale/products/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de los productos y servicios en las ventas'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Gestión de Paquetes'
module.url = '/reports/sale/packages/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los informes de la paqueteria en bodega'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Cambiar password'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

group = Group()
group.name = 'Administrador'
group.save()
print(f'insertado {group.name}')

for m in Module.objects.filter():
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

user = User()
user.names = 'William Jair Dávila Vargas'
user.username = 'admin'
user.dni = ''.join(random.choices(numbers, k=10))
user.email = 'davilawilliam93@gmail.com'
user.is_active = True
user.is_superuser = True
user.is_staff = True
user.set_password('hacker94')  # 3xpr3ss2022
user.save()
user.groups.add(group)
print(f'Bienvenido {user.names}')
