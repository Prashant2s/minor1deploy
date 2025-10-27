# Setting Up PostgreSQL Database on Render

## 🗄️ PostgreSQL Database Setup Guide

Your application currently uses SQLite, which is ephemeral on Render (data is lost on redeploy). For production, use PostgreSQL for persistent storage.

## 📋 Option 1: Add PostgreSQL to render.yaml (Recommended)

### Step 1: Update render.yaml

Add a PostgreSQL database service to your `render.yaml`:

```yaml
services:
  # PostgreSQL Database
  - type: pserv
    name: university-verifier-db
    env: docker
    plan: free
    region: oregon
    ipAllowList: []  # Allow connections from Render services only

  # Backend API Service
  - type: web
    name: university-verifier-backend
    env: docker
    plan: free
    region: oregon
    dockerfilePath: ./backend/Dockerfile
    dockerContext: ./backend
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: university-verifier-db
          property: connectionString
      - key: DB_URL
        fromDatabase:
          name: university-verifier-db
          property: connectionString
      - key: OPENAI_API_KEY
        sync: false
      - key: UNIVERSITY_PORTAL_URL
        sync: false
      - key: CORS_ORIGIN
        value: "*"
      - key: UPLOAD_DIR
        value: "/app/uploads"
      - key: MAX_FILE_SIZE
        value: "10485760"
      - key: PORT
        value: "10000"
      - key: HOST
        value: "0.0.0.0"
    healthCheckPath: /api/v1/health
```

### Step 2: Push to GitHub

```bash
git add render.yaml
git commit -m "Add PostgreSQL database to Render config"
git push origin main
```

### Step 3: Redeploy on Render

- Go to Render Dashboard
- Your Blueprint will detect the change
- Click "Sync" or "Redeploy"
- Render will automatically create the PostgreSQL database

---

## 📋 Option 2: Manual Database Creation (Current Setup)

If you want to keep the current SQLite setup or manually create a database:

### Step 1: Create PostgreSQL Database on Render

1. **Log in to Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create New PostgreSQL Database**
   - Click **"New +"** button
   - Select **"PostgreSQL"**

3. **Configure Database**
   - **Name**: `university-verifier-db`
   - **Database**: `university_verifier` (will be auto-created)
   - **User**: `university_verifier_user` (or leave default)
   - **Region**: `Oregon (US West)` (match your services)
   - **Plan**: **Free**
   - Click **"Create Database"**

4. **Wait for Database Provisioning**
   - Takes 1-2 minutes
   - Status will change to "Available"

### Step 2: Get Database Connection String

1. **In the database dashboard**, you'll see:
   - **Internal Database URL** (use this for Render services)
   - **External Database URL** (for local connections)

2. **Copy the Internal Database URL**
   - Format: `postgresql://user:password@host:5432/database`
   - Example: `postgresql://university_verifier_user:abc123@dpg-xxxxx-a.oregon-postgres.render.com/university_verifier_db`

### Step 3: Update Backend Service Environment Variables

1. **Go to your Backend Service**
   - Navigate to `university-verifier-backend` in Render dashboard

2. **Add/Update Environment Variables**
   - Go to **"Environment"** tab
   - Click **"Add Environment Variable"**
   
   Add these:
   ```
   Key: DATABASE_URL
   Value: [paste the Internal Database URL]
   
   Key: DB_URL
   Value: [paste the Internal Database URL]
   ```

3. **Click "Save Changes"**
   - Service will automatically redeploy

### Step 4: Initialize Database Schema

The backend automatically creates tables on startup, but you can verify:

1. **Check Backend Logs**
   - Go to backend service → **"Logs"** tab
   - Look for messages like: "Database tables created successfully"

2. **Manual Schema Creation (if needed)**
   - Connect to database using External URL:
   ```bash
   psql "postgresql://user:password@host:5432/database"
   ```
   
   - Or use Render's built-in Shell:
     - Go to database → **"Shell"** tab
     - Run migrations manually if needed

### Step 5: Verify Database Connection

1. **Test Backend Health Endpoint**
   ```bash
   curl https://your-backend-url.onrender.com/api/v1/health
   ```

2. **Check for Database Errors in Logs**
   - If connection fails, verify DATABASE_URL is correct
   - Ensure database is in "Available" state

---

## 🔄 Migration from SQLite to PostgreSQL

If you have existing data in SQLite that you want to migrate:

### Option A: Export/Import Data

1. **Export from SQLite** (locally)
   ```bash
   python backend/export_data.py
   ```

2. **Import to PostgreSQL** (via API)
   - Use the admin portal or API to re-add certificates

### Option B: Use pgloader (Advanced)

```bash
# Install pgloader
# Convert SQLite to PostgreSQL
pgloader sqlite://university.db postgresql://user:pass@host:5432/db
```

---

## 🔐 Database Security Best Practices

1. **IP Allowlist** (Optional)
   - In database settings, restrict connections
   - Only allow Render internal network

2. **Connection Pooling**
   - Backend already uses SQLAlchemy connection pooling
   - No additional configuration needed

3. **Backups**
   - Free tier: 7 days of automated backups
   - Paid tier: 30 days + point-in-time recovery

4. **Monitoring**
   - Check database metrics in Render dashboard
   - Monitor connection count and query performance

---

## 🐛 Troubleshooting

### Database Connection Refused
- ✅ Verify DATABASE_URL is correct
- ✅ Check database status is "Available"
- ✅ Ensure backend is in same region

### Tables Not Created
- ✅ Check backend logs for SQLAlchemy errors
- ✅ Verify database user has CREATE TABLE permissions
- ✅ Manually run migrations if needed

### Performance Issues
- ✅ Free tier has connection limits (5 concurrent)
- ✅ Consider upgrading for more connections
- ✅ Optimize queries and add indexes

---

## 📊 Database Limits (Free Tier)

- **Storage**: 1 GB
- **Connections**: 5 concurrent
- **Backups**: 7 days retention
- **Databases**: 1 per instance

For production, consider upgrading to paid tier for:
- More storage (10GB+)
- More connections (100+)
- Better performance
- Longer backup retention

---

## ✅ Verification Checklist

After setup:
- [ ] Database shows "Available" status in Render
- [ ] Backend has DATABASE_URL environment variable set
- [ ] Backend service deployed successfully
- [ ] Health check endpoint returns 200 OK
- [ ] Can create/read certificates via API
- [ ] No database connection errors in logs

---

**Your database is now ready for production use!** 🎉

For questions or issues, check:
1. Render database logs
2. Backend service logs
3. Database connection metrics
