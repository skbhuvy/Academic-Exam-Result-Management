import java.io.*;
import java.io.*;
import javax.swing.*;
import java.util.*;
import java.awt.*;
import javax.swing.table.*;

class FeeSlabCalculator implements Serializable {
    public static String calculate(double cgpa) {
        if (cgpa >= 8.5) {
            return "First Slab";
        } else if (cgpa >= 8.0) {
            return "Second Slab";
        } else if (cgpa >= 7.5) {
            return "Third Slab";
        } else {
            return "No slab assigned";
        }
    }
}

class DataValidator implements Serializable {
    public static boolean validateCGPA(double cgpa) {
        return cgpa >= 0 && cgpa <= 10;
    }

    public static boolean validateAttendance(double attendance) {
        return attendance >= 0 && attendance <= 100;
    }

    public static boolean validateMarks(double[] marks) {
        for (double mark : marks) {
            if (mark < 0 || mark > 100) {
                return false;
            }
        }
        return true;
    }

    public static boolean validateName(String name) {
        return name.matches("[a-zA-Z\\s]+");
    }
}

class Student implements Serializable {
    public int id;
    public String name;
    public double[] marks;
    public double cgpa;
    public double attendance;
    public String feeSlab;

    public Student(int id, String name, double[] marks, double attendance) {
        this.id = id;
        this.name = name;
        this.marks = marks;
        this.cgpa = computeCGPA(marks);
        this.attendance = attendance;
        this.feeSlab = FeeSlabCalculator.calculate(this.cgpa);
    }

    private double computeCGPA(double[] marks) {
        double total = 0;
        for (double mark : marks) {
            total += mark;
        }
        double average = total / marks.length;
        return average / 10.0;
    }

    public boolean isEligible() {
        return attendance >= 75.0;
    }

    // Format marks as a string
    public String getMarksAsString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < marks.length; i++) {
            sb.append(marks[i]);
            if (i < marks.length - 1) {
                sb.append(", ");
            }
        }
        return sb.toString();
    }
}

class BSTNode implements Serializable {
    Student student;
    BSTNode left, right;

    public BSTNode(Student student) {
        this.student = student;
        left = right = null;
    }
}

class StudentBST implements Serializable {
    private BSTNode root;

    public StudentBST() {
        root = null;
    }

    public void insert(Student student) {
        root = insertRec(root, student);
    }

    private BSTNode insertRec(BSTNode root, Student student) {
        if (root == null) {
            root = new BSTNode(student);
            return root;
        }
        if (student.id < root.student.id) {
            root.left = insertRec(root.left, student);
        } else if (student.id > root.student.id) {
            root.right = insertRec(root.right, student);
        } else {
            throw new RuntimeException("Student with id " + student.id + " already exists.");
        }
        return root;
    }

    public Student search(int id) {
        BSTNode node = searchRec(root, id);
        return (node != null ? node.student : null);
    }

    private BSTNode searchRec(BSTNode root, int id) {
        if (root == null || root.student.id == id) {
            return root;
        }
        if (id < root.student.id) {
            return searchRec(root.left, id);
        } else {
            return searchRec(root.right, id);
        }
    }

    public void delete(int id) {
        root = deleteRec(root, id);
    }

    private BSTNode deleteRec(BSTNode root, int id) {
        if (root == null) {
            return root;
        }
        if (id < root.student.id) {
            root.left = deleteRec(root.left, id);
        } else if (id > root.student.id) {
            root.right = deleteRec(root.right, id);
        } else {
            if (root.left == null)
                return root.right;
            else if (root.right == null)
                return root.left;

            root.student = minValue(root.right);
            root.right = deleteRec(root.right, root.student.id);
        }
        return root;
    }

    private Student minValue(BSTNode root) {
        Student minStudent = root.student;
        while (root.left != null) {
            minStudent = root.left.student;
            root = root.left;
        }
        return minStudent;
    }

    public void inorder(java.util.List<Student> list) {
        inorderRec(root, list);
    }

    private void inorderRec(BSTNode root, java.util.List<Student> list) {
        if (root != null) {
            inorderRec(root.left, list);
            list.add(root.student);
            inorderRec(root.right, list);
        }
    }
}

class StudentService implements Serializable {
    private StudentBST studentBST;
    private PriorityQueue<Student> rankingQueue;

    public StudentService() {
        studentBST = new StudentBST();
        rankingQueue = new PriorityQueue<>(new Comparator<Student>() {
            public int compare(Student s1, Student s2) {
                int cmp = Double.compare(s2.cgpa, s1.cgpa);
                if (cmp == 0) {
                    return Integer.compare(s1.id, s2.id);
                }
                return cmp;
            }
        });
    }

    public void addStudent(Student student) {
        studentBST.insert(student);
        rankingQueue.offer(student);
    }

    public Student searchStudent(int id) {
        return studentBST.search(id);
    }

    public void removeStudent(int id) {
        Student student = searchStudent(id);
        if (student != null) {
            studentBST.delete(id);
            removeFromRankingQueue(id);
        }
    }

    private void removeFromRankingQueue(int id) {
        PriorityQueue<Student> tempQueue = new PriorityQueue<>(rankingQueue.comparator());
        while (!rankingQueue.isEmpty()) {
            Student s = rankingQueue.poll();
            if (s.id != id) {
                tempQueue.offer(s);
            }
        }
        rankingQueue = tempQueue;
    }

    public java.util.List<Student> getRankedStudents() {
        java.util.List<Student> rankedList = new ArrayList<>();
        PriorityQueue<Student> tempQueue = new PriorityQueue<>(rankingQueue);

        while (!tempQueue.isEmpty()) {
            rankedList.add(tempQueue.poll());
        }

        return rankedList;
    }

    public java.util.List<Student> getAllStudents() {
        java.util.List<Student> allStudents = new ArrayList<>();
        studentBST.inorder(allStudents);
        return allStudents;
    }

    public void saveStudents(String filename) {
        java.util.List<Student> students = getAllStudents();
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(filename))) {
            oos.writeObject(students);
        } catch (IOException e) {
            throw new RuntimeException("Error saving students: " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    public void loadStudents(String filename) {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            java.util.List<Student> students = (java.util.List<Student>) ois.readObject();

            // Clear current data
            studentBST = new StudentBST();
            rankingQueue.clear();

            // Add loaded students
            for (Student student : students) {
                addStudent(student);
            }
        } catch (IOException | ClassNotFoundException e) {
            throw new RuntimeException("Error loading students: " + e.getMessage());
        }
    }
}

// Main application class with Swing UI
public class Main extends JFrame {

    private StudentService studentService;
    private JTabbedPane tabbedPane;

    // Components for Add Student panel
    private JPanel addStudentPanel;
    private JTextField idField, nameField, attendanceField;
    private JPanel marksPanel;
    private java.util.List<JTextField> markFields;  // Fixed the ambiguous reference here
    private JButton addMarksButton, removeMarksButton, addStudentButton;

    // Components for View Students panel
    private JPanel viewStudentsPanel;
    private JTable studentsTable;
    private DefaultTableModel tableModel;
    private JButton refreshButton, deleteButton, searchButton;
    private JTextField searchField;

    // Components for Ranking panel
    private JPanel rankingPanel;
    private JTable rankingTable;
    private DefaultTableModel rankingTableModel;
    private JButton refreshRankingButton;

    // Components for Student Details panel
    private JPanel studentDetailsPanel;
    private JTextArea studentDetailsArea;

    // File menu items
    private JMenuItem saveMenuItem, loadMenuItem;

    public Main() {
        studentService = new StudentService();
        markFields = new ArrayList<>();

        setTitle("Academic Exam Result Management");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        createMenuBar();
        createTabbedPane();

        add(tabbedPane);
        setVisible(true);
    }

    private void createMenuBar() {
        JMenuBar menuBar = new JMenuBar();

        JMenu fileMenu = new JMenu("File");
        saveMenuItem = new JMenuItem("Save Records");
        loadMenuItem = new JMenuItem("Load Records");

        saveMenuItem.addActionListener(e -> saveRecords());
        loadMenuItem.addActionListener(e -> loadRecords());

        fileMenu.add(saveMenuItem);
        fileMenu.add(loadMenuItem);
        menuBar.add(fileMenu);

        setJMenuBar(menuBar);
    }

    private void createTabbedPane() {
        tabbedPane = new JTabbedPane();

        createAddStudentPanel();
        createViewStudentsPanel();
        createRankingPanel();
        createStudentDetailsPanel();

        tabbedPane.addTab("Add Student", addStudentPanel);
        tabbedPane.addTab("View Students", viewStudentsPanel);
        tabbedPane.addTab("Ranking", rankingPanel);
        tabbedPane.addTab("Student Details", studentDetailsPanel);
    }

    private void createAddStudentPanel() {
        addStudentPanel = new JPanel(new BorderLayout(10, 10));
        addStudentPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        JPanel formPanel = new JPanel(new GridLayout(0, 2, 5, 5));

        formPanel.add(new JLabel("Student ID:"));
        idField = new JTextField();
        formPanel.add(idField);

        formPanel.add(new JLabel("Student Name:"));
        nameField = new JTextField();
        formPanel.add(nameField);

        formPanel.add(new JLabel("Attendance (%):"));
        attendanceField = new JTextField();
        formPanel.add(attendanceField);

        addStudentPanel.add(formPanel, BorderLayout.NORTH);

        // Marks panel with dynamic adding/removing of mark fields
        JPanel marksContainer = new JPanel(new BorderLayout());
        marksContainer.setBorder(BorderFactory.createTitledBorder("Subject Marks"));

        marksPanel = new JPanel(new GridLayout(0, 2, 5, 5));

        // Add initial mark field
        addMarkField();

        JPanel buttonPane = new JPanel(new FlowLayout(FlowLayout.LEFT));
        addMarksButton = new JButton("Add Subject");
        removeMarksButton = new JButton("Remove Subject");

        addMarksButton.addActionListener(e -> addMarkField());
        removeMarksButton.addActionListener(e -> removeMarkField());

        buttonPane.add(addMarksButton);
        buttonPane.add(removeMarksButton);

        JScrollPane marksScrollPane = new JScrollPane(marksPanel);
        marksScrollPane.setPreferredSize(new Dimension(300, 150));

        marksContainer.add(marksScrollPane, BorderLayout.CENTER);
        marksContainer.add(buttonPane, BorderLayout.SOUTH);

        addStudentPanel.add(marksContainer, BorderLayout.CENTER);

        // Submit button
        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        addStudentButton = new JButton("Add Student");
        addStudentButton.addActionListener(e -> addStudent());
        bottomPanel.add(addStudentButton);

        addStudentPanel.add(bottomPanel, BorderLayout.SOUTH);
    }

    private void addMarkField() {
        int subjectNumber = markFields.size() + 1;
        marksPanel.add(new JLabel("Subject " + subjectNumber + ":"));
        JTextField markField = new JTextField();
        markFields.add(markField);
        marksPanel.add(markField);
        marksPanel.revalidate();
        marksPanel.repaint();
    }

    private void removeMarkField() {
        int size = markFields.size();
        if (size > 1) {
            markFields.remove(size - 1);
            marksPanel.remove(marksPanel.getComponentCount() - 1);
            marksPanel.remove(marksPanel.getComponentCount() - 1);
            marksPanel.revalidate();
            marksPanel.repaint();
        }
    }

    private void createViewStudentsPanel() {
        viewStudentsPanel = new JPanel(new BorderLayout(10, 10));
        viewStudentsPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Search panel
        JPanel searchPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        searchPanel.add(new JLabel("Search by ID:"));
        searchField = new JTextField(10);
        searchPanel.add(searchField);
        searchButton = new JButton("Search");
        searchButton.addActionListener(e -> searchStudent());
        searchPanel.add(searchButton);

        viewStudentsPanel.add(searchPanel, BorderLayout.NORTH);

        // Students table
        String[] columns = {"ID", "Name", "CGPA", "Attendance", "Fee Slab", "Eligible"};
        tableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        studentsTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(studentsTable);
        viewStudentsPanel.add(scrollPane, BorderLayout.CENTER);

        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        refreshButton = new JButton("Refresh");
        deleteButton = new JButton("Delete Selected");

        refreshButton.addActionListener(e -> refreshStudentsTable());
        deleteButton.addActionListener(e -> deleteSelectedStudent());

        buttonPanel.add(refreshButton);
        buttonPanel.add(deleteButton);

        viewStudentsPanel.add(buttonPanel, BorderLayout.SOUTH);

        // Selection listener for table
        studentsTable.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                displaySelectedStudentDetails();
            }
        });
    }

    private void createRankingPanel() {
        rankingPanel = new JPanel(new BorderLayout(10, 10));
        rankingPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Ranking table
        String[] columns = {"Rank", "ID", "Name", "CGPA", "Fee Slab"};
        rankingTableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        rankingTable = new JTable(rankingTableModel);
        JScrollPane scrollPane = new JScrollPane(rankingTable);
        rankingPanel.add(scrollPane, BorderLayout.CENTER);

        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        refreshRankingButton = new JButton("Refresh Ranking");
        refreshRankingButton.addActionListener(e -> refreshRankingTable());
        buttonPanel.add(refreshRankingButton);

        rankingPanel.add(buttonPanel, BorderLayout.SOUTH);

        // Selection listener for table
        rankingTable.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                displaySelectedRankedStudentDetails();
            }
        });
    }

    private void createStudentDetailsPanel() {
        studentDetailsPanel = new JPanel(new BorderLayout(10, 10));
        studentDetailsPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        studentDetailsArea = new JTextArea();
        studentDetailsArea.setEditable(false);
        studentDetailsArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));

        JScrollPane scrollPane = new JScrollPane(studentDetailsArea);
        studentDetailsPanel.add(scrollPane, BorderLayout.CENTER);
    }

    private void addStudent() {
        try {
            // Validate inputs
            int id = Integer.parseInt(idField.getText().trim());
            String name = nameField.getText().trim();
            double attendance = Double.parseDouble(attendanceField.getText().trim());

            // Validate name
            if (name.isEmpty()) {
                throw new IllegalArgumentException("Student name cannot be empty");
            }
            if (!DataValidator.validateName(name)) {
                throw new IllegalArgumentException("Student name must contain only alphabetic characters and spaces");
            }

            // Collect marks
            double[] marks = new double[markFields.size()];
            for (int i = 0; i < markFields.size(); i++) {
                marks[i] = Double.parseDouble(markFields.get(i).getText().trim());
            }

            // Create new student
            Student student = new Student(id, name, marks, attendance);

            // Validate data
            if (!DataValidator.validateCGPA(student.cgpa)) {
                throw new IllegalArgumentException("Invalid CGPA value: " + student.cgpa);
            }
            if (!DataValidator.validateAttendance(student.attendance)) {
                throw new IllegalArgumentException("Invalid attendance value: " + student.attendance);
            }
            if (!DataValidator.validateMarks(student.marks)) {
                throw new IllegalArgumentException("Invalid marks detected");
            }

            // Add student to service
            studentService.addStudent(student);

            // Clear form
            clearAddStudentForm();

            // Refresh tables
            refreshStudentsTable();
            refreshRankingTable();

            JOptionPane.showMessageDialog(this, "Student added successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Please enter valid numeric values", "Input Error", JOptionPane.ERROR_MESSAGE);
        } catch (RuntimeException e) {
            JOptionPane.showMessageDialog(this, e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void clearAddStudentForm() {
        idField.setText("");
        nameField.setText("");
        attendanceField.setText("");

        // Clear mark fields
        for (JTextField field : markFields) {
            field.setText("");
        }
    }

    private void refreshStudentsTable() {
        tableModel.setRowCount(0);

        java.util.List<Student> students = studentService.getAllStudents();
        for (Student student : students) {
            tableModel.addRow(new Object[]{
                    student.id,
                    student.name,
                    String.format("%.2f", student.cgpa),
                    String.format("%.1f%%", student.attendance),
                    student.feeSlab,
                    student.isEligible() ? "Yes" : "No"
            });
        }
    }

    private void refreshRankingTable() {
        rankingTableModel.setRowCount(0);

        java.util.List<Student> rankedStudents = studentService.getRankedStudents();
        int rank = 1;
        for (Student student : rankedStudents) {
            rankingTableModel.addRow(new Object[]{
                    rank++,
                    student.id,
                    student.name,
                    String.format("%.2f", student.cgpa),
                    student.feeSlab
            });
        }
    }

    private void displaySelectedStudentDetails() {
        int selectedRow = studentsTable.getSelectedRow();
        if (selectedRow >= 0) {
            int studentId = (Integer) tableModel.getValueAt(selectedRow, 0);
            displayStudentDetails(studentId);
        }
    }

    private void displaySelectedRankedStudentDetails() {
        int selectedRow = rankingTable.getSelectedRow();
        if (selectedRow >= 0) {
            int studentId = (Integer) rankingTableModel.getValueAt(selectedRow, 1);
            displayStudentDetails(studentId);
        }
    }

    private void displayStudentDetails(int studentId) {
        Student student = studentService.searchStudent(studentId);
        if (student != null) {
            StringBuilder sb = new StringBuilder();
            sb.append("STUDENT DETAILS\n");
            sb.append("==============\n\n");
            sb.append("ID: ").append(student.id).append("\n");
            sb.append("Name: ").append(student.name).append("\n");
            sb.append("CGPA: ").append(String.format("%.2f", student.cgpa)).append("\n");
            sb.append("Attendance: ").append(String.format("%.1f%%", student.attendance)).append("\n");
            sb.append("Fee Slab: ").append(student.feeSlab).append("\n");
            sb.append("Eligibility: ").append(student.isEligible() ? "Eligible" : "Not Eligible").append("\n\n");

            sb.append("SUBJECT MARKS\n");
            sb.append("=============\n");
            for (int i = 0; i < student.marks.length; i++) {
                sb.append("Subject ").append(i + 1).append(": ");
                sb.append(String.format("%.1f", student.marks[i])).append("\n");
            }

            studentDetailsArea.setText(sb.toString());
            tabbedPane.setSelectedComponent(studentDetailsPanel);
        }
    }

    private void deleteSelectedStudent() {
        int selectedRow = studentsTable.getSelectedRow();
        if (selectedRow >= 0) {
            int studentId = (Integer) tableModel.getValueAt(selectedRow, 0);
            int confirm = JOptionPane.showConfirmDialog(
                    this,
                    "Are you sure you want to delete student with ID: " + studentId + "?",
                    "Confirm Delete",
                    JOptionPane.YES_NO_OPTION
            );

            if (confirm == JOptionPane.YES_OPTION) {
                studentService.removeStudent(studentId);
                refreshStudentsTable();
                refreshRankingTable();
                studentDetailsArea.setText("");
                JOptionPane.showMessageDialog(this, "Student deleted successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
            }
        } else {
            JOptionPane.showMessageDialog(this, "Please select a student to delete", "No Selection", JOptionPane.WARNING_MESSAGE);
        }
    }

    private void searchStudent() {
        try {
            int id = Integer.parseInt(searchField.getText().trim());
            Student student = studentService.searchStudent(id);

            if (student != null) {
                // Find and select the row in the table
                for (int i = 0; i < tableModel.getRowCount(); i++) {
                    if ((Integer) tableModel.getValueAt(i, 0) == id) {
                        studentsTable.setRowSelectionInterval(i, i);
                        displayStudentDetails(id);
                        break;
                    }
                }
            } else {
                JOptionPane.showMessageDialog(this, "Student with ID: " + id + " not found", "Not Found", JOptionPane.INFORMATION_MESSAGE);
            }
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Please enter a valid ID", "Input Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void saveRecords() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Save Records");

        int userSelection = fileChooser.showSaveDialog(this);
        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToSave = fileChooser.getSelectedFile();
            try {
                studentService.saveStudents(fileToSave.getAbsolutePath());
                JOptionPane.showMessageDialog(this, "Records saved successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception e) {
                JOptionPane.showMessageDialog(this, "Error: " + e.getMessage(), "Save Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void loadRecords() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Load Records");

        int userSelection = fileChooser.showOpenDialog(this);
        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToLoad = fileChooser.getSelectedFile();
            try {
                studentService.loadStudents(fileToLoad.getAbsolutePath());
                refreshStudentsTable();
                refreshRankingTable();
                JOptionPane.showMessageDialog(this, "Records loaded successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception e) {
                JOptionPane.showMessageDialog(this, "Error: " + e.getMessage(), "Load Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    public static void main(String[] args) {
        try {
            // Set look and feel to system default
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        SwingUtilities.invokeLater(() -> new Main());
    }
}