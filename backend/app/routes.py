from flask import Blueprint, jsonify, request
from flask import current_app as app
from .models import User, Chapter, Subject, Quiz, Question, Score  # Updated imports
from . import db
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    hashed_password = generate_password_hash(data['password'], method='scrypt')
    new_user = User(
        username=data['username'],
        password=hashed_password,
        is_admin=False,
        dob = datetime.strptime(data['dob'], '%d/%m/%Y').date(),
        qualification = data['qualification']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@api.route('/login', methods=['POST']) 
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
        
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'is_admin': user.is_admin
    }), 200

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({
        'message': 'Protected endpoint',
        'user': user.username,
        'is_admin': user.is_admin
    })

@api.route('/admin-only', methods=['GET'])
@jwt_required()
def admin_only():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.is_admin == False:
        return jsonify({'error': 'Admin access required'}), 403
        
    return jsonify({'message': 'Admin endpoint'})






@api.route('/admin/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    data = request.get_json()
    new_subject = Subject(
        name=data['name'],
        description=data['description']
    )
    
    db.session.add(new_subject)
    db.session.commit()
    
    return jsonify({'message': 'Subject created successfully'}), 201

@api.route('/admin/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required()
def update_subject(subject_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    
    db.session.commit()
    return jsonify({'message': 'Subject updated successfully'})

@api.route('/admin/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    
    return jsonify({'message': 'Subject deleted successfully'})

@api.route('/admin/chapters', methods=['POST'])
@jwt_required()
def create_chapter():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    data = request.get_json()
    new_chapter = Chapter(
        name=data['name'],
        description=data['description'],
        subject_id=data['subject_id']
    )
    
    db.session.add(new_chapter)
    db.session.commit()
    
    return jsonify({'message': 'Chapter created successfully'}), 201

@api.route('/admin/chapters/<int:chapter_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_chapter(chapter_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        chapter.name = data.get('name', chapter.name)
        chapter.description = data.get('description', chapter.description)
        chapter.subject_id = data.get('subject_id', chapter.subject_id)
        db.session.commit()
        return jsonify({'message': 'Chapter updated successfully'})
        
    elif request.method == 'DELETE':
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({'message': 'Chapter deleted successfully'})

@api.route('/admin/quizzes', methods=['POST'])
@jwt_required()
def create_quiz():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    data = request.get_json()
    new_quiz = Quiz(
        chapter_id=data['chapter_id'],
        date_of_quiz=datetime.strptime(data['date_of_quiz'], '%Y-%m-%d %H:%M:%S'),
        time_duration=timedelta(minutes=int(data['duration_minutes'])),
        remarks=data.get('remarks', '')
    )
    
    db.session.add(new_quiz)
    db.session.commit()
    
    for q in data['questions']:
        question = Question(
            quiz_id=new_quiz.id,
            question_statement=q['question'],
            option1=q['options'][0],
            option2=q['options'][1],
            option3=q['options'][2],
            option4=q['options'][3],
            correct_option=q['correct_option']
        )
        db.session.add(question)
        
    db.session.commit()
    return jsonify({'message': 'Quiz created successfully'}), 201

@api.route('/admin/search/users', methods=['GET'])
@jwt_required()
def search_users():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    query = request.args.get('q', '')
    users = User.query.filter(User.username.ilike(f'%{query}%')).all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'is_admin': u.is_admin,
        'qualification': u.qualification
    } for u in users])

@api.route('/admin/search/subjects', methods=['GET'])
@jwt_required()
def search_subjects():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    query = request.args.get('q', '')
    subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description
    } for s in subjects])

@api.route('/admin/search/quizzes', methods=['GET'])
@jwt_required()
def search_quizzes():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    chapter_id = request.args.get('chapter_id')
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all() if chapter_id else Quiz.query.all()
    
    return jsonify([{
        'id': q.id,
        'chapter_id': q.chapter_id,
        'date_of_quiz': q.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S'),
        'duration_minutes': q.time_duration.total_seconds() / 60,
        'remarks': q.remarks
    } for q in quizzes])

@api.route('/admin/dashboard/summary', methods=['GET'])
@jwt_required()
def get_admin_dashboard_summary():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    total_users = User.query.filter_by(is_admin=False).count()
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    
    recent_scores = Score.query.order_by(Score.time_stamp_of_attempt.desc()).limit(10).all()
    
    return jsonify({
        'statistics': {
            'total_users': total_users,
            'total_subjects': total_subjects,
            'total_quizzes': total_quizzes
        },
        'recent_scores': [{
            'user': score.user.username,
            'quiz_id': score.quiz_id,
            'score': score.total_scored,
            'timestamp': score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S')
        } for score in recent_scores]
    })

@api.route('/admin/quizzes/<int:quiz_id>/questions', methods=['POST'])
@jwt_required()
def create_question(quiz_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    data = request.get_json()
    new_question = Question(
        quiz_id=quiz_id,
        question_statement=data['question_statement'],
        option1=data['option1'],
        option2=data['option2'], 
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option']
    )
    
    db.session.add(new_question)
    db.session.commit()
    
    return jsonify({'message': 'Question created successfully'}), 201

@api.route('/admin/questions/<int:question_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_question(question_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
        
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        question.question_statement = data.get('question_statement', question.question_statement)
        question.option1 = data.get('option1', question.option1)
        question.option2 = data.get('option2', question.option2)
        question.option3 = data.get('option3', question.option3)
        question.option4 = data.get('option4', question.option4)
        question.correct_option = data.get('correct_option', question.correct_option)
        db.session.commit()
        return jsonify({'message': 'Question updated successfully'})
        
    elif request.method == 'DELETE':
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message': 'Question deleted successfully'})

@api.route('/quizzes/available', methods=['GET'])
@jwt_required()
def get_available_quizzes():
    quizzes = Quiz.query.filter(Quiz.date_of_quiz > datetime.now()).all()
    return jsonify([{
        'id': q.id,
        'chapter_id': q.chapter_id,
        'chapter_name': q.chapter.name,
        'subject_name': q.chapter.subject.name,
        'date_of_quiz': q.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S'),
        'duration_minutes': q.time_duration.total_seconds() / 60,
        'remarks': q.remarks
    } for q in quizzes])

@api.route('/quizzes/<int:quiz_id>/attempt', methods=['POST'])
@jwt_required()
def attempt_quiz(quiz_id):
    current_user_id = get_jwt_identity()
    quiz = Quiz.query.get_or_404(quiz_id)
    
    now = datetime.now()
    if now < quiz.date_of_quiz or now > quiz.date_of_quiz + quiz.time_duration:
        return jsonify({'error': 'Quiz is not currently active'}), 400
        
    data = request.get_json()
    answers = data['answers']
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    correct_count = sum(1 for q, a in zip(questions, answers) if q.correct_option == a)
    total_score = (correct_count / len(questions)) * 100
    
    new_score = Score(
        quiz_id=quiz_id,
        user_id=current_user_id,
        time_stamp_of_attempt=datetime.now(),
        total_scored=total_score
    )
    
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({
        'message': 'Quiz submitted successfully',
        'score': total_score
    })

@api.route('/user/quiz-history', methods=['GET'])
@jwt_required()
def get_quiz_history():
    current_user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=current_user_id).order_by(Score.time_stamp_of_attempt.desc()).all()
    
    return jsonify([{
        'quiz_id': score.quiz_id,
        'chapter_name': score.quiz.chapter.name,
        'subject_name': score.quiz.chapter.subject.name,
        'score': score.total_scored,
        'attempt_date': score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S')
    } for score in scores])

@api.route('/user/dashboard/summary', methods=['GET'])
@jwt_required()
def get_user_dashboard_summary():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    print("printing user and current_user_id", user, current_user_id)

    user_scores = Score.query.filter_by(user_id=current_user_id).all()
    if not user_scores:
        print("No scores found for user")  # Debug: Check if user has scores
        return jsonify({'error': 'No scores found for this user', 'user_id': current_user_id}), 422

    total_quizzes_attempted = len(user_scores)
    avg_score = sum(score.total_scored for score in user_scores) / total_quizzes_attempted if total_quizzes_attempted > 0 else 0
    
    return jsonify({
        'statistics': {
            'total_attempts': total_quizzes_attempted,
            'average_score': avg_score
        },
        'recent_attempts': [{
            'quiz_id': score.quiz_id,
            'chapter_name': score.quiz.chapter.name,
            'score': score.total_scored,
            'attempt_date': score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S')
        } for score in user_scores[:5]]
    })

@api.route('/quizzes/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz_details(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    return jsonify({
        'quiz': {
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_minutes': quiz.time_duration.total_seconds() / 60,
            'remarks': quiz.remarks,
            'questions': [{
                'id': q.id,
                'question': q.question_statement,
                'options': [q.option1, q.option2, q.option3, q.option4],
                'correct_option': q.correct_option
            } for q in questions]
        }
    })
@api.route('/subjects/<int:subject_id>/chapters', methods=['GET'])
def get_subject_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject.id).all()
    
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in chapters])
