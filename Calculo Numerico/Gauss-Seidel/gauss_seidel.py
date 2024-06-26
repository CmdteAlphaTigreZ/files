# Resolvedor de sistemas de ecuaciones lineales por Gauss-Seidel
# Autor: Santiago Pinto             Fecha: 2024-05-15

import numpy as np

class GaussSeidel:

    __MSG_ERROR_NO_TENSOR = "'%s' no es un tensor de numpy"
    __MSG_ERROR_AMBOS_TENSORES = "tanto 'coeficientes' como 'terms_indep'" \
                                 " deben proporcionarse o ser None"
    __CANT_COMPARADOS = 3  # Véase el método resolver

    def __init__(self, coeficientes=None, terms_indep=None, estandar=True):
        if coeficientes is None and terms_indep is None:
            self.__coeficientes = None
            self.__terms_indep = None
            self.__variables = None
            self.__resuelto = None #tri-estado
        elif (coeficientes is None) ^ (terms_indep is None):
            raise TypeError(GaussSeidel.__MSG_ERROR_AMBOS_TENSORES)
        else:
            self.__comprobar_atributos(coeficientes, terms_indep, estandar)
            # Se usa internamente las traspuestas de los tensores
            # por simplicidad (aunque no es convencional).
            # Si es estandar, se realizan las conversiones apropiadas
            if estandar:
                self.__coeficientes = coeficientes.transpose().astype(np.float64)
                self.__terms_indep = np.ravel(terms_indep).astype(np.float64)
            else:
                self.__coeficientes = coeficientes.astype(np.float64)
                self.__terms_indep = terms_indep.astype(np.float64)
            self.__variables = np.zeros(self.__coeficientes.shape[:1], np.float64)
            self.__resuelto = False
        self.__error_abs_max_real = float("Inf")
        self.__iteraciones_reales = 0

    def resolver(self, coeficientes=None, terms_indep=None,
                 error_abs_max=1e-6, iteraciones_max=50, estandar=True):
        if coeficientes is not None and terms_indep is not None:
            self.__init__(coeficientes, terms_indep, estandar)
            variables = self.__variables
        elif (coeficientes is None) ^ (terms_indep is None):
            raise TypeError(GaussSeidel.__MSG_ERROR_AMBOS_TENSORES)
        else:
            if self.__resuelto is None:
                raise RuntimeError("Objeto '%s' no inicializado"
                                   % str(type(self)) )
            if self.__resuelto and isinstance(self.__variables, np.ndarray) \
                and self.__variables.shape == self.__coeficientes.shape[:1] \
                and (self.__error_abs_max_real <= error_abs_max
                     or self.__iteraciones_reales >= iteraciones_max):
                variables = self.__variables
                return (variables[:, np.newaxis] if estandar else variables) \
                       .copy()  # Copia del 'return' final
            try:
                self.__comprobar_atributos(self.__coeficientes,
                                           self.__terms_indep, estandar=False)
            except (TypeError, ValueError) as e:
                raise RuntimeError("Objeto '%s' en estado inválido"
                                   % str(type(self)) ) from e
            variables = self.__variables \
                = np.zeros(self.__coeficientes.shape[:1], np.float64)
        if np.linalg.det(self.__coeficientes) == 0:
            raise ValueError("El sistema de ecuaciones no tiene solución")

        self.__ajustar_diagonal()
        terms_indep = self.__terms_indep
        diagonal = np.diag(self.__coeficientes)
        resto = self.__coeficientes.copy()
        np.fill_diagonal(resto, 0)
        variables_anteriores = np.empty(variables.shape, np.float64)
        cant_comparados = self.__CANT_COMPARADOS
        if (cant_comparados <= iteraciones_max):
            errores_abs_max = np.empty(cant_comparados)
            # Se descarta el primer error porque puede estar sesgado
            # debido a la estimación inicial de las variables
            for j in range(-1, cant_comparados):
                variables_anteriores[:] = variables
                for i in range(variables.size):
                    variables[i] = (terms_indep[i] - variables.dot(resto[:, i])) \
                                / diagonal[i]
                errores_abs_max[j] = np.abs(variables - variables_anteriores).max()
            if all(errores_abs_max[i + 1] > errores_abs_max[i]
                   for i in range(cant_comparados - 1) ):
                # Puede que no cubra todos los casos posibles
                # (ej., divergencia convexa)
                raise RuntimeError("La sucesión de soluciones no es convergente."
                                "  El método de Gauss-Seidel no es apropiado")
            del errores_abs_max
            cant_comparados += 1  # Cuenta la iteración extra
        else:
            cant_comparados = 0
        # Copia de arriba, no comprobación de convergencia y sí de error absoluto
        for iteraciones_reales in range(iteraciones_max - cant_comparados):
            variables_anteriores[:] = variables
            for i in range(variables.size):
                variables[i] = (terms_indep[i] - variables.dot(resto[:, i])) \
                               / diagonal[i]
            if np.abs(variables - variables_anteriores).max() <= error_abs_max:
                break
        # Fin de copia
        iteraciones_reales += cant_comparados
        self.__error_abs_max_real = np.abs(variables - variables_anteriores).max()
        self.__iteraciones_reales = iteraciones_reales
        self.__resuelto = True
        return (variables[:, np.newaxis] if estandar else variables).copy()

    def __ajustar_diagonal(self, coeficientes=None, terms_indep=None,
                           variables=None):
        if all(arg is not None for arg in (coeficientes, terms_indep, variables)):
            self.__coeficientes, self.__terms_indep, self.__variables \
                = coeficientes, terms_indep, variables
        for permutacion in self.__permutar_indices():
            # Permutando columnas para no tener que permutar variables luego
            coeficientes = self.__coeficientes[:, permutacion]
            if np.diag(coeficientes).all():
                self.__coeficientes = coeficientes
                self.__terms_indep = self.__terms_indep[permutacion]
                return
        raise ValueError("La matriz de coeficientes no se puede reordenar"
                         " para que tenga una diagonal sin ceros")

    def __permutar_indices(self, cant_indices=None):
        if cant_indices is None:
            cant_indices = self.__coeficientes.shape[1]
        permutacion = np.empty((cant_indices,), np.int64)
        indices = [i for i in range(cant_indices - 1, -1, -1)]
        yield from self.__permutar_indices_rec(indices, permutacion,
                                               cant_indices - 1)

    @staticmethod
    def __permutar_indices_rec(indices, permutacion, indice_perm):
        if indice_perm < 0:
            yield permutacion
        for i, indice in enumerate(indices):
            if indice is None:
                continue
            permutacion[indice_perm] = indice
            indices[i] = None
            yield from GaussSeidel.__permutar_indices_rec(indices, permutacion,
                                                          indice_perm - 1)
            indices[i] = indice

    @staticmethod
    def __comprobar_atributos(coeficientes, terms_indep, estandar=True):
        if not isinstance(coeficientes, np.ndarray):
            raise TypeError(GaussSeidel.__MSG_ERROR_NO_TENSOR % "coeficientes")
        if not isinstance(terms_indep, np.ndarray):
            raise TypeError(GaussSeidel.__MSG_ERROR_NO_TENSOR % "terms_indep")
        if coeficientes.ndim != 2:
            raise TypeError("'coeficientes' no es una matriz (2D)")
        if estandar:
            if not (terms_indep.ndim == 1
                    or terms_indep.ndim == 2 and terms_indep.shape[1] == 1):
                raise TypeError("'terms_indep' no es un vector columna"
                                " (2D, len(2a_dim)==1) ni un vector fila (1D)")
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

def _probar():
    coeficientes = np.arange(9).reshape((3, 3))
    terms_indep = np.arange(1, 4)
    Resolvedor = GaussSeidel()
    locales = locals()
    print("Tipos o valores incorrectos")
    _probar_fallo("Resolvedor.resolver(1)", locales)
    _probar_fallo("Resolvedor.resolver(coeficientes, 1)", locales)
    _probar_fallo("Resolvedor.resolver(coeficientes[np.newaxis], terms_indep)", locales)
    _probar_fallo("Resolvedor.resolver(coeficientes, np.vstack((terms_indep, np.ones(3))) )", locales)
    _probar_fallo("Resolvedor.resolver(coeficientes, np.hstack((terms_indep, np.ones(3))) )", locales)
    _probar_fallo("Resolvedor.resolver(coeficientes, terms_indep[:, np.newaxis], estandar=False)", locales)
    _probar_fallo("Resolvedor.resolver(coeficientes, np.hstack((terms_indep, np.ones(3))), estandar=False)", locales)
    _probar_fallo("Resolvedor.resolver(np.hstack((coeficientes, terms_indep[:, np.newaxis])), terms_indep)", locales)
    print("Matriz de coeficientes singular")
    _probar_fallo("Resolvedor.resolver(coeficientes, terms_indep)", locales)
    print("Sistema no convergente")
    coeficientes[0, 0] = 1
    _probar_fallo("Resolvedor.resolver(coeficientes, terms_indep)", locales)
    print("Matriz de coeficientes diagonalmente dominante")
    coeficientes = np.array( ((20,  4, -5),
                              (-2, 30,  1),
                              ( 7, -1, 35)) )
    for i, j in zip(coeficientes, terms_indep[:, np.newaxis]):
        print(i, j)
    np.set_printoptions(13)
    print(Resolvedor.resolver(coeficientes, terms_indep, error_abs_max=0.5e-6))
    print("Reutilización de calculos",
          Resolvedor.resolver(error_abs_max=0.5e-6),
          Resolvedor.resolver(error_abs_max=0.5e-9),
          Resolvedor.resolver(iteraciones_max=100),
          Resolvedor.resolver(error_abs_max=0.5e-13, iteraciones_max=5),
          Resolvedor.resolver(error_abs_max=0.5e-13),
          sep="\n")
    print("Resultado de numpy",
          np.linalg.solve(coeficientes, terms_indep)[:, np.newaxis],
          sep="\n")
    np.set_printoptions(8)

def _probar_fallo(codigo_fuente, locales):
    try:
        exec(codigo_fuente, globals(), locales)
    except (TypeError, ValueError, RuntimeError) as e:
        print("\t", e, sep="")
    else:
        raise RuntimeError("Prueba fallida:\n" + codigo_fuente)
