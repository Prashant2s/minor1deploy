# ⚡ QUICKSTART - Get Running in 3 Steps

## Step 1: Setup Environment (1 minute)

```powershell
# Copy environment file
cp env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
POSTGRES_PASSWORD=mypassword123
```

## Step 2: Start Docker (2 minutes)

```powershell
docker-compose up --build
```

Wait for all services to start. You should see:
- ✅ database system is ready to accept connections
- ✅ backend running on port 5000
- ✅ frontend running on port 5173  
- ✅ university-portal running on port 3000

## Step 3: Test It! (1 minute)

```powershell
# Run test script
.\test-docker.ps1
```

Or manually test:
1. Open **http://localhost:5173** (Frontend)
2. Upload a certificate
3. See AI extraction + University verification ✨

## Quick Links

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | Upload certificates |
| **Backend API** | http://localhost:5000 | API endpoints |
| **University Portal** | http://localhost:3000 | Certificate database |

## What's Happening?

```
YOU → Upload Certificate (5173)
      ↓
AI BACKEND (5000) → Extracts data with OpenAI
      ↓
UNIVERSITY PORTAL (3000) → Verifies against database
      ↓
YOU ← See results with ✅ or ❌ verification status
```

## Sample Test Data

Try uploading a certificate with these details (already in database):

| Name | Enrollment | Branch | CGPA |
|------|------------|--------|------|
| Arjun Kumar Sharma | 19BTCSE001 | CSE | 8.75 |
| Priya Singh | 19BTECE002 | ECE | 9.12 |
| Amit Verma | 18BTCSE005 | CSE | 9.45 |

## Troubleshooting

**Ports already in use?**
```powershell
# Stop existing containers
docker-compose down

# Kill processes on ports
Stop-Process -Name "node","python" -Force
```

**Backend not starting?**
- Check `.env` has valid `OPENAI_API_KEY`
- Run: `docker-compose logs backend`

**Need fresh start?**
```powershell
docker-compose down -v
docker-compose up --build
```

## Next Steps

✅ System is running  
✅ Upload works  
✅ Verification works  

Now see **SIMPLE_SETUP.md** for:
- How verification works
- API endpoints
- Adding certificates to university DB
- Deployment to Netlify

## Stop Everything

```powershell
docker-compose down
```

---

**That's it! 🎉** You now have a working AI certificate verifier with university database verification.
