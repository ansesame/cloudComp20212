# Tablero para el cuidado cardiaco

En este repositorio se presentan dos versión de un tablero que presenta visualizaciones referentes a posibles determinantes de enfermedades cardíacas con datos extraidos desde Kaggle, y desarrollado con la librería Dash de Python.

1. En la carpeta appCardiaca se encuentra una versión que permite suscribirse a un sistema de mensajería que envía periodicamente recomendaciones sobre el cuidado del corazón. Esto por medio de los servicios Lambda y SNS de AWS.

2. En la carpeta appCardiaca_Docker_DB se encuentra una versión del tablero que almacena la información en una base de datos y es desplegado usando Docker y Docker Compose.
