import os

class SparseMatrix:
    def __init__(self, numRows, numCols):
        """
        Initialize a SparseMatrix with given number of rows and columns.
        """
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}  # Dictionary to store non-zero elements

    def setElement(self, row, col, value):
        """
        Set the value at the specified row and column.
        If the value is zero, remove the element from the dictionary to save space.
        """
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]  # Remove zero elements to save space

    def getElement(self, row, col):
        """
        Get the value at the specified row and column.
        Returns 0 if the element is not found in the dictionary.
        """
        return self.elements.get((row, col), 0)  # Returns 0 if not found

    @staticmethod
    def fromFile(filePath):
        """
        Create a SparseMatrix from a file.
        The file should contain the number of rows and columns on the first two lines,
        followed by the non-zero elements in the format (row, col, value).
        """
        matrix = None
        with open(filePath, 'r') as file:
            lines = file.readlines()
            rows = int(lines[0].split('=')[1].strip())
            cols = int(lines[1].split('=')[1].strip())
            matrix = SparseMatrix(rows, cols)
            for line in lines[2:]:
                row, col, value = eval(line.strip())  # Unsafe, replace with proper parsing
                matrix.setElement(row, col, value)
        return matrix

    def toFile(self, filePath):
        """
        Write the SparseMatrix to a file.
        The file will contain the number of rows and columns on the first two lines,
        followed by the non-zero elements in the format (row, col, value).
        """
        with open(filePath, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")

    @staticmethod
    def addMatrices(matrix1, matrix2):
        """
        Add two SparseMatrices and return the result.
        The matrices must have the same dimensions.
        """
        if matrix1.numRows != matrix2.numRows or matrix1.numCols != matrix2.numCols:
            raise ValueError("Matrices dimensions must match for addition.")
        result = SparseMatrix(matrix1.numRows, matrix1.numCols)
        for key in set(matrix1.elements.keys()).union(matrix2.elements.keys()):
            result.setElement(key[0], key[1], matrix1.getElement(key[0], key[1]) + matrix2.getElement(key[0], key[1]))
        return result

    @staticmethod
    def subtractMatrices(matrix1, matrix2):
        """
        Subtract the second SparseMatrix from the first and return the result.
        The matrices must have the same dimensions.
        """
        if matrix1.numRows != matrix2.numRows or matrix1.numCols != matrix2.numCols:
            raise ValueError("Matrices dimensions must match for subtraction.")
        result = SparseMatrix(matrix1.numRows, matrix1.numCols)
        for key in set(matrix1.elements.keys()).union(matrix2.elements.keys()):
            result.setElement(key[0], key[1], matrix1.getElement(key[0], key[1]) - matrix2.getElement(key[0], key[1]))
        return result

    @staticmethod
    def multiplyMatrices(matrix1, matrix2):
        """
        Multiply two SparseMatrices and return the result.
        The number of columns in the first matrix must be equal to the number of rows in the second matrix.
        """
        if matrix1.numCols != matrix2.numRows:
            raise ValueError("Number of columns in first matrix must be equal to number of rows in second matrix.")
        result = SparseMatrix(matrix1.numRows, matrix2.numCols)
        for (i, k) in matrix1.elements.keys():
            for j in range(matrix2.numCols):
                if (k, j) in matrix2.elements:
                    result.setElement(i, j, result.getElement(i, j) + matrix1.getElement(i, k) * matrix2.getElement(k, j))
        return result

def list_files(directory):
    """
    Lists all the text files in the given directory.
    """
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not files:
        print("No files found in the directory.")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    return files

def get_file_choice(files):
    """
    Prompts the user to choose a file from the list.
    """
    while True:
        choice = input("Select a file by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        print("Invalid choice. Please enter a number from the list.")

def main():
    """
    Main function to handle user interaction, perform matrix operations, and save results to a file.
    """
    home_directory = os.path.expanduser("~")
    directory = os.path.join(home_directory, "Desktop/dsa/sparse_matrix/sample_input_for_students/")
    
    # List available files for Matrix 1 and get user choice
    print("Available files for Matrix 1:")
    files1 = list_files(directory)
    file1 = get_file_choice(files1)

    # List available files for Matrix 2 and get user choice
    print("Available files for Matrix 2:")
    files2 = list_files(directory)
    file2 = get_file_choice(files2)

    # Load matrices from files
    matrix1 = SparseMatrix.fromFile(os.path.join(directory, file1))
    matrix2 = SparseMatrix.fromFile(os.path.join(directory, file2))

    # Get the operation from the user
    operation = input("Enter the matrix operation (add, subtract, multiply): ").strip().lower()

    # Perform the chosen operation
    if operation == "add":
        result = SparseMatrix.addMatrices(matrix1, matrix2)
    elif operation == "subtract":
        result = SparseMatrix.subtractMatrices(matrix1, matrix2)
    elif operation == "multiply":
        result = SparseMatrix.multiplyMatrices(matrix1, matrix2)
    else:
        print("Invalid operation")
        return

    # Get the output filename from the user and save the result
    output_filename = input("Enter the output filename: ").strip()
    output_directory = os.path.join(home_directory, "Desktop/dsa(1)/dsa/sparse_matrix/sample_results/")
    os.makedirs(output_directory, exist_ok=True)
    result.toFile(os.path.join(output_directory, output_filename))

    print(f"Result saved to {os.path.join(output_directory, output_filename)}")

if __name__ == "__main__":
    main()
