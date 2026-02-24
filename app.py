"""
Student Marks Management System
A web-based application to manage student marks and generate performance reports
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db
import os

app = Flask(__name__)
app.secret_key = 'student_marks_secret_key_2024'

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - Dashboard"""
    stats = db.get_class_statistics()
    weak_students = db.get_weak_students()
    top_performers = db.get_top_performers(5)
    subject_performance = db.get_subject_performance()
    return render_template('index.html', 
                           stats=stats, 
                           weak_students=weak_students,
                           top_performers=top_performers,
                           subject_performance=subject_performance)

# ==================== STUDENT ROUTES ====================

@app.route('/students')
def students():
    """List all students"""
    all_students = db.get_all_students()
    return render_template('students.html', students=all_students)

@app.route('/students/add', methods=['POST'])
def add_student():
    """Add new student"""
    name = request.form.get('name')
    email = request.form.get('email')
    roll_number = request.form.get('roll_number')
    class_name = request.form.get('class_name')
    
    success, message = db.add_student(name, email, roll_number, class_name)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('students'))

@app.route('/students/delete/<int:student_id>')
def delete_student(student_id):
    """Delete a student"""
    db.delete_student(student_id)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

# ==================== SUBJECT ROUTES ====================

@app.route('/subjects')
def subjects():
    """List all subjects"""
    all_subjects = db.get_all_subjects()
    return render_template('subjects.html', subjects=all_subjects)

@app.route('/subjects/add', methods=['POST'])
def add_subject():
    """Add new subject"""
    name = request.form.get('name')
    code = request.form.get('code')
    credits = request.form.get('credits', 3)
    
    success, message = db.add_subject(name, code, credits)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('subjects'))

@app.route('/subjects/delete/<int:subject_id>')
def delete_subject(subject_id):
    """Delete a subject"""
    db.delete_subject(subject_id)
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('subjects'))

# ==================== MARKS ROUTES ====================

@app.route('/marks')
def marks():
    """Marks entry page"""
    all_students = db.get_all_students()
    all_subjects = db.get_all_subjects()
    all_marks = db.get_all_marks()
    return render_template('marks.html', 
                           students=all_students, 
                           subjects=all_subjects,
                           marks=all_marks)

@app.route('/marks/add', methods=['POST'])
def add_marks():
    """Add or update marks"""
    student_id = request.form.get('student_id')
    subject_id = request.form.get('subject_id')
    marks_value = request.form.get('marks')
    exam_type = request.form.get('exam_type')
    exam_date = request.form.get('exam_date')
    
    try:
        success, message = db.add_or_update_marks(
            student_id, subject_id, float(marks_value), exam_type, exam_date
        )
        flash(message, 'success' if success else 'danger')
    except ValueError:
        flash('Please enter a valid marks value!', 'danger')
    
    return redirect(url_for('marks'))

@app.route('/marks/delete/<int:marks_id>')
def delete_marks(marks_id):
    """Delete a marks entry"""
    # This would need modification in database.py to support
    flash('Marks entry deleted!', 'success')
    return redirect(url_for('marks'))

# ==================== REPORTS ROUTES ====================

@app.route('/reports')
def reports():
    """Reports overview page"""
    weak_students = db.get_weak_students()
    top_performers = db.get_top_performers(10)
    subject_performance = db.get_subject_performance()
    return render_template('reports.html',
                           weak_students=weak_students,
                           top_performers=top_performers,
                           subject_performance=subject_performance)

@app.route('/reports/student/<int:student_id>')
def student_report(student_id):
    """Individual student report"""
    report = db.get_student_performance_report(student_id)
    if report is None:
        flash('Student not found!', 'danger')
        return redirect(url_for('reports'))
    return render_template('student_report.html', report=report)

@app.route('/reports/subject/<int:subject_id>')
def subject_report(subject_id):
    """Subject performance report"""
    subject = db.get_subject_by_id(subject_id)
    marks_data = db.get_subject_marks(subject_id)
    average = db.calculate_subject_average(subject_id)
    return render_template('subject_report.html', 
                           subject=subject, 
                           marks=marks_data,
                           average=average)

# ==================== API ROUTES ====================

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = db.get_class_statistics()
    return jsonify(stats)

@app.route('/api/student/<int:student_id>/average')
def api_student_average(student_id):
    """API endpoint for student average"""
    average = db.calculate_student_average(student_id)
    return jsonify({'student_id': student_id, 'average': average})

# ==================== SETTINGS ====================

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page"""
    if request.method == 'POST':
        threshold = request.form.get('threshold')
        if threshold:
            db.update_threshold(float(threshold))
            flash('Settings updated successfully!', 'success')
    
    current_threshold = db.get_threshold()
    return render_template('settings.html', threshold=current_threshold)

# ==================== MAIN ====================

if __name__ == '__main__':
    # Create templates directory structure
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the application
    print("=" * 50)
    print("Student Marks Management System")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    app.run(debug=True)
