from flask import Flask, redirect, render_template, url_for, flash, session, request
from models.database import db, User
from routes.analyzer import analyze_marks
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MySQL DB config – used your own credentials here of mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/student_analyzer_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            flash("No file selected.", "danger")
            return redirect(url_for('index'))

        if not file.filename.endswith('.csv'):
            flash("Invalid file type. Please upload a CSV.", "danger")
            return redirect(url_for('index'))

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        upload = User(filename=file.filename)
        db.session.add(upload)
        db.session.commit()

        flash("File uploaded successfully!", "success")
        return redirect(url_for('analyzer', filename=file.filename))

    return render_template('index.html')


@app.route('/analyzer/<filename>')
def analyzer(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    summary = analyze_marks(filepath)
    if not summary:
        flash("Error analyzing file.", "danger")
        return redirect(url_for('index'))

    return render_template('analyzer.html',
                           average=summary["Average"],
                           maximum=summary["Highest"],
                           minimum=summary["Lowest"],
                           labels=summary["HeaderS"],
                           marks=summary["Average"],
                           chart_path=summary["Chart_path"])


if __name__ == "__main__":
    app.run(debug=True)