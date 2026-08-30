import time
from typing import Optional
from flask import Blueprint, render_template, request, jsonify, session, redirect

from app.services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__)
chat_service = ChatService()


@chat_bp.route('/chat', methods=['GET'])
@chat_bp.route('/farmer/chat', methods=['GET'])
def chat_view():
    """
    Renders the dedicated, full-featured Agri-SLM Conversational AI workspace.
    """
    user_name = session.get('user_name', 'Farmer')
    user_id = session.get('user_id', None)
    return render_template(
        'farmer/chat.html',
        user_name=user_name,
        user_id=user_id
    )


@chat_bp.route('/chat/api', methods=['POST'])
def chat_api():
    """
    Conversational text interface for Sinhala, English, and Tamil agricultural queries.
    Accepts JSON: {"message": "...", "language": "auto", "session_id": "..."}
    """
    try:
        data = request.get_json(silent=True) or {}
        message = data.get('message') or data.get('query') or ''
        language = data.get('language', 'auto')
        session_id = data.get('session_id')

        if not message.strip():
            return jsonify({
                "reply": "කරුණාකර ඔබගේ කෘෂිකාර්මික ගැටලුව හෝ පස් පරීක්ෂණ දත්ත ඇතුළත් කරන්න. (Please enter your agricultural query or soil test parameters.)",
                "detected_language": "si",
                "model_source": "system_guardrail"
            }), 200

        response = chat_service.generate_response(
            query=message,
            forced_lang=language,
            session_id=session_id
        )

        res_dict = response.model_dump() if hasattr(response, "model_dump") else response.dict()
        return jsonify(res_dict), 200

    except Exception as exc:
        return jsonify({
            "error": str(exc),
            "reply": f"පද්ධති දෝෂයක් හටගන්නා ලදී (System error occurred): {str(exc)}"
        }), 500


@chat_bp.route('/chat/upload', methods=['POST'])
def chat_upload():
    """
    Ingests and parses laboratory soil test sheets (PDF, CSV, TXT),
    extracts N, P, K, pH parameters, and evaluates them with the trained ML classifier.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        message = request.form.get('message', 'Please analyze this soil report and recommend the best high-yielding crops.')
        language = request.form.get('language', 'auto')
        session_id = request.form.get('session_id')

        content_bytes = file.read()
        response = chat_service.process_file_upload(
            file_bytes=content_bytes,
            filename=file.filename or "uploaded_report",
            user_prompt=message,
            session_id=session_id,
            language=language or "auto"
        )

        res_dict = response.model_dump() if hasattr(response, "model_dump") else response.dict()
        return jsonify(res_dict), 200

    except Exception as exc:
        return jsonify({"error": f"Failed to process file: {str(exc)}"}), 500


@chat_bp.route('/chat/status', methods=['GET'])
def chat_status():
    """
    Returns live engine health, active ML classifier specs, and zero-cloud confirmation.
    """
    status_obj = chat_service.get_engine_status()
    res_dict = status_obj.model_dump() if hasattr(status_obj, "model_dump") else status_obj.dict()
    return jsonify(res_dict), 200
