# -*- coding: utf-8 -*-
"""
End-to-end live test for the Mental Health AI Agent backend.

Starts the FastAPI server as a subprocess, waits for it to be ready,
runs a full suite of HTTP tests, then shuts it down cleanly.

Usage (from project root):
    python test_e2e.py

Requirements: backend/.env must have a valid OPENAI_API_KEY and SECRET_KEY.
If the OpenAI key is invalid the chat tests are skipped with a clear message;
all other endpoint tests still run.
"""
import subprocess
import sys
import io

# Force UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import time
import os
import requests

BASE_URL = "http://localhost:8000"
SERVER_STARTUP_TIMEOUT = 90  # seconds

# ---- colour helpers ---------------------------------------------------------
def green(s):  return f"\033[32m{s}\033[0m"
def red(s):    return f"\033[31m{s}\033[0m"
def yellow(s): return f"\033[33m{s}\033[0m"
def cyan(s):   return f"\033[36m{s}\033[0m"
def bold(s):   return f"\033[1m{s}\033[0m"

# ---- result tracking --------------------------------------------------------
passed  = []
failed  = []
skipped = []

def check(name, condition, detail=""):
    if condition:
        passed.append(name)
        print(f"  {green('[PASS]')} {name}")
    else:
        failed.append(name)
        print(f"  {red('[FAIL]')} {name}" + (f" -- {detail}" if detail else ""))

def skip(name, reason=""):
    skipped.append(name)
    print(f"  {yellow('[SKIP]')} {name}" + (f" -- {reason}" if reason else ""))

def section(title):
    print(f"\n{bold(cyan('--- ' + title + ' ---'))}")

def get(path, **kw):
    return requests.get(f"{BASE_URL}{path}", timeout=10, **kw)

def post(path, payload, **kw):
    return requests.post(f"{BASE_URL}{path}", json=payload, timeout=30, **kw)

# ---- server management ------------------------------------------------------
def start_server():
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", "0.0.0.0", "--port", "8000", "--no-access-log"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

def wait_for_server(proc, timeout=SERVER_STARTUP_TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            out = proc.stdout.read()
            print(red(f"\nServer exited early (code {proc.returncode}):"))
            print(out[-3000:])
            return False
        try:
            r = requests.get(f"{BASE_URL}/api/health", timeout=2)
            if r.status_code == 200:
                svc = r.json().get("services", {})
                if svc.get("rag") and svc.get("ai_agent"):
                    return True
                print(f"  {yellow('[wait]')} Services initialising... {svc}", end="\r")
        except requests.exceptions.ConnectionError:
            print(f"  {yellow('[wait]')} Waiting for server...                  ", end="\r")
        except Exception:
            pass
        time.sleep(2)
    return False

# ---- helper: read last N bytes of log for error detection -------------------
def _read_log_tail(n=6000):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "backend", "logs", "app.log")
    try:
        with open(log_path, encoding="utf-8", errors="replace") as f:
            return f.read()[-n:]
    except Exception:
        return ""

# ---- test suites ------------------------------------------------------------

def test_health_and_info():
    section("Health & Info Endpoints")

    r = get("/api/health")
    check("GET /api/health -> 200", r.status_code == 200)
    data = r.json()
    check("health.status == 'healthy'", data.get("status") == "healthy")
    check("RAG service running",     data.get("services", {}).get("rag") is True)
    check("AI agent running",        data.get("services", {}).get("ai_agent") is True)

    r = get("/")
    check("GET / -> 200", r.status_code == 200)
    body = r.json()
    check("Root has disclaimer field",    "disclaimer" in body)
    check("Root disclaimer is non-empty", bool(body.get("disclaimer")))

    r = get("/api/disclaimer")
    check("GET /api/disclaimer -> 200", r.status_code == 200)
    body = r.json()
    check("Disclaimer has 'disclaimer' key", "disclaimer" in body)
    check("Disclaimer has 'emergency' key",  "emergency" in body)
    check("Disclaimer has 'privacy' key",    "privacy" in body)

    r = get("/api/crisis-helplines?country=india")
    check("GET /api/crisis-helplines?country=india -> 200", r.status_code == 200)
    check("Helplines has AASRA entry", "AASRA" in r.json().get("helplines", {}))

    r = get("/api/crisis-helplines?country=mars")
    check("Unknown country -> 404", r.status_code == 404)


def test_resources():
    section("Resource Endpoints")

    r = get("/api/resources/mindfulness")
    check("GET /api/resources/mindfulness -> 200", r.status_code == 200)
    check("Mindfulness has resources list", isinstance(r.json().get("resources"), list))

    check("GET /api/resources/coping-strategies -> 200",
          get("/api/resources/coping-strategies").status_code == 200)
    check("GET /api/resources/self-care -> 200",
          get("/api/resources/self-care").status_code == 200)

    r = get("/api/resources/all")
    check("GET /api/resources/all -> 200", r.status_code == 200)
    keys = list(r.json().get("resources", {}).keys())
    check("All resources has mindfulness/coping/self_care",
          all(k in keys for k in ["mindfulness", "coping_strategies", "self_care"]))

    r = get("/api/resources/breathing-exercises")
    check("GET /api/resources/breathing-exercises -> 200", r.status_code == 200)
    check("Breathing exercises has 4+ exercises",
          len(r.json().get("exercises", [])) >= 4)

    r = get("/api/resources/emergency-resources")
    check("GET /api/resources/emergency-resources -> 200", r.status_code == 200)
    check("Emergency resources has crisis_helplines", "crisis_helplines" in r.json())


def test_user():
    section("User / Consent / Mood Endpoints")

    r = post("/api/user/consent", {
        "user_id": "test_e2e_user",
        "consent_type": "risk_monitoring",
        "granted": True,
    })
    check("POST /api/user/consent -> 200", r.status_code == 200)
    check("Consent response has user_id", r.json().get("user_id") == "test_e2e_user")

    r = get("/api/user/consent/test_e2e_user")
    check("GET /api/user/consent/{id} -> 200", r.status_code == 200)
    check("Consent stored correctly",
          r.json().get("consents", {}).get("risk_monitoring", {}).get("granted") is True)

    r = post("/api/user/mood", {
        "user_id": "test_e2e_user",
        "mood_score": 0.65,
        "notes": "Feeling okay today",
    })
    check("POST /api/user/mood -> 200", r.status_code == 200)

    r = get("/api/user/mood/test_e2e_user")
    check("GET /api/user/mood/{id} -> 200", r.status_code == 200)
    check("Mood entry returned", len(r.json().get("entries", [])) >= 1)

    check("GET /api/user/profile/{id} -> 200",
          get("/api/user/profile/test_e2e_user").status_code == 200)

    r = requests.delete(f"{BASE_URL}/api/user/data/test_e2e_user", timeout=10)
    check("DELETE /api/user/data/{id} -> 200", r.status_code == 200)


def test_risk_assessment():
    section("Risk Assessment Endpoints")

    r = post("/api/risk/assess", {
        "user_id": "test_risk_user",
        "messages": ["I feel a bit stressed about work today"],
    })
    check("POST /api/risk/assess -> 200", r.status_code == 200)
    body = r.json()
    check("Risk level present", body.get("risk_level") in ["low", "medium", "high"])
    check("Risk score in [0,1]", 0.0 <= body.get("risk_score", -1) <= 1.0)
    check("Recommendations present", len(body.get("recommendations", [])) > 0)

    r = post("/api/risk/assess", {
        "user_id": "test_risk_user_high",
        "messages": ["I want to kill myself", "I see no point in living"],
    })
    check("High-risk message assessed -> 200", r.status_code == 200)
    body = r.json()
    check("High-risk -> risk_level=high",         body.get("risk_level") == "high")
    check("High-risk -> requires_immediate_action", body.get("requires_immediate_action") is True)

    check("GET /api/risk/alerts -> 200 (no data)",
          get("/api/risk/alerts/test_risk_user_no_data").status_code == 200)
    check("GET /api/risk/history -> 200 (no data)",
          get("/api/risk/history/test_risk_user_no_data").status_code == 200)

    r = get("/api/risk/predict/test_risk_user_no_data")
    check("GET /api/risk/predict -> 200 (no data)", r.status_code == 200)
    body = r.json()
    check("Predict no-data has 'prediction' key",  "prediction" in body)
    check("Predict no-data message returned",
          body.get("prediction") == "insufficient_data")


def test_chat_agent():
    section("Chat / AI Agent Endpoints (uses live OpenAI)")

    USER = "test_chat_user_e2e"

    # ---- normal message ----
    print(f"  {yellow('[wait]')} Sending message to AI agent (may take ~5s)...")
    r = post("/api/chat/message", {
        "user_id": USER,
        "message": "I've been feeling quite anxious about my exams lately.",
        "context": {"mood": "anxious"},
    })

    # Detect invalid API key before reporting as a test failure
    api_key_invalid = False
    if r.status_code != 200:
        log = _read_log_tail()
        if "401" in log and "api_key" in log.lower():
            api_key_invalid = True
            print()
            print(f"  {yellow('[!]')} OpenAI API key is invalid or expired.")
            print(f"  {yellow('[!]')} Update OPENAI_API_KEY in backend/.env with a valid key.")
            print(f"  {yellow('[!]')} All other endpoints passed -- skipping chat/AI tests.")

    check("POST /api/chat/message -> 200", r.status_code == 200)
    if r.status_code == 200:
        body = r.json()
        check("Chat response has 'response' field",
              bool(body.get("response")))
        check("Chat response has risk_assessment",
              "risk_assessment" in body)
        check("Chat response has recommendations",
              len(body.get("recommendations", [])) > 0)
        check("requires_immediate_attention is bool",
              isinstance(body.get("requires_immediate_attention"), bool))
        check("No crisis helplines for low-risk message",
              body.get("crisis_helplines") is None or
              not body.get("requires_immediate_attention"))
        print(f"\n    {cyan('Agent said:')} {body['response'][:150]}...")
    else:
        reason = "invalid OpenAI API key -- update backend/.env" if api_key_invalid else "chat request failed"
        for t in ["Chat response has 'response' field", "Chat response has risk_assessment",
                  "Chat response has recommendations", "requires_immediate_attention is bool",
                  "No crisis helplines for low-risk message"]:
            skip(t, reason)

    # ---- high-risk message ----
    print(f"\n  {yellow('[wait]')} Sending high-risk message...")
    r = post("/api/chat/message", {
        "user_id": USER + "_crisis",
        "message": "I want to kill myself. I have a plan and I see no reason to continue.",
        "context": {},
    })
    check("POST /api/chat/message (high-risk) -> 200", r.status_code == 200)
    if r.status_code == 200:
        body = r.json()
        check("High-risk -> requires_immediate_attention=True",
              body.get("requires_immediate_attention") is True)
        check("High-risk -> crisis_helplines provided",
              body.get("crisis_helplines") is not None)
        print(f"\n    {cyan('Agent excerpt:')} {body.get('response','')[:150]}...")
    else:
        reason = "invalid OpenAI API key" if api_key_invalid else "chat request failed"
        skip("High-risk -> requires_immediate_attention=True", reason)
        skip("High-risk -> crisis_helplines provided", reason)

    # ---- history / clear ----
    r = get(f"/api/chat/history/{USER}")
    check("GET /api/chat/history/{id} -> 200", r.status_code == 200)
    if not api_key_invalid:
        check("History has at least 2 messages", r.json().get("message_count", 0) >= 2)
    else:
        skip("History has at least 2 messages", "no messages sent (API key invalid)")

    r = requests.delete(f"{BASE_URL}/api/chat/history/{USER}", timeout=10)
    check("DELETE /api/chat/history/{id} -> 200", r.status_code == 200)

    r = get(f"/api/chat/history/{USER}")
    check("History empty after clear", r.json().get("message_count") == 0)


# ---- entry point ------------------------------------------------------------

def main():
    print(bold("\n=== Mental Health AI Agent -- E2E Test Suite ==="))

    server_already_running = False
    proc = None
    try:
        r = requests.get(f"{BASE_URL}/api/health", timeout=3)
        if r.status_code == 200 and r.json().get("services", {}).get("ai_agent"):
            server_already_running = True
            print(f"\n{green('[OK]')} Server already running -- skipping startup")
    except Exception:
        pass

    if not server_already_running:
        print(f"\n{yellow('[wait]')} Starting backend server...")
        proc = start_server()
        print(f"  PID: {proc.pid}")
        if not wait_for_server(proc):
            print(f"\n{red('[FAIL]')} Server failed to start within {SERVER_STARTUP_TIMEOUT}s")
            print("  Make sure backend/.env has valid OPENAI_API_KEY and SECRET_KEY")
            if proc:
                proc.terminate()
            sys.exit(1)
        print(f"\n{green('[OK]')} Server ready")

    try:
        test_health_and_info()
        test_resources()
        test_user()
        test_risk_assessment()
        test_chat_agent()
    finally:
        if proc and not server_already_running:
            print(f"\n{yellow('Stopping server...')}")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    total = len(passed) + len(failed) + len(skipped)
    print(f"\n{bold('== Results ==')}")
    print(f"  {green(str(len(passed)) + ' passed')}  "
          f"{red(str(len(failed)) + ' failed')}  "
          f"{yellow(str(len(skipped)) + ' skipped')}  "
          f"/ {total} total")

    if failed:
        print(f"\n{red('Failed:')}")
        for f in failed:
            print(f"  - {f}")

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
