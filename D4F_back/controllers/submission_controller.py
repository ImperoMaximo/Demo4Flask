from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Submission

bp = Blueprint('submissions', __name__, url_prefix='/api')


@bp.route('/submissions', methods=['GET'])
def get_submissions():
    items = Submission.query.order_by(Submission.created_at.desc()).all()
    return jsonify([i.to_dict() for i in items]), 200


@bp.route('/submissions', methods=['POST'])
def create_submission():
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'error': 'text is required'}), 400

    s = Submission(text=text)
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201
