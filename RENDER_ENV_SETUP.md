# 🔐 Render Environment Variables Setup Guide

Complete guide for configuring environment variables for Render deployment.

---

## 📋 Quick Setup Checklist

When deploying to Render, configure these environment variables:

### Backend Service (`university-verifier-backend`)

| Variable | Value | Required | Notes |
|----------|-------|----------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes | **Manual setup required** |
| `DATABASE_URL` | Auto-generated | ✅ Yes | Render auto-injects from PostgreSQL service |
| `CORS_ORIGIN` | `*` or frontend URL | ✅ Yes | Set to `*` for testing |
| `UPLOAD_DIR` | `/app/uploads` | No | Default is `./uploads` |
| `MAX_FILE_SIZE` | `10485760` | No | Default is 10MB |
| `JWT_SECRET` | Auto-generated | ✅ Yes | Render can auto-generate |

### Frontend Service (`university-verifier-frontend`)

| Variable | Value | Required | Notes |
|----------|-------|----------|-------|
| `VITE_API_URL` | Backend service URL | ✅ Yes | Auto-linked by Render |

### University Portal (`university-verifier-portal`)

| Variable | Value | Required | Notes |
|----------|-------|----------|-------|
| `DATABASE_URL` | Auto-generated | ✅ Yes | Same as backend |
| `SECRET_KEY` | Auto-generated | ✅ Yes | Render can auto-generate |

### PostgreSQL Database (`university-verifier-db`)

| Variable | Value | Required | Notes |
|----------|-------|----------|-------|
| `POSTGRES_DB` | `university_verifier` | ✅ Yes | Set in render.yaml |
| `POSTGRES_USER` | `postgres` | ✅ Yes | Set in render.yaml |
| `POSTGRES_PASSWORD` | Auto-generated | ✅ Yes | Render auto-generates |

---

## 🔑 OpenAI API Key Setup

### Option 1: OpenAI (Recommended)

1. **Get API Key**:
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-proj-...`)

2. **Add to Render**:
   - Find your `university-verifier-backend` service
   - Go to **Environment** tab
   - Click **Add Environment Variable**
   - Key: `OPENAI_API_KEY`
   - Value: Paste your key
   - Click **Save Changes**

3. **Cost Estimate**:
   - Model: `gpt-4o-mini`
   - Cost: ~$0.002 per certificate
   - 1000 certificates ≈ $2

### Option 2: OpenRouter (Cheaper Alternative)

1. **Get API Key**:
   - Go to https://openrouter.ai/keys
   - Create account and get API key
   - Starts with `sk-or-v1-...`

2. **Add to Render**:
   - Backend service → **Environment** tab
   - Add: `OPENAI_API_KEY` = your OpenRouter key
   - Add: `OPENAI_BASE_URL` = `https://openrouter.ai/api/v1`

3. **Benefits**:
   - More models available
   - Often cheaper than OpenAI
   - Same API interface

---

## 🛠️ Step-by-Step Render Configuration

### 1. Deploy Services (Automatic)

After connecting your GitHub repository and clicking "Apply" in Render:

```
✅ PostgreSQL database created
✅ Backend service created
✅ Frontend service created
✅ University portal created
```

### 2. Configure Backend Environment

**Automatic (by render.yaml)**:
- `DATABASE_URL` - Linked from PostgreSQL service
- `CORS_ORIGIN` - Set to `*`
- `UPLOAD_DIR` - Set to `/app/uploads`
- `MAX_FILE_SIZE` - Set to `10485760`

**Manual (you must add)**:
- `OPENAI_API_KEY` - Your OpenAI API key

**Steps**:
1. Go to Render dashboard
2. Click on `university-verifier-backend` service
3. Click **Environment** tab
4. Click **Add Environment Variable**
5. Add `OPENAI_API_KEY` with your key
6. Click **Save Changes**
7. Service will automatically redeploy

### 3. Verify Environment Variables

Check that backend has all required variables:

```bash
# After deployment, check health endpoint
curl https://your-backend.onrender.com/api/v1/health

# Should return:
{
  "status": "healthy",
  "ai_status": "configured",  # ✅ Means OpenAI key works
  "service": "University Certificate Verifier API",
  "version": "1.0.0"
}
```

If `ai_status` is not `"configured"`:
- ❌ OpenAI API key is missing or invalid
- Go back and check environment variables

---

## 🔄 Updating Environment Variables

### During Deployment

If you need to add or change environment variables:

1. Go to service in Render dashboard
2. Click **Environment** tab
3. Add/Edit variables
4. Click **Save Changes**
5. Service automatically redeploys

### After Deployment

Same process - changes trigger automatic redeployment.

---

## 🧪 Testing Environment Configuration

### Local Testing (Before Render)

```bash
# 1. Copy example file
cp .env.example .env

# 2. Edit .env with your values
# Add your OpenAI API key

# 3. Test with Docker
docker-compose up -d

# 4. Check backend health
curl http://localhost:5000/api/v1/health

# Should show "ai_status": "configured"
```

### Production Testing (On Render)

```bash
# 1. Get your backend URL from Render dashboard
# Example: https://university-verifier-backend.onrender.com

# 2. Test health endpoint
curl https://your-backend.onrender.com/api/v1/health

# 3. Expected response:
{
  "status": "healthy",
  "ai_status": "configured",
  "features": [
    "AI-powered certificate extraction",
    "OCR text recognition",
    "Tabular data formatting",
    "University verification",
    "User authentication",
    "File downloads"
  ]
}
```

---

## 🚨 Common Issues

### Issue 1: "ai_status": "missing" or "error"

**Problem**: OpenAI API key not configured

**Solution**:
1. Go to backend service → Environment tab
2. Check if `OPENAI_API_KEY` exists
3. If missing, add it
4. If exists, verify the key is valid at https://platform.openai.com/api-keys

### Issue 2: Database Connection Error

**Problem**: `DATABASE_URL` not set or incorrect

**Solution**:
1. Verify PostgreSQL service is running
2. Check backend environment for `DATABASE_URL`
3. Should be auto-injected by Render from database service
4. Format: `postgresql://user:pass@host:port/dbname`

### Issue 3: Frontend Can't Reach Backend

**Problem**: CORS errors in browser console

**Solution**:
1. Backend service → Environment tab
2. Check `CORS_ORIGIN` value
3. Should be `*` for testing
4. Or set to your frontend URL: `https://your-frontend.onrender.com`

### Issue 4: File Upload Fails

**Problem**: File size limit or upload directory

**Solution**:
1. Check `MAX_FILE_SIZE` (default 10MB)
2. Check `UPLOAD_DIR` is set to `/app/uploads`
3. Verify upload directory exists (auto-created by app)

---

## 🔐 Security Best Practices

### For Production

1. **CORS Origin**:
   ```
   # Development
   CORS_ORIGIN=*
   
   # Production (more secure)
   CORS_ORIGIN=https://your-frontend.onrender.com
   ```

2. **Secret Keys**:
   - Use Render's auto-generate feature
   - Or generate manually: `openssl rand -hex 32`
   - Never commit secrets to git

3. **API Keys**:
   - Rotate OpenAI API key periodically
   - Set spending limits in OpenAI dashboard
   - Monitor usage

4. **Database**:
   - Use Render's Internal Database URL (not External)
   - Enable backups (paid plan)
   - Don't expose credentials

---

## 📊 Environment Variable Reference

### Complete List for Production

```bash
# Backend Service
OPENAI_API_KEY=sk-proj-...         # Manual - Your API key
DATABASE_URL=postgresql://...      # Auto - From Render
CORS_ORIGIN=*                      # Auto - From render.yaml
UPLOAD_DIR=/app/uploads            # Auto - From render.yaml
MAX_FILE_SIZE=10485760            # Auto - From render.yaml
JWT_SECRET=<auto-generated>        # Auto - By Render

# Frontend Service
VITE_API_URL=https://...          # Auto - Linked from backend

# University Portal
DATABASE_URL=postgresql://...      # Auto - From Render
SECRET_KEY=<auto-generated>        # Auto - By Render

# PostgreSQL Database
POSTGRES_DB=university_verifier    # Auto - From render.yaml
POSTGRES_USER=postgres            # Auto - From render.yaml
POSTGRES_PASSWORD=<auto-gen>      # Auto - By Render
```

---

## ✅ Deployment Checklist

**Before Deployment**:
- [x] `.env.example` is up to date
- [x] `.env` file NOT committed to git
- [x] OpenAI API key ready
- [x] Tested locally with Docker

**During Deployment**:
- [ ] Render Blueprint created from `render.yaml`
- [ ] All 4 services created successfully
- [ ] OpenAI API key added to backend service
- [ ] Services show "Live" status

**After Deployment**:
- [ ] Backend health check passes
- [ ] `ai_status` shows `"configured"`
- [ ] Frontend loads correctly
- [ ] Can upload and process certificates
- [ ] University portal accessible

---

## 🎯 Quick Commands

### Generate Secure Secrets

```bash
# Linux/Mac
openssl rand -hex 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Max 256 }))

# Online
https://randomkeygen.com/
```

### Check Environment

```bash
# Local
curl http://localhost:5000/api/v1/health

# Production
curl https://your-backend.onrender.com/api/v1/health
```

### View Render Logs

```bash
# In Render dashboard
Service → Logs tab → Real-time logs
```

---

## 📞 Support

If you encounter issues:

1. Check Render service logs
2. Verify all environment variables are set
3. Test OpenAI API key at https://platform.openai.com/playground
4. Check Render documentation: https://render.com/docs

---

**Status**: ✅ Environment variables documented and ready for deployment

**Last Updated**: 2025-10-26
