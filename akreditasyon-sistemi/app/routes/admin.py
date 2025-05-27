from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app.models import Student, Course, ProgramOutcome, Exam, StudentExamScore, ExamProgramOutcome, Semester
from app import db
import pandas as pd
from datetime import datetime
import io
import json
import os
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Öğrenci Yönetimi
@bp.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        student = Student(
            student_number=request.form['student_number'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email']
        )
        
        try:
            db.session.add(student)
            db.session.commit()
            flash('Öğrenci başarıyla eklendi!', 'success')
            return redirect(url_for('main.student_list'))
        except Exception as e:
            db.session.rollback()
            flash('Hata oluştu! Öğrenci eklenemedi.', 'error')
    
    return render_template('admin/add_student.html')

@bp.route('/edit-student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        student.student_number = request.form['student_number']
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.email = request.form['email']
        student.phone = request.form['phone']
        
        try:
            db.session.commit()
            flash('Öğrenci başarıyla güncellendi!', 'success')
            return redirect(url_for('main.student_list'))
        except Exception as e:
            db.session.rollback()
            flash('Hata oluştu! Öğrenci güncellenemedi.', 'error')
    
    return render_template('admin/edit_student.html', student=student)

@bp.route('/delete-student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Yetkiniz yok!'})
    student = Student.query.get_or_404(student_id)
    try:
        # Önce ilişkili sınav notlarını sil
        StudentExamScore.query.filter_by(student_id=student.id).delete()
        db.session.delete(student)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Ders Yönetimi
@bp.route('/add-course', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        course = Course(
            course_code=request.form['course_code'],
            course_name=request.form['course_name'],
            credits=int(request.form['credits']),
            instructor_name=request.form['instructor_name'],
            semester_id=int(request.form['semester_id'])
        )
        
        try:
            db.session.add(course)
            db.session.commit()
            
            # Program çıktılarını ekle
            program_outcomes = request.form.getlist('program_outcomes[]')
            for outcome_id in program_outcomes:
                course.program_outcomes.append(ProgramOutcome.query.get(int(outcome_id)))
            
            db.session.commit()
            flash('Ders başarıyla eklendi!', 'success')
            return redirect(url_for('main.course_list'))
        except Exception as e:
            db.session.rollback()
            flash('Hata oluştu! Ders eklenemedi.', 'error')
    
    program_outcomes = ProgramOutcome.query.all()
    semesters = Semester.query.all()
    return render_template('admin/add_course.html', program_outcomes=program_outcomes, semesters=semesters)

@bp.route('/edit-course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        course.course_code = request.form['course_code']
        course.course_name = request.form['course_name']
        course.credits = int(request.form['credits'])
        course.instructor_name = request.form['instructor_name']
        course.semester_id = int(request.form['semester_id'])
        
        # Program çıktılarını güncelle
        course.program_outcomes = []
        program_outcomes = request.form.getlist('program_outcomes[]')
        for outcome_id in program_outcomes:
            course.program_outcomes.append(ProgramOutcome.query.get(int(outcome_id)))
        
        try:
            db.session.commit()
            flash('Ders başarıyla güncellendi!', 'success')
            return redirect(url_for('main.course_list'))
        except Exception as e:
            db.session.rollback()
            flash('Hata oluştu! Ders güncellenemedi.', 'error')
    
    program_outcomes = ProgramOutcome.query.all()
    semesters = Semester.query.all()
    return render_template('admin/edit_course.html', course=course, program_outcomes=program_outcomes, semesters=semesters)

@bp.route('/delete-course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Yetkiniz yok!'})
        
    course = Course.query.get_or_404(course_id)
    
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Sınav Yönetimi
@bp.route('/add-exam', methods=['GET', 'POST'])
@login_required
def add_exam():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        exam = Exam(
            course_id=int(request.form['course_id']),
            exam_name=request.form['exam_name'],
            exam_date=datetime.strptime(request.form['exam_date'], '%Y-%m-%d'),
            weight=float(request.form['weight'])
        )
        
        try:
            db.session.add(exam)
            db.session.flush()  # ID almak için flush

            # Program çıktılarını kaydet
            program_outcomes = request.form.getlist('program_outcomes[]')
            weights = request.form.getlist('weights[]')
            
            # Program çıktıları ve ağırlıkları eşleştir
            for i, outcome_id in enumerate(program_outcomes):
                if i < len(weights):  # Ağırlık değeri varsa
                    exam_outcome = ExamProgramOutcome(
                        exam_id=exam.id,
                        program_outcome_id=int(outcome_id),
                        weight=float(weights[i])
                    )
                    db.session.add(exam_outcome)
                else:  # Ağırlık değeri yoksa varsayılan 1.0 kullan
                    exam_outcome = ExamProgramOutcome(
                        exam_id=exam.id,
                        program_outcome_id=int(outcome_id),
                        weight=1.0
                    )
                    db.session.add(exam_outcome)

            db.session.commit()
            flash('Sınav başarıyla eklendi!', 'success')
            return redirect(url_for('main.exam_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu! Sınav eklenemedi. {str(e)}', 'error')
    
    courses = Course.query.all()
    program_outcomes = ProgramOutcome.query.all()
    return render_template('admin/add_exam.html', courses=courses, program_outcomes=program_outcomes)

@bp.route('/edit-exam/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def edit_exam(exam_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    exam = Exam.query.get_or_404(exam_id)
    
    if request.method == 'POST':
        exam.course_id = int(request.form['course_id'])
        exam.exam_name = request.form['exam_name']
        exam.exam_date = datetime.strptime(request.form['exam_date'], '%Y-%m-%d')
        exam.weight = float(request.form['weight'])
        
        # Program çıktılarını güncelle
        ExamProgramOutcome.query.filter_by(exam_id=exam.id).delete()
        program_outcomes = request.form.getlist('program_outcomes[]')
        weights = request.form.getlist('weights[]')
        
        for i, outcome_id in enumerate(program_outcomes):
            exam_outcome = ExamProgramOutcome(
                exam_id=exam.id,
                program_outcome_id=int(outcome_id),
                weight=float(weights[i])
            )
            db.session.add(exam_outcome)
        
        try:
            db.session.commit()
            flash('Sınav başarıyla güncellendi!', 'success')
            return redirect(url_for('main.exam_list'))
        except Exception as e:
            db.session.rollback()
            flash('Hata oluştu! Sınav güncellenemedi.', 'error')
    
    courses = Course.query.all()
    program_outcomes = ProgramOutcome.query.all()
    return render_template('admin/edit_exam.html', exam=exam, courses=courses, program_outcomes=program_outcomes)

@bp.route('/delete-exam/<int:exam_id>', methods=['POST'])
@login_required
def delete_exam(exam_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Yetkiniz yok!'})
        
    exam = Exam.query.get_or_404(exam_id)
    
    try:
        db.session.delete(exam)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'csv'}

@bp.route('/upload-scores/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def upload_scores(exam_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    exam = Exam.query.get_or_404(exam_id)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Dosya seçilmedi!', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('Dosya seçilmedi!', 'error')
            return redirect(request.url)
            
        if not allowed_file(file.filename):
            flash('Geçersiz dosya formatı! Sadece Excel (.xlsx) ve CSV (.csv) dosyaları yüklenebilir.', 'error')
            return redirect(request.url)
            
        try:
            # Excel/CSV dosyasını oku
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
                
            # Gerekli sütunları kontrol et
            required_columns = ['student_id', 'score']
            if not all(col in df.columns for col in required_columns):
                flash('Dosya formatı hatalı! Gerekli sütunlar: student_id, score', 'error')
                return redirect(request.url)
                
            # Notları kaydet
            for _, row in df.iterrows():
                student = Student.query.filter_by(student_number=str(row['student_id'])).first()
                if student:
                    # Sınavın bağlı olduğu dersin dönem bilgisini al
                    semester_id = exam.course.semester_id
                    score = StudentExamScore(
                        student_id=student.id,
                        exam_id=exam_id,
                        score=float(row['score']),
                        semester_id=semester_id
                    )
                    db.session.add(score)
                    score.calculate_pc_scores()
                    
            db.session.commit()
            flash('Notlar başarıyla yüklendi!', 'success')
            return redirect(url_for('main.exam_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu! {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('admin/upload_scores.html', exam=exam)

# Raporlama
@bp.route('/reports/student/<int:student_id>')
@login_required
def student_report(student_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
    
    student = Student.query.get_or_404(student_id)
    semester = request.args.get('semester')
    academic_year = request.args.get('academic_year')
    
    # Sınav notlarını al
    scores = StudentExamScore.query.filter_by(student_id=student_id).all()
    if semester:
        scores = [s for s in scores if s.exam.semester == semester]
    if academic_year:
        scores = [s for s in scores if s.exam.academic_year == academic_year]
    
    # Program çıktılarını hesapla
    pc_scores = student.get_pc_scores(semester, academic_year)
    program_outcomes = ProgramOutcome.query.all()
    
    return render_template('admin/student_report.html',
                         student=student,
                         scores=scores,
                         pc_scores=pc_scores,
                         program_outcomes=program_outcomes,
                         semester=semester,
                         academic_year=academic_year)

@bp.route('/reports/course/<int:course_id>')
@login_required
def course_report(course_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    course = Course.query.get_or_404(course_id)
    semester = request.args.get('semester')
    academic_year = request.args.get('academic_year')
    
    # Sınav notlarını al
    scores = StudentExamScore.query.join(Exam).filter(
        Exam.course_id == course_id
    ).all()
    
    if semester:
        scores = [s for s in scores if s.exam.semester == semester]
    if academic_year:
        scores = [s for s in scores if s.exam.academic_year == academic_year]
    
    # Program çıktılarını hesapla
    pc_scores = course.get_pc_scores(semester, academic_year)
    program_outcomes = ProgramOutcome.query.all()
    
    return render_template('admin/course_report.html',
                         course=course,
                         scores=scores,
                         pc_scores=pc_scores,
                         program_outcomes=program_outcomes,
                         semester=semester,
                         academic_year=academic_year)

@bp.route('/reports/program-outcome/<int:outcome_id>')
@login_required
def program_outcome_report(outcome_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    outcome = ProgramOutcome.query.get_or_404(outcome_id)
    semester = request.args.get('semester')
    academic_year = request.args.get('academic_year')
    
    # Tüm derslerin bu PÇ'ye katkılarını hesapla
    courses = Course.query.filter(
        Course.program_outcomes.contains(outcome)
    ).all()
    
    course_scores = {}
    for course in courses:
        scores = course.get_pc_scores(semester, academic_year)
        course_scores[course.id] = scores.get(str(outcome.id), 0)
    
    # Genel ortalama
    if course_scores:
        average = sum(course_scores.values()) / len(course_scores)
    else:
        average = 0
    
    return render_template('admin/program_outcome_report.html',
                         outcome=outcome,
                         course_scores=course_scores,
                         average=average,
                         semester=semester,
                         academic_year=academic_year)

@bp.route('/reports/export/<string:report_type>/<int:id>')
@login_required
def export_report(report_type, id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
        
    semester = request.args.get('semester')
    academic_year = request.args.get('academic_year')
    
    if report_type == 'student':
        student = Student.query.get_or_404(id)
        pc_scores = student.get_pc_scores(semester, academic_year)
        program_outcomes = ProgramOutcome.query.all()
        
        # Excel dosyası oluştur
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # PÇ puanları
            df = pd.DataFrame({
                'Program Çıktısı': [pc.code for pc in program_outcomes],
                'Puan': [pc_scores.get(str(pc.id), 0) for pc in program_outcomes]
            })
            df.to_excel(writer, sheet_name='PÇ Puanları', index=False)
            
            # Sınav notları
            scores = StudentExamScore.query.filter_by(
                student_id=student.id
            ).all()
            
            if semester:
                scores = [s for s in scores if s.semester == semester]
            if academic_year:
                scores = [s for s in scores if s.academic_year == academic_year]
            
            df = pd.DataFrame([{
                'Ders': s.exam.course.course_name,
                'Sınav': s.exam.exam_name,
                'Not': s.score,
                'Dönem': s.semester,
                'Akademik Yıl': s.academic_year
            } for s in scores])
            df.to_excel(writer, sheet_name='Sınav Notları', index=False)
        
        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'ogrenci_raporu_{student.student_number}.xlsx'
        )
        
    elif report_type == 'course':
        course = Course.query.get_or_404(id)
        pc_scores = course.get_pc_scores(semester, academic_year)
        program_outcomes = ProgramOutcome.query.all()
        
        # Excel dosyası oluştur
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # PÇ puanları
            df = pd.DataFrame({
                'Program Çıktısı': [pc.code for pc in program_outcomes],
                'Puan': [pc_scores.get(str(pc.id), 0) for pc in program_outcomes]
            })
            df.to_excel(writer, sheet_name='PÇ Puanları', index=False)
            
            # Öğrenci notları
            scores = StudentExamScore.query.join(Exam).filter(
                Exam.course_id == course.id
            ).all()
            
            if semester:
                scores = [s for s in scores if s.semester == semester]
            if academic_year:
                scores = [s for s in scores if s.academic_year == academic_year]
            
            df = pd.DataFrame([{
                'Öğrenci No': s.student.student_number,
                'Ad Soyad': s.student.get_full_name(),
                'Sınav': s.exam.exam_name,
                'Not': s.score,
                'Dönem': s.semester,
                'Akademik Yıl': s.academic_year
            } for s in scores])
            df.to_excel(writer, sheet_name='Öğrenci Notları', index=False)
        
        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'ders_raporu_{course.course_code}.xlsx'
        )
        
    elif report_type == 'program-outcome':
        outcome = ProgramOutcome.query.get_or_404(id)
        score = outcome.get_scores(semester, academic_year)
        
        # Excel dosyası oluştur
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # PÇ puanı
            df = pd.DataFrame({
                'Program Çıktısı': [outcome.code],
                'Puan': [score]
            })
            df.to_excel(writer, sheet_name='PÇ Puanı', index=False)
            
            # Ders bazlı puanlar
            courses = Course.query.filter(
                Course.program_outcomes.contains(outcome)
            ).all()
            
            df = pd.DataFrame([{
                'Ders Kodu': course.course_code,
                'Ders Adı': course.course_name,
                'Puan': course.get_pc_scores(semester, academic_year).get(str(outcome.id), 0)
            } for course in courses])
            df.to_excel(writer, sheet_name='Ders Bazlı Puanlar', index=False)
        
        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'pc_raporu_{outcome.code}.xlsx'
        )

@bp.route('/download-score-template')
@login_required
def download_score_template():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('main.index'))
    
    # Öğrenci listesini al
    students = Student.query.all()
    
    # Excel şablonu oluştur
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Notlar sayfası
        df = pd.DataFrame({
            'student_id': [s.student_number for s in students],
            'score': [''] * len(students)
        })
        df.to_excel(writer, sheet_name='Notlar', index=False)
        
        # Açıklama sayfası
        info_df = pd.DataFrame({
            'Alan': ['student_id', 'score'],
            'Açıklama': [
                'Öğrenci numarası (Değiştirmeyin)',
                'Sınav notu (0-100 arası)'
            ],
            'Örnek': ['2024001', '85']
        })
        info_df.to_excel(writer, sheet_name='Açıklama', index=False)
    
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='not_sablonu.xlsx'
    )

# API endpoint for getting course program outcomes
@bp.route('/api/course/<int:course_id>/program-outcomes')
@login_required
def get_course_program_outcomes(course_id):
    course = Course.query.get_or_404(course_id)
    program_outcomes = [po.id for po in course.program_outcomes]
    return jsonify({'program_outcomes': program_outcomes}) 