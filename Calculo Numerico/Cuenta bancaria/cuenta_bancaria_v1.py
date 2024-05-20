# Biblioteca simple de gestión de cuentas bancarias
# Autor: Santiago Pinto             Fecha: 2024-04-17

class Cuenta:
    "Cuenta bancaria con titular y saldo.\
\nLos montos están definidos en centésimos."

    __MSG_ERROR_TIPO = "'{:s}' debe ser un '{:s}': '{:!s}'"

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

    @staticmethod
    def __comprobar_tipos(argumentos, tipos, locales):
        "Los argumentos deben ser tipo 'str'"
        for argumento, tipo in zip(argumentos, tipos):
            if not isinstance(eval(argumento, None, locales), tipo):
                raise TypeError(
                    __MSG_ERROR_TIPO.format(argumento, tipo.__name__,
                                            eval(argumento, locals=locales)) )

    def get_titular(self):
        return self.__titular

    def set_titular(self, titular):
        Cuenta.__comprobar_tipos(("titular",), (str,), locals())
        self.__titular = titular

    def get_saldo(self):
        return self.__saldo

