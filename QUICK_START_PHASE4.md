# Quick Start Guide - Phase 4 CRUD Features
**Premium Todo App - Full CRUD Implementation**

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL database (Neon or local)

---

## 1. Start Backend API

```bash
# Navigate to backend directory
cd /mnt/f/Maryam/Quarter_4/hackathon2-todo-app/backend

# Activate virtual environment (if using)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies (if not already done)
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your_neon_database_url"
export SECRET_KEY="your_secret_key_at_least_32_chars"

# Run the API server
python -m app.main
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify**: Open http://localhost:8000/docs to see API documentation

---

## 2. Start Frontend Dev Server

```bash
# Open NEW terminal
# Navigate to frontend directory
cd /mnt/f/Maryam/Quarter_4/hackathon2-todo-app/frontend

# Install dependencies (if not already done)
npm install

# Set environment variables
# Create .env.local file:
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

**Expected Output**:
```
▲ Next.js 16.1.1 (Turbopack)
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000

✓ Ready in 2.5s
```

---

## 3. Access the Application

**URL**: http://localhost:3000

### First-Time Setup
1. **Welcome Page** → Click "Get Started"
2. **Sign Up** → Enter email, name, password
3. **Redirects to Dashboard** → See empty state

---

## 4. Test CRUD Features

### Create Tasks
1. Click the **blue FAB** (+ button) in bottom-right corner
2. Enter task details:
   - Title: "Buy groceries"
   - Description: "Milk, eggs, bread"
3. Click **Create Task**
4. ✅ Task appears immediately
5. ✅ Toast: "Task created successfully"

**Create 2-3 more tasks for testing**

---

### View Tasks
- All tasks display in reverse chronological order
- Each task shows:
  - Checkbox (left)
  - Title and description preview
  - Date created
  - Edit/Delete buttons (on hover)

---

### Complete Tasks
1. Click **checkbox** on any task
2. ✅ Strikethrough animation
3. ✅ Text turns gray
4. ✅ Toast: "Task completed!"

**Uncheck** to reopen:
- ✅ Strikethrough removed
- ✅ Toast: "Task reopened"

---

### Edit Tasks
1. **Hover** on task → Edit button (pencil icon) appears
2. Click **Edit**
3. Modal opens with pre-filled data
4. Modify title or description
5. Click **Update Task**
6. ✅ Changes appear immediately
7. ✅ Toast: "Task updated successfully"

---

### Delete Tasks
1. **Hover** on task → Delete button (trash icon) appears
2. Click **Delete**
3. Confirmation dialog appears
4. Click **Cancel** → Task remains
5. Click **Delete** again → Click **Delete** (red button)
6. ✅ Task removed immediately
7. ✅ Toast: "Task deleted successfully"

---

## 5. Features Demo Sequence (2 minutes)

**Perfect for showing judges/stakeholders:**

```
1. Open app → Beautiful welcome page with gradient
   ⏱️ 5 seconds

2. Sign up → Quick form, instant redirect
   ⏱️ 15 seconds

3. Dashboard → See empty state with "Create Task" button
   ⏱️ 5 seconds

4. Click FAB → Modal opens, create first task
   Title: "Prepare presentation"
   ⏱️ 10 seconds

5. Create 2 more tasks quickly
   ⏱️ 15 seconds

6. Toggle first task complete → Show animation
   ⏱️ 5 seconds

7. Edit second task → Show pre-filled modal
   ⏱️ 10 seconds

8. Delete third task → Show confirmation dialog
   ⏱️ 10 seconds

9. Resize browser → Show responsive design
   Mobile, tablet, desktop
   ⏱️ 15 seconds

10. Highlight key features:
    - Optimistic updates (instant feedback)
    - Beautiful animations
    - Confirmation dialogs
    - Toast notifications
    ⏱️ 20 seconds

Total: ~2 minutes
```

---

## 6. Key Features to Highlight

### 🚀 Performance
- **Optimistic Updates**: All actions show immediately
- **SWR Caching**: Efficient data fetching
- **Instant Feedback**: No waiting for API responses

### 🎨 User Experience
- **Smooth Animations**: Strikethrough, fade-in, scale
- **Toast Notifications**: Clear success/error messages
- **Confirmation Dialogs**: Prevent accidental deletions
- **Loading States**: Clear feedback during operations

### 📱 Responsive Design
- **Mobile-First**: Works perfectly on all devices
- **Large Touch Targets**: 56x56px FAB, accessible buttons
- **Adaptive Layout**: Grid system adjusts to screen size

### ♿ Accessibility
- **ARIA Labels**: Screen reader friendly
- **Keyboard Navigation**: Full keyboard support
- **Color Contrast**: WCAG AA compliant
- **Focus Management**: Proper focus handling in modals

### 🔒 Security
- **JWT Authentication**: Secure token-based auth
- **User Isolation**: Each user sees only their tasks
- **Input Validation**: Zod schema validation
- **XSS Prevention**: React's built-in protection

---

## 7. Component Architecture

```
frontend/src/
├── app/
│   ├── dashboard/
│   │   ├── layout.tsx          # Protected route layout
│   │   └── page.tsx            # Main dashboard with CRUD
│   ├── sign-in/page.tsx
│   ├── sign-up/page.tsx
│   └── page.tsx                # Welcome page
├── components/
│   ├── dashboard/
│   │   ├── AddTaskButton.tsx   # 🆕 FAB for creating tasks
│   │   ├── TaskModal.tsx       # 🆕 Create/Edit modal
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── EmptyState.tsx
│   │   └── DashboardHeader.tsx
│   ├── shared/
│   │   ├── ConfirmationDialog.tsx  # 🆕 Delete confirmation
│   │   └── TaskListSkeleton.tsx
│   └── ui/                     # shadcn/ui components
│       ├── dialog.tsx
│       ├── alert-dialog.tsx    # 🆕 Added in Phase 4
│       ├── button.tsx
│       ├── input.tsx
│       ├── checkbox.tsx
│       └── ...
├── hooks/
│   ├── useTasks.ts            # SWR + optimistic updates
│   └── useAuth.ts
├── lib/
│   ├── api.ts                 # API client
│   ├── types.ts               # TypeScript types
│   └── validations.ts         # Zod schemas
└── ...
```

---

## 8. API Endpoints Used

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login

### Tasks (all require JWT)
- `GET /api/users/{user_id}/tasks` - List user tasks
- `POST /api/users/{user_id}/tasks` - Create task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete task
- `POST /api/users/{user_id}/tasks/{task_id}/toggle` - Toggle complete

---

## 9. Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI primitives)
- **Forms**: React Hook Form + Zod
- **Data Fetching**: SWR (optimistic updates)
- **Icons**: Lucide React
- **Notifications**: Sonner (toast)
- **Animations**: Motion (framer-motion successor)

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: JWT tokens
- **Validation**: Pydantic

---

## 10. Troubleshooting

### Issue: "Failed to fetch tasks"
**Solution**:
1. Check backend is running (http://localhost:8000/docs)
2. Verify DATABASE_URL is set correctly
3. Check CORS settings in backend

### Issue: "Token expired" or auth errors
**Solution**:
1. Clear browser localStorage
2. Sign in again
3. Check SECRET_KEY matches between backend and frontend

### Issue: Modal doesn't open
**Solution**:
1. Check browser console for errors
2. Verify shadcn/ui dialog component installed
3. Check React version compatibility

### Issue: Validation not working
**Solution**:
1. Verify Zod schema imported
2. Check zodResolver in useForm hook
3. Console log form errors

### Issue: Optimistic update not showing
**Solution**:
1. Check SWR key matches in useTasks hook
2. Verify mutate() called before API call
3. Check task data structure matches type

---

## 11. Build for Production

```bash
# Frontend
cd frontend
npm run build
npm start

# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 12. Next Steps

### Phase 5 (Optional Polish)
- [ ] Add confetti animation on first task completion
- [ ] Enhance micro-interactions (hover states)
- [ ] Add session expiry handling
- [ ] Final responsive design QA
- [ ] Performance optimization

### Deployment
- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Configure production environment variables
- [ ] Set up custom domain

---

## 13. Documentation

### For Developers
- **Spec**: `/specs/002-todo-frontend-ui/spec.md`
- **Plan**: `/specs/002-todo-frontend-ui/plan.md`
- **Tasks**: `/specs/002-todo-frontend-ui/tasks.md`
- **Completion Report**: `/specs/002-todo-frontend-ui/PHASE4_COMPLETION_REPORT.md`
- **Visual Test Guide**: `/specs/002-todo-frontend-ui/VISUAL_TEST_GUIDE.md`

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

---

## Success Indicators

✅ **Backend running** on port 8000
✅ **Frontend running** on port 3000
✅ **Can sign up** and create account
✅ **Can create tasks** with FAB
✅ **Can edit tasks** with pre-filled modal
✅ **Can delete tasks** with confirmation
✅ **Can toggle completion** with animation
✅ **Optimistic updates** work smoothly
✅ **Toast notifications** appear for all actions
✅ **Responsive design** works on mobile/tablet/desktop

---

**Estimated Setup Time**: 5 minutes
**Full Demo Time**: 2 minutes
**Status**: ✅ MVP Complete - Ready for Demo!

For issues or questions, check:
1. Console logs (browser DevTools)
2. API logs (backend terminal)
3. Network tab (failed requests)
4. Documentation in /specs folder
