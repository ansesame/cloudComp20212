from socket import *

servidorNombre = "3.235.19.182" 
servidorPuerto = 12000
clienteSocket = socket(AF_INET, SOCK_STREAM)
clienteSocket.connect((servidorNombre,servidorPuerto))

#Confirmación de conexión y bienvenida
mensajeBienvenida = clienteSocket.recv(1024)
print(str(mensajeBienvenida, "utf-8"))

while 1:
    mensaje = input("Ingrese acción a realizar:")
    clienteSocket.send(bytes(mensaje, "utf-8"))

    mensajeRespuesta = clienteSocket.recv(1024)
    print("Respuesta:\n" + str(mensajeRespuesta, "utf-8"))

    if mensajeRespuesta == 'Terminar minibanquito':
        break
        clienteSocket.close()
