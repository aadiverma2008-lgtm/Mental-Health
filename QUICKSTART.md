# Quick Start Guide - Testing the Mental Health AI Agent

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.9 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] OpenAI API key (get from https://platform.openai.com/api-keys)
- [ ] Git installed (optional, for version control)

---

## Step-by-Step Testing Guide

### Step 1: Set Up Backend (5 minutes)

#### 1.1 Open Terminal in Backend Directory

```bash
cd backend
```

#### 1.2 Create Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 1.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will take 2-3 minutes. You'll see packages being installed.

#### 1.4 Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env    # Windows
# OR
cp .env.example .env      # Mac/Linux
```

**Edit the `.env` file** and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
SECRET_KEY=your-secret-key-here-use-any-random-string
```

To generate a secure SECRET_KEY:
```bash
# Windows PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})

# Mac/Linux
openssl rand -hex 32
```

#### 1.5 Create Required Directories

```bash
mkdir data\vector_store logs    # Windows
# OR
mkdir -p data/vector_store logs  # Mac/Linux
```

#### 1.6 Start the Backend Server

```bash
python main.py
```

**Expected Output:**
```
INFO: Starting Mental Health AI Agent...
INFO: RAG Service initialized
INFO: AI Agent initialized successfully
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is now running!** Keep this terminal open.

---

### Step 2: Set Up Frontend (3 minutes)

#### 2.1 Open New Terminal in Frontend Directory

```bash
cd frontend
```

#### 2.2 Install Node Dependencies

```bash
npm install
```

This will take 2-3 minutes.

#### 2.3 Create Frontend Environment File

Create a file named `.env` in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

#### 2.4 Start the Frontend Development Server

```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view mental-health-ai-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

Your browser should automatically open to `http://localhost:3000`

✅ **Frontend is now running!**

---

## Step 3: Test the Application (10 minutes)

### Test 1: Initial Setup Flow

1. **Disclaimer Dialog**
   - ✅ Verify disclaimer appears on first load
   - ✅ Read through the medical disclaimer
   - ✅ Click "I Understand and Accept"

2. **Consent Dialog**
   - ✅ Review consent options
   - ✅ Check at least "Risk Monitoring" or "Data Collection"
   - ✅ Click "Save Preferences and Continue"

### Test 2: Chat Functionality

1. **Navigate to Chat**
   - Click "Chat" in the navigation menu

2. **Test Low-Risk Message**
   ```
   Send: "I'm feeling a bit stressed about work today"
   ```
   - ✅ Verify you get an empathetic response
   - ✅ Check risk level shows as "low"
   - ✅ Verify recommendations are provided

3. **Test Medium-Risk Message**
   ```
   Send: "I feel hopeless and don't know what to do"
   ```
   - ✅ Verify risk level increases to "medium"
   - ✅ Check for supportive recommendations
   - ✅ Verify empathetic tone in response

4. **Test High-Risk Message** (IMPORTANT TEST)
   ```
   Send: "I'm thinking about ending my life"
   ```
   - ✅ Verify risk level shows as "HIGH"
   - ✅ **CRITICAL**: Verify crisis helplines are displayed
   - ✅ Verify immediate support message
   - ✅ Check that response is compassionate and urgent

### Test 3: Resources

1. **Navigate to Resources**
   - Click "Resources" in navigation

2. **Test Resource Categories**
   - ✅ Click "Mindfulness" - verify content loads
   - ✅ Click "Coping Strategies" - verify content loads
   - ✅ Click "Self-Care" - verify content loads
   - ✅ Click "Breathing Exercises" - verify detailed instructions

3. **Test Search**
   - Search for "anxiety"
   - ✅ Verify relevant results appear

### Test 4: Emergency Resources

1. **Navigate to Emergency Page**
   - Click "Emergency" in navigation (or the emergency button)

2. **Verify Crisis Helplines**
   - ✅ Check India helplines are displayed
   - ✅ Check international helplines are shown
   - ✅ Verify 24/7 availability information
   - ✅ Check emergency actions are listed

### Test 5: Dashboard (if implemented)

1. **Navigate to Dashboard**
   - Click "Dashboard" in navigation

2. **Log a Mood Entry**
   - ✅ Enter mood score (0-1)
   - ✅ Add optional notes
   - ✅ Submit and verify it's saved

3. **View Statistics**
   - ✅ Check if mood history displays
   - ✅ Verify risk statistics (if available)

---

## Step 4: Test Backend API Directly

### Using Browser

Open these URLs in your browser:

1. **API Documentation**
   ```
   http://localhost:8000/docs
   ```
   - ✅ Verify Swagger UI loads
   - ✅ Try the "Try it out" feature on any endpoint

2. **Health Check**
   ```
   http://localhost:8000/api/health
   ```
   - ✅ Should return: `{"status": "healthy", "services": {...}}`

3. **Crisis Helplines**
   ```
   http://localhost:8000/api/crisis-helplines?country=india
   ```
   - ✅ Verify helpline information is returned

### Using cURL (Optional)

```bash
# Health check
curl http://localhost:8000/api/health

# Send a chat message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling anxious",
    "user_id": "test_user_123"
  }'

# Get resources
curl http://localhost:8000/api/resources/mindfulness
```

---

## Step 5: Verify Key Features

### ✅ Safety Features Checklist

- [ ] Disclaimer shows on first visit
- [ ] Consent is required before use
- [ ] High-risk messages trigger crisis response
- [ ] Crisis helplines are prominently displayed
- [ ] Emergency page is easily accessible
- [ ] Responses are empathetic and supportive

### ✅ Functionality Checklist

- [ ] Chat messages send and receive responses
- [ ] Risk assessment works for different message types
- [ ] Resources load correctly
- [ ] Search functionality works
- [ ] Mood logging works (if implemented)
- [ ] Navigation works smoothly

### ✅ Technical Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] API calls succeed (check browser console)
- [ ] No CORS errors
- [ ] Responses are reasonably fast (< 5 seconds)

---

## Troubleshooting Common Issues

### Issue 1: Backend Won't Start

**Error: "ModuleNotFoundError"**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Error: "OpenAI API key not found"**
```bash
# Solution: Check .env file
# Make sure OPENAI_API_KEY is set correctly
```

**Error: "Port 8000 already in use"**
```bash
# Solution: Change port in .env
API_PORT=8001

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue 2: Frontend Won't Start

**Error: "npm command not found"**
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Error: "Port 3000 already in use"**
```bash
# Solution: Use a different port
# When prompted, type 'Y' to use a different port
```

**Error: "Module not found"**
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Issue 3: API Connection Errors

**Error: "Network Error" in browser console**

1. Check backend is running (http://localhost:8000/api/health)
2. Check REACT_APP_API_URL in frontend/.env
3. Check CORS settings in backend/main.py

**Error: "CORS policy blocked"**

Edit `backend/config.py`:
```python
ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
```

### Issue 4: OpenAI API Errors

**Error: "Invalid API key"**
- Verify your API key at https://platform.openai.com/api-keys
- Make sure there are no extra spaces in .env file

**Error: "Rate limit exceeded"**
- You've hit OpenAI's rate limit
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

**Error: "Insufficient quota"**
- Add credits to your OpenAI account
- Visit https://platform.openai.com/account/billing

---

## Step 6: Advanced Testing (Optional)

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py (see docs/TESTING.md)

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

### Unit Testing

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test
```

---

## Expected Behavior Summary

### ✅ What Should Work

1. **Chat Interface**
   - Messages send and receive responses
   - Responses are empathetic and relevant
   - Risk levels are assessed correctly
   - High-risk messages trigger crisis response

2. **Risk Detection**
   - Low-risk: General stress, mild anxiety
   - Medium-risk: Hopelessness, feeling trapped
   - High-risk: Suicidal thoughts, self-harm

3. **Resources**
   - All resource categories load
   - Search returns relevant results
   - Breathing exercises show instructions

4. **Safety Features**
   - Disclaimer appears first time
   - Consent is required
   - Crisis helplines always accessible
   - Emergency page available

### ⚠️ Known Limitations

1. **Response Time**: First message may take 3-5 seconds (AI initialization)
2. **Vector Store**: First run creates the vector database (takes ~10 seconds)
3. **Memory**: Conversation history limited to last 20 messages
4. **Storage**: Uses in-memory storage (data lost on restart)

---

## Next Steps After Testing

### If Everything Works ✅

1. **Explore Features**
   - Try different types of messages
   - Test all resource categories
   - Log multiple mood entries
   - Check dashboard analytics

2. **Review Documentation**
   - Read `docs/API_DOCUMENTATION.md` for API details
   - Check `docs/ARCHITECTURE.md` for system design
   - Review `docs/DEPLOYMENT.md` for production setup

3. **Customize**
   - Modify system prompts in `backend/services/ai_agent.py`
   - Add more resources in `backend/config.py`
   - Customize UI theme in `frontend/src/App.js`

### If Issues Occur ❌

1. **Check Logs**
   - Backend: Look at terminal output
   - Frontend: Check browser console (F12)
   - Backend logs: `backend/logs/app.log`

2. **Verify Setup**
   - Python version: `python --version` (should be 3.9+)
   - Node version: `node --version` (should be 16+)
   - Dependencies installed correctly

3. **Get Help**
   - Review error messages carefully
   - Check troubleshooting section above
   - Review documentation in `docs/` folder

---

## Quick Reference Commands

### Start Everything

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Stop Everything

- Press `Ctrl+C` in both terminals
- Or close the terminal windows

### Reset Everything

```bash
# Backend
cd backend
rm -rf data/vector_store/* logs/*
rm mental_health.db  # if exists

# Frontend
cd frontend
rm -rf node_modules
npm install
```

---

## Success Criteria

You've successfully tested the system if:

✅ Backend starts without errors
✅ Frontend loads in browser
✅ Disclaimer and consent dialogs appear
✅ Chat messages work and get responses
✅ High-risk messages show crisis helplines
✅ Resources load correctly
✅ Emergency page is accessible
✅ No console errors in browser

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages in terminal/console
3. Verify all prerequisites are met
4. Check that .env files are configured correctly
5. Ensure OpenAI API key is valid and has credits

---

## Important Reminders

⚠️ **This is a demonstration system**
- Not for production use without professional review
- Requires medical professional oversight
- Should not replace actual mental health services
- Always prioritize real emergency services in crisis

🔒 **Privacy & Security**
- Don't use real personal information during testing
- OpenAI API calls are logged by OpenAI
- Local data is not encrypted in development mode
- Use test user IDs only

💡 **Best Practices**
- Test with various message types
- Verify safety features work correctly
- Check that crisis responses are appropriate
- Ensure empathetic tone in all responses

---

**Ready to test? Start with Step 1!** 🚀