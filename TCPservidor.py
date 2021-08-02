from socket import *

servidorPuerto = 12000
servidorSocket = socket(AF_INET,SOCK_STREAM)
servidorSocket.bind(('',servidorPuerto))
servidorSocket.listen(1)
print("El servidor está listo para recibir mensajes")

# Función del banco
def accionesBanco(accion, monto=0):
    if accion=='saldo':
        # Para consultar saldo 
        file = open("saldo.txt", "r")
        return('Saldo: '+file.read())

    elif accion=='debitar':
        # Debitar
        debitar = monto

        file = open("saldo.txt", "r")
        saldo = float(file.read())
        file.close()

        if debitar > saldo:
            return('Saldo insuficiente')
        else:
            saldo -= debitar
            file = open("saldo.txt", "w")
            file.write(str(saldo))
            file.close()
            return('OK')

    elif accion=='acreditar:
        # Acreditar
        acreditar = monto

        file = open("saldo.txt", "r")
        saldo = float(file.read())
        file.close()

        saldo += acreditar

        file = open("saldo.txt", "w")
        file.write(str(saldo))
        file.close()
        return('Nuevo saldo: '+str(saldo))

    else:
        return('Acción no identificada')


#Confirmación conexión
conexionSocket, clienteDireccion = servidorSocket.accept()
print("Conexión establecida con ", clienteDireccion)
mensajeBienvenida = """Bienvenido al minibanquito
    Aquí puede:
    Consultar su saldo [saldo]
    Debitar de su cuenta [debitar X]
    Acreditar a la cuenta [acreditar X]
    Terminar [T]"""
conexionSocket.send(bytes(mensajeBienvenida, "utf-8"))

while 1:
    mensajeEntrada = str( conexionSocket.recv(1024), "utf-8" )
    accion = mensajeEntrada.split()
    
    if accion[0]=='T':
        mensajeSalida = 'Terminar minibanquito'
        conexionSocket.send(bytes(mensajeSalida, "utf-8"))
        conexionSocket.close()
    elif accion[0]=='saldo':
        mensajeSalida = accionesBanco(accion[0])
    else:
        mensajeSalida = accionesBanco(accion[0], float(accion[1]))
    print(mensajeSalida)
    conexionSocket.send(bytes(mensajeSalida, "utf-8"))


