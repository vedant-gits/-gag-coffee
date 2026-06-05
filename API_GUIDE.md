# API Testing Guide — GAG Coffee Co.

Quick reference for testing and integrating with the API.

---

## 🧪 Test with cURL

### 1. Place an Order (Public)

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Arjun Shah",
    "phone": "9876543210",
    "pickup_time": "In 15 minutes",
    "items": ["The Classic Gag", "Almond Croissant"],
    "note": "Extra shot, less sugar"
  }'
```

Expected Response (201):
```json
{
  "message": "Order placed!",
  "order": {
    "_id": "507f1f77bcf86cd799439011",
    "order_id": "GAG-ABC123",
    "name": "Arjun Shah",
    "phone": "9876543210",
    "pickup_time": "In 15 minutes",
    "items": ["The Classic Gag", "Almond Croissant"],
    "total": 300,
    "note": "Extra shot, less sugar",
    "status": "pending",
    "created_at": "2024-06-04T10:30:00.000000Z",
    "updated_at": "2024-06-04T10:30:00.000000Z"
  }
}
```

### 2. Submit Contact Form (Public)

```bash
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sam Patel",
    "email": "sam@example.com",
    "message": "Great coffee! Can you cater events?"
  }'
```

### 3. Admin Login (Get JWT Token)

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "is_admin": true,
  "username": "admin"
}
```

Save the `access` token for authenticated requests.

### 4. List All Orders (Admin Only)

```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 5. Get Order Details (Admin Only)

```bash
curl -X GET http://localhost:8000/api/orders/507f1f77bcf86cd799439011/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 6. Update Order Status (Admin Only)

```bash
curl -X PATCH http://localhost:8000/api/orders/507f1f77bcf86cd799439011/status/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -d '{
    "status": "confirmed"
  }'
```

Valid statuses: `pending`, `confirmed`, `ready`, `completed`, `cancelled`

### 7. Get Dashboard Stats (Admin Only)

```bash
curl -X GET http://localhost:8000/api/admin/stats/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 8. List All Messages (Admin Only)

```bash
curl -X GET http://localhost:8000/api/contact/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 📮 Test with Postman

### Import Collection

1. Download or create a Postman collection with these requests:

```json
{
  "info": {
    "name": "GAG Coffee Co. API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Orders",
      "item": [
        {
          "name": "Create Order",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"Arjun Shah\",\n  \"phone\": \"9876543210\",\n  \"pickup_time\": \"In 15 minutes\",\n  \"items\": [\"The Classic Gag\", \"Almond Croissant\"],\n  \"note\": \"\"\n}"
            },
            "url": {"raw": "http://localhost:8000/api/orders/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api", "orders", ""]}
          }
        },
        {
          "name": "List Orders (Admin)",
          "request": {
            "method": "GET",
            "header": [{"key": "Authorization", "value": "Bearer {{access_token}}"}],
            "url": {"raw": "http://localhost:8000/api/orders/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api", "orders", ""]}
          }
        }
      ]
    },
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {"mode": "raw", "raw": "{\n  \"username\": \"admin\",\n  \"password\": \"admin\"\n}"},
            "url": {"raw": "http://localhost:8000/api/auth/login/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api", "auth", "login", ""]}
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": ["var jsonData = pm.response.json();", "pm.environment.set(\"access_token\", jsonData.access);"]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

2. Import this into Postman: `File → Import`
3. Set your API base URL as an environment variable: `{{base_url}}`
4. Run "Login" first to get access token
5. Use the token in other admin requests

---

## 📱 Test from Frontend

The frontend automatically calls the API when you:

1. **Place an order:**
   - Navigate to "Order Ahead" page
   - Fill in form and click "Confirm Order"
   - Saves to `/api/orders/`

2. **Submit contact form:**
   - Navigate to "Contact & Map" page
   - Fill form and click "Send Message"
   - Saves to `/api/contact/`

3. **Access admin dashboard:**
   - Click "Admin" in sidebar
   - Login with admin credentials
   - Fetches `/api/admin/stats/`, `/api/orders/`, `/api/contact/`

---

## 🔍 Monitor API

### Check backend logs (Docker)

```bash
docker-compose logs backend -f
```

### Check MongoDB directly

```bash
# If running locally
mongo

# Connect to specific DB
use gagcoffee

# List all orders
db.orders.find()

# List all messages
db.contacts.find()

# Check collection stats
db.orders.stats()
```

### Check API response times

```bash
# Use curl with timing
curl -w "\nResponse time: %{time_total}s\n" http://localhost:8000/api/orders/
```

---

## ✅ Common Issues & Solutions

### 401 Unauthorized (Admin endpoints)

**Problem:** Getting 401 when accessing `/api/orders/` as admin

**Solution:**
1. Make sure you logged in and got the access token
2. Include token in header: `Authorization: Bearer <token>`
3. Make sure token isn't expired (expires in 8 hours)
4. Refresh token if needed: `POST /api/auth/refresh/` with refresh token

### 403 Forbidden

**Problem:** Login works but still can't access admin endpoints

**Solution:**
1. Make sure your user is a superuser: `python manage.py createsuperuser`
2. Or in Django admin, mark user as "Staff status" checked
3. Try logging out and logging back in

### CORS Error

**Problem:** Frontend can't reach API

**Solution:**
1. Check `API_BASE` URL in frontend/index.html (line ~285)
2. Make sure backend is running
3. Check CORS_ALLOWED_ORIGINS in backend/.env
4. Restart backend after changing .env

### MongoDB Connection Failed

**Problem:** `MongoServerSelectionError` in logs

**Solution:**
1. Verify MongoDB URI is correct in .env
2. Check username/password are URL-encoded if they have special chars
3. Whitelist your IP in MongoDB Atlas (Network Access)
4. For local MongoDB: make sure `mongod` is running

---

## 📊 Performance Tips

### Optimize queries
- Orders list limited to 200 most recent
- Messages list limited to 200
- Use `?status=pending` to filter orders: `GET /api/orders/?status=pending`

### Cache admin stats
- Stats are calculated on-demand
- Consider adding Redis caching for production

### Database indexes
```javascript
// In MongoDB Atlas > Database > Collections
db.orders.createIndex({ "status": 1, "created_at": -1 })
db.orders.createIndex({ "order_id": 1 })
db.contacts.createIndex({ "created_at": -1 })
```

---

## 🚀 Next: Add More Features

Once API is working:

1. **Email notifications:** Send order confirmation emails
2. **SMS alerts:** Notify staff of new orders via SMS (Twilio)
3. **Payment:** Add Razorpay/Stripe for pre-payment
4. **Search:** Add full-text search for orders/messages
5. **Webhooks:** Trigger external integrations (Slack, Google Sheets)
6. **Rate limiting:** Prevent abuse of public endpoints

---

Made with ☕ for GAG Coffee Co.
