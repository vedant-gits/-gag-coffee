#!/bin/bash
# Quick Start Script for GAG Coffee Co.
# Run: bash setup.sh

set -e  # Exit on error

echo "🚀 GAG Coffee Co. — Setup Script"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create virtual environment
echo -e "${BLUE}Step 1: Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}✓ Virtual environment already exists${NC}"
fi

# Step 2: Activate venv and install dependencies
echo ""
echo -e "${BLUE}Step 2: Installing Python dependencies...${NC}"
source venv/bin/activate || . venv/Scripts/activate
pip install -q -r backend/requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 3: Check .env file
echo ""
echo -e "${BLUE}Step 3: Checking environment configuration...${NC}"
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠ .env file not found. Copying from .env.example...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your MongoDB URI${NC}"
    cat backend/.env
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Step 4: Run migrations
echo ""
echo -e "${BLUE}Step 4: Setting up Django database...${NC}"
cd backend
python manage.py migrate --run-syncdb
echo -e "${GREEN}✓ Database configured${NC}"

# Step 5: Create superuser (if doesn't exist)
echo ""
echo -e "${BLUE}Step 5: Creating superuser (if needed)...${NC}"
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gagcoffee.local', 'admin')
    print("✓ Superuser created: admin / admin")
else:
    print("✓ Superuser already exists")
END

cd ..

# Step 6: Summary
echo ""
echo -e "${GREEN}=================================="
echo "✅ Setup Complete!"
echo "==================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1️⃣  Terminal 1 - Start Django backend:"
echo -e "   ${YELLOW}cd backend && python manage.py runserver 0.0.0.0:8000${NC}"
echo ""
echo "2️⃣  Terminal 2 - Serve frontend (in frontend/ directory):"
echo -e "   ${YELLOW}python -m http.server 5500${NC}"
echo ""
echo "3️⃣  Open your browser:"
echo -e "   Frontend: ${YELLOW}http://localhost:5500${NC}"
echo -e "   Admin: ${YELLOW}http://localhost:5500 → click 'Admin' (login: admin/admin)${NC}"
echo -e "   Django Admin: ${YELLOW}http://localhost:8000/admin${NC}"
echo ""
echo -e "${BLUE}Troubleshooting:${NC}"
echo "- Edit backend/.env to add your MongoDB URI"
echo "- Make sure ports 5500 and 8000 are free"
echo "- Check that MongoDB is running (if local)"
echo ""
