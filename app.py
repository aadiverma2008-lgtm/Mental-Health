"""
Agentic AI Mental Health Awareness & Suicide Prevention Agent
Flask Application Entry Point
"""
import os
from flask import Flask, render_template, request, jsonify, session
from services.agent import MentalHealthAgent

# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)

    # Secret key for session management — override via environment variable in production
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-prod")

    # Optional: OpenAI / Gemini API key injected from environment
    app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
    app.config["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY", "")

    # Instantiate the agent once (stateless per request; history is passed from client)
    agent = MentalHealthAgent(
        openai_api_key=app.config["OPENAI_API_KEY"],
        gemini_api_key=app.config["GEMINI_API_KEY"],
    )

    # -----------------------------------------------------------------------
    # Routes
    # -----------------------------------------------------------------------

    @app.route("/")
    def index():
        """Landing / dashboard page."""
        return render_template("index.html")

    @app.route("/chat")
    def chat():
        """Chat interface page."""
        # Initialise fresh conversation history for this browser session
        if "history" not in session:
            session["history"] = []
        return render_template("chat.html")

    @app.route("/api/chat", methods=["POST"])
    def api_chat():
        """
        JSON endpoint consumed by the frontend Fetch calls.

        Expected body:
            { "message": "<user text>", "history": [ {"role": "...", "content": "..."}, ... ] }

        Response:
            {
              "reply":     "<assistant text>",
              "risk_level": "low" | "medium" | "high",
              "crisis":     true | false,
              "nudge":      "<optional proactive suggestion>" | null
            }
        """
        data = request.get_json(force=True, silent=True) or {}
        user_message: str = (data.get("message") or "").strip()
        history: list   = data.get("history") or []

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        result = agent.respond(user_message=user_message, history=history)
        return jsonify(result)

    @app.route("/api/health")
    def health():
        """Simple liveness probe."""
        return jsonify({"status": "ok"})

    return app


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
