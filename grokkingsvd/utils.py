def to_x_y(mat):
    xis = []
    yis = []
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            xis += [i] * v
            yis += [j] * v
    return xis, yis