from .Generalmatrix import Matrix


class MatrixOperations(Matrix):
    """
    Matrix operations class for performing mathematical operations on
    matrices. The operation are carried out between 2 matrices or between a matrix
    and a scaler

    Attributes:
        matrix: (array)        represents the first input in the operations.
        other : (float,array)  represents the second input in the operations.
    """
    def __init__(self, dims, fill):
        Matrix.__init__(dims=(self.rows, self.cols),fill=0)

    def matrix_addition(self, other):

        """
        Function creates and performs addtion operations.
        The operation is performed on between 2 matrices or between a scaler
        object - a single value.

        Parameters
        ----------
        self: matrix
            the original matrix

        other: float or matrix
            the second object which can be a float or a matrix
        Returns
        -------
            matrix: which is a sum of the original matrix and the other object
        """
        # Create a new matrix
        C = Matrix(dims=(self.rows, self.cols), fill=0)

        # Check if the other object is of type Matrix
        if isinstance(other, Matrix):
            # Add the corresponding element of 1 matrices to another
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.mat[i][j] + other.mat[i][j]

        # If the other object is a scaler
        elif isinstance(other, (int, float)):
            # Add that constant to every element of A
            for i in range(self.rows):
                for j in range(self.cols):
                    C.mat[i][j] = self.mat[i][j] + other

        return C

    def right_matrix_addition(self, other):
        """
        Function performs right addition  by calling left addition

        Parameters
        ----------
        other : float or matrix
            the second object

        Returns
        -------
        matrix : a sum of the original matric and a scaler or a second matrix.
        """
        return self.matrix_addition(other)

    def matrix_multiplication(self, other):
        """
        Function performs  multiplication between
        a matrix and a scaler or matrix

        steps: - Create a matrix
               - identify the other object (float or matrix)
               - Scaler multiplication
               - Point-wise multiplication
               - matrix-matrix multiplication

        Parameters
        ----------
        other: float or matrix
            second object to peform multiplication with the original matrix

        Returns
        -------
        Result_matrix:
            Result matrix the same number of rows and columns as the original matrix
        """
        # Createa a new matrix
        C = Matrix(dims=(self.rows, self.cols), fill=0)
        if isinstance(other, Matrix):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.mat[i][j] = self.mat[i][j] * other.mat[i][j]

        # Scaler multiplication
        elif isinstance(other, (int, float)):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.mat[i][j] = self.mat[i][j] * other

        return C

    # Point-wise multiplication is also commutative
    def right_matrix_multiplication(self, other):
        """Function performs point-wise multiplication
        This operation can be performed on matrices of the same dimensions

        Parameters
        ----------
        other: float or matrix
            second object to peform multiplication with the original matrix

        Returns
        -------
        Result_matrix:
            Result matrix the same number of rows and columns as the original matrix

        """
        return self.matrix_multiplication(other)

    # matrix-matrix multiplication
    def two_matrix_multiplication(self, other):
        """Function performs  multiplication between 2 matrices
        This operation can be performed on matrices of different sizes

        Parameters
        ----------
        other:matrix
            second object to peform multiplication with the original matrix
        Returns
        -------
        Result_matrix:
            The result matrix has the number of rows of the first and the number of columns of the second matrix.
        """

        if isinstance(other, Matrix):
            C = Matrix(dims=(self.rows, self.cols), fill=0)

            # Multiply the elements in the same row of the first matrix
            # to the elements in the same col of the second matrix
            for i in range(self.rows):
                for j in range(self.cols):
                    acc = 0

                    for k in range(self.rows):
                        acc += self.mat[i][k] * other.mat[k][j]

                    C.mat[i][j] = acc

        return C

    def __getitem__(self, key):
        """Function instatiates a matrix object

        Parameters
        ----------
        key: row or column

        Returns
        -------
        matrix
        """
        if isinstance(key, tuple):
            i = key[0]
            j = key[1]
            return self.mat[i][j]

    def __setitem__(self, key, value):
        """Function instatiates a scaler object

        Parameters
        ----------
        key: row, column

        Returns
        -------
         value: float
        """
        if isinstance(key, tuple):
            i = key[0]
            j = key[1]
            self.mat[i][j] = value

