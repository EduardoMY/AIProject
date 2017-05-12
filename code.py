#appJar used to implement GUI

from appJar import gui
from pyswip import Prolog
                    
def formatText(word):
    rWord=word.lower().replace(" ", "")
    
    for l in rWord:
        if l < 'a' or l> 'z':
            rWord=""
            break
        
    return rWord

def formatNumber(number):
    rNumber = number.replace(" ", "")
    if not rNumber.isdigit():
        return "NaN"
    else:
        return rNumber
    
def formatKey(key):
    rKey = key.lower().replace(" ", "")
    
    if rKey=="":
        return ""
    
    if formatText(rKey[0]) =="":
        return ""
    for n in rKey[1:-1]:
        if n < '0' or n > '9':
            return ""
    return rKey
    
def vueloExists(clave):
    if vuelosCounter and list(prolog.query("vuelo("+clave+", O, D, C)")):
        return True
    else:
        return False
    

def aeropuertoExists(clave):
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
        prolog.retractall("vuelo(K,"+clave+", D, C)")
        
    if vuelosCounter != 0:
        vuelosCounter -= len(list(prolog.query("vuelo(K, O, "+clave+", C)")))
        prolog.retractall("vuelo(K, O, "+clave+", C)")
    
def deleteAeropuerto(clave):
    prolog.retract("aeropuerto("+clave+",X)")
    global aeropuertosCounter
    aeropuertosCounter -= 1
    
def changeVuelo(clave, origen, destino, costo):
    deleteVuelo(clave)
    addVuelo(clave, origen, destino, costo)

def changeAeropuerto(clave, name):
    deleteAeropuerto(clave)
    addAeropuerto(clave, name)
        
def abcAeropuerto(btn):
    clave = formatText(app.getEntry("aeropuertoClave"))
    nombre = formatText(app.getEntry("aeropuertoName"))
    
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
            deleteAllVuelos(clave)
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
    clave = formatKey(app.getEntry("vueloClave"))
    origen = formatText(app.getEntry("aeropuertoOrigen"))
    destino = formatText(app.getEntry("aeropuertoDestino"))
    costo = formatNumber(app.getEntry("Costo"))

    if clave== "":
        app.warningBox("Error", "No se encontro clave")
    elif btn == "_Alta":
        if not vueloExists(clave):
            if origen != "" and destino != "" and costo != "":
                if aeropuertoExists(origen) and aeropuertoExists(destino) and origen != destino:
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
            app.warningBox("Error", "Esa clave no esta ligada a ningun Vuelo")
            
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
    
def menu(btn):
    aeropuertoOrigen = formatText(app.getEntry("flight0"))
    aeropuertoDestino = formatText(app.getEntry("flight1"))
    escalas = formatNumber(app.getOptionBox("Escalas"))
    resultados = []
    if btn=="Salir":
        app.stop()
    elif btn == "Ayuda":
        message="=========Ayuda=======\n"
        message += "==> Aeropuerto\n"
        message += "* Alta: Es necesario tener clave y nombre.\n"
        message += "* Baja: Solo se necesita una clave valida.\n"
        message += "* Cambio: Solo se necesita una clave valida, el nombre se cambiara.\n"
        message += "** Clave y Nombre deben de ser formato alfabetico (a-z).\n"
        message += "==> Vuelo\n"
        message += "* Alta: Es necesario tener clave y aeropuerto Origen, Destino y Costo (valor entero positivo).\n"
        message += "* Baja: Solo se necesita una clave (de vuelo) valida.\n"
        message += "* Cambio: Se basa en la clave de vuelo valida. Todo cambia menos la clave de vuelo.\n"
        message += "** Clave de Origen y Destino son alfabetico. Costo es numero entero.\n"
        message += "** Origen y Destino no pueden ser el mismo valor.\n"
        message += "** Clave de vuelo debe de ser letra(1) + numeros(n).\n"
        message += "==> Consultas\n"
        message += "Dependiendo del boton veras los aeropuertos o vuelos\n"
        message += "==> Encontrar vuelos\n"
        message += "La clave del aeropuerto origen y destino deben de ser validas\n"
        message += "Tienes la opcion de poner escalas [default=0, 3]\n"
        app.infoBox("-- Ayuda --", message)
    else:
        if aeropuertoOrigen != "" and aeropuertoDestino != "":
            if aeropuertoExists(aeropuertoOrigen) and  aeropuertoExists(aeropuertoDestino):
                resultados = list(prolog.query("vuelos("+aeropuertoOrigen+", "+aeropuertoDestino+", "+escalas+", Ciudades, Vuelos, C)"))
                print resultados
                vuelos=""
                ciudades=""
                costo=""
                message=""
                for e in resultados:
                    for c in e['Ciudades']:
                        ciudades+= str(c) + ","
                    for v in e['Vuelos']:
                        vuelos+= str(v) + ","
                    costo=str(e['C'])
                    message += "Ciudades:" + ciudades + "\nVuelos:" + vuelos + "\nCosto: " + costo+"\n----------------\n"
                    ciudades=""
                    vuelos=""
                    costo=""
                app.infoBox("Resultados - Busqueda", message)
            else:
                app.warningBox("Error", "Hubo un problema con las claves. El sistema no las reconocio.")
        else:
            app.warningBox("Error", "Las claves no son validas.")
        
app = gui("Programa de aviones")
prolog = Prolog()

aeropuertosCounter = 0
vuelosCounter = 0 
'''
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
'''
prolog.consult("/home/emedina/Documents/AIProject/aviones.prolog")

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
#app.addLabelOptionBox("aeropuertoOrigen", ["-E-"],5, 1, 2)
app.addLabel("aeropuertoDestino", "Destino", 5, 2, 1)
app.addEntry("aeropuertoDestino", 5, 3, 1)
#app.addLabelOptionBox("aeropuertoDestino", ["-E-"],5, 3, 2)
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
app.addButtons(["Obtener viajes", "Ayuda","Salir"], menu, 12, 0, 4)

app.go()
