import NumPy as np

A = np.array([[1, 2, 1], [2, -1, 1], [3, 1, -1]])
B = np.array([4, 1, -2])
x = np.linalg.solve(A, B)

print(x)
