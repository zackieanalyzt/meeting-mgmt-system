# Deployment Checklist - Phase 9.2

## Pre-Deployment Checks

### Backend Verification
- [ ] Backend starts without errors
- [ ] All database tables created
- [ ] Dummy users seeded successfully
- [ ] Swagger docs accessible at /docs
- [ ] Health endpoint returns 200
- [ ] CORS configured for frontend URL
- [ ] JWT secret key is secure
- [ ] Database connections working

### Frontend Verification
- [ ] Frontend builds without errors
- [ ] No console errors on load
- [ ] All routes accessible
- [ ] API base URL configured correctly
- [ ] Token storage working
- [ ] Role guards functioning
- [ ] Protected routes redirect properly

---

## Functional Testing

### Authentication
- [ ] Login with admin works
- [ ] Login with group_admin works
- [ ] Login with user1 works
- [ ] Invalid credentials rejected
- [ ] Token stored in localStorage
- [ ] Token persists on refresh
- [ ] Logout clears token
- [ ] 401 redirects to login

### Dashboard
- [ ] User info displays correctly
- [ ] Roles shown accurately
- [ ] Meeting stats load
- [ ] Quick actions visible
- [ ] Role-based buttons show/hide
- [ ] Permission summary correct

### Meeting List
- [ ] Meetings load from API
- [ ] Filter dropdown works
- [ ] Status badges display
- [ ] Click navigates to detail
- [ ] Create button (admin only)
- [ ] Empty state shows correctly

### Meeting Detail
- [ ] Meeting info displays
- [ ] Dates formatted correctly
- [ ] Status badge shows
- [ ] Admin buttons (admin only)
- [ ] Close meeting works
- [ ] Delete meeting works
- [ ] Back button navigates

### Create Meeting
- [ ] Form accessible (admin only)
- [ ] All fields editable
- [ ] Date picker works
- [ ] Time picker works
- [ ] Form validation works
- [ ] Submit creates meeting
- [ ] Success redirects
- [ ] Error handling works

### Role-Based Access
- [ ] Admin sees all features
- [ ] Group admin sees limited features
- [ ] Regular user sees view-only
- [ ] RoleGuard blocks unauthorized
- [ ] Access denied message shows
- [ ] Fallback navigation works

---

## API Testing

### Auth Endpoints
```bash
# Test login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -F "username=admin" \
  -F "password=test"

# Expected: 200 with token and user data
```

### Meeting Endpoints
```bash
# Get all meetings
curl -X GET http://127.0.0.1:8000/api/v1/meetings \
  -H "Authorization: Bearer <token>"

# Expected: 200 with array of meetings

# Create meeting (admin only)
curl -X POST http://127.0.0.1:8000/api/v1/meetings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_name": "Test Meeting",
    "meeting_date": "2024-11-15",
    "meeting_time": "14:00",
    "location": "Room A",
    "description": "Test"
  }'

# Expected: 201 with created meeting

# Get meeting by ID
curl -X GET http://127.0.0.1:8000/api/v1/meetings/1 \
  -H "Authorization: Bearer <token>"

# Expected: 200 with meeting data

# Close meeting (admin only)
curl -X POST http://127.0.0.1:8000/api/v1/meetings/1/close \
  -H "Authorization: Bearer <token>"

# Expected: 200 with updated meeting

# Delete meeting (admin only)
curl -X DELETE http://127.0.0.1:8000/api/v1/meetings/1 \
  -H "Authorization: Bearer <token>"

# Expected: 204 No Content
```

---

## Security Checks

### Authentication
- [ ] JWT tokens expire correctly
- [ ] Invalid tokens rejected
- [ ] Expired tokens handled
- [ ] Password not logged
- [ ] Token not exposed in URL

### Authorization
- [ ] Admin endpoints protected
- [ ] Non-admin cannot create meetings
- [ ] Non-admin cannot delete meetings
- [ ] Non-admin cannot close meetings
- [ ] Role checks working

### Data Protection
- [ ] SQL injection prevented (ORM)
- [ ] XSS prevented (React escaping)
- [ ] CSRF not applicable (JWT)
- [ ] Sensitive data not logged
- [ ] Error messages safe

---

## Performance Checks

### Frontend
- [ ] Initial load < 3 seconds
- [ ] Page transitions smooth
- [ ] No memory leaks
- [ ] API calls optimized
- [ ] Images optimized (if any)

### Backend
- [ ] API response < 500ms
- [ ] Database queries optimized
- [ ] No N+1 queries
- [ ] Connection pooling working
- [ ] Error handling efficient

---

## Browser Compatibility

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (basic)

---

## Database Checks

### PostgreSQL
```sql
-- Check tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check dummy users
SELECT u.username, u.fullname, r.role_name 
FROM users_local u
JOIN user_roles ur ON u.user_id = ur.user_id
JOIN roles r ON ur.role_id = r.role_id;

-- Check meetings
SELECT meeting_id, meeting_name, status, meeting_date 
FROM meetings;
```

### MariaDB
```sql
-- Check HR personnel table
SELECT COUNT(*) FROM hr.personnel;

-- Test user exists
SELECT username FROM hr.personnel WHERE username = 'admin';
```

---

## Environment Configuration

### Backend (.env or config)
- [ ] POSTGRES_HOST configured
- [ ] POSTGRES_PORT configured
- [ ] POSTGRES_DB configured
- [ ] POSTGRES_USER configured
- [ ] POSTGRES_PASSWORD configured
- [ ] MARIADB_HOST configured
- [ ] MARIADB_PORT configured
- [ ] SECRET_KEY set (secure)
- [ ] ALLOWED_ORIGINS includes frontend URL

### Frontend
- [ ] API base URL correct
- [ ] Build configuration correct
- [ ] Environment variables set

---

## Documentation Checks

- [ ] README.md updated
- [ ] API documentation complete
- [ ] User guide available
- [ ] Deployment guide available
- [ ] Troubleshooting guide available

---

## Monitoring Setup

### Logs
- [ ] Backend logs configured
- [ ] Frontend errors logged
- [ ] Database logs enabled
- [ ] Log rotation configured

### Metrics
- [ ] API response times tracked
- [ ] Error rates monitored
- [ ] User activity logged
- [ ] Database performance tracked

---

## Backup & Recovery

- [ ] Database backup configured
- [ ] Backup schedule set
- [ ] Recovery procedure tested
- [ ] Data retention policy defined

---

## Post-Deployment

### Immediate (Day 1)
- [ ] Monitor error logs
- [ ] Check user feedback
- [ ] Verify all features working
- [ ] Monitor performance metrics

### Short-term (Week 1)
- [ ] Review usage patterns
- [ ] Identify bottlenecks
- [ ] Gather user feedback
- [ ] Plan improvements

### Long-term (Month 1)
- [ ] Analyze metrics
- [ ] Plan Phase 9.3
- [ ] Review security
- [ ] Optimize performance

---

## Rollback Plan

### If Issues Found
1. Stop frontend server
2. Stop backend server
3. Restore database backup
4. Deploy previous version
5. Verify functionality
6. Investigate issues
7. Fix and redeploy

### Rollback Commands
```bash
# Stop services
# Frontend: Ctrl+C
# Backend: Ctrl+C

# Restore database (if needed)
psql -U postgres -d meeting_mgmt < backup.sql

# Deploy previous version
git checkout v3.5.0
# Restart services
```

---

## Sign-off

### Development Team
- [ ] Code reviewed
- [ ] Tests passed
- [ ] Documentation complete
- [ ] Ready for deployment

### QA Team
- [ ] Functional tests passed
- [ ] Security tests passed
- [ ] Performance tests passed
- [ ] User acceptance passed

### Operations Team
- [ ] Infrastructure ready
- [ ] Monitoring configured
- [ ] Backup configured
- [ ] Support ready

---

## Deployment Steps

### 1. Pre-deployment
```bash
# Backup database
pg_dump -U postgres meeting_mgmt > backup_$(date +%Y%m%d).sql

# Pull latest code
git pull origin main

# Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### 2. Deployment
```bash
# Start backend
cd backend
python -m uvicorn app.main:app --reload

# Start frontend
cd frontend
npm run dev
```

### 3. Verification
```bash
# Check backend health
curl http://127.0.0.1:8000/health

# Check frontend
curl http://localhost:5173
```

### 4. Post-deployment
- Monitor logs for errors
- Test critical paths
- Verify user access
- Check performance

---

## Emergency Contacts

- **Backend Developer:** [Contact]
- **Frontend Developer:** [Contact]
- **Database Admin:** [Contact]
- **DevOps:** [Contact]
- **Project Manager:** [Contact]

---

## Status

- [ ] All checks passed
- [ ] Ready for deployment
- [ ] Deployment successful
- [ ] Post-deployment verified

**Deployment Date:** ___________  
**Deployed By:** ___________  
**Version:** v3.5.1  
**Status:** ___________

---

**Good luck with deployment! 🚀**
