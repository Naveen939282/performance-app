"""
Database Module for Student Marks Management System
Handles all database operations using SQLite
"""

import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="marks.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                roll_number TEXT UNIQUE NOT NULL,
                class_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Subjects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                credits INTEGER DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Marks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                marks REAL NOT NULL,
                exam_type TEXT NOT NULL,
                exam_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id),
                UNIQUE(student_id, subject_id, exam_type)
            )
        ''')
        
        # Create Settings table for threshold
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Insert default settings
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value) 
            VALUES ('weak_threshold', '35')
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    # ==================== STUDENT OPERATIONS ====================
    
    def add_student(self, name, email, roll_number, class_name):
        """Add a new student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (name, email, roll_number, class_name)
                VALUES (?, ?, ?, ?)
            ''', (name, email, roll_number, class_name))
            conn.commit()
            return True, "Student added successfully!"
        except sqlite3.IntegrityError as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def get_all_students(self):
        """Get all students"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY name')
        students = cursor.fetchall()
        conn.close()
        return [dict(row) for row in students]
    
    def get_student_by_id(self, student_id):
        """Get student by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        return dict(student) if student else None
    
    def update_student(self, student_id, name, email, roll_number, class_name):
        """Update student information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students 
            SET name = ?, email = ?, roll_number = ?, class_name = ?
            WHERE id = ?
        ''', (name, email, roll_number, class_name, student_id))
        conn.commit()
        conn.close()
        return True
    
    def delete_student(self, student_id):
        """Delete a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM marks WHERE student_id = ?', (student_id,))
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        return True
    
    # ==================== SUBJECT OPERATIONS ====================
    
    def add_subject(self, name, code, credits=3):
        """Add a new subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO subjects (name, code, credits)
                VALUES (?, ?, ?)
            ''', (name, code, credits))
            conn.commit()
            return True, "Subject added successfully!"
        except sqlite3.IntegrityError as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def get_all_subjects(self):
        """Get all subjects"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subjects ORDER BY name')
        subjects = cursor.fetchall()
        conn.close()
        return [dict(row) for row in subjects]
    
    def get_subject_by_id(self, subject_id):
        """Get subject by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,))
        subject = cursor.fetchone()
        conn.close()
        return dict(subject) if subject else None
    
    def delete_subject(self, subject_id):
        """Delete a subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM marks WHERE subject_id = ?', (subject_id,))
        cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
        conn.commit()
        conn.close()
        return True
    
    # ==================== MARKS OPERATIONS ====================
    
    def add_or_update_marks(self, student_id, subject_id, marks, exam_type, exam_date=None):
        """Add or update marks for a student in a subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if exam_date is None:
            exam_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            cursor.execute('''
                INSERT INTO marks (student_id, subject_id, marks, exam_type, exam_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, subject_id, marks, exam_type, exam_date))
            conn.commit()
            return True, "Marks added successfully!"
        except sqlite3.IntegrityError:
            # Update existing marks
            cursor.execute('''
                UPDATE marks 
                SET marks = ?, exam_type = ?, exam_date = ?
                WHERE student_id = ? AND subject_id = ?
            ''', (marks, exam_type, exam_date, student_id, subject_id))
            conn.commit()
            return True, "Marks updated successfully!"
        finally:
            conn.close()
    
    def get_student_marks(self, student_id):
        """Get all marks for a specific student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, s.name as subject_name, s.code as subject_code
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = ?
            ORDER BY s.name
        ''', (student_id,))
        marks = cursor.fetchall()
        conn.close()
        return [dict(row) for row in marks]
    
    def get_subject_marks(self, subject_id):
        """Get all marks for a specific subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, s.name as student_name, s.roll_number
            FROM marks m
            JOIN students s ON m.student_id = s.id
            WHERE m.subject_id = ?
            ORDER BY s.roll_number
        ''', (subject_id,))
        marks = cursor.fetchall()
        conn.close()
        return [dict(row) for row in marks]
    
    def get_all_marks(self):
        """Get all marks with student and subject details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, st.name as student_name, st.roll_number,
                   sub.name as subject_name, sub.code as subject_code
            FROM marks m
            JOIN students st ON m.student_id = st.id
            JOIN subjects sub ON m.subject_id = sub.id
            ORDER BY st.name, sub.name
        ''')
        marks = cursor.fetchall()
        conn.close()
        return [dict(row) for row in marks]
    
    # ==================== ANALYTICS OPERATIONS ====================
    
    def calculate_student_average(self, student_id):
        """Calculate average marks for a student"""
        marks_data = self.get_student_marks(student_id)
        if not marks_data:
            return 0
        total = sum(m['marks'] for m in marks_data)
        return round(total / len(marks_data), 2)
    
    def calculate_subject_average(self, subject_id):
        """Calculate average marks for a subject"""
        marks_data = self.get_subject_marks(subject_id)
        if not marks_data:
            return 0
        total = sum(m['marks'] for m in marks_data)
        return round(total / len(marks_data), 2)
    
    def get_weak_students(self, threshold=None):
        """Get students with marks below threshold"""
        if threshold is None:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'weak_threshold'")
            result = cursor.fetchone()
            threshold = float(result['value']) if result else 35
            conn.close()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT st.*, AVG(m.marks) as average
            FROM students st
            JOIN marks m ON st.id = m.student_id
            GROUP BY st.id
            HAVING average < ?
            ORDER BY average
        ''', (threshold,))
        students = cursor.fetchall()
        conn.close()
        return [dict(row) for row in students]
    
    def get_top_performers(self, limit=5):
        """Get top performing students"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT st.*, AVG(m.marks) as average
            FROM students st
            JOIN marks m ON st.id = m.student_id
            GROUP BY st.id
            ORDER BY average DESC
            LIMIT ?
        ''', (limit,))
        students = cursor.fetchall()
        conn.close()
        return [dict(row) for row in students]
    
    def get_subject_performance(self):
        """Get performance analysis for each subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sub.id, sub.name, sub.code,
                   AVG(m.marks) as average,
                   MAX(m.marks) as max_marks,
                   MIN(m.marks) as min_marks,
                   COUNT(m.id) as total_entries
            FROM subjects sub
            LEFT JOIN marks m ON sub.id = m.subject_id
            GROUP BY sub.id
            ORDER BY average DESC
        ''')
        subjects = cursor.fetchall()
        conn.close()
        return [dict(row) for row in subjects]
    
    def get_student_performance_report(self, student_id):
        """Generate complete performance report for a student"""
        student = self.get_student_by_id(student_id)
        marks_data = self.get_student_marks(student_id)
        
        if not student:
            return None
        
        # Get threshold
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'weak_threshold'")
        result = cursor.fetchone()
        threshold = float(result['value']) if result else 35
        conn.close()
        
        # Calculate statistics
        total_marks = sum(m['marks'] for m in marks_data)
        average = total_marks / len(marks_data) if marks_data else 0
        
        # Find weak subjects
        weak_subjects = [m for m in marks_data if m['marks'] < threshold]
        
        # Find strong subjects
        strong_subjects = [m for m in marks_data if m['marks'] >= threshold]
        
        return {
            'student': student,
            'marks': marks_data,
            'total_subjects': len(marks_data),
            'total_marks': total_marks,
            'average': round(average, 2),
            'threshold': threshold,
            'weak_subjects': weak_subjects,
            'strong_subjects': strong_subjects,
            'performance': 'Excellent' if average >= 75 else ('Good' if average >= 60 else ('Average' if average >= 45 else 'Needs Improvement'))
        }
    
    def get_class_statistics(self):
        """Get overall class statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total students
        cursor.execute('SELECT COUNT(*) as count FROM students')
        total_students = cursor.fetchone()['count']
        
        # Total subjects
        cursor.execute('SELECT COUNT(*) as count FROM subjects')
        total_subjects = cursor.fetchone()['count']
        
        # Total marks entries
        cursor.execute('SELECT COUNT(*) as count FROM marks')
        total_entries = cursor.fetchone()['count']
        
        # Class average
        cursor.execute('SELECT AVG(marks) as avg FROM marks')
        class_average = round(cursor.fetchone()['avg'], 2) if cursor.fetchone()['avg'] else 0
        
        # Weak students count
        cursor.execute("SELECT value FROM settings WHERE key = 'weak_threshold'")
        result = cursor.fetchone()
        threshold = float(result['value']) if result else 35
        
        cursor.execute('''
            SELECT COUNT(DISTINCT student_id) as count
            FROM marks
            GROUP BY student_id
            HAVING AVG(marks) < ?
        ''', (threshold,))
        weak_count = len(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_students': total_students,
            'total_subjects': total_subjects,
            'total_entries': total_entries,
            'class_average': class_average,
            'weak_students_count': weak_count,
            'threshold': threshold
        }
    
    # ==================== SETTINGS ====================
    
    def update_threshold(self, threshold):
        """Update weak student threshold"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE settings SET value = ? WHERE key = 'weak_threshold'
        ''', (str(threshold),))
        conn.commit()
        conn.close()
        return True
    
    def get_threshold(self):
        """Get current threshold"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'weak_threshold'")
        result = cursor.fetchone()
        conn.close()
        return float(result['value']) if result else 35


# Create database instance
db = Database()
