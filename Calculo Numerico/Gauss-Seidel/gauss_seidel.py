# Resolvedor de sistemas de ecuaciones lineales por Gauss-Seidel
# Autor: Santiago Pinto             Fecha: 2024-05-15

import numpy as np

class Gauss_Seidel:

    __MSG_ERROR_NO_TENSOR = "'%s' no es un tensor de numpy"

    def __init__(self, coeficientes=None, terms_indep=None):
        if coeficientes == None and terms_indep == None:
            self.__coeficientes = None
            self.__terms_indep = None
            self.__variables = None
            self.__resuelto = None #tri-estado
        elif coeficientes == None ^ terms_indep == None:
            raise TypeError("ambos parametros deben proporcionarse o ser None")
        else:
            self.__comprobar_atributos(coeficientes, terms_indep)
            # Se usa internamente las traspuestas de los tensores por simplicidad
            # (aunque no es convencional)
            self.__coeficientes = coeficientes.transpose().astype(np.float64)
            self.__terms_indep = terms_indep.transpose().astype(np.float64)
            self.__variables = np.zeros(coeficientes.shape[:1], np.float64)
            self.__resuelto = False

    def resolver(self, coeficientes, terms_indep, error_abs_max=1e-6, iteraciones_max=50):
        self.__init__(coeficientes, terms_indep)
        pass

    @staticmethod
    def __comprobar_atributos(coeficientes, terms_indep):
        if not isinstance(coeficientes, np.ndarray):
            raise TypeError(Gauss_Seidel.__MSG_ERROR_NO_TENSOR % "coeficientes")
        if not isinstance(terms_indep, np.ndarray):
            raise TypeError(Gauss_Seidel.__MSG_ERROR_NO_TENSOR % "terms_indep")
        if coeficientes.ndim != 2:
            raise TypeError("'coeficientes' no es una matriz (2D)")
        if not (terms_indep.ndim == 2 and terms_indep.shape[1] == 1):
            raise TypeError("'terms_indep' no es un vector columna (2D - len(2a_dim)==1)")
        if coeficientes.shape[0] != terms_indep.shape[0]:
            raise ValueError("La matriz de coeficientes y el vector de"
                             " términos independientes no tienen el mismo"
                             " número de filas")
        if coeficientes.shape[0] != coeficientes.shape[1]:
            raise TypeError("La matriz de coeficientes no es cuadrada")
