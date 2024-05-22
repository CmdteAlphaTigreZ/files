# Resolvedor de sistemas de ecuaciones lineales por Gauss-Seidel
# Autor: Santiago Pinto             Fecha: 2024-05-15

import numpy as np

class Gauss_Seidel:

    __MSG_ERROR_NO_TENSOR = "'%s' no es un tensor de numpy"
    __MSG_ERROR_AMBOS_TENSORES = "tanto 'coeficientes' como 'terms_indep' deben proporcionarse o ser None"

    def __init__(self, coeficientes=None, terms_indep=None, estandar=True):
        if coeficientes == None and terms_indep == None:
            self.__coeficientes = None
            self.__terms_indep = None
            self.__variables = None
            self.__resuelto = None #tri-estado
        elif coeficientes == None ^ terms_indep == None:
            raise TypeError(Gauss_Seidel.__MSG_ERROR_AMBOS_TENSORES)
        else:
            self.__comprobar_atributos(coeficientes, terms_indep, estandar)
            # Se usa internamente las traspuestas de los tensores
            # por simplicidad (aunque no es convencional).
            # Si es estandar, se realizan las conversiones apropiadas
            if estandar:
                self.__coeficientes = coeficientes.transpose().astype(np.float64)
                self.__terms_indep = terms_indep.transpose().astype(np.float64)
            else:
                self.__coeficientes = coeficientes.astype(np.float64)
                self.__terms_indep = terms_indep.astype(np.float64)
            self.__variables = np.zeros(self.__coeficientes.shape[:1], np.float64)
            self.__resuelto = False

    def resolver(self, coeficientes=None, terms_indep=None,
                 error_abs_max=1e-6, iteraciones_max=50, estandar=True):
        if coeficientes != None and terms_indep != None:
            self.__init__(coeficientes, terms_indep, estandar)
            variables = self.__variables
        elif coeficientes == None ^ terms_indep == None:
            raise TypeError(Gauss_Seidel.__MSG_ERROR_AMBOS_TENSORES)
        else:
            if self.__resuelto == None:
                raise RuntimeError("Objeto '%s' no inicializado"
                                   % str(type(self)) )
            if self.__resuelto and isinstance(self.__variables, np.ndarray) \
                and self.__variables.shape == self.__coeficientes.shape[:1]:
                return self.__variables
            try:
                self.__comprobar_atributos(self.__coeficientes,
                                           self.__terms_indep, estandar=False)
            except (TypeError, ValueError) as e:
                raise RuntimeError("Objeto '%s' en estado inválido"
                                   % str(type(self)) ) from e
            variables = self.__variables \
                = np.zeros(self.__coeficientes.shape[:1], np.float64)

        coeficientes, terms_indep = self.__coeficientes, self.__terms_indep
        self.__ajustar_diagonal()
        pass

    def __ajustar_diagonal(self, coeficientes=None, terms_indep=None, variables=None):
        if all(arg != None for arg in (coeficientes, terms_indep, variables)):
            self.__coeficientes, self.__terms_indep, self.__variables \
                = coeficientes, terms_indep, variables
        for permutacion in self.__permutar_indices():
            coeficientes = self.__coeficientes[permutacion]
            if np.diag(coeficientes).all():
                # Por ahora no se hace nada con las variables
                self.__coeficientes = coeficientes
                return
        raise ValueError("La matriz de coeficientes no se puede reordenar"
                         " para que tenga una diagonal sin ceros")

    def __permutar_indices(self, cant_indices=None):
        if cant_indices == None:
            cant_indices = self.__coeficientes.shape[0]
        permutacion = np.empty((cant_indices,), np.int64)
        indices = [i for i in range(cant_indices - 1, -1, -1)]
        yield from self.__permutar_indices_rec(indices, permutacion, cant_indices - 1)

    @staticmethod
    def __permutar_indices_rec(indices, permutacion, indice_perm):
        if indice_perm < 0:
            yield permutacion
        for i, indice in enumerate(indices):
            if indice == None:
                continue
            permutacion[indice_perm] = indice
            indices[i] = None
            yield from Gauss_Seidel.__permutar_indices_rec(indices, permutacion, indice_perm - 1)
            indices[i] = indice

    @staticmethod
    def __comprobar_atributos(coeficientes, terms_indep, estandar=True):
        if not isinstance(coeficientes, np.ndarray):
            raise TypeError(Gauss_Seidel.__MSG_ERROR_NO_TENSOR % "coeficientes")
        if not isinstance(terms_indep, np.ndarray):
            raise TypeError(Gauss_Seidel.__MSG_ERROR_NO_TENSOR % "terms_indep")
        if coeficientes.ndim != 2:
            raise TypeError("'coeficientes' no es una matriz (2D)")
        if estandar:
            if not (terms_indep.ndim == 2 and terms_indep.shape[1] == 1):
                raise TypeError("'terms_indep' no es un vector columna"
                                " (2D, len(2a_dim)==1)")
            if coeficientes.shape[0] != terms_indep.shape[0]:
                raise ValueError("La matriz de coeficientes y el vector de"
                                " términos independientes no tienen el mismo"
                                " número de filas")
        else:
            if not terms_indep.ndim == 1:
                raise TypeError("'terms_indep' no es un vector fila"
                                " (1D, modo no estandar)")
            if coeficientes.shape[1] != terms_indep.shape[0]:
                raise ValueError("La matriz de coeficientes y el vector de"
                                " términos independientes no tienen el mismo"
                                " número de columnas (modo no estandar)")
        if coeficientes.shape[0] != coeficientes.shape[1]:
            raise TypeError("La matriz de coeficientes no es cuadrada")
