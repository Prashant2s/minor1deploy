# Deployment Guide for AI Certificate Verifier

## 🚀 Quick Deployment Steps

### 1. Backend Deployment (Choose one platform)

#### Option A: Railway (Recommended)

1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` folder
4. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `POSTGRES_PASSWORD`: Strong password
   - `CORS_ORIGIN`: Your Netlify frontend URL
5. Deploy automatically

#### Option B: Render

1. Go to [Render](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `cd backend && pip install -r requirements.txt`
5. Set start command: `cd backend && gunicorn app.main:app`
6. Add PostgreSQL database
7. Set environment variables

#### Option C: Heroku

1. Install Heroku CLI
2. Create Heroku App: `heroku create your-app-name`
3. Add PostgreSQL: `heroku addons:create heroku-postgresql:mini`
4. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set POSTGRES_PASSWORD=your_secure_password
   heroku config:set CORS_ORIGIN=https://your-frontend-domain.netlify.app
   ```
5. Deploy: `git push heroku main`

### 2. Frontend Deployment (Netlify)

1. **Connect to Netlify**:

   - Go to [Netlify](https://netlify.com)
   - Connect your GitHub repository
   - Select the repository

2. **Update Configuration**:

   - Edit `netlify.toml` and replace `your-backend-url.railway.app` with your actual backend URL
   - Set environment variable `VITE_API_URL` in Netlify dashboard to your backend URL

3. **Deploy**:
   - Netlify will automatically build and deploy from the `frontend/dist` folder

### 3. Environment Variables

#### Backend Environment Variables:

```bash
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_PASSWORD=your_secure_password
CORS_ORIGIN=https://your-frontend-domain.netlify.app
MAX_FILE_SIZE=10485760
LOG_LEVEL=INFO
JWT_SECRET=your_secure_jwt_secret
```

#### Frontend Environment Variables (Netlify):

```bash
VITE_API_URL=https://your-backend-url.railway.app/api/v1
```

### 4. Testing Your Deployment

1. **Test Backend**:

   - Visit: `https://your-backend-url.railway.app/health`
   - Should return: `{"status": "healthy", "service": "University Certificate Verifier API"}`

2. **Test Frontend**:
   - Visit your Netlify URL
   - Try uploading a certificate
   - Check if API calls work

### 5. Common Issues & Solutions

#### CORS Errors:

- Ensure `CORS_ORIGIN` is set to your exact Netlify URL
- Check that the frontend URL matches exactly (including protocol)

#### API Key Issues:

- Verify OpenAI API key is correctly set
- Check API key has sufficient credits

#### Database Connection:

- Ensure PostgreSQL is running and accessible
- Verify connection string format

#### File Upload Issues:

- Check `MAX_FILE_SIZE` is appropriate
- Verify file format is supported
- Ensure upload directory has write permissions

### 6. Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed on Netlify
- [ ] Environment variables set correctly
- [ ] CORS configured properly
- [ ] OpenAI API key configured
- [ ] Database connection working
- [ ] File uploads working
- [ ] Health check endpoint responding
- [ ] SSL certificates working
- [ ] Error handling in place

### 7. Monitoring & Maintenance

- Monitor OpenAI API usage and costs
- Check application logs regularly
- Monitor database performance
- Set up alerts for errors
- Regular security updates

## 🔧 Local Development

For local development, create a `.env` file in the root directory:

```bash
# Copy from env.example
cp env.example .env

# Edit .env with your values
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_PASSWORD=your_secure_password
CORS_ORIGIN=http://localhost:5173
```

Then run:

```bash
# Backend
cd backend
python run_local.py

# Frontend
cd frontend
npm run dev
```

## 📞 Support

If you encounter issues:

1. Check the logs in your deployment platform
2. Verify all environment variables are set
3. Test the health check endpoint
4. Check CORS configuration
5. Verify OpenAI API key is valid
