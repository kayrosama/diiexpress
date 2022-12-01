MONTHS = (
    ('', '-----------'),
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre')
)

TYPE_HEADINGS = (
    ('ingress', 'INGRESOS'),
    ('egress', 'EGRESOS'),
)

CALCULATION_METHOD = (
    ('salary', 'Se calcula con el salario neto'),
    ('amount', 'Se ingresa una cantidad y valor'),
    ('value', 'Se calcula con un valor'),
)

TYPE_SALE = (
    ('housekeeping', 'Limpieza'),
    ('parcel_service', 'Paqueteria'),
)

STATUS_SENDING = (
    ('received', 'Recibido'),
    ('on_route', 'En Ruta'),
    ('delivered', 'Entregado'),
)

TYPE_PRODUCT = (
    ('product', 'Produto'),
    ('service_day', 'Servicio por día'),
    ('service_hour', 'Servicio por horas'),
)
