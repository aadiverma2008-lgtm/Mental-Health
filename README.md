# 🌿 Solace — Agentic AI Mental Health Awareness & Suicide Prevention Agent

> **Disclaimer:** Solace is an AI companion, **not** a licensed therapist or medical professional.
> It is designed to provide a safe, empathetic first point of support — not to replace professional mental health care.
> If you or someone you know is in crisis, please call **988** (Suicide & Crisis Lifeline) or text **HOME** to **741741** immediately.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [API Reference](#api-reference)
- [AI Agent Architecture](#ai-agent-architecture)
- [Safety Guardrails](#safety-guardrails)
- [LLM Configuration](#llm-configuration)
- [Crisis Resources](#crisis-resources)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Solace** is a Flask-based web application that provides an empathetic, agentic AI-powered conversational companion for mental health awareness and suicide prevention. It bridges the gap between "suffering alone" and "receiving professional care" by offering a stigma-free, always-available, safety-first support space.

The system is built around three core principles:

1. **Safety First** — high-risk inputs bypass the LLM entirely; only hard-coded crisis hotline content is returned.
2. **Proactive Support** — real-time sentiment analysis nudges users toward mindfulness exercises before distress escalates.
3. **Radical Transparency** — Solace always identifies itself as an AI and actively encourages professional help.

---

## Features

| Feature | Description |
|---|---|
| 💬 **Empathetic Chat Interface** | Clean, calming UI with a full conversation history, typing indicator, and markdown rendering |
| 🛡️ **Safety Override** | 25-pattern regex risk engine classifies every message; HIGH risk bypasses the LLM entirely |
| 🆘 **Permanent Crisis Banner** | Undismissable sticky banner on every page with 988, 741741, and 911 links |
| 🧘 **Proactive Mindfulness Nudges** | 6 evidence-based exercises (box breathing, grounding, journaling, etc.) surfaced contextually |
| 📊 **Real-Time Risk Badge** | Live low / medium / high indicator shown in the chat header |
| 🔁 **LLM Fallback Chain** | OpenAI GPT-4o-mini → Google Gemini 1.5 Flash → built-in mock (zero API cost) |
| 🔒 **Privacy by Design** | No database, no persistent logging — conversation lives in browser session only |
| ♿ **Accessible UI** | ARIA live regions, `role` attributes, focus rings, reduced-motion support |
| 📱 **Fully Responsive** | Mobile-first layout that works on all screen sizes |

---

## Project Structure

```
flask-project-mental-health/
│
├── app.py                  # Flask application factory, routes, API endpoints
│
├── services/
│   ├── __init__.py         # Package init
│   └── agent.py            # MentalHealthAgent — risk engine, LLM chain, nudge logic
│
├── templates/
│   ├── base.html           # Base layout: sticky crisis banner, nav, footer
│   ├── index.html          # Landing / dashboard page
│   └── chat.html           # Chat interface + Fetch API JavaScript
│
├── static/
│   └── css/
│       └── styles.css      # Custom CSS — chat bubbles, animations, crisis overlay
│
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Primary language |
| Flask | ≥ 3.0.0 | Web framework, routing, sessions, JSON API |
| Jinja2 | bundled | Server-side HTML templating |
| python-dotenv | ≥ 1.0.0 | Environment variable management |
| Python `re` | stdlib | Risk assessment regex engine |
| Python `random` | stdlib | Probabilistic nudge selection |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| HTML5 | — | Semantic markup, ARIA accessibility |
| Tailwind CSS | v3 (CDN) | Utility-first styling with custom calm/sage palette |
| Custom CSS3 | — | Chat bubbles, animations, crisis overlay (315 lines) |
| Vanilla JavaScript | ES2020 | Fetch API, conversation state, DOM rendering |
| Inter + Lora | Google Fonts | UI typeface (Inter) + heading typeface (Lora) |

### AI / LLM
| Provider | Model | Activation |
|---|---|---|
| OpenAI *(optional)* | GPT-4o-mini | Set `OPENAI_API_KEY` |
| Google Gemini *(optional)* | Gemini 1.5 Flash | Set `GEMINI_API_KEY` |
| Built-in Mock | — | Auto-used when no API key is set |

---

## Getting Started

### Prerequisites

- Python **3.10** or higher
- `pip` package manager
- *(Optional)* An OpenAI or Google Gemini API key for real AI responses

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/solace-mental-health.git
cd solace-mental-health
```

**2. Create and activate a virtual environment** *(recommended)*

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. *(Optional)* Install an LLM provider**

```bash
# For OpenAI (GPT-4o-mini)
pip install openai>=1.30.0

# For Google Gemini
pip install google-generativeai>=0.5.0
```

### Environment Variables

Create a `.env` file in the project root:

```env
# Required in production — change this to a strong random string
FLASK_SECRET_KEY=your-secret-key-here

# Optional — provide ONE of these for real AI responses
# If neither is set, the built-in mock responses are used automatically
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

> ⚠️ **Never commit your `.env` file to version control.** Add it to `.gitignore`.

### Running the App

**Development server:**

```bash
python app.py
```

The app will be available at **http://localhost:5000**

**Production *(example with Gunicorn)*:**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:app"
```

---

## API Reference

### `GET /`
Returns the landing / dashboard page.

---

### `GET /chat`
Returns the chat interface page.

---

### `POST /api/chat`
The primary JSON endpoint consumed by the frontend.

**Request body:**
```json
{
  "message": "I've been feeling really anxious lately",
  "history": [
    { "role": "user",      "content": "Hello" },
    { "role": "assistant", "content": "Hi! I'm Solace..." }
  ]
}
```

**Response:**
```json
{
  "reply":      "I hear you — anxiety can feel really overwhelming...",
  "risk_level": "medium",
  "crisis":     false,
  "nudge":      "💨 Box Breathing — Try this with me: Breathe in for 4 counts..."
}
```

| Field | Type | Description |
|---|---|---|
| `reply` | `string` | The assistant's response (may contain Markdown) |
| `risk_level` | `"low"` \| `"medium"` \| `"high"` | Assessed risk level of the user's message |
| `crisis` | `boolean` | `true` if safety override was triggered; LLM was bypassed |
| `nudge` | `string` \| `null` | Optional proactive mindfulness suggestion |

**Error response (400):**
```json
{ "error": "Empty message" }
```

---

### `GET /api/health`
Liveness probe for monitoring and deployment health checks.

**Response:**
```json
{ "status": "ok" }
```

---

## AI Agent Architecture

The `MentalHealthAgent` class in [`services/agent.py`](services/agent.py) is a **stateless agent** — conversation history is passed in on every call, making it safe across multiple workers and processes.

```
User message
     │
     ▼
┌─────────────────────────────┐
│   1. Risk Assessment Layer  │  ← 25 regex patterns → low / medium / high
└────────────┬────────────────┘
             │
     ┌───────┴───────┐
     │               │
  HIGH risk       MEDIUM / LOW risk
     │               │
     ▼               ▼
┌──────────┐   ┌────────────────────────────────┐
│ SAFETY   │   │  2. LLM Call                   │
│ OVERRIDE │   │  OpenAI → Gemini → Mock        │
│ (no LLM) │   └──────────────┬─────────────────┘
└──────────┘                  │
                              ▼
                   ┌──────────────────────┐
                   │  3. Nudge Engine     │
                   │  30% (medium risk)   │
                   │  15% (low risk)      │
                   └──────────┬───────────┘
                              │
                              ▼
                      JSON Response
           { reply, risk_level, crisis, nudge }
```

### Risk Assessment Patterns

| Level | Pattern Count | Examples |
|---|---|---|
| **HIGH** — crisis | 17 keyword patterns | "suicidal", "kill myself", "end my life", "cutting myself", "overdose" |
| **HIGH** — despair | 8 phrase patterns | "I feel hopeless", "I'm a burden", "nothing matters", "I give up" |
| **MEDIUM** — distress | 9 phrase patterns | "I feel depressed", "I'm overwhelmed", "panic attack", "feeling lonely" |

### Proactive Nudges

Six evidence-based exercises are available in the nudge library:

| Type | Exercise |
|---|---|
| 🌬️ Breathing | Box Breathing (4-4-4-4 counts) |
| 🌿 Grounding | 5-4-3-2-1 Sensory Technique |
| 🧘 Mindfulness | One-Minute Breath Observation |
| 💛 Self-Compassion | Loving-Kindness Touch Practice |
| 🚶 Movement | 30-Second Micro-Movement Break |
| 📓 Journaling | 3-Sentence Reflective Prompt |

---

## Safety Guardrails

Safety is the **primary architectural concern** — not an afterthought.

### 1. Hard-coded Safety Override
When `assess_risk()` returns `"high"`, the `respond()` function returns **immediately** before any LLM is called. The response is a Python constant (`CRISIS_RESPONSE`) containing only:
- A compassionate acknowledgement
- 988 Suicide & Crisis Lifeline
- Crisis Text Line (741741)
- IASP International Crisis Centres directory

This cannot be overridden by prompt injection, API failure, or any runtime condition.

### 2. Permanent Crisis Banner
`templates/base.html` contains a `position: sticky; top: 0; z-index: 50` red banner with **no close button**, visible on every page at all times. It includes direct `tel:` links for 988 and 911, and an `sms:` link for 741741.

### 3. In-Chat Crisis Overlay
When the API returns `crisis: true`, the JavaScript in `chat.html` displays a full-width overlay inside the chat window with three large, tappable hotline buttons.

### 4. XSS Prevention
- Jinja2 auto-escapes all server-rendered variables
- The JavaScript markdown renderer HTML-encodes all user input (`&`, `<`, `>`) before any DOM insertion

### 5. No Persistent Data
Zero database. No server-side conversation logging. All history is stored exclusively in the browser session — conversations are gone when the tab closes.

---

## LLM Configuration

The agent uses a priority fallback chain:

```
OPENAI_API_KEY set?  ──YES──▶  GPT-4o-mini (Chat Completions API)
       │
       NO
       │
GEMINI_API_KEY set?  ──YES──▶  Gemini 1.5 Flash (GenerativeModel API)
       │
       NO
       │
       ▼
  Built-in mock responses (7 empathetic templates, rotated by conversation length)
```

The built-in mock requires **zero API keys and zero cost** — the app is fully functional for demos and development without any external service.

### System Prompt
The LLM is instructed to:
- Identify as "Solace", an AI companion (not a therapist)
- Listen actively, validate emotions, ask open-ended questions
- Never diagnose, prescribe, or give medical advice
- Keep responses concise (3–5 sentences)
- Always encourage professional help for persistent concerns

---

## Crisis Resources

These resources are hard-coded into the application and displayed at all times:

| Resource | Contact | Availability |
|---|---|---|
| 🆘 988 Suicide & Crisis Lifeline | Call or text **988** | 24/7, US |
| 💬 Crisis Text Line | Text **HOME** to **741741** | 24/7, US |
| 🌍 IASP International Crisis Centres | https://www.iasp.info/resources/Crisis_Centres/ | Worldwide |
| 🤝 NAMI Helpline | 1-800-950-NAMI (6264) | Mon–Fri, 10am–10pm ET |
| 🚨 Emergency Services | **911** | 24/7, US |

---

## Contributing

Contributions that improve safety, empathy, or accessibility are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes, ensuring no existing safety guardrails are weakened
4. Test thoroughly, paying special attention to crisis detection patterns
5. Submit a pull request with a clear description of changes

> ⚠️ **Critical:** Do not submit PRs that modify `CRISIS_RESPONSE`, `CRISIS_KEYWORDS`, or `HIGH_RISK_PHRASES` without a very detailed safety justification. These constants exist to protect users.

---

## License

This project is released under the **MIT License**.

---

<div align="center">

Built with care and responsibility. 💙

**If you are in crisis right now, please call [988](tel:988) immediately.**

</div>
