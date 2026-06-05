# GAG Coffee Co. — Full Stack Upgrade

Complete Django + MongoDB + Vercel stack for the GAG Coffee website.

**Stack:**
- Backend: Django (Python) + Django REST Framework
- Database: MongoDB (Atlas)
- Frontend: Single-file HTML + vanilla JS
- Deploy: Vercel (free tier)
- Auth: JWT + Django Admin

---

## 📁 Project Structure

```
gagcoffee/
├── backend/                      # Django project
│   ├── gagcoffee/               # Project config
│   │   ├── settings.py          # Django settings (MongoDB, JWT, CORS)
│   │   ├── urls.py              # Main URL routing
│   │   ├── wsgi.py              # WSGI entry point
│   │   └── mongo.py             # MongoDB connection helper
│   ├── api/                     # REST API app
│   │   ├── views.py             # Order, contact, auth endpoints
│   │   ├── urls.py              # API routes
│   │   └── apps.py              # App config
│   ├── manage.py                # Django CLI
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variables template
├── frontend/
│   ├── index.html               # Full website + admin dashboard
│   ├── images/                  # Gallery images (optional)
│   └── static/                  # (Placeholder for additional assets)
├── vercel.json                  # Vercel deployment config
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## 🚀 Local Setup (5 minutes)

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas account)
- Git

### Step 1: Clone & Install

```bash
# Clone this repo
git clone <your-repo-url>
cd gagcoffee

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 2: Configure Environment

Copy `.env.example` to `.env` and fill in values:

```bash
cp backend/.env.example backend/.env
```

**`backend/.env`:**
```env
SECRET_KEY=your-super-secret-key-change-this-in-production!!!
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=gagcoffee

# Frontend URLs for CORS
CORS_ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

**How to get MongoDB Atlas URI:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Click "Connect" → "Drivers"
4. Copy the connection string
5. Replace `<password>` with your DB password

### Step 3: Run Django

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser  # Create admin user (e.g. admin/admin)
python manage.py runserver 0.0.0.0:8000
```

✅ Backend running at `http://localhost:8000`

### Step 4: Serve Frontend

Open a new terminal:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 5500

# Or use VS Code Live Server extension
# Or any other local server on port 5500
```

✅ Frontend running at `http://localhost:5500`

### Step 5: Test the Flow

1. **Frontend:** http://localhost:5500
   - Place an order (saves to MongoDB)
   - Submit contact form (saves to MongoDB)

2. **Admin Dashboard:**
   - Go to http://localhost:5500 → click "Admin" in sidebar
   - Login with your superuser credentials (admin/admin)
   - See orders, messages, stats, and update order statuses

3. **Django Admin:**
   - http://localhost:8000/admin
   - Manage users, create staff accounts

---

## 🔧 API Endpoints

All responses are JSON. Base URL: `/api/`

### Orders

**POST `/api/orders/`** — Place a new order (public)
```json
{
  "name": "Arjun Shah",
  "phone": "9876543210",
  "pickup_time": "In 15 minutes",
  "items": ["The Classic Gag", "Almond Croissant"],
  "note": "Extra shot, less sugar"
}
```
Response:
```json
{
  "message": "Order placed!",
  "order": {
    "_id": "507f1f77bcf86cd799439011",
    "order_id": "GAG-ABC123",
    "name": "Arjun Shah",
    "status": "pending",
    "total": 300,
    "created_at": "2024-06-04T10:30:00Z"
  }
}
```

**GET `/api/orders/`** — List all orders (admin only)
Requires JWT token in header: `Authorization: Bearer <token>`

**GET `/api/orders/<id>/`** — Single order detail (admin only)

**PATCH `/api/orders/<id>/status/`** — Update order status (admin only)
```json
{ "status": "confirmed" }
```
Valid statuses: `pending`, `confirmed`, `ready`, `completed`, `cancelled`

### Contact Messages

**POST `/api/contact/`** — Submit contact form (public)
```json
{
  "name": "Sam Patel",
  "email": "sam@example.com",
  "message": "Great coffee! Can you cater events?"
}
```

**GET `/api/contact/`** — List all messages (admin only)

### Authentication

**POST `/api/auth/login/`** — Get JWT tokens (public)
```json
{
  "username": "admin",
  "password": "your-password"
}
```
Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLC...",
  "refresh": "eyJ0eXAiOiJKV1QiLC...",
  "is_admin": true,
  "username": "admin"
}
```

**POST `/api/auth/refresh/`** — Get new access token (public)
```json
{ "refresh": "<refresh-token>" }
```

### Admin Stats

**GET `/api/admin/stats/`** — Dashboard overview (admin only)
Response:
```json
{
  "total_orders": 45,
  "total_revenue": 12500,
  "status_counts": {"pending": 5, "confirmed": 8, "ready": 2, "completed": 30, "cancelled": 0},
  "top_items": [{"name": "Vietnamese Cold", "count": 12}],
  "unread_messages": 3,
  "recent_orders": [...]
}
```

---

## 🌐 Deployment to Vercel

### Step 1: Create Vercel Account
Go to [vercel.com](https://vercel.com) and sign up with GitHub.

### Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Django + MongoDB + frontend"
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy Backend on Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Select your GitHub repo
4. **Framework Preset:** None (Python)
5. **Root Directory:** Leave blank
6. **Build Command:** `pip install -r backend/requirements.txt`
7. **Start Command:** `gunicorn gagcoffee.wsgi`
8. **Environment Variables** → Add these:
   ```
   DJANGO_SETTINGS_MODULE=gagcoffee.settings
   SECRET_KEY=<generate-strong-secret>
   DEBUG=False
   ALLOWED_HOSTS=<your-vercel-url>.vercel.app
   MONGODB_URI=<your-mongodb-atlas-uri>
   MONGODB_DB=gagcoffee
   CORS_ALLOWED_ORIGINS=https://<your-vercel-url>.vercel.app
   ```
9. Click "Deploy"

✅ Backend deployed! Note the URL: `https://<your-project>.vercel.app`

### Step 4: Deploy Frontend on Vercel (Option A)

Use Vercel's static hosting:

1. Create a new Vercel project
2. Select "Other" (static)
3. **Root Directory:** `frontend`
4. Deploy

Or modify `frontend/index.html` to point to your deployed backend:

```javascript
// Line ~285 in index.html
var API_BASE = 'https://<your-backend>.vercel.app/api';
```

### Step 5: Deploy Frontend on GitHub Pages (Option B)

```bash
# Commit and push to GitHub
git push origin main

# Go to repo Settings → Pages
# Set source to "Deploy from a branch"
# Select "main" branch, /frontend folder
```

✅ Frontend live at `https://<username>.github.io/<repo-name>`

Update API URL in `frontend/index.html`:
```javascript
var API_BASE = 'https://<your-backend>.vercel.app/api';
```

---

## 🛡️ Production Checklist

Before going live:

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate a strong `SECRET_KEY` (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set `CORS_ALLOWED_ORIGINS` to your frontend URL
- [ ] Enable HTTPS (Vercel does this automatically)
- [ ] Create admin user on production: `python manage.py createsuperuser`
- [ ] Backup MongoDB (enable automated backups in Atlas)
- [ ] Test the full flow (order → admin dashboard → update status)
- [ ] Monitor API error logs
- [ ] Set up email notifications (optional)

---

## 🔗 Custom Domain (Optional)

### Add your domain to Vercel

1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records at your registrar (Vercel will show you exactly what to add)
4. Wait 24-48 hours for propagation

### Update CORS & ALLOWED_HOSTS

In Vercel environment variables:
```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 🐛 Troubleshooting

### "API Offline" indicator shows red

1. Check backend is running: `http://localhost:8000/api/orders/`
2. Check `API_BASE` URL in `frontend/index.html` (line ~285)
3. Check CORS settings in `backend/gagcoffee/settings.py`
4. Check `.env` file exists and has `MONGODB_URI`

### MongoDB connection error

1. Check your MongoDB Atlas connection string
2. Make sure your IP is whitelisted in Atlas (Network Access → Add IP Address)
3. Verify username and password don't have special characters (or URL-encode them)

### Admin login returns 401

1. Make sure you created a superuser: `python manage.py createsuperuser`
2. Check credentials are correct (case-sensitive)
3. Verify `SECRET_KEY` is set in `.env`

### Orders not saving

1. Check MongoDB is running and accessible
2. Look at Django logs for error messages
3. Test MongoDB connection: `mongo <connection-string>`

---

## 📚 Tech Stack Details

### Django REST Framework
- Simple, powerful API framework
- Built-in authentication (JWT)
- Request/response validation

### MongoDB
- NoSQL, flexible schema
- Free tier: 512 MB (perfect for startups)
- Paid: $10/month for production-grade

### Vercel
- Zero-config deployment
- Automatic HTTPS
- Serverless functions (Python via `gunicorn`)
- Free tier: 100 GB bandwidth/month

### Frontend
- Zero dependencies (vanilla HTML/CSS/JS)
- Responsive mobile-first design
- Works offline with graceful degradation

---

## 📧 Next Steps

1. **Add WhatsApp Integration** — Use Twilio API to auto-send WhatsApp order confirmations
2. **Email Notifications** — Send staff alerts on new orders using Django Celery
3. **Payment Gateway** — Add Razorpay or Stripe for online payments
4. **Analytics** — Track order trends, popular items, peak hours
5. **SMS Reminders** — Send pickup reminders to customers
6. **Loyalty Program** — Track repeat customers, offer discounts

---

## 🤝 Support & Issues

- Django: [django.readthedocs.io](https://django.readthedocs.io)
- MongoDB: [docs.mongodb.com](https://docs.mongodb.com)
- Vercel: [vercel.com/docs](https://vercel.com/docs)
- API Testing: Use Postman or Insomnia to test endpoints

---

**Made with ☕ for GAG Coffee Co.**

Last Updated: June 2024
