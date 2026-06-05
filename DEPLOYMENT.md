# 🚀 Deployment Guide — GAG Coffee Co.

Step-by-step instructions for deploying to various platforms.

---

## Option 1: Vercel (Recommended)

**Cost:** Free tier included (100 GB/month bandwidth)  
**Setup time:** 15 minutes  
**Best for:** Quick global deployment with automatic scaling

### Backend on Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Push Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "GAG Coffee - Full Stack"
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```

3. **Deploy to Vercel**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Select your GitHub repo
   - **Framework:** None (Python)
   - **Root Directory:** Leave empty
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Output Directory:** `/backend`
   - **Start Command:** `gunicorn gagcoffee.wsgi`

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add these:
   ```
   DJANGO_SETTINGS_MODULE = gagcoffee.settings
   DEBUG = False
   SECRET_KEY = <run: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
   ALLOWED_HOSTS = <your-vercel-url>.vercel.app
   MONGODB_URI = <your-mongodb-atlas-uri>
   MONGODB_DB = gagcoffee
   CORS_ALLOWED_ORIGINS = https://<your-frontend-url>.com
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Note your backend URL: `https://<project>.vercel.app`

### Frontend on Vercel

1. **Option A: Deploy as separate Vercel project**
   - New Project → select repo
   - **Root Directory:** `frontend`
   - Deploy

2. **Option B: Host on GitHub Pages (free, static)**
   - Repo Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`, folder: `/frontend`

3. **Update API URL**
   - Edit `frontend/index.html` line ~285:
   ```javascript
   var API_BASE = 'https://<your-backend-url>.vercel.app/api';
   ```
   - Commit and push

---

## Option 2: Railway.app (Django-friendly)

**Cost:** Free tier included, then $5-50/month  
**Setup time:** 10 minutes  
**Best for:** Python apps, built-in PostgreSQL/MongoDB support

### Steps

1. **Sign up at [railway.app](https://railway.app)**

2. **Create new project**
   - "Deploy from GitHub repo"
   - Select your repo
   - Auto-detect Python

3. **Add MongoDB service**
   - Click "New"
   - Add "MongoDB"
   - Railway generates `MONGODB_URL`

4. **Environment Variables**
   ```
   DJANGO_SETTINGS_MODULE=gagcoffee.settings
   SECRET_KEY=<random-secret>
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   MONGODB_URI=${{Mongo.MONGODB_URL}}
   MONGODB_DB=gagcoffee
   CORS_ALLOWED_ORIGINS=https://<your-frontend>.com
   ```

5. **Deploy Command**
   - Settings → Deploy → Start Command:
   ```
   cd backend && gunicorn gagcoffee.wsgi
   ```

6. **Link Domain**
   - Settings → Domains
   - Add custom domain or use Railway subdomain

---

## Option 3: Render.com (Simple & Free)

**Cost:** Free tier, then $7/month  
**Setup time:** 12 minutes  
**Best for:** Simple deployments, easy UI

### Steps

1. **Sign up at [render.com](https://render.com)**

2. **Create Web Service**
   - Select GitHub repo
   - **Environment:** Python 3.11
   - **Build Command:**
   ```bash
   pip install -r backend/requirements.txt
   ```
   - **Start Command:**
   ```bash
   cd backend && gunicorn gagcoffee.wsgi
   ```

3. **Add MongoDB (external)**
   - Use MongoDB Atlas (free tier)
   - Add to Environment Variables

4. **Environment Variables**
   ```
   DJANGO_SETTINGS_MODULE=gagcoffee.settings
   SECRET_KEY=<random-secret>
   ALLOWED_HOSTS=<your-render-url>.onrender.com
   MONGODB_URI=<mongodb-atlas-uri>
   MONGODB_DB=gagcoffee
   ```

5. **Custom Domain**
   - Settings → Custom Domain
   - Update DNS at registrar

---

## Option 4: Heroku (Classic)

**Cost:** Free tier discontinued (was free)  
**Cost now:** $7/month minimum  
**Setup time:** 15 minutes  
**Note:** Free tier is no longer available

### Steps (if using paid tier)

1. **Install Heroku CLI**
   ```bash
   brew install heroku  # or download from heroku.com
   ```

2. **Login & Create App**
   ```bash
   heroku login
   heroku create <your-app-name>
   ```

3. **Add MongoDB Atlas**
   ```bash
   heroku config:set MONGODB_URI=<mongodb-uri>
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Check logs**
   ```bash
   heroku logs -t
   ```

---

## Option 5: Docker + Self-Hosted VPS

**Cost:** $3-10/month (DigitalOcean, Linode, Vultr)  
**Setup time:** 30 minutes  
**Best for:** Full control, custom domain, scaling

### Using DigitalOcean App Platform

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Create account (free $100 credit for 60 days)

2. **Create App**
   - Click "Create" → "Apps"
   - Select GitHub repo
   - Choose "Python" runtime
   - Settings:
     - **Build Command:** `pip install -r backend/requirements.txt`
     - **Run Command:** `cd backend && gunicorn gagcoffee.wsgi`

3. **Create MongoDB**
   - Databases → Create → MongoDB
   - Link to app
   - Get connection string from app

4. **Environment Variables**
   - Add all `.env` variables

5. **Deploy**
   - Click "Deploy"
   - Get app URL from dashboard

### Using Docker directly

1. **Create VPS** (DigitalOcean Droplet / Linode)
   ```bash
   # SSH into server
   ssh root@<ip-address>
   
   # Update system
   apt update && apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com | sh
   ```

2. **Clone and Deploy**
   ```bash
   git clone <your-repo>
   cd gagcoffee
   docker-compose up -d
   ```

3. **Setup Nginx Reverse Proxy**
   ```bash
   apt install nginx
   ```
   
   Create `/etc/nginx/sites-available/gagcoffee`:
   ```nginx
   server {
     listen 80;
     server_name yourdomain.com;

     location / {
       proxy_pass http://localhost:5500;
       proxy_set_header Host $host;
     }

     location /api/ {
       proxy_pass http://localhost:8000;
       proxy_set_header Host $host;
     }
   }
   ```
   
   Enable and restart:
   ```bash
   ln -s /etc/nginx/sites-available/gagcoffee /etc/nginx/sites-enabled/
   systemctl restart nginx
   ```

4. **Setup SSL (Let's Encrypt)**
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com
   ```

---

## MongoDB Atlas Setup (Required for all options)

1. **Create Account**
   - Go to [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
   - Sign up free

2. **Create Cluster**
   - Click "Create Cluster"
   - Choose "Free Tier" (M0)
   - Region: India (Mumbai) for GAG Coffee
   - Wait 5 minutes for creation

3. **Get Connection String**
   - Cluster → "Connect"
   - "Drivers" → Python
   - Copy connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

4. **Add IP Whitelist**
   - Network Access → Add IP Address
   - For development: Add "0.0.0.0/0" (allow all)
   - For production: Add only your server IPs

5. **Create Database User**
   - Database Access → Add Database User
   - Username: `gagcoffee`
   - Password: `<strong-password>`
   - Add to cluster

---

## Domain Setup (Custom Domain)

### 1. Register Domain
- [Namecheap](https://namecheap.com)
- [GoDaddy](https://godaddy.com)
- [Google Domains](https://domains.google)

### 2. Update DNS

**For Vercel:**
```
CNAME: <project>.vercel.app
```

**For Railway:**
```
CNAME: <railway-url>.up.railway.app
```

**For DigitalOcean:**
```
A record: <droplet-ip>
```

### 3. Update CORS
In your deployment's environment variables:
```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## SSL/HTTPS Certificate

All major platforms include free SSL:
- **Vercel**: Automatic
- **Railway**: Automatic
- **Render**: Automatic
- **DigitalOcean**: Use Let's Encrypt (certbot)
- **Self-hosted**: Use Let's Encrypt (certbot)

---

## Monitoring & Maintenance

### Check Server Status
```bash
# Vercel/Railway/Render: Check dashboard
# Self-hosted: 
curl https://yourdomain.com/api/orders/
```

### View Logs
```bash
# Vercel
vercel logs <project-name>

# Railway
railway logs

# Render
dashboard → logs

# Self-hosted
docker-compose logs -f backend
```

### Backup MongoDB
```bash
# Atlas: Enable automated backups in web UI

# Self-hosted:
mongodump --uri="<mongodb-uri>" --out=./backup
```

---

## Scaling (When You Get Popular 🎉)

### Database
- Upgrade MongoDB Atlas to paid tier ($57/month standard)
- Enable sharding for horizontal scaling

### Backend
- Vercel: Auto-scales (pay per execution)
- Railway: Increase memory/CPU in Settings
- Self-hosted: Add more servers + load balancer

### Frontend
- Vercel: Already scales globally
- GitHub Pages: Already on CDN
- Self-hosted: Add Cloudflare CDN ($20/month)

---

## Cost Breakdown (Production)

| Component | Vercel | Railway | Self-hosted |
|-----------|--------|---------|------------|
| Backend | Free (fair use) | $7-50/mo | Included |
| Frontend | Free | Free | Included |
| MongoDB | Free (free tier) | Free | - |
| MongoDB (prod) | $57/mo | $57/mo | $57/mo |
| Domain | $10/year | $10/year | $10/year |
| **Total** | ~$5/mo | ~$15/mo | ~$65/mo |

**Recommendation:** Start with Vercel + MongoDB Atlas (free tier), upgrade when you hit 512 MB data limit.

---

## Troubleshooting Deployments

### "Module not found" error
```bash
# Verify requirements.txt is complete
pip freeze > backend/requirements.txt
git add backend/requirements.txt && git commit -m "Update deps"
```

### API returns 500 error
1. Check deployment logs
2. Verify environment variables are set
3. Restart the service
4. Check MongoDB connection is whitelisted

### Frontend can't reach API
1. Verify CORS_ALLOWED_ORIGINS includes frontend URL
2. Check API_BASE in index.html is correct
3. Restart backend
4. Check firewall/network rules

### Database connection timeout
1. Whitelist all IPs: Network Access → 0.0.0.0/0
2. Check username/password are correct
3. Verify cluster is created and running

---

Made with ☕ for GAG Coffee Co.
