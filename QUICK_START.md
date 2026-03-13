# Quick Start Guide - Flexible Work & Life Balance Policy System

## ⚡ 5-Minute Setup

### Step 1: Activate Virtual Environment
```powershell
. venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies (if not already done)
```powershell
pip install -r requirements.txt
```

### Step 3: Navigate to Backend
```powershell
cd backend
```

### Step 4: Start the Application
```powershell
python app.py
```

### Step 5: Access in Browser
Open your browser and go to:
```
http://localhost:5000
```

---

## 🎯 Expected Output

When you run `python app.py`, you should see:

```
============================================================
Flexible Work & Life Balance Policy System
============================================================
Starting Flask application...
Open http://localhost:5000 in your browser
============================================================
✓ Policy document loaded successfully
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## 🌐 Web Interface Walkthrough

### 1. **Home Page** (Default)
- Welcome message and overview
- 4 quick access cards (Policy, AI Assistant, Status, Workflow)
- Feature highlights

### 2. **View Policy** Tab
- Complete policy document
- Quick access links to key sections
- Get Summary button
- Quick questions

### 3. **AI Assistant** Tab
- Ask any policy question
- Get instant RAG-powered answers
- Generate voice notes in 14+ languages
- Download audio files

### 4. **Status** Tab
- View complete approval workflow (6 steps)
- Understand approval criteria
- Contact HR information

---

## 🎤 Testing Voice Generation

### Example Workflow:

1. Go to **AI Assistant** tab
2. Ask: "What are the types of flexible work arrangements?"
3. Click **Ask** button
4. Wait for AI response
5. Select language (e.g., "English" or "Hindi")
6. Click **Generate Voice Note**
7. Listen to the audio playback

---

## 📝 Sample Questions to Try

```
1. "What types of flexible work arrangements are available?"
2. "How long does the approval process take?"
3. "What are the approval criteria?"
4. "What is remote work policy?"
5. "How is performance monitored?"
6. "What are the benefits of flexible work?"
7. "What is caregiving support?"
8. "How do employees request flexible work?"
9. "What happens if my request is denied?"
10. "What are the eligibility criteria?"
```

---

## 🎯 Key Features to Explore

### RAG (Retrieval-Augmented Generation)
- Ask natural language questions
- AI retrieves relevant policy sections
- Provides accurate, context-aware answers
- Explains complex policy content

### Multi-Language Voice
- Select from 14+ languages
- Generate professional voice notes
- Download audio for offline listening
- Share with team members

### Professional Policy Document
- 23-section comprehensive policy
- Covers all types of arrangements
- Includes approval process
- Explains appeal procedures

---

## 🔧 Troubleshooting Quick Tips

### Issue: "Policy document not loaded"
**Fix**: Ensure `documents/policy.txt` exists and restart

### Issue: Voice generation fails
**Fix**: Check internet connection, ensure gTTS is installed:
```powershell
pip install --upgrade gTTS
```

### Issue: "Address already in use"
**Fix**: Kill the process using port 5000:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Can't connect to backend
**Fix**: Make sure Flask app is running and port 5000 is not blocked

---

## 📋 File Structure

```
backend/
├── app.py                    # Main Flask application
├── rag_engine.py           # RAG system
└── voice_synthesizer.py    # Voice generation

frontend/
├── index.html              # Web interface
└── static/
    ├── styles.css         # Styling
    └── script.js          # JavaScript

documents/
├── policy.txt             # Policy text
└── policy.html            # Policy in HTML

voice_outputs/             # Generated MP3 files
```

---

## ✅ Verification Checklist

After starting the app, verify:

- [ ] Flask server is running (port 5000)
- [ ] Web interface loads at http://localhost:5000
- [ ] Home page displays correctly
- [ ] Policy document is accessible
- [ ] AI Assistant can answer questions
- [ ] Voice generation works
- [ ] Download functionality works
- [ ] Workflow steps are displayed

---

## 🚀 Running in Background

To run the server in the background (PowerShell):

```powershell
$job = Start-Job -ScriptBlock { cd backend; python app.py }
```

To stop it:
```powershell
Stop-Job -Id $job.Id
```

---

## 🌐 Testing via Browser DevTools

1. Open Browser DevTools (F12)
2. Go to **Network** tab
3. Ask a question in AI Assistant
4. Observe API calls to `/api/explain`
5. Check response in **Response** tab

---

## 📞 Common API Endpoints

```
GET  http://localhost:5000/              # Web interface
GET  http://localhost:5000/policy        # Policy document
GET  http://localhost:5000/api/policy-status
POST http://localhost:5000/api/explain   # Ask questions
POST http://localhost:5000/api/voice     # Voice generation
GET  http://localhost:5000/api/summary   # Policy summary
GET  http://localhost:5000/api/languages # Supported languages
GET  http://localhost:5000/api/request-flow  # Workflow steps
```

---

## 💡 Pro Tips

1. **Multiple Browsers**: Test in different browsers (Chrome, Firefox, Edge)
2. **Different Languages**: Generate voice in multiple languages to test
3. **Long Explanations**: Ask complex questions to see RAG in action
4. **Download Audio**: Download voice files and share with team
5. **Policy Reference**: Keep HTML policy open in another tab for reference

---

## 🐛 Debug Mode

The app runs in debug mode by default. To see detailed logs:
1. Check Flask terminal output
2. Open browser DevTools (F12)
3. Check **Console** tab for JavaScript errors
4. Check **Network** tab for API responses

---

## 📊 Expected Performance

- **Question Response**: 2-5 seconds
- **Voice Generation**: 1-3 seconds
- **Page Load**: <1 second
- **Concurrent Users**: 10+

If slower, check:
- Internet connection
- System resources (CPU, RAM)
- API availability (genailab.tcs.in)

---

## For More Information

See the full **README.md** file for:
- Detailed architecture explanation
- API documentation
- Advanced configuration
- Production deployment
- Security considerations

---

**You're all set! Happy exploring! 🎉**
