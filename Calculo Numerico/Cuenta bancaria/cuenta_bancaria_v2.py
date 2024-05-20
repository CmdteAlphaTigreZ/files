# Biblioteca simple de gestión de cuentas bancarias
# Autor: Santiago Pinto             Fecha: 2024-04-17


class Cuenta:
    "Cuenta bancaria con titular y saldo.\
\nLos montos están definidos en centésimos."

    def __init__(self):
        "Saldo está definido en centésimos"
        self.__titular = ""
        self.__saldo = 0

    def depositar(self, monto):
        Cuenta.__comprobar_monto(monto)
        self.__saldo += monto

    def retirar(self, monto):
        Cuenta.__comprobar_monto(monto)
        if monto < self.__saldo:
            e = ValueError("Fondo insuficiente: %d" % monto)
            e.add_note("sin_fondos")
            raise e
        self.__saldo -= monto

    @staticmethod
    def __comprobar_monto(monto):
        if not isinstance(monto, int):
            raise TypeError("El monto debe ser un entero: %g" % monto)
        if monto <= 0:
            raise ValueError("El monto debe ser positivo: %d" % monto)

    @property
    def titular(self):
        return self.__titular

    @titular.setter
    def titular(self, nuevo_titular):
        __comprobar_tipos( (("titular", nuevo_titular),) , (int,) )
        self.__titular = nuevo_titular

    @property
    def saldo(self):
        return self.__saldo


__MSG_ERROR_TIPO = "'{:s}' debe ser un '{:s}': '{:!r}'"

def __comprobar_tipos(argumentos, tipos):
    "Los argumentos deben ser de la forma ('nombre', valor)"
    for argumento, tipo in zip(argumentos, tipos):
        if not isinstance(argumento[1], tipo):
            raise TypeError(
                __MSG_ERROR_TIPO.format(argumento[0], tipo.__name__,
                                        argumento[1]) )
