# QUICK REFERENCE - All Policies Available

## ✅ WOMEN-SPECIFIC POLICIES (All Included)

### 1. MATERNITY LEAVE
- **Duration**: Pre-natal (4 weeks) + Post-natal (6 months)
- **Pay**: 3 months fully paid + 2 months 50% paid
- **Benefits**: Medical appointments, job protection, benefits continuation
- **Location in Policy**: Section 4.3.1

### 2. PATERNITY LEAVE  
- **Duration**: Up to 3 months
- **Pay**: 2 weeks fully paid + flexible hours for remaining
- **Eligibility**: Fathers, co-parents, same-sex couples
- **Location in Policy**: Section 4.3.2

### 3. ADOPTION LEAVE
- **Duration**: Up to 3 months for primary caregiver
- **Pay**: Fully paid
- **Eligible Age**: Children up to age 5
- **Location in Policy**: Section 4.3.3

### 4. MENSTRUAL LEAVE
- **Duration**: 2 days per month (optional)
- **Pay**: Paid
- **Confidentiality**: No questions asked
- **Location in Policy**: Section 4.4.1

### 5. BREASTFEEDING & LACTATION
- **Duration**: 2 hours daily breaks up to 24 months
- **Facilities**: Private room, refrigerator, seating
- **Pay**: Paid time
- **Location in Policy**: Section 4.5

### 6. CHILDCARE SUPPORT
- **Financial**: 30% cost subsidy (max $300/month)
- **Emergency**: 5 days/year paid leave
- **Facilities**: On-site partnerships, school coordination
- **Location in Policy**: Section 4.7

### 7. ELDER CARE & DEPENDENT SUPPORT
- **Leave**: 10 days/year paid dependent care
- **Financial**: Up to $150/month eldercare subsidy
- **Support**: EAP counseling (24/7)
- **Location in Policy**: Section 4.8

### 8. FERTILITY & FAMILY PLANNING
- **Appointments**: 2 days/month for fertility treatment
- **Miscarriage**: 5 days paid + 15 counseling sessions
- **Adoption**: $5,000 reimbursement
- **Surrogacy**: Same benefits as maternity/paternity
- **Location in Policy**: Section 4.9

### 9. WORKPLACE SAFETY & HARASSMENT
- **Policy**: Zero-tolerance for harassment/discrimination
- **Reporting**: Anonymous hotline + confidential investigation
- **Transport**: Company shuttle/ride-share for night shift
- **Protection**: Non-retaliation guarantee
- **Location in Policy**: Section 4.11

### 10. HEALTH & WELLNESS
- **Coverage**: Gynecological screening (free)
- **Programs**: Menopause support, mental health
- **Checkups**: Annual women's health screening
- **Preventive**: Breast/cervical cancer screening
- **Location in Policy**: Section 4.12

### 11. GENDER PAY EQUITY
- **Salary**: No reduction during maternity leave
- **Increases**: Guaranteed upon return
- **Audits**: Annual pay equity verification
- **Transparency**: Published salary ranges
- **Location in Policy**: Section 4.13

### 12. SPECIAL PROTECTIONS
- **Pregnancy**: Ergonomic accommodations, no heavy lifting
- **Domestic Violence**: 5 days/month paid leave
- **Medical**: Unlimited leave for serious complications
- **Bereavement**: Leave for pregnancy loss
- **Location in Policy**: Section 4.14

---

## 🤖 HOW RAG RETRIEVES POLICIES

When user asks: **"What is maternity leave?"**

1. **Question Processing**: RAG breaks it down to keywords
   - Key terms: [maternity, leave, duration, benefits]

2. **Policy Search**: Searches `policy.txt` for matching sections
   - Finds Section 4.3.1 (Maternity Leave)
   - Retrieves duration, pay, benefits details

3. **Context Building**: Extracts relevant chunks:
   - 3-5 paragraphs about maternity leave
   - Medical certifications required
   - Application process

4. **LLM Generation**: Sends to Gemini 2.5 Pro:
   - Context: Maternity leave policy details
   - Question: "What is maternity leave?"
   - Output: Coherent answer with all details

5. **Response**: Delivers to user:
   - Text answer in chat
   - Voice option (pyttsx3 TTS)
   - Downloads available

---

## 📞 TEST THESE QUESTIONS

Copy and paste in the AI Assistant to test RAG + Voice:

1. "What is the maternity leave policy and how long does it last?"
2. "Are there any provisions for employees experiencing menstrual difficulties?"
3. "How much childcare support will the company provide?"
4. "What happens if I experience workplace harassment?"
5. "Is there equal pay protection for women?"
6. "What support is available for fertility treatment?"
7. "Can I take leave for pregnancy complications?"
8. "What are the breastfeeding support provisions?"
9. "Is there adoption leave available?"
10. "How does the company support elder care needs?"

**Expected Results**:
- ✅ Text answer appears in chat (from RAG)
- ✅ Answer references specific policy sections
- ✅ Can generate voice note in English
- ✅ Audio file plays or downloads

---

## 📊 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    WEB BROWSER                          │
│              (http://localhost:5000)                     │
├─────────────────────────────────────────────────────────┤
│                  FRONTEND (HTML/CSS/JS)                 │
│  • User asks question  • Displays answers               │
│  • Selects language    • Shows voice player             │
├─────────────────────────────────────────────────────────┤
│              FLASK API (BACKEND - Port 5000)            │
│  • /api/explain       (RAG Q&A endpoint)                │
│  • /api/voice         (Voice generation)                │
│  • /voice/<file>      (Audio streaming)                │
├─────────────────────────────────────────────────────────┤
│                    RAG ENGINE                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Policy Document (policy.txt - 3000+ lines)     │   │
│  │  • All 14 sections loaded into memory           │   │
│  │  • Keyword-based chunking & retrieval           │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                 LLM (AI GENERATION)                     │
│  Gemini 2.5 Pro via GenAI Lab API                       │
│  • Receives policy context + question                  │
│  • Generates policy-aware answers                       │
├─────────────────────────────────────────────────────────┤
│              VOICE SYNTHESIZER (TTS)                    │
│  pyttsx3 - Offline Text-to-Speech                       │
│  • Converts answer text to audio                       │
│  • Saves as WAV files                                  │
│  • Streams to browser for playback                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 DEPLOYMENT STATUS

| Component | Status | Details |
|-----------|--------|---------|
| Backend API | ✅ Running | Port 5000 |
| Frontend UI | ✅ Running | Port 5000 |
| Policy DB | ✅ Loaded | 3000+ lines, 14 sections |
| RAG Engine | ✅ Active | Keyword-based retrieval |
| LLM (Gemini 2.5) | ✅ Connected | GenAI Lab API |
| Voice Synthesis | ✅ Working | pyttsx3 TTS engine |
| PDF Extracts | ✅ Available | 3 reference documents |

---

**All systems operational and ready for use!**

Generated: March 13, 2026
