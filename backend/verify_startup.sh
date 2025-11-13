#!/bin/bash
# Startup verification script for Meeting Management System

echo "🚀 Meeting Management System - Startup Verification"
echo "=================================================="
echo ""

# Test 1: ORM Relationships
echo "📋 Test 1: Verifying ORM relationships..."
python test_orm_relationships.py
if [ $? -eq 0 ]; then
    echo "✅ ORM relationships test passed"
else
    echo "❌ ORM relationships test failed"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ All verification tests passed!"
echo ""
echo "You can now start the server with:"
echo "  uvicorn app.main:app --reload"
echo ""
