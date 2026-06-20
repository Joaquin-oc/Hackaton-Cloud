# Hackaton UTEC Cloud Computing 2026-1  <img width="22" height="18" alt="image" src="https://github.com/user-attachments/assets/523cd109-270b-451a-86eb-d49ca1e7f8b9" />


Integrantes:
- Joaquin Andre Ocaña Aniya
- Benjamin Mario Augusto Suarez Arzapalo
- Valeria Valentina Ríos Gómez

Solución: 

JOBMATCH AI es una plataforma que permite al candidato subir un archivo CSV con cantidad de ofertas laborales. El sistema procesa cada oferta de forma asíncrona usando un modelo de lenguaje (LLM) a través de la **API de Groq**, y devuelve un análisis personalizado basado en el perfil del usuario.

## Despliegue Paso a Paso

### Descripción del Despliegue 

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

### Instalaciones
- Verificar que tiene instalado node.js > v20, npm aws CLI. 
Correr los siguientes comandos
```bash
node -v
npm -v
aws --version 
```
- Ademas instalar serverless
```bash
sudo npm install -g serverless
```



