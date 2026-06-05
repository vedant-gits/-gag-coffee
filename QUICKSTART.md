✅ GAG Coffee Co. — Full Stack Setup Checklist

═══════════════════════════════════════════════════════════════════════════════

🎯 LOCAL DEVELOPMENT (5 minutes)

☐ 1. Python 3.9+ installed
☐ 2. Run: bash setup.sh
☐ 3. Edit backend/.env with MongoDB URI
☐ 4. Terminal 1: cd backend && python manage.py runserver
☐ 5. Terminal 2: cd frontend && python -m http.server 5500
☐ 6. Open http://localhost:5500
☐ 7. Test: Place an order, check admin dashboard

═══════════════════════════════════════════════════════════════════════════════

🌐 MONGODB ATLAS SETUP (10 minutes)

☐ 1. Go to mongodb.com/cloud/atlas → Create Account
☐ 2. Create Cluster (Free M0 tier, Mumbai region)
☐ 3. Wait 5 minutes for cluster to be ready
☐ 4. Network Access → Add IP 0.0.0.0/0 (dev) or your IPs (prod)
☐ 5. Database Access → Create user 'gagcoffee' with strong password
☐ 6. Copy Connection String: mongodb+srv://...
☐ 7. Add to backend/.env as MONGODB_URI
☐ 8. Test connection: python manage.py shell
   ├─ from gagcoffee.mongo import db
   ├─ db.orders.insert_one({"test": "data"})
   └─ Exit and verify in Atlas UI

═══════════════════════════════════════════════════════════════════════════════

🚀 DEPLOY TO VERCEL (15 minutes)

☐ 1. Push code to GitHub:
   ├─ git init
   ├─ git add .
   ├─ git commit -m "GAG Coffee Full Stack"
   ├─ git remote add origin https://github.com/<user>/<repo>
   └─ git push -u origin main

☐ 2. Go to vercel.com → Create Account → New Project
☐ 3. Select your GitHub repo
☐ 4. Settings:
   ├─ Framework: None (Python)
   ├─ Root Directory: (empty)
   ├─ Build: pip install -r backend/requirements.txt
   └─ Start: cd backend && gunicorn gagcoffee.wsgi

☐ 5. Environment Variables (click "Add"):
   ├─ DJANGO_SETTINGS_MODULE = gagcoffee.settings
   ├─ DEBUG = False
   ├─ SECRET_KEY = (run: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
   ├─ ALLOWED_HOSTS = <project>.vercel.app
   ├─ MONGODB_URI = <your-mongodb-uri>
   ├─ MONGODB_DB = gagcoffee
   └─ CORS_ALLOWED_ORIGINS = https://<frontend-domain>.com

☐ 6. Click "Deploy" and wait 2-3 minutes
☐ 7. Copy your backend URL: https://<project>.vercel.app

═══════════════════════════════════════════════════════════════════════════════

📱 DEPLOY FRONTEND (5 minutes)

Option A: GitHub Pages (Free)
  ☐ 1. Repo → Settings → Pages
  ☐ 2. Deploy from branch: main / /frontend
  ☐ 3. Wait 2 minutes, get URL

Option B: Separate Vercel Project (Free)
  ☐ 1. New Vercel Project → Same repo
  ☐ 2. Root Directory: frontend
  ☐ 3. Deploy

Option C: Deploy to same Vercel project
  ☐ 1. Add static file serving in Vercel config
  ☐ 2. Update frontend index.html to use same domain

═══════════════════════════════════════════════════════════════════════════════

🔧 UPDATE API URL IN FRONTEND

☐ 1. Edit frontend/index.html
☐ 2. Find line ~285: var API_BASE = '...'
☐ 3. Change to: var API_BASE = 'https://<your-backend>.vercel.app/api'
☐ 4. Commit and push
☐ 5. Wait for frontend redeploy

═══════════════════════════════════════════════════════════════════════════════

✅ TESTING

Frontend:
  ☐ Home page loads
  ☐ "Order Ahead" shows menu items
  ☐ Place an order (goes to database)
  ☐ Contact form works
  ☐ API status shows "Online" (green dot)

Admin Dashboard:
  ☐ Click "Admin" in sidebar
  ☐ Login with admin/admin
  ☐ See orders, messages, stats
  ☐ Update order status (pending → confirmed)

═══════════════════════════════════════════════════════════════════════════════

📊 CHECK WHAT'S SAVING

MongoDB Atlas UI:
  ☐ Collections → orders → See your test orders
  ☐ Collections → contacts → See your messages

Django Admin:
  ☐ http://<backend-url>/admin/
  ☐ Login with admin credentials
  ☐ Users → Confirm admin user exists

═══════════════════════════════════════════════════════════════════════════════

🎯 NEXT STEPS

☐ 1. Test order flow end-to-end (frontend → DB → admin dashboard)
☐ 2. Add custom domain (optional)
☐ 3. Add WhatsApp integration (Twilio)
☐ 4. Add payment (Razorpay)
☐ 5. Setup email notifications
☐ 6. Setup analytics

═══════════════════════════════════════════════════════════════════════════════

📚 DOCUMENTATION

- README.md        — Complete setup and architecture overview
- API_GUIDE.md     — Testing API with cURL, Postman
- DEPLOYMENT.md    — Detailed deploy instructions for 5+ platforms
- setup.sh         — Automated local setup script

═══════════════════════════════════════════════════════════════════════════════

💬 TROUBLESHOOTING

API offline?
  → Check backend URL in frontend/index.html
  → Make sure backend is running
  → Check CORS_ALLOWED_ORIGINS includes frontend URL

MongoDB error?
  → Verify connection string in .env
  → Whitelist your IP in MongoDB Atlas
  → Check username/password are correct

Admin login fails?
  → Create superuser: python manage.py createsuperuser
  → Verify user is marked as "Staff" in Django admin

═══════════════════════════════════════════════════════════════════════════════

Made with ☕ for GAG Coffee Co.

Questions? Check:
- Django docs: django.readthedocs.io
- MongoDB: docs.mongodb.com
- Vercel: vercel.com/docs
- REST API: restfulapi.net
