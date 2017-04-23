#appJar used to implement GUI

from appJar import gui
from pyswip import Prolog

def menu(btn):
    if btn=="Cancel":
        app.stop()
    else:
        print "Todos los viajes"
        
def abcAeropuerto(btn):
    if btn == "Alta":
        print "sii"
        app.infoBox("hola", "LOL")
    elif btn == "Baja":
        print "Baja"
    else:
        print "Cambio"

def abcVuelo(btn):
    if btn == "_Alta":
        print "Holis ss"
    elif btn == "_Baja":
        print "_Baja"
    else:
        print "_Cambio"

def show(btn):
    if btn == "Mostrar Aeropuertos":
        print "LALAL"
    else:
        print "LL"
        
app = gui("Programa de aviones")
prolog = Prolog()
prolog.assertz("vuelo(sara)")
prolog.assertz("aeropuerto(uno)")
prolog.assertz("vuelo(sarah)")
#print list(prolog.query("father(michael,X)"))
print list(prolog.query("vuelo(sarah)"))
print list(prolog.query("aeropuerto(dos)"))
prolog.assertz("aeropuerto(tres)")
print list(prolog.query("aeropuerto(tres)"))

app.addLabel("titleAeropuertos", "Aeropuertos", 0, 0, 4)
app.setLabelBg("titleAeropuertos", "red")
app.addLabel("aeropuertoClave", "Clave", 1, 0, 1)
app.addEntry("aeropuertoClave", 1, 1, 1)
app.addLabel("aeropuertoName", "Nombre", 1, 2, 1)
app.addEntry("aeropuertoName", 1, 3, 1)
app.addButtons(["Alta", "Baja", "Cambio"], abcAeropuerto, 2, 0, 4)

app.addLabel("titleVuelos", "Vuelos" , 3,0,4)
app.setLabelBg("titleVuelos", "red")
app.addLabel("vueloClave", "Clave", 4, 0, 1)
app.addEntry("vueloClave", 4, 1, 1)
app.addLabel("Costo", "costo", 4, 2, 1)
app.addEntry("costo", 4, 3, 1)
app.addLabel("aeropuertoOrigen", "Origen", 5, 0, 1)
app.addEntry("aeropuertoOrigen", 5, 1, 1)
app.addLabel("aeropuertoDestino", "Destino", 5, 2, 1)
app.addEntry("aeropuertoDestino", 5, 3, 1)
app.addButtons(["_Alta", "_Baja", "_Cambio"], abcVuelo, 6, 0, 4)

app.addLabel("consultas", "Consultas", 7, 0, 4)
app.setLabelBg("consultas", "yellow")
app.addButtons(["Mostrar Aeropuertos","Mostrar Vuelos"], show, 8, 0, 4)

app.addLabel("titleFindFlights","Encontrar vuelos", 9, 0, 4)
app.setLabelBg("titleFindFlights", "blue")


app.addLabel("flight0", "Aeropuerto Inicio", 10, 0, 1)
app.addEntry("flight0", 10, 1, 1)
app.addLabel("flight1", "Aeropuerto Destino", 10, 2, 1)
app.addEntry("flight1", 10, 3, 1)
app.addLabelOptionBox("Escalas", ["0", "1", "2", "3"],11, 0, 4 )
app.addButtons(["Obtener viajes", "Salir"], menu, 12, 0, 4)

app.go()

