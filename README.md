# Hackaton UTEC Cloud Computing 2026-1  <img width="22" height="18" alt="image" src="https://github.com/user-attachments/assets/523cd109-270b-451a-86eb-d49ca1e7f8b9" />


Integrantes:
- Joaquin Andre Ocaña Aniya
- Benjamin Mario Augusto Suarez Arzapalo
- Valeria Valentina Ríos Gómez

Solución: 

JOBMATCH AI es una plataforma que permite al candidato subir un archivo CSV con cantidad de ofertas laborales. El sistema procesa cada oferta de forma asíncrona usando un modelo de lenguaje (LLM) a través de la **API de Groq**, y devuelve un análisis personalizado basado en el perfil del usuario.

## Despliegue Paso a Paso

### Descripción

JobMatch AI utiliza Serverless Framework para definir toda la infraestructura como codigo (IaC). El despliegue se realiza desde una instancia EC2 a partir de una AMI llamado Cloud9Ubuntu22. 

### Configuración de Instancia 
• Paso 1: Ingresar al servicio EC2
• Paso 2: Ingresar al menú “Imágenes” / “AMI”
• Paso 3: Buscar “Imágenes públicas” y Cloud9ubuntu22
• Paso 4: Elegir la más reciente y botón “Lanzar instancia a partir de
una AMI”
• Paso 5: Elija “Par de claves” = “vockey”
• Paso 6: En “Configuraciones de Red” marcar:
     “Permitir el tráfico de SSH desde” “Cualquier lugar”
     “Permitir el tráfico de HTTP desde Internet” “Cualquier lugar”
• Paso 7: Configurar 20 Gb de almacenamiento
• Paso 8: Botón “Lanzar instancia”

#### Instalaciones e Configuraciones

1. Verificar que tiene instalado node.js > v20, npm y  aws CLI. 
Correr los siguientes comandos.
```bash
node -v
npm -v
aws --version
```
2. Ademas instalar serverless.
```bash
sudo npm install -g serverless
```
3. Acceda o cree el directorio /home/ubuntu/.aws. Ademas cree el archivo credentials dentro del directorio anterior con el contenido de las credenciales de acceso a AWS.
```bash
mkdir .aws
cd .aws
nano credentials
```
4. Cree un usuario en https://www.serverless.com/ con su correo de @utec y un nombre de Organization. 
<img width="393" height="64" alt="Captura de pantalla 2026-06-20 a la(s) 4 40 21 p  m" src="https://github.com/user-attachments/assets/8443c8b9-8fc4-4fce-b81e-97ca4f44c67a" />

#### Clonar el repositorio 
- Haga git clone del directorio /home/ubuntu/ de este repositorio. Ingrese a la carpeta lambdas
```bash
git clone https://github.com/Joaquin-oc/Hackaton-Cloud.git
cd Hackaton-Cloud
cd lambdas
```
La estructura del proyecto es:

- Modificar el org y role en serverless.yml
<img width="393" height="210" alt="Captura de pantalla 2026-06-20 a la(s) 4 46 10 p  m" src="https://github.com/user-attachments/assets/51162b22-0fb3-46d9-8d74-db106207fd40" />

- Login a serverless y confirmar al correo electronico. 
```bash
serverless login
```
- Exportar la variable del entorno de la API KEY DE GROG. (API AI)
```bash
export GROG_API_KEY = 
```
#### Sobre el contendio del serveless.yml 
Este archivo define toda la infraestructura de JobMatch AI. No necesita crear nada manualmente en la consola de AWS.

El serverless.yml crea automaticamente:
•	7 funciones Lambda con sus triggers configurados
•	1 cola SQS principal 
•	1 Dead Letter Queue para mensajes fallidos despues de 3 intentos automaticos. 
•	3 tablas DynamoDB
•	API Gateway con todos los endpoints HTTP
•	Roles y permisos IAM necesarios

#### Desplegar Infraestructura
- Deployar por defecto en stage dev. 
```bash
serverless deploy
```
o

```bash
sls deploy
```
- Al finalizar, Serverless muestra en pantalla las url's de los endpoints. Estas se configuran en el frontend para invocar a nuestros lambdas. Tambien utilizadas para pruebas en postman. 


### Despliegue del frontend 

### Probar la Plataforma Completa

#### Flujo de prueba paso a paso
1.	Abrir la URL del frontend en el navegador
2.	Registrar perfil: ingresar skills, anos de experiencia y salario esperado
3.	Hacer clic en 'Subir CSV' y seleccionar ofertas_prueba.csv
4.	Hacer clic en 'Analizar ofertas'
5.	Esperar 2 a 3 minutos — la tabla se llena en tiempo real
6.	Verificar que cada oferta muestra score, skills match y resumen



















