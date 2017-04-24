#appJar used to implement GUI

from appJar import gui
from pyswip import Prolog

def vueloExists(clave):
    #print vuelosCounter
    if vuelosCounter and list(prolog.query("vuelo("+clave+", O, D, C)")):
        return True
    else:
        return False

    
def aeropuertoExists(clave):
    #print aeropuertosCounter
    if aeropuertosCounter and list(prolog.query("aeropuerto("+clave+", X)")):
        return True
    else:
        return False

def addVuelo(clave, origen, destino, costo):
    prolog.assertz("vuelo("+clave+","+origen+","+destino+"," +costo+")")
    global vuelosCounter
    vuelosCounter += 1
    
def addAeropuerto(clave, name):
    prolog.assertz("aeropuerto("+clave+", "+name+")")
    global aeropuertosCounter
    aeropuertosCounter += 1

def deleteVuelo(clave):
    prolog.retract("vuelo("+clave+", O, D, C)")
    global vuelosCounter
    vuelosCounter -= 1

def deleteAllVuelos(clave):
    global vuelosCounter
    
    if vuelosCounter != 0:
        vuelosCounter -= len(list(prolog.query("vuelo(K, "+clave+", D, C)")))
        prolog.retract("vuelo(K,"+clave+", D, C)")
        
    if vuelosCounter != 0:
        vuelosCounter -= len(list(prolog.query("vuelo(K, O, "+clave+", C)")))
        prolog.retract("vuelo(K, O, "+clave+", C)")
    
def deleteAeropuerto(clave):
    prolog.retract("aeropuerto("+clave+",X)")
    deleteAllVuelos(clave)
    global aeropuertosCounter
    aeropuertosCounter -= 1
    
def changeVuelo(clave, origen, destino, costo):
    deleteVuelo(clave)
    addVuelo(clave, origen, destino, costo)

def changeAeropuerto(clave, name):
    deleteAeropuerto(clave)
    addAeropuerto(clave, name)

def menu(btn):
    if btn=="Cancel":
        app.stop()
    else:
        print "Todos los viajes"
        
def abcAeropuerto(btn):
    clave = app.getEntry("aeropuertoClave").lower().replace(" ", "")
    nombre = app.getEntry("aeropuertoName").lower().replace(" ", "")
    
    if clave == "":
      app.warningBox("Error", "No se encontro clave")
      
    elif btn == "Alta":
        if not aeropuertoExists(clave):
            if nombre != "":
                addAeropuerto(clave, nombre)
            else:
                app.warningBox("Error", "Nombre no valido")
        else:
            app.warningBox("Error", "Aeropuerto ya existe")
            
    elif btn == "Baja":
        if aeropuertoExists(clave):
            deleteAeropuerto(clave)
        else:
            app.warningBox("Error","Esa clave no esta ligada a ningun Aeropuerto")
            
    else: #Cambio
        if aeropuertoExists(clave):
            if nombre != "":
                changeAeropuerto(clave, nombre)
            else:
                app.warningBox("Error", "Nombre no valido")
        else:
            app.warningBox("Error","Esa clave no esta ligada a ningun Aeropuerto")

def abcVuelo(btn):
    clave = app.getEntry("vueloClave").lower().replace(" ", "")
    origen = app.getEntry("aeropuertoOrigen").lower().replace(" ", "")
    destino = app.getEntry("aeropuertoDestino").lower().replace(" ", "")
    costo = app.getEntry("Costo").lower().replace(" ", "")

    if clave== "":
        app.warningBox("Error", "No se encontro clave")
    elif btn == "_Alta":
        if not vueloExists(clave):
            if origen != "" and destino != "" and costo != "":
                if aeropuertoExists(origen) and aeropuertoExists(destino):
                    if costo.isdigit():
                        addVuelo(clave, origen, destino, costo)
                    else:
                        app.warningBox("Error", "Costo no es un numero valido")
                else:
                    app.warningBox("Error", "Hubo un problema con los aeropuertos")
            else:
                app.warningBox("Error", "Los datos no son validos")
        else:
            app.warningBox("Error", "Vuelo ya existe")
            
    elif btn == "_Baja":
        if vueloExists(clave):
            deleteVuelo(clave)
        else:
            app.warningBox("Error", "Esa clave no esta ligada a ningun VVuelo")
            
    else:
        if vueloExists(clave):
            if origen != "" and destino != "" and costo != "":
                if aeropuertoExists(origen) and aeropuertoExists(destino):
                    if costo.isdigit():
                        changeVuelo(clave, origen, destino, costo)
                    else:
                        app.warningBox("Error", "Costo no es un numero valido")
                else:
                    app.warningBox("Error", "Hubo un problema con los aeropuertos")
            else:
                app.warningBox("Error", "Los datos no son validos")
        else:
            app.warningBox("Error", "Esa clave no esta ligada a ningun Vuelo")

def show(btn):
    message = ""
    if btn == "Mostrar Aeropuertos":
        if aeropuertosCounter:
            message = "Clave \t Nombre\n\n"
            for a in list(prolog.query("aeropuerto(K, N)")):
                message += a['K'] +"\t"+a['N'] +"\n"
        else:
            message =  "No se encontraron Aeropuertos"
    else:
        if vuelosCounter:
            message = "Clave \t Origen \t Destino \t Costo\n\n"
            for a in list(prolog.query("vuelo(K, O, D, C)")):
                message += a['K'] +"\t"+a['O'] +"\t"+ a['D']+ "\t"+str(a['C']) +"\n"
        else:
            message =  "No se encontraron Vuelos"
    app.infoBox("Resultados", message)
        
app = gui("Programa de aviones")
prolog = Prolog()

aeropuertosCounter = 0
vuelosCounter = 0 

#Informacion por default para pruebas
prolog.assertz("aeropuerto(mxl, mexicali)")
prolog.assertz("aeropuerto(bar, barcelona)")
prolog.assertz("aeropuerto(cal, calcuta)")
prolog.assertz("aeropuerto(dam, damasco)")
prolog.assertz("aeropuerto(est, estambul)")
prolog.assertz("aeropuerto(den, denver)")
aeropuertosCounter =+ 6

prolog.assertz("vuelo(v001, mxl, den, 300)")
prolog.assertz("vuelo(v002, mxl, bar, 125)")
prolog.assertz("vuelo(v003,  bar, cal, 125)")
prolog.assertz("vuelo(v004, cal, den, 125)")
vuelosCounter =+4

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
