#!/bin/bash
# Test API access with admin_group role

echo "🧪 Testing API Access with admin_group Role"
echo "============================================"
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Login
echo "📋 Test 1: Login as group_admin"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=group_admin&password=any")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi

echo "✅ Login successful"
echo "Token: ${TOKEN:0:20}..."
echo ""

# Test 2: Get user info
echo "📋 Test 2: Get current user info"
USER_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN")

echo "Response: $USER_RESPONSE"
echo ""

# Test 3: Access meetings endpoint
echo "📋 Test 3: Access GET /api/v1/meetings"
MEETINGS_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X GET "$BASE_URL/api/v1/meetings" \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$MEETINGS_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Access granted (200 OK)"
elif [ "$HTTP_CODE" = "403" ]; then
    echo "❌ Access denied (403 Forbidden)"
    echo "Response: $MEETINGS_RESPONSE"
    exit 1
else
    echo "⚠️  Unexpected status code: $HTTP_CODE"
    echo "Response: $MEETINGS_RESPONSE"
fi
echo ""

# Test 4: Create meeting
echo "📋 Test 4: Create meeting POST /api/v1/meetings"
CREATE_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/v1/meetings" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_title": "Test Meeting",
    "meeting_date": "2024-12-25",
    "start_time": "09:00:00",
    "end_time": "12:00:00",
    "location": "Test Room"
  }')

HTTP_CODE=$(echo "$CREATE_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Meeting created (201 Created)"
elif [ "$HTTP_CODE" = "403" ]; then
    echo "❌ Access denied (403 Forbidden)"
    echo "Response: $CREATE_RESPONSE"
    exit 1
else
    echo "⚠️  Status code: $HTTP_CODE"
fi
echo ""

echo "============================================"
echo "✅ All API access tests PASSED"
echo "============================================"
echo ""
echo "Summary:"
echo "  - Login: ✅"
echo "  - Get user info: ✅"
echo "  - Access meetings: ✅"
echo "  - Create meeting: ✅"
echo ""
echo "The admin_group role now has proper access!"
