from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for
)
from sqlalchemy import func
import os

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db, User, Analysis

from utils.parser import (
    extract_text_from_pdf,
    extract_skills,
    get_matching_and_missing_skills,
    generate_ai_suggestions
)

from utils.report_generator import generate_report

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']

        password = generate_password_hash(
            request.form['password']
        )

        user = User(
    username=username,
    email=email,
    password=password
)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():

    message = ""
    extracted_text = ""

    detected_skills = []

    matching_skills = []
    missing_skills = []

    ats_score = 0

    suggestions = []

    report_ready = False

    if request.method == 'POST':

        file = request.files['resume']

        job_description = request.form['job_description']

        if file.filename != '':

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )

            file.save(filepath)

            message = "Resume uploaded successfully!"

            extracted_text = extract_text_from_pdf(filepath)

            detected_skills = extract_skills(
                extracted_text
            )

            matching_skills, missing_skills, ats_score = get_matching_and_missing_skills(
                detected_skills,
                job_description
            )

            suggestions = generate_ai_suggestions(
                missing_skills,
                ats_score
            )

            report_path = os.path.join(
                app.config['REPORT_FOLDER'],
                'resume_report.pdf'
            )

            generate_report(
                report_path,
                ats_score,
                matching_skills,
                missing_skills,
                suggestions
            )

            report_ready = True

            analysis = Analysis(
                filename=file.filename,
                ats_score=ats_score,
                user_id=current_user.id
            )

            db.session.add(analysis)
            db.session.commit()

    return render_template(
        'index.html',
        message=message,
        extracted_text=extracted_text,
        detected_skills=detected_skills,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        ats_score=ats_score,
        report_ready=report_ready,
        suggestions=suggestions,
        username=current_user.username
    )


@app.route('/download-report')
@login_required
def download_report():

    report_path = os.path.join(
        app.config['REPORT_FOLDER'],
        'resume_report.pdf'
    )

    return send_file(
        report_path,
        as_attachment=True
    )


@app.route('/history')
@login_required
def history():

    analyses = Analysis.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        'history.html',
        analyses=analyses
    )
@app.route('/admin')
@login_required
def admin():

    if not current_user.is_admin:

        return "Access Denied"


    total_users = User.query.count()

    total_analyses = Analysis.query.count()

    average_score = db.session.query(
        func.avg(Analysis.ats_score)
    ).scalar()

    if average_score:

        average_score = round(
            average_score,
            2
        )

    else:

        average_score = 0

    recent_analyses = Analysis.query.order_by(
        Analysis.id.desc()
    ).limit(5).all()

    return render_template(

        'admin.html',

        total_users=total_users,

        total_analyses=total_analyses,

        average_score=average_score,

        recent_analyses=recent_analyses
    )

if __name__ == '__main__':

    app.run(debug=True)