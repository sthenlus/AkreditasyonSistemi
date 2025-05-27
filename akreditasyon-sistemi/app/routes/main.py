from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Student, Course, ProgramOutcome, Exam, StudentExamScore, Semester
from datetime import datetime
from sqlalchemy import or_
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    total_students = Student.query.count()
    total_courses = Course.query.count()
    total_outcomes = ProgramOutcome.query.count()
    
    return render_template('main/index.html',
                         total_students=total_students,
                         total_courses=total_courses,
                         total_outcomes=total_outcomes)

@bp.route('/exams')
@login_required
def exam_list():
    # Filtreleri al
    course_id = request.args.get('course_id', type=int)
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    
    # Sınavları sorgula
    query = Exam.query
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    if date_start:
        query = query.filter(Exam.exam_date >= datetime.strptime(date_start, '%Y-%m-%d'))
    
    if date_end:
        query = query.filter(Exam.exam_date <= datetime.strptime(date_end, '%Y-%m-%d'))
    
    # Sınavları tarihe göre sırala
    exams = query.order_by(Exam.exam_date.desc()).all()
    courses = Course.query.order_by(Course.course_code).all()
    
    return render_template('main/exam_list.html', exams=exams, courses=courses)

@bp.route('/students')
@login_required
def student_list():
    # Arama filtresini al
    search = request.args.get('search', '')
    
    # Öğrencileri sorgula
    query = Student.query
    
    if search:
        # Öğrenci no veya isimde arama yap
        query = query.filter(
            or_(
                Student.student_number.ilike(f'%{search}%'),
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%')
            )
        )
    
    # Öğrenci numarasına göre sırala
    students = query.order_by(Student.student_number).all()
    
    return render_template('main/students.html', students=students)

@bp.route('/courses')
@login_required
def course_list():
    courses = Course.query.all()
    semesters = Semester.query.all()
    return render_template('main/courses.html', courses=courses, semesters=semesters)

@bp.route('/program-outcomes')
@login_required
def program_outcomes():
    outcomes = ProgramOutcome.query.all()
    return render_template('main/program_outcomes.html', outcomes=outcomes)

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('main/course_detail.html', course=course)

@bp.route('/student/<int:student_id>')
@login_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    from app.models import Semester
    semesters = Semester.query.all()
    pc_scores_by_semester = student.get_pc_scores_by_semester()
    return render_template('main/student_detail.html', student=student, semesters=semesters, pc_scores_by_semester=pc_scores_by_semester) 