# Pasos para la instalación del Sistema Factora

# Instaladores

| Nombre                   | Instalador                                                                                                                                                                                                                     |
|:-------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| `Compilador`             | [Python3](https://www.python.org/downloads/release/python-396/ "Python3")                                                                                                                                                      |
| `IDE de programación`    | [Visual Studio Code](https://code.visualstudio.com/ "Visual Studio Code"), [Sublime Text](https://www.sublimetext.com/ "Sublime Text"), [Pycharm](https://www.jetbrains.com/es-es/pycharm/download/#section=windows "Pycharm") |
| `Motor de base de datos` | [Sqlite Studio](https://github.com/pawelsalawa/sqlitestudio/releases "Sqlite Studio"), [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads "PostgreSQL"), [MySQL](https://www.apachefriends.org/es/index.html "MySQL") |

# Pasos de instalación

##### 1) Descomprimir el proyecto en una carpeta de tu sistema operativo

##### 2) Crear un entorno virtual para posteriormente instalar las librerias del proyecto

Para windows:

```bash
python3 -m venv venv 
```

Para linux:

```bash
virtualenv venv -ppython3 
```

##### 3) Instalar el complemento de [weasyprint](https://weasyprint.org/ "weasyprint")

Si estas usando Windows debe descargar el complemento de [GTK3 installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases "GTK3 installer"). En algunas ocaciones se debe colocar en las variables de entorno como primera para que funcione y se debe reiniciar el computador.

Si estas usando Linux debes instalar las [librerias](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#linux "librerias") correspondientes a la distribución que tenga instalado en su computador.

##### 4) Activar el entorno virtual de nuestro proyecto

Para windows:

```bash
cd venv\Scripts\activate.bat 
```

Para Linux:

```bash
source venv/bin/active
```

##### 5) Instalar todas las librerias del proyecto que se encuentran en la carpeta deploy

```bash
pip install -r deploy/requirements.txt
```

##### 6) Crear la tablas de la base de datos a partir de las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

##### 7) Vamos ahora a restaurar la base de datos con un respaldo que tenemos, para eso
debemos borrar las tablas que se crean en django y reiniciamos sus incrementadores desde 0.
Dependiendo la base de datos que tengamos debemos usar los siguientes comandos.
```bash
// RESET INCREMENT SQLITE
delete from auth_permission;
delete from sqlite_sequence where name='auth_permission';
delete from django_content_type;
delete from sqlite_sequence where name='django_content_type';

// RESET INCREMENT POSTGRESQL
delete from public.auth_permission;
ALTER SEQUENCE public.auth_permission_id_seq RESTART WITH 1;
delete from public.django_content_type;
ALTER SEQUENCE public.django_content_type_id_seq RESTART WITH 1;

// RESET INCREMENT MYSQL
delete from auth_permission;
ALTER TABLE auth_permission AUTO_INCREMENT = 1;
delete from django_content_type;
ALTER TABLE django_content_type AUTO_INCREMENT = 1;
```

##### 8) Restauramos la base de datos con el archivo que se encuentra en la carpeta deploy

```bash
python manage.py loaddata deploy/backup.json
```

##### 9) Iniciamos el servidor del proyecto

```bash
python manage.py runserver 
```

Si deseas verlo en toda tu red puedes ejecutarlo asi:

```bash
python manage.py runserver 0:8000 o python manage.py runserver 0.0.0.0:8000
```

##### 10) Iniciar sesión en el sistema (Puede cambiar la clave y usuario que se crea en el archivo core/init.py del paso 7)

```bash
username: admin
password: 3xpr3ss2022
```

------------