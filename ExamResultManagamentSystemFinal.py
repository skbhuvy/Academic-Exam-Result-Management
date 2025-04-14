import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import pickle
import os

class PersistenceManager:
    @staticmethod
    def save_data(filename, data):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    @staticmethod
    def load_data(filename):
        try:
            if os.path.exists(filename):
                with open(filename, 'rb') as file:
                    return pickle.load(file)
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            return None

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
            if not isinstance(mark, (int, float)) or mark < 0 or mark > 100:
                return False
        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        return isinstance(name, str) and name.replace(" ", "").isalpha()

    @staticmethod
    def validate_id(student_id) -> bool:
        return isinstance(student_id, int) and student_id > 0

class Student:
    def __init__(self, student_id: int, name: str, marks: list, attendance: float):
        if not DataValidator.validate_id(student_id):
            raise ValueError("Invalid student ID")
        if not DataValidator.validate_name(name):
            raise ValueError("Invalid student name")
        if not DataValidator.validate_marks(marks):
            raise ValueError("Invalid marks - must be between 0 and 100")
        if not DataValidator.validate_attendance(attendance):
            raise ValueError("Invalid attendance - must be between 0 and 100")
            
        self.id = student_id
        self.name = name
        self.marks = marks
        self.cgpa = self._compute_cgpa(marks)
        self.attendance = attendance
        self.fee_slab = FeeSlabCalculator.calculate(self.cgpa)

    def _compute_cgpa(self, marks: list) -> float:
        total = sum(marks)
        average = total / len(marks)
        return round(average / 10.0, 2)

    def is_eligible(self) -> bool:
        return self.attendance >= 75.0

    def display_info(self):
        info = f"ID: {self.id}\nName: {self.name}\nCGPA: {self.cgpa}\nAttendance: {self.attendance}%\nFee Slab: {self.fee_slab}\nEligible: {'Yes' if self.is_eligible() else 'No'}"
        return info

class BSTNode:
    def __init__(self, student: Student):
        self.student = student
        self.left = None
        self.right = None

class StudentBST:
    def __init__(self):
        self.root = None

    def insert(self, student: Student):
        try:
            if self.search(student.id) is not None:
                raise ValueError(f"Student with ID {student.id} already exists.")
            self.root = self._insert_rec(self.root, student)
            return True
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return False

    def _insert_rec(self, node: BSTNode, student: Student) -> BSTNode:
        if node is None:
            return BSTNode(student)
        if student.id < node.student.id:
            node.left = self._insert_rec(node.left, student)
        elif student.id > node.student.id:
            node.right = self._insert_rec(node.right, student)
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
    def __init__(self):
        self._data = []

    def insert(self, element: tuple):
        self._data.append(element)
        self._heapify_up(len(self._data) - 1)

    def remove(self, student_id: int):
        index = None
        for i, (_, neg_id, student) in enumerate(self._data):
            if student.id == student_id:
                index = i
                break
        if index is None:
            return
        self._data[index] = self._data[-1]
        self._data.pop()
        if index < len(self._data):
            self._heapify_down(index)
            self._heapify_up(index)

    def sorted_elements(self) -> list:
        return sorted(self._data, reverse=True)

    def _heapify_up(self, index: int):
        parent = (index - 1) // 2
        if index > 0 and self._data[index][:2] > self._data[parent][:2]:
            self._data[index], self._data[parent] = self._data[parent], self._data[index]
            self._heapify_up(parent)

    def _heapify_down(self, index: int):
        size = len(self._data)
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < size and self._data[left][:2] > self._data[largest][:2]:
            largest = left
        if right < size and self._data[right][:2] > self._data[largest][:2]:
            largest = right
        if largest != index:
            self._data[index], self._data[largest] = self._data[largest], self._data[index]
            self._heapify_down(largest)

class StudentService:
    def __init__(self):
        self.student_bst = StudentBST()
        self.ranking_queue = MaxHeap()
        self.load_data()

    def add_student(self, student: Student):
        try:
            if self.student_bst.insert(student):
                self.ranking_queue.insert((student.cgpa, -student.id, student))
                self.save_data()
                messagebox.showinfo("Success", "Student added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_student(self, student_id: int) -> Student:
        return self.student_bst.search(student_id)

    def remove_student(self, student_id: int):
        try:
            if self.student_bst.search(student_id) is None:
                messagebox.showinfo("Info", f"Student with ID {student_id} not found.")
                return
            self.student_bst.delete(student_id)
            self.ranking_queue.remove(student_id)
            self.save_data()
            messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_ranking(self):
        sorted_ranking = self.ranking_queue.sorted_elements()
        if not sorted_ranking:
            messagebox.showinfo("Info", "No students available for ranking.")
            return
        ranking_text = "=== Student Ranking (by CGPA Descending) ===\n"
        rank = 1
        for cgpa, neg_id, student in sorted_ranking:
            ranking_text += f"Rank {rank}:\nID: {student.id}\nName: {student.name}\nCGPA: {student.cgpa}\nAttendance: {student.attendance}%\n---------------------------\n"
            rank += 1
        messagebox.showinfo("Student Ranking", ranking_text)

    def display_all_students(self):
        students = []
        self.student_bst.inorder(students)
        if not students:
            messagebox.showinfo("Info", "No student records to display.")
            return
        all_students_text = "=== All Student Records (Sorted by ID) ===\n"
        for student in students:
            all_students_text += f"ID: {student.id}\nName: {student.name}\nCGPA: {student.cgpa}\nAttendance: {student.attendance}%\n---------------------------\n"
        messagebox.showinfo("All Students", all_students_text)

    def save_data(self):
        students = []
        self.student_bst.inorder(students)
        data = {
            'students': students,
            'ranking': self.ranking_queue._data
        }
        PersistenceManager.save_data('student_data.pkl', data)

    def load_data(self):
        data = PersistenceManager.load_data('student_data.pkl')
        if data:
            for student in data.get('students', []):
                self.student_bst.insert(student)
            for item in data.get('ranking', []):
                self.ranking_queue._data.append(item)
            self.ranking_queue._data.sort(reverse=True)

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str, role: str):
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return False
        if username in self.users:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return False
        self.users[username] = {"password": password, "role": role}
        self.save_users()
        messagebox.showinfo("Success", f"{role.capitalize()} registered successfully.")
        return True

    def login(self, username: str, password: str, role: str):
        user = self.users.get(username)
        if user and user["password"] == password and user["role"] == role:
            messagebox.showinfo("Success", f"Login successful as {role}.")
            return True
        messagebox.showerror("Error", "Invalid username, password, or role.")
        return False

    def save_users(self):
        PersistenceManager.save_data('user_credentials.pkl', self.users)

    def load_users(self):
        loaded_users = PersistenceManager.load_data('user_credentials.pkl')
        if loaded_users:
            self.users = loaded_users

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Exam Result Management System")
        self.root.geometry("600x400")
        self.center_window()
        self.user_manager = UserManager()
        self.student_service = StudentService()
        self.current_user = None
        self.data_file_path = None  # To store the current data file path
        self.create_welcome_screen()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_welcome_screen(self):
        self.clear_screen()
        ttk.Label(self.root, text="Welcome to the Academic Portal", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Button(self.root, text="Register", command=self.register_panel).pack(pady=10)
        ttk.Button(self.root, text="Login", command=self.login_panel).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def register_panel(self):
        self.clear_screen()
        ttk.Label(self.root, text="Register Panel", font=("Arial", 14, "bold")).pack(pady=10)
        role = tk.StringVar(value="faculty")
        ttk.Radiobutton(self.root, text="Faculty", variable=role, value="faculty").pack()
        ttk.Radiobutton(self.root, text="Student", variable=role, value="student").pack()
        ttk.Label(self.root, text="Username:").pack()
        username_entry = ttk.Entry(self.root)
        username_entry.pack()
        ttk.Label(self.root, text="Password:").pack()
        password_entry = ttk.Entry(self.root, show="*")
        password_entry.pack()
        ttk.Button(
            self.root,
            text="Register",
            command=lambda: self.handle_register(role.get(), username_entry.get(), password_entry.get()),
        ).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_welcome_screen).pack()

    def handle_register(self, role, username, password):
        if self.user_manager.register(username, password, role):
            self.create_welcome_screen()

    def login_panel(self):
        self.clear_screen()
        ttk.Label(self.root, text="Login Panel", font=("Arial", 14, "bold")).pack(pady=10)
        role = tk.StringVar(value="faculty")
        ttk.Radiobutton(self.root, text="Faculty", variable=role, value="faculty").pack()
        ttk.Radiobutton(self.root, text="Student", variable=role, value="student").pack()
        ttk.Label(self.root, text="Username:").pack()
        username_entry = ttk.Entry(self.root)
        username_entry.pack()
        ttk.Label(self.root, text="Password:").pack()
        password_entry = ttk.Entry(self.root, show="*")
        password_entry.pack()
        ttk.Button(
            self.root,
            text="Login",
            command=lambda: self.handle_login(role.get(), username_entry.get(), password_entry.get()),
        ).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_welcome_screen).pack()

    def handle_login(self, role, username, password):
        if self.user_manager.login(username, password, role):
            self.current_user = {"role": role, "username": username}
            if role == "faculty":
                self.faculty_dashboard()
            elif role == "student":
                self.student_dashboard()

    def faculty_dashboard(self):
        self.clear_screen()
        ttk.Label(self.root, text="Faculty Dashboard", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create a frame for the file operations buttons
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=5)
        
        ttk.Button(file_frame, text="Save Data", command=self.save_data_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Load Data", command=self.load_data_dialog).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.root, text="Add Student", command=self.add_student).pack(pady=5)
        ttk.Button(self.root, text="Search Student", command=self.search_student).pack(pady=5)
        ttk.Button(self.root, text="Delete Student", command=self.delete_student).pack(pady=5)
        ttk.Button(self.root, text="Display Ranking", command=self.display_ranking).pack(pady=5)
        ttk.Button(self.root, text="Display All Students", command=self.display_all_students).pack(pady=5)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def student_dashboard(self):
        self.clear_screen()
        ttk.Label(self.root, text="Student Dashboard", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(self.root, text="Enter Your Student ID:").pack()
        student_id_entry = ttk.Entry(self.root)
        student_id_entry.pack()
        ttk.Button(
            self.root,
            text="View Profile",
            command=lambda: self.view_profile(student_id_entry.get()),
        ).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def save_data_dialog(self):
        # Ask for file path to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            title="Save student data to..."
        )
        
        if not file_path:  # User cancelled
            return
            
        try:
            # Prepare data for saving
            students = []
            self.student_service.student_bst.inorder(students)
            data = {
                'students': students,
                'ranking': self.student_service.ranking_queue._data
            }
            
            # Save using PersistenceManager
            PersistenceManager.save_data(file_path, data)
            self.data_file_path = file_path
            messagebox.showinfo("Success", f"Student data saved successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def load_data_dialog(self):
        # Ask for file path to load
        file_path = filedialog.askopenfilename(
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            title="Select student data file to load"
        )
        
        if not file_path:  # User cancelled
            return
            
        try:
            # Clear current data
            self.student_service = StudentService()
            
            # Load data
            data = PersistenceManager.load_data(file_path)
            if data:
                for student in data.get('students', []):
                    self.student_service.student_bst.insert(student)
                for item in data.get('ranking', []):
                    self.student_service.ranking_queue._data.append(item)
                self.student_service.ranking_queue._data.sort(reverse=True)
                
                self.data_file_path = file_path
                messagebox.showinfo("Success", f"Student data loaded successfully from:\n{file_path}")
            else:
                messagebox.showinfo("Info", "No valid student data found in the selected file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def add_student(self):
        try:
            student_id = simpledialog.askinteger("Input", "Enter Student ID (must be positive integer):", parent=self.root, minvalue=1)
            if student_id is None:
                return
                
            name = simpledialog.askstring("Input", "Enter Student Name (letters only):", parent=self.root)
            if not name or not DataValidator.validate_name(name):
                messagebox.showerror("Error", "Invalid name. Please use only letters and spaces.")
                return
                
            num_subjects = simpledialog.askinteger("Input", "Enter number of subjects (1-10):", parent=self.root, minvalue=1, maxvalue=10)
            if num_subjects is None:
                return
                
            marks = []
            for i in range(num_subjects):
                mark = simpledialog.askfloat("Input", f"Enter marks for subject {i + 1} (0-100):", parent=self.root, minvalue=0, maxvalue=100)
                if mark is None:
                    return
                marks.append(mark)
                
            attendance = simpledialog.askfloat("Input", "Enter Attendance percentage (0-100):", parent=self.root, minvalue=0, maxvalue=100)
            if attendance is None:
                return
                
            student = Student(student_id, name, marks, attendance)
            self.student_service.add_student(student)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_student(self):
        student_id = simpledialog.askinteger("Input", "Enter Student ID to search:", parent=self.root, minvalue=1)
        if student_id is None:
            return
        student = self.student_service.search_student(student_id)
        if student:
            messagebox.showinfo("Student Found", student.display_info())
        else:
            messagebox.showinfo("Info", f"Student with ID {student_id} not found.")

    def delete_student(self):
        student_id = simpledialog.askinteger("Input", "Enter Student ID to delete:", parent=self.root, minvalue=1)
        if student_id is None:
            return
        self.student_service.remove_student(student_id)

    def display_ranking(self):
        self.student_service.display_ranking()

    def display_all_students(self):
        self.student_service.display_all_students()

    def view_profile(self, student_id_str):
        try:
            student_id = int(student_id_str)
            student = self.student_service.search_student(student_id)
            if student:
                messagebox.showinfo("Profile", student.display_info())
            else:
                messagebox.showinfo("Info", f"Student with ID {student_id} not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student ID (numbers only)")

    def logout(self):
        self.current_user = None
        self.create_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()