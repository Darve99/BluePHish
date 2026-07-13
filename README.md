# 🎣 BluePHish

**Email Phishing Detection & Analysis Platform** | Rule-Based Scoring + Optional AI Analysis

BluePHish is a comprehensive web application for detecting and analyzing phishing emails. It combines a powerful rule-based scoring engine with optional AI-assisted analysis to provide security professionals and end-users with actionable threat intelligence.

> **Safety Note:** This project is strictly defensive and educational. It does not generate offensive content or provide phishing campaign tooling.

---

## ✨ Features

### 🔐 Authentication & Security
- User registration and login with JWT tokens
- Access tokens (30-minute expiration)
- Refresh tokens (7-day expiration)
- Password hashing with Argon2
- Role-based access control

### 📊 Email Analysis
- **RFC 2822 Email Parsing** - Full header and body extraction
- **Rule-Based Scoring** - 14+ phishing detection rules with weighted scoring (0-100)
- **SPF/DKIM/DMARC Validation** - Authentication framework verification
- **URL Analysis** - Protocol detection, shortened URL identification, IP-based threats
- **Header Chain Analysis** - Received-chain verification
- **AI-Powered Explanations** - Optional GPT-4o-mini integration for insights
- **Risk Classification** - Low / Medium / High categorization

### 📈 Dashboard & Metrics
- Real-time KPIs (total analyzed, average risk, high-risk count)
- Risk distribution visualization (high/medium/low breakdown)
- 7-day activity trend chart
- Analysis history with timestamps
- Responsive design (desktop/mobile)

### 📋 Admin Panel
- System statistics
- Rule management & customization
- User listing
- Analysis tracking

### 📄 Reporting
- PDF report generation with full analysis details
- Risk score breakdown
- Indicator explanations
- Downloadable artifacts

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI 0.100+, Uvicorn, SQLAlchemy ORM |
| **Frontend** | React 18+, TypeScript, Vite, Tailwind CSS |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Authentication** | JWT (python-jose), Argon2 hashing |
| **Optional AI** | OpenAI GPT-4o-mini |
| **Reporting** | ReportLab (PDF generation) |
| **Deployment** | Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ LTS
- Git

### Backend Setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start API server
uvicorn main:app --host 127.0.0.1 --port 8000
```

API will be available at **http://127.0.0.1:8000**

### Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Frontend will be available at **http://localhost:3000**

### Database Initialization

SQLite database (`bluephish.db`) is created automatically on first backend startup.

**For PostgreSQL (production):**
```powershell
$env:DATABASE_URL="postgresql://user:password@localhost/bluephish"
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user |

### Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analysis` | Analyze raw email text |
| POST | `/analysis/upload` | Upload & analyze .eml file |
| GET | `/history` | Get user's analysis history |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/stats` | System statistics |
| GET | `/admin/rules` | List all rules |
| POST | `/report` | Generate PDF report |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

---

## 🧪 Testing

### Backend Tests

```powershell
cd backend
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html
```

### Frontend Tests

```powershell
cd frontend

# Unit tests
npm test

# Type checking
npx tsc --noEmit

# Linting
npm run lint

# Build verification
npm run build
```

### GitHub Actions CI/CD

Automated workflows run on every push:
- **Backend:** Python linting (flake8), type checking (mypy), pytest coverage
- **Frontend:** Node.js linting (ESLint), TypeScript checks, build verification

---

## 🔍 Phishing Detection Rules

BluePHish uses a weighted rule engine to detect phishing indicators:

| Rule | Weight | Detection |
|------|--------|-----------|
| Credential Request | **35** | Requests for password, username, token, PIN |
| Typosquatting Domain | **30** | Confusing characters (0l, l0, rn, 1l, 5s) |
| Urgent Language | **20** | "24 horas", "suspendida", "bloqueada", "inmediatamente" |
| Verify Identity | **25** | "verificar", "reactivar", "confirmar identidad" |
| Suspicious Sender | **25** | Spoofed official domains (paypal, microsoft, amazon, etc.) |
| Shortened URLs | **20** | bit.ly, tinyurl, t.co detection |
| Insecure URL | **15** | HTTP instead of HTTPS |
| Suspicious Attachment | **20** | .exe, .zip references |
| Multiple URLs | **10** | >3 links in email |
| Missing Sender | **8** | No From header |
| SPF Failure | **20** | Failed SPF authentication |
| DKIM Failure | **20** | Failed DKIM authentication |
| DMARC Failure | **20** | Failed DMARC authentication |

**Risk Score Calculation:**
- **0-29:** Low Risk 🟢
- **30-69:** Medium Risk 🟡
- **70-100:** High Risk 🔴

---

## 🤖 AI Integration (Optional)

BluePHish includes **optional GPT-4o-mini integration** for advanced analysis:

```powershell
# Enable AI analysis
$env:OPENAI_API_KEY="sk-your-api-key-here"
uvicorn main:app --host 127.0.0.1 --port 8000
```

When enabled, AI provides:
- Natural language classification
- Detailed threat explanations
- Personalized recommendations
- Executive summaries

**Without an API key:** System falls back to rule-based analysis (still highly accurate).

---

## 📁 Project Structure

```
BluePHish/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── auth.py                 # Authentication & JWT
│   │   ├── analysis.py             # Rule engine & scoring
│   │   ├── parser.py               # RFC 2822 email parser
│   │   ├── header_analyzer.py      # Header analysis
│   │   ├── url_analyzer.py         # URL threat detection
│   │   ├── ai_service.py           # GPT-4o-mini integration
│   │   ├── history.py              # Analysis history
│   │   ├── reporting.py            # PDF generation
│   │   ├── admin.py                # Admin features
│   │   ├── db_persistence.py       # Database ORM
│   │   └── database.py             # SQLAlchemy setup
│   ├── tests/                      # 16+ test files
│   ├── requirements.txt
│   ├── pytest.ini
│   └── .venv/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AuthForm.tsx
│   │   │   ├── EmailAnalysisForm.tsx
│   │   │   ├── DashboardMetrics.tsx
│   │   │   ├── HistoryList.tsx
│   │   │   ├── ReportButton.tsx
│   │   │   └── AdminPanel.tsx
│   │   ├── lib/
│   │   │   └── api.ts             # HTTP client
│   │   ├── App.tsx                # Main component
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── .github/workflows/             # CI/CD pipelines
├── docker-compose.yml
└── README.md
```

---

## 🚢 Deployment

### Docker Compose (Production)

```powershell
docker-compose up --build
```

Services:
- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **Database:** PostgreSQL (postgres:15)

### Environment Variables

```powershell
# Backend
$env:DATABASE_URL="postgresql://user:password@localhost/bluephish"
$env:OPENAI_API_KEY="sk-your-api-key"  # Optional
$env:JWT_SECRET_KEY="your-secret-key"

# Frontend
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
```

---

## 📊 Statistics

| Component | Count | Status |
|-----------|-------|--------|
| Backend Modules | 10+ | ✅ Complete |
| Frontend Components | 8 | ✅ Complete |
| Detection Rules | 14 | ✅ Active |
| API Endpoints | 11 | ✅ Functional |
| Test Files | 16+ | ✅ Passing |
| Database Tables | 3 | ✅ SQLAlchemy ORM |

---

## 🔮 Roadmap

### v1.0 ✅ (Current)
- Email phishing detection
- Rule-based + AI analysis
- User authentication
- Dashboard & reporting
- Admin panel

### v2.0 (Planned)
- **SMS/WhatsApp Smishing** - Text message phishing detection
- **Social Media** - LinkedIn, Discord, Telegram analysis
- **QR Code Analysis** - URL destination verification
- **ML-Based Scoring** - Ensemble machine learning models
- **Enterprise Features** - SMTP gateway, webhooks, SSO, audit logging

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact & Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check existing documentation in this README
- Review test files for usage examples

---

**Made with ❤️ for cybersecurity education**
