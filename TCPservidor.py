from socket import *

servidorPuerto = 12000
servidorSocket = socket(AF_INET,SOCK_STREAM)
servidorSocket.bind(('',servidorPuerto))
servidorSocket.listen(1)
print("El servidor está listo para recibir mensajes")
while 1:
    #Confirmación conexión
    conexionSocket, clienteDireccion = servidorSocket.accept()
    print("Conexión establecida con ", clienteDireccion)
    mensajeBienvenida = """Bienvenido al minibanquito
    Aquí puede:
    Consultar su saldo [1]
    Debitar de su cuenta [2]
    Acreditar a la cuenta [3] """
    conexionSocket.send(bytes(mensajeBienvenida, "utf-8"))

    mensaje = str( conexionSocket.recv(1024), "utf-8" )
    print("Mensaje recibido de ", clienteDireccion)
    print(mensaje)

    mensajeRespuesta = mensaje.upper()
    print(mensajeRespuesta)
    conexionSocket.send(bytes(mensajeRespuesta, "utf-8"))
    conexionSocket.close()
