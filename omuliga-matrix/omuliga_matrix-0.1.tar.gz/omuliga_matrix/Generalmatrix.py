class Matrix:

    def __init__(self, dims, fill):
        """
        Generic matrix class for creating matrices and
        performing basic operations scalar:matrix or matrix:matrix
        basic operations.

        Attributes:
        dims (int) defines the dimensions of the matrix
        row (int) representing the number of rows in a matrix
        col (int) representing the number of columns in a matrix
        """
        self.rows = dims[0]
        self.cols = dims[1]
        self.mat = [[fill] * self.cols for i in range(self.rows)]

