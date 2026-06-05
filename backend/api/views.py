"""
GAG Coffee Co. — API Views
────────────────────────────
POST /api/orders/          → Place a new order (public)
GET  /api/orders/          → List all orders  (admin only)
GET  /api/orders/<id>/     → Single order     (admin only)
PATCH /api/orders/<id>/status/ → Update status (admin only)

POST /api/contact/         → Submit contact form (public)
GET  /api/contact/         → List messages (admin only)

POST /api/auth/login/      → Get JWT tokens
POST /api/auth/refresh/    → Refresh access token
GET  /api/admin/stats/     → Dashboard stats (admin only)
"""
import uuid
import threading
from datetime import datetime, timezone

from bson import ObjectId
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from gagcoffee.mongo import db


def send_order_email(order):
    """Send order notification email to owner in a background thread."""
    def _send():
        try:
            items_list = ", ".join(order.get("items", []))
            subject = f"☕ New Order {order['order_id']} — GAG Coffee Co."
            message = (
                f"New order received!\n\n"
                f"Order ID : {order['order_id']}\n"
                f"Name     : {order['name']}\n"
                f"Phone    : {order['phone']}\n"
                f"Items    : {items_list}\n"
                f"Total    : ₹{order['total']}\n"
                f"Pickup   : {order['pickup_time']}\n"
                f"Note     : {order.get('note') or 'None'}\n"
                f"Time     : {order['created_at']}\n\n"
                f"Login to dashboard: http://127.0.0.1:5501/index.html"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=f"GAG Coffee Co. <{settings.EMAIL_HOST_USER}>",
                recipient_list=[settings.OWNER_EMAIL],
                fail_silently=False,
            )
            print(f"[Email] Order notification sent for {order['order_id']}")
        except Exception as e:
            print(f"[Email Error] {e}")
    threading.Thread(target=_send, daemon=True).start()


# ── helpers ───────────────────────────────────────────────────────────────────

def _fmt(doc: dict) -> dict:
    """Convert ObjectId/_id to string so it's JSON-serialisable."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _order_id() -> str:
    return "GAG-" + uuid.uuid4().hex[:6].upper()


VALID_STATUSES = ["pending", "confirmed", "ready", "completed", "cancelled"]


# ── Orders ────────────────────────────────────────────────────────────────────

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def orders(request):
    # ── POST: place a new order (public) ──────────────────────────────────────
    if request.method == "POST":
        d = request.data
        name  = str(d.get("name", "")).strip()
        phone = str(d.get("phone", "")).strip().replace(" ", "")
        time_ = str(d.get("pickup_time", "")).strip()
        items = d.get("items", [])
        note  = str(d.get("note", "")).strip()

        # Validation
        errors = {}
        if not name:
            errors["name"] = "Name is required."
        digits = phone.lstrip("+")
        if digits.startswith("91") and len(digits) >= 12:
            digits = digits[2:]
        if not digits.isdigit() or len(digits) != 10 or digits[0] not in "6789":
            errors["phone"] = "Valid 10-digit phone number required."
        if not time_:
            errors["pickup_time"] = "Pickup time is required."
        if not isinstance(items, list) or not items:
            errors["items"] = "At least one item must be selected."
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Build total from allowed menu prices
        PRICES = {
            "The Classic Gag": 180, "Matcha Mess": 240, "Honey Drift": 260,
            "Spice Riot": 210, "Vietnamese Cold": 220, "Almond Croissant": 120,
            "Dark Ganache": 150,
        }
        total = sum(PRICES.get(i, 0) for i in items)

        doc = {
            "order_id":   _order_id(),
            "name":       name,
            "phone":      phone,
            "pickup_time": time_,
            "items":      items,
            "total":      total,
            "note":       note,
            "status":     "pending",
            "created_at": _now(),
            "updated_at": _now(),
        }
        result = db.orders.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        send_order_email(doc)
        return Response(
            {"message": "Order placed!", "order": doc},
            status=status.HTTP_201_CREATED,
        )

    # ── GET: list orders (admin only) ─────────────────────────────────────────
    if not (request.user and request.user.is_staff):
        return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

    filter_status = request.query_params.get("status")
    query = {}
    if filter_status and filter_status in VALID_STATUSES:
        query["status"] = filter_status

    cursor = db.orders.find(query).sort("created_at", -1).limit(200)
    return Response([_fmt(o) for o in cursor])


@api_view(["GET"])
@permission_classes([IsAdminUser])
def order_detail(request, order_id: str):
    """GET /api/orders/<mongo_id>/"""
    try:
        doc = db.orders.find_one({"_id": ObjectId(order_id)})
    except Exception:
        doc = db.orders.find_one({"order_id": order_id})
    if not doc:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(_fmt(doc))


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def update_order_status(request, order_id: str):
    """PATCH /api/orders/<mongo_id>/status/  body: {"status": "confirmed"}"""
    new_status = request.data.get("status")
    if new_status not in VALID_STATUSES:
        return Response(
            {"detail": f"Invalid status. Choose from: {VALID_STATUSES}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        oid = ObjectId(order_id)
    except Exception:
        return Response({"detail": "Invalid ID."}, status=status.HTTP_400_BAD_REQUEST)

    result = db.orders.update_one(
        {"_id": oid},
        {"$set": {"status": new_status, "updated_at": _now()}},
    )
    if result.matched_count == 0:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Status updated.", "status": new_status})


# ── Contact ───────────────────────────────────────────────────────────────────

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def contact(request):
    if request.method == "POST":
        d = request.data
        name    = str(d.get("name", "")).strip()
        email   = str(d.get("email", "")).strip()
        message = str(d.get("message", "")).strip()

        errors = {}
        if not name:
            errors["name"] = "Name is required."
        if not email or "@" not in email:
            errors["email"] = "Valid email required."
        if not message:
            errors["message"] = "Message is required."
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        doc = {
            "name":       name,
            "email":      email,
            "message":    message,
            "read":       False,
            "created_at": _now(),
        }
        result = db.contacts.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return Response({"message": "Message received! We'll be in touch."}, status=status.HTTP_201_CREATED)

    # GET (admin only)
    if not (request.user and request.user.is_staff):
        return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)
    cursor = db.contacts.find({}).sort("created_at", -1).limit(200)
    return Response([_fmt(c) for c in cursor])


# ── Auth ──────────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """POST /api/auth/login/  body: {username, password}"""
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    refresh = RefreshToken.for_user(user)
    return Response({
        "access":       str(refresh.access_token),
        "refresh":      str(refresh),
        "is_admin":     user.is_staff,
        "username":     user.username,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_view(request):
    """POST /api/auth/refresh/  body: {refresh}"""
    try:
        refresh = RefreshToken(request.data.get("refresh", ""))
        return Response({"access": str(refresh.access_token)})
    except Exception:
        return Response({"detail": "Invalid or expired token."}, status=status.HTTP_401_UNAUTHORIZED)


# ── Admin Stats ───────────────────────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """GET /api/admin/stats/ — dashboard numbers"""
    pipeline_revenue = [
        {"$match": {"status": {"$nin": ["cancelled"]}}},
        {"$group": {"_id": None, "total": {"$sum": "$total"}}},
    ]
    rev_result = list(db.orders.aggregate(pipeline_revenue))
    total_revenue = rev_result[0]["total"] if rev_result else 0

    status_counts = {}
    for s in VALID_STATUSES:
        status_counts[s] = db.orders.count_documents({"status": s})

    # Top items
    pipeline_items = [
        {"$unwind": "$items"},
        {"$group": {"_id": "$items", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    top_items = [{"name": r["_id"], "count": r["count"]} for r in db.orders.aggregate(pipeline_items)]

    # Recent 5 orders
    recent = [_fmt(o) for o in db.orders.find({}).sort("created_at", -1).limit(5)]

    return Response({
        "total_orders":    db.orders.count_documents({}),
        "total_revenue":   total_revenue,
        "status_counts":   status_counts,
        "top_items":       top_items,
        "unread_messages": db.contacts.count_documents({"read": False}),
        "recent_orders":   recent,
    })
