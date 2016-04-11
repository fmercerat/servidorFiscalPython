from BaseHTTPServer import BaseHTTPRequestHandler
import json
from pyfiscalprinter import epsonFiscal
import os.path

def crearConfig():
    data = {}
    data["puerto"] = raw_input("Ingrese puerto [eg:COM1]: ")
    data["impresora"] = raw_input("Ingrese modelo de impresora [eg:tm-220-af]: ")
    data["prueba"] = raw_input("Ingrese estado de prueba [eg:False]: ")
    
    cad = json.dumps(data)
    
    f = open("conf.json", "w")
    f.write(cad)
    
if not os.path.isfile("conf.json"):
    crearConfig()

f = open("conf.json", "r")
cad = f.read()
data = json.loads(cad)

impresora = data["impresora"]
puerto = data["puerto"]
#prueba = bool(data["prueba"])
prueba = False

if prueba:
    print "Modo prueba\n"

# FUNCION
# 0 - Imprimir Ticket (Descuentos, Devoluciones, Interes, Items[Nombre, Cantidad, PrecioUnitario, Descuento])
# 1 - Cierre Z

class PostHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        #print post_body
        #imprimeTicket(post_body)
        eligeFuncion(post_body)
        return

def eligeFuncion(data):
    res = json.loads(data)
    funcion = int(res['Funcion'])
    print funcion
    if funcion == 0:
        imprimeTicket(data)
        return
    if funcion == 1:
        imprimeCierreZ(data)
        return
    if funcion == 2:
        imprimeCierreX(data)
        return
    
    #Para compatibilidad
    imprimeTicket(data)
    
def imprimeCierreZ(data):
    printer = epsonFiscal.EpsonPrinter(deviceFile=puerto,model=impresora,dummy=prueba)
    printer.dailyClose("Z")

def imprimeCierreX(data):
    printer = epsonFiscal.EpsonPrinter(deviceFile=puerto,model=impresora,dummy=prueba)
    printer.dailyClose("X")

def imprimeTicket(data):
    res = json.loads(data)
    descuentos = float(res['Descuentos'])
    devoluciones = float(res['Devoluciones'])
    interes = float(res['InteresTarjeta'])
    #print "Descuentos: {0}\nDevoluciones: {1}\nInteres: {2}\n".format(descuentos, devoluciones, interes)
    total = 0
    printer = epsonFiscal.EpsonPrinter(deviceFile=puerto,model=impresora,dummy=prueba)
    printer.openBillTicket("B","","","","",epsonFiscal.EpsonPrinter.IVA_TYPE_CONSUMIDOR_FINAL)

    for i in res['Items']:
        cantidad = float(i['Cantidad'])
        nombre = i['Nombre']
        precioUnitario = float(i['PrecioUnitario'])
        descuento = float(i['Descuento'])
        dd = float(0)
        #print "Descuento: {0}".format(descuento)
        if descuento > 0:
            #montoDescuento = precioUnitario * cantidad * descuento
            montoDescuento = descuento
            #print "Descuento Total: {0}".format(montoDescuento)
            printer.addItem(nombre, cantidad, precioUnitario, 21, 0, "", False)
            total = total + precioUnitario * cantidad - montoDescuento
            dd = dd + montoDescuento
        else:
            printer.addItem(nombre, cantidad, precioUnitario, 21, 0, "", False)
            total = total + precioUnitario * cantidad 
        
    if devoluciones > 0:
        printer.addAdditional("Devoluciones", devoluciones, 21, True)
        total = total - devoluciones
        
    if (descuentos + dd) > 0:
        printer.addAdditional("Descuentos", descuentos + dd, 21, True)
        total = total - descuentos
        
    if interes > 1:
        interesTotal = total * (interes - 1)
        #print "Interes Total: {0}".format(interesTotal)
        printer.addAdditional("Interes Tarjeta", interesTotal, 21, False)
        total = total + interesTotal
        
    printer.addPayment("Pago", total)
    printer.closeDocument()
    printer.close()

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 8080), PostHandler)
    print 'Iniciando servidor, use <Ctrl-C> para apagar\nPuerto: ' + data["puerto"] + " Impresora: " + data["impresora"]
    server.serve_forever()
