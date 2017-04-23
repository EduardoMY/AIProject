#appJar used to implement GUI

from appJar import gui
from pyswip import Prolog


def aeropuertoExists(clave):
    print aeropuertosCounter
    if aeropuertosCounter and list(prolog.query("aeropuerto("+clave+", X)")):
        return True
    else:
        return False
    
def vueloExists(clave):
    print vuelosCounter
    if vuelosCounter and list(prolog.query("vuelo("+clave+", O, D, C)")):
        return True
    else:
        return False
    
def addAeropuerto(clave, name):
    prolog.assertz("aeropuerto("+clave+", "+name+")")
    global aeropuertosCounter
    aeropuertosCounter += 1
    
def addVuelo(clave, origen, destino, costo):
    prolog.assertz("vuelo("+clave+","+origen+","+destino+"," +costo+")")
    global vuelosCounter
    vuelosCounter += 1

def deleteAeropuerto(clave):
    prolog.retract("aeropuerto("+clave+",X)")
    global aeropuertosCounter
    aeropuertosCounter -= 1

def deleteVuelo(clave):
    prolog.retract("vuelo(m, moda)")
    global vuelosCounter
    vuelosCounter -= 1

def changeAeropuerto(clave, name):
    deleteAeropuerto(clave)
    addAeropuerto(clave, name)

def changeVuelo(clave, origen, destino, costo):
    deleteVuelo(clave)
    addVuelo(clave, origen, destino, costo)

def menu(btn):
    if btn=="Cancel":
        app.stop()
    else:
        print "Todos los viajes"
        
def abcAeropuerto(btn):
    clave = app.getEntry("aeropuertoClave")
    if clave == "":
      app.warningBox("Error", "No se encontro clave")  
    elif btn == "Alta":
        if not aeropuertoExists(clave):
            addAeropuerto(clave, app.getEntry("aeropuertoName"))
        else:
            app.warningBox("Error", "Aeropuerto ya existe")
    elif btn == "Baja":
        if aeropuertoExists(clave):
            deleteAeropuerto(clave)
        else:
            app.warningBox("Error","Esa clave no esta ligada a ningun Aeropuerto")
    else: #Cambio
        if aeropuertoExists(clave):
            changeAeropuerto(clave, app.getEntry("aeropuertoName"))
        else:
            app.warningBox("Error","Esa clave no esta ligada a ningun Aeropuerto")

def abcVuelo(btn):
    clave = app.getEntry("aeropuertoClave")
    if clave== "":
        app.warningBox("Error", "No se encontro clave")
    elif btn == "_Alta":
        print "Holis ss"
    elif btn == "_Baja":
        print "_Baja"
    else:
        print "_Cambio"

def show(btn):
    if btn == "Mostrar Aeropuertos":
        if aeropuertosCounter:
            print list(prolog.query("aeropuerto(Y, X)"))
    else:
        print "LL"
        
app = gui("Programa de aviones")
prolog = Prolog()

aeropuertosCounter = 0
vuelosCounter = 0 

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
app.addLabel("Costo", "Costo", 4, 2, 1)
app.addEntry("Costo", 4, 3, 1)
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

