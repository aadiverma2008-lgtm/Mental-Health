# 🚀 Setup Instructions - Do This Now!

## ⚠️ IMPORTANT: You Need to Complete These Steps

The installation is running in the background. Here's what you need to do:

---

## Step 1: Get Your OpenAI API Key (5 minutes)

### If you DON'T have an OpenAI API key:

1. Go to: **https://platform.openai.com/signup**
2. Create an account (or sign in if you have one)
3. Go to: **https://platform.openai.com/api-keys**
4. Click **"Create new secret key"**
5. Give it a name like "Mental Health AI"
6. **COPY THE KEY** (it starts with `sk-...`)
7. **IMPORTANT**: Save it somewhere safe - you can't see it again!

### If you already have an OpenAI API key:
- Just have it ready to paste

---

## Step 2: Add Your API Key to the Backend

I've created a file `backend/.env` for you. You need to edit it:

1. **Open the file**: `backend/.env`
2. **Find this line**:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
3. **Replace** `your_openai_api_key_here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
4. **Find this line**:
   ```
   SECRET_KEY=your_secret_key_here_replace_with_random_string
   ```
5. **Replace** with any random string (or use this one):
   ```
   SECRET_KEY=mental-health-ai-secret-key-2024-change-in-production
   ```
6. **Save the file**

---

## Step 3: Wait for Installation to Complete

The terminal is currently installing Python packages. This takes 2-3 minutes.

**You'll know it's done when you see**:
```
Successfully installed fastapi-... uvicorn-... openai-...
```

---

## Step 4: What Happens Next

Once the installation completes, I will:

1. ✅ Start the backend server
2. ✅ Install frontend dependencies
3. ✅ Start the frontend
4. ✅ Open your browser to test the application

---

## 📋 Quick Checklist

Before we continue, make sure:

- [ ] You have an OpenAI API key
- [ ] You've edited `backend/.env` with your API key
- [ ] You've set a SECRET_KEY in `backend/.env`
- [ ] You've saved the file
- [ ] The installation in the terminal has completed

---

## 💰 OpenAI API Costs

**Important**: This application uses OpenAI's API which costs money.

- **Estimated cost per conversation**: $0.01 - $0.05
- **You need credits in your OpenAI account**
- **Check your balance**: https://platform.openai.com/account/billing

### Free Tier
- New accounts get $5 free credits
- Good for ~100-500 test conversations

---

## 🆘 Need Help?

### "I don't have an OpenAI account"
- Sign up at: https://platform.openai.com/signup
- It's free to create an account
- You'll need to add payment info for API access

### "I can't find my API key"
- Go to: https://platform.openai.com/api-keys
- Create a new one if needed

### "The installation is taking too long"
- It's normal - can take 3-5 minutes
- Don't close the terminal
- Wait for "Successfully installed..." message

### "I see errors in the terminal"
- That's okay during installation
- Wait for it to complete
- I'll help troubleshoot if needed

---

## ✅ Ready to Continue?

Once you've:
1. ✅ Added your OpenAI API key to `backend/.env`
2. ✅ Set the SECRET_KEY in `backend/.env`
3. ✅ Saved the file
4. ✅ Seen the installation complete

**Let me know and I'll start the servers!**

---

## 📝 What You're Testing

This Mental Health AI Agent includes:

1. **Empathetic AI Chat** - Talk about mental health concerns
2. **Risk Detection** - Automatically detects distress signals
3. **Crisis Response** - Shows helplines for high-risk messages
4. **Mental Health Resources** - Breathing exercises, coping strategies
5. **Mood Tracking** - Log and track your mood over time
6. **Privacy First** - Consent-based, secure, GDPR compliant

---

## 🎯 First Test Scenario

When the app starts, you'll:

1. See a **medical disclaimer** - read and accept it
2. See a **consent dialog** - choose your preferences
3. Go to the **chat page**
4. Send a test message: "I'm feeling stressed about work"
5. Get an empathetic AI response
6. See risk assessment and recommendations

Then try a high-risk message to see crisis response!

---

**Ready? Edit the `.env` file now and let me know when done!** 🚀