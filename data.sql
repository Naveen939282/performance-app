-- Student Marks Management System - Sample Data
-- This file contains sample data to help you get started

-- Sample Students
INSERT INTO students (name, email, roll_number, class_name) VALUES 
('John Smith', 'john.smith@example.com', 'CS001', 'Class 1'),
('Sarah Johnson', 'sarah.johnson@example.com', 'CS002', 'Class 1'),
('Michael Brown', 'michael.brown@example.com', 'CS003', 'Class 1'),
('Emily Davis', 'emily.davis@example.com', 'CS004', 'Class 2'),
('David Wilson', 'david.wilson@example.com', 'CS005', 'Class 2'),
('Lisa Anderson', 'lisa.anderson@example.com', 'CS006', 'Class 2'),
('James Taylor', 'james.taylor@example.com', 'CS007', 'Class 3'),
('Jennifer Martin', 'jennifer.martin@example.com', 'CS008', 'Class 3');

-- Sample Subjects
INSERT INTO subjects (name, code, credits) VALUES 
('Mathematics', 'MATH101', 4),
('Physics', 'PHY101', 4),
('Chemistry', 'CHEM101', 4),
('Computer Science', 'CS101', 3),
('English', 'ENG101', 3);

-- Sample Marks (for Class 1 students in Mathematics)
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(1, 1, 85, 'Midterm', '2024-02-15'),
(2, 1, 78, 'Midterm', '2024-02-15'),
(3, 1, 92, 'Midterm', '2024-02-15'),
(1, 1, 88, 'Final', '2024-05-20'),
(2, 1, 82, 'Final', '2024-05-20'),
(3, 1, 95, 'Final', '2024-05-20');

-- Sample Marks (for Class 1 students in Physics)
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(1, 2, 78, 'Midterm', '2024-02-20'),
(2, 2, 85, 'Midterm', '2024-02-20'),
(3, 2, 70, 'Midterm', '2024-02-20'),
(1, 2, 80, 'Final', '2024-05-25'),
(2, 2, 88, 'Final', '2024-05-25'),
(3, 2, 75, 'Final', '2024-05-25');

-- Sample Marks (for Class 1 students in Computer Science)
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(1, 4, 90, 'Midterm', '2024-02-25'),
(2, 4, 82, 'Midterm', '2024-02-25'),
(3, 4, 88, 'Midterm', '2024-02-25'),
(1, 4, 92, 'Final', '2024-05-30'),
(2, 4, 85, 'Final', '2024-05-30'),
(3, 4, 78, 'Final', '2024-05-30');

-- Sample Marks (for Class 2 students)
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(4, 1, 65, 'Midterm', '2024-02-15'),
(5, 1, 72, 'Midterm', '2024-02-15'),
(6, 1, 55, 'Midterm', '2024-02-15'),
(4, 1, 68, 'Final', '2024-05-20'),
(5, 1, 75, 'Final', '2024-05-20'),
(6, 1, 58, 'Final', '2024-05-20');

-- Sample Marks for weak student demonstration
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(6, 2, 30, 'Midterm', '2024-02-20'),
(6, 2, 28, 'Final', '2024-05-25'),
(6, 4, 32, 'Midterm', '2024-02-25'),
(6, 4, 25, 'Final', '2024-05-30');

-- Sample Marks (for Class 3 students)
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(7, 1, 95, 'Midterm', '2024-02-15'),
(8, 1, 88, 'Midterm', '2024-02-15'),
(7, 1, 98, 'Final', '2024-05-20'),
(8, 1, 91, 'Final', '2024-05-20');

-- Sample Marks in English (all classes)
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(1, 5, 82, 'Midterm', '2024-03-01'),
(2, 5, 75, 'Midterm', '2024-03-01'),
(3, 5, 88, 'Midterm', '2024-03-01'),
(4, 5, 70, 'Midterm', '2024-03-01'),
(5, 5, 78, 'Midterm', '2024-03-01');

-- Sample Marks in Chemistry
INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date) VALUES 
(1, 3, 80, 'Midterm', '2024-03-05'),
(2, 3, 72, 'Midterm', '2024-03-05'),
(3, 3, 85, 'Midterm', '2024-03-05'),
(7, 3, 90, 'Midterm', '2024-03-05'),
(8, 3, 86, 'Midterm', '2024-03-05');
