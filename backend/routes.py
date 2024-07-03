# backend/routes.py
from flask import render_template, request, jsonify, current_app as app
from . import db
from .models import User, CV, ParsedData, Ranking, AnalysisResult

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cv_upload_page')
def cv_upload_page():
    return render_template('cv_upload_page.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    user_id = request.form['user_id']
    file = request.files['file']
    file_path = f'uploads/{file.filename}'
    file.save(file_path)

    new_cv = CV(user_id=user_id, file_path=file_path)
    db.session.add(new_cv)
    db.session.commit()

    return jsonify({"message": "CV uploaded successfully", "cv_id": new_cv.id})

@app.route('/parse_cv', methods=['POST'])
def parse_cv():
    cv_id = request.form['cv_id']
    parsed_data = "Parsed data from CV"  # Placeholder

    new_parsed_data = ParsedData(cv_id=cv_id, data=parsed_data)
    db.session.add(new_parsed_data)
    db.session.commit()

    return jsonify({"message": "CV parsed successfully", "parsed_data_id": new_parsed_data.id})

@app.route('/rank_candidates', methods=['POST'])
def rank_candidates():
    cv_id = request.form['cv_id']
    rank = 1  # Placeholder

    new_ranking = Ranking(cv_id=cv_id, rank=rank)
    db.session.add(new_ranking)
    db.session.commit()

    return jsonify({"message": "Candidates ranked successfully", "ranking_id": new_ranking.id})

@app.route('/analysis_progress', methods=['GET'])
def analysis_progress():
    cv_id = request.args.get('cv_id')
    progress = 50  # Placeholder

    return jsonify({"cv_id": cv_id, "progress": progress})

@app.route('/get_results', methods=['GET'])
def get_results():
    cv_id = request.args.get('cv_id')
    results = AnalysisResult.query.filter_by(cv_id=cv_id).first()

    if results:
        return jsonify({"cv_id": cv_id, "results": results.results})
    else:
        return jsonify({"message": "No results found"}), 404
