import pickle

class FeeSlabCalculator:
    @staticmethod
    def calculate(cgpa: float) -> str:
        if cgpa >= 8.5:
            return "First Slab"
        elif cgpa >= 8.0:
            return "Second Slab"
        elif cgpa >= 7.5:
            return "Third Slab"
        else:
            return "No slab assigned"

class DataValidator:
    @staticmethod
    def validate_cgpa(cgpa: float) -> bool:
        return 0 <= cgpa <= 10

    @staticmethod
    def validate_attendance(attendance: float) -> bool:
        return 0 <= attendance <= 100

    @staticmethod
    def validate_marks(marks: list) -> bool:
        for mark in marks:
            if mark < 0 or mark > 100:
                return False
        return True

class Student:
    """
    Represents a student with basic academic details.
    """
    def __init__(self, student_id: int, name: str, marks: list, attendance: float):
        self.id = student_id
        self.name = name
        self.marks = marks  
        self.cgpa = self._compute_cgpa(marks)
        self.attendance = attendance  
        self.fee_slab = FeeSlabCalculator.calculate(self.cgpa)

    def _compute_cgpa(self, marks: list) -> float:
        total = sum(marks)
        average = total / len(marks)
        return average / 10.0


    def is_eligible(self) -> bool:
        return self.attendance >= 75.0

    def display_info(self):
        print("ID:", self.id)
        print("Name:", self.name)
        print("Marks:", " ".join(str(mark) for mark in self.marks))
        print("Calculated CGPA:", self.cgpa)
        print("Attendance:", f"{self.attendance}%")
        print("Fee Slab:", self.fee_slab)
        print("Exam Eligibility:", "Eligible" if self.is_eligible() else "Not Eligible")

class BSTNode:
    def __init__(self, student: Student):
        self.student = student
        self.left = None
        self.right = None

class StudentBST:
    """
    A simple Binary Search Tree for managing student records.
    """
    def __init__(self):
        self.root = None

    def insert(self, student: Student):
        self.root = self._insert_rec(self.root, student)

    def _insert_rec(self, node: BSTNode, student: Student) -> BSTNode:
        if node is None:
            return BSTNode(student)
        if student.id < node.student.id:
            node.left = self._insert_rec(node.left, student)
        elif student.id > node.student.id:
            node.right = self._insert_rec(node.right, student)
        else:
            print(f"Student with id {student.id} already exists.")
        return node

    def search(self, student_id: int) -> Student:
        node = self._search_rec(self.root, student_id)
        return node.student if node else None

    def _search_rec(self, node: BSTNode, student_id: int) -> BSTNode:
        if node is None or node.student.id == student_id:
            return node
        if student_id < node.student.id:
            return self._search_rec(node.left, student_id)
        else:
            return self._search_rec(node.right, student_id)

    def delete(self, student_id: int):
        self.root = self._delete_rec(self.root, student_id)

    def _delete_rec(self, node: BSTNode, student_id: int) -> BSTNode:
        if node is None:
            print(f"Student with id {student_id} not found.")
            return node
        if student_id < node.student.id:
            node.left = self._delete_rec(node.left, student_id)
        elif student_id > node.student.id:
            node.right = self._delete_rec(node.right, student_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_student = self._min_value(node.right)
            node.student = min_student
            node.right = self._delete_rec(node.right, min_student.id)
        return node

    def _min_value(self, node: BSTNode) -> Student:
        current = node
        while current.left is not None:
            current = current.left
        return current.student

    def inorder(self, students: list):
        self._inorder_rec(self.root, students)

    def _inorder_rec(self, node: BSTNode, students: list):
        if node:
            self._inorder_rec(node.left, students)
            students.append(node.student)
            self._inorder_rec(node.right, students)

class MaxHeap:
    """
    Custom Max Heap implementation using an array.
    Each element is a tuple: (cgpa, -student_id, student)
    This ensures that the student with the highest CGPA and then smallest ID comes first.
    """
    def __init__(self):
        self._data = []

    def insert(self, element: tuple):
        """Insert an element into the heap."""
        self._data.append(element)
        self._heapify_up(len(self._data) - 1)

    def remove(self, student_id: int):
        """Remove an element from the heap by matching student_id."""
        index = None
        for i, (_, neg_id, student) in enumerate(self._data):
            if student.id == student_id:
                index = i
                break
        if index is None:
            return  # Student not found in the heap
        self._data[index] = self._data[-1]
        self._data.pop()
        if index < len(self._data):
            self._heapify_down(index)
            self._heapify_up(index)

    def sorted_elements(self) -> list:
        """
        Return a list of elements sorted in descending order
        without modifying the underlying heap.
        """
        return sorted(self._data, reverse=True)

    def _heapify_up(self, index: int):
        parent = (index - 1) // 2
        if index > 0 and self._data[index] > self._data[parent]:
            self._data[index], self._data[parent] = self._data[parent], self._data[index]
            self._heapify_up(parent)

    def _heapify_down(self, index: int):
        size = len(self._data)
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < size and self._data[left] > self._data[largest]:
            largest = left
        if right < size and self._data[right] > self._data[largest]:
            largest = right
        if largest != index:
            self._data[index], self._data[largest] = self._data[largest], self._data[index]
            self._heapify_down(largest)

class StudentService:
    """
    Provides services for managing students including insertion, deletion, searching,
    and ranking based on CGPA using a custom max heap.
    """
    def __init__(self):
        self.student_bst = StudentBST()
        self.ranking_queue = MaxHeap()

    def add_student(self, student: Student):
        self.student_bst.insert(student)
        # Insert into max heap with key (cgpa, -student.id, student)
        self.ranking_queue.insert((student.cgpa, -student.id, student))

    def search_student(self, student_id: int) -> Student:
        return self.student_bst.search(student_id)

    def remove_student(self, student_id: int):
        self.student_bst.delete(student_id)
        self.ranking_queue.remove(student_id)

    def display_ranking(self):
        sorted_ranking = self.ranking_queue.sorted_elements()
        if not sorted_ranking:
            print("No students available for ranking.")
            return
        print("\n=== Student Ranking (by CGPA Descending) ===")
        rank = 1
        for cgpa, neg_id, student in sorted_ranking:
            print(f"Rank {rank}:")
            student.display_info()
            print("---------------------------")
            rank += 1

    def display_all_students(self):
        students = []
        self.student_bst.inorder(students)
        if not students:
            print("No student records to display.")
            return
        print("\n=== All Student Records (Sorted by ID) ===")
        for student in students:
            student.display_info()
            print("---------------------------")

class PersistenceManager:
    @staticmethod
    def save_students(students: list, filename: str):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(students, file)
            print("Students saved successfully.")
        except Exception as e:
            print("Error saving students:", e)

    @staticmethod
    def load_students(filename: str) -> list:
        students = []
        try:
            with open(filename, 'rb') as file:
                students = pickle.load(file)
            print("Students loaded successfully.")
        except Exception as e:
            print("Error loading students:", e)
        return students

def create_student():
    try:
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Student Name: ")
        num_subjects = int(input("Enter number of subjects: "))
        marks = []
        for i in range(num_subjects):
            mark = float(input(f"Enter marks for subject {i+1}: "))
            marks.append(mark)
        attendance = float(input("Enter Attendance percentage: "))
        student = Student(student_id, name, marks, attendance)
        if not DataValidator.validate_cgpa(student.cgpa):
            raise ValueError("Invalid CGPA value.")
        if not DataValidator.validate_attendance(student.attendance):
            raise ValueError("Invalid attendance value.")
        if not DataValidator.validate_marks(student.marks):
            raise ValueError("Invalid marks detected.")
        return student
    except ValueError as ve:
        print("Error:", ve)
        return None

def main():
    student_service = StudentService()
    while True:
        print("\n=== Academic Exam Result Management ===")
        print("1. Insert Student Record (Admin)")
        print("2. Delete Student Record (Admin)")
        print("3. Search Student by ID")
        print("4. Display Ranking (by CGPA)")
        print("5. Display All Records (Inorder Traversal)")
        print("6. Save All Records")
        print("7. Load Records")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        choice = int(choice)
        if choice == 1:
            student = create_student()
            if student is not None:
                student_service.add_student(student)
                print("Student inserted successfully.")
        elif choice == 2:
            student_id = int(input("Enter student ID to delete: "))
            student_service.remove_student(student_id)
            print("If existed, student record has been deleted.")
        elif choice == 3:
            student_id = int(input("Enter student ID to search: "))
            found = student_service.search_student(student_id)
            if found:
                print("Student Found:")
                found.display_info()
            else:
                print(f"Student with id {student_id} not found.")
        elif choice == 4:
            student_service.display_ranking()
        elif choice == 5:
            student_service.display_all_students()
        elif choice == 6:
            students = []
            student_service.student_bst.inorder(students)
            filename = input("Enter filename to save records: ")
            PersistenceManager.save_students(students, filename)
        elif choice == 7:
            filename = input("Enter filename to load records: ")
            loaded_students = PersistenceManager.load_students(filename)
            if loaded_students:
                student_service = StudentService()
                for student in loaded_students:
                    student_service.add_student(student)
        elif choice == 8:
            print("Exiting the system. Bye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
