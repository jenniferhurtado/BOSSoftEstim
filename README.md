# README #

### ¿Qué es BOSSoftEstim? ###

BOSSoftEstim es una herramienta de apoyo a los equipos de desarrollo 
software para la estimación automática de coste y esfuerzo de historias 
de usuario que consiste en una aplicación web con dos funcionalidades
principales: (1) generar un modelo de aprendizaje a partir de las tareas 
que han sido previamente estimadas; y (2) predecir el coste de las 
historias de usuario que aún no han sido evaluadas. Las historias de usuario
se recuperan de un proyecto JIRA que debe ser configurado.

### Dependencias ###

Esta aplicación está disponible solo para Linux (se ha probado en 
Ubuntu 18.04, pero otras distribuciones también podrían servir); 
los paquetes y herramientas necesarios para ejecutarla son:

- git (sudo apt-get install git)
- python (Version 3.6)
- El resto de requisitos se encuentran en el fichero requirements.txt

### Clonar el repositorio ###
En un terminal, moverse al directorio donde se desea guardar el proyecto, 
y clonar el repositorio ejecutando el comando:

> git clone https://github.com/jenniferhurtado/BOSSoftEstim.git

### Preparar el entorno ###
En un terminal, moverse al directorio en el que se ha clonado el 
repositorio, e instalar los requerimientos del fichero requirements.txt.
Se recomienda instalar los paquetes en un entorno virtual

> pip install -r requirements.txt

### Ejecución ###
Para ejecutar el código, abrimos un terminar python. Se recomienda
utilizar ipython

#### Preparar la base de datos ####
Ir al directorio raíz, donde se encuentra el fichero manage.py y ejecutar:
> python manage.py migrate

Esto generará los modelos en la base de datos. Para poder usar la
aplicación, se debe crear al menos un usuario (User) y un perfil (Profile)
con los datos correpondientes al proyecto de JIRA con el que se va a
trabajar.

#### Generar el modelo de entrenamiento ####
Ir al directorio raíz, donde se encuentra el fichero manage.py y ejecutar:
> python manage.py update_model

Esto generará el modelo de entrenamiento necesario para que la aplicación
estime las historias de usuario.


#### Ejecutar el proyecto ####
Ir al directorio raíz, donde se encuentra el fichero manage.py y ejecutar:
> python manage.py runserver 

Esto ejecutará la aplicación en la dirección local 127.0.0.1:8000