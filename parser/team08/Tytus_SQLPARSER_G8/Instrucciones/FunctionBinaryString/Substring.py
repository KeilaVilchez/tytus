from Instrucciones.Identificador import Identificador
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato
from Instrucciones.Expresiones.Primitivo import Primitivo
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.Excepcion import *

class Substring(Instruccion):
    def __init__(self, valor, inicio, fin, tipo, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna)
        self.valor = valor
        self.inicio = inicio
        self.fin = fin

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        if isinstance(self.valor, Primitivo):
            if self.valor.tipo.tipo== Tipo_Dato.CHAR or self.valor.tipo.tipo== Tipo_Dato.VARCHAR or self.valor.tipo.tipo== Tipo_Dato.VARYING or self.valor.tipo.tipo== Tipo_Dato.CHARACTER or self.valor.tipo.tipo== Tipo_Dato.TEXT:
                return str(self.valor.valor)[int(self.inicio):int(self.fin)] 
        elif isinstance(self.valor,Identificador):
            print("FALTA PROGRAMAR PARA IDENTIFICADOR SUBSTRING")
        error = Excepcion('42883',"Semántico",f"No existe la función MD5({self.valor.tipo.toString()})",self.linea,self.columna)
        arbol.excepciones.append(error)
        arbol.consola.append("HINT: Ninguna función coincide en el nombre y tipos de argumentos. Puede ser necesario agregar conversión explícita de tipos.")
        arbol.consola.append(error.toString())
        return error
'''
instruccion = Substring("hola mundo",None, 1,2)
instruccion.ejecutar(None,None)
'''