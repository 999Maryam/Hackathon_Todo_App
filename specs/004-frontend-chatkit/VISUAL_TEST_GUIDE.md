# Visual Testing Guide - Phase 4 CRUD Features
**Quick verification checklist for Phase 4 implementation**

## Prerequisites
1. Backend API running on http://localhost:8000
2. Frontend dev server running: `cd frontend && npm run dev`
3. Browser open to http://localhost:3000

---

## Test Sequence (10 minutes)

### 1. Login/Signup
**Action**: Navigate to app, sign up or log in
**Expected**:
- ✅ Smooth redirect to /dashboard after auth
- ✅ See dashboard header with user avatar/initials
- ✅ See "My Tasks" heading

---

### 2. Floating Action Button (FAB)
**Visual Check**:
```
Location: Bottom-right corner
Size: Large circular button (56x56px)
Color: Primary blue
Icon: White plus (+) icon
```

**Interactions**:
- ✅ Hover → Button scales to 110% + shadow increases
- ✅ Click → Button scales to 95% (active state)
- ✅ FAB visible on all screen sizes (mobile, tablet, desktop)

**Screenshot**: FAB should look like this:
```
                                    [screen]



                                    [+]  ← Blue circle, bottom-right
```

---

### 3. Create Task Modal
**Action**: Click FAB

**Modal Appearance**:
```
┌─────────────────────────────────────┐
│ Create New Task                  [×]│
│ Add a new task to your list.        │
│                                     │
│ Title *                             │
│ ┌─────────────────────────────────┐ │
│ │ Enter task title...             │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Description (optional)              │
│ ┌─────────────────────────────────┐ │
│ │ Add details about this task...  │ │
│ │                                 │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│                    [Cancel] [Create]│
└─────────────────────────────────────┘
```

**Verify**:
- ✅ Modal centered on screen
- ✅ Background dimmed (overlay)
- ✅ Title has red asterisk (*)
- ✅ Description shows "(optional)"
- ✅ Create button is primary blue
- ✅ Focus on title input field

---

### 4. Form Validation
**Test Cases**:

#### a) Empty Title
**Action**: Click Create without entering anything
**Expected**:
- ✅ Red error text appears: "Title is required"
- ✅ Title input border turns red
- ✅ Form does NOT submit
- ✅ Modal stays open

#### b) Title Too Long
**Action**: Enter 201 characters in title
**Expected**:
- ✅ Error: "Title must be less than 200 characters"
- ✅ Red border on title input

#### c) Valid Task
**Action**:
1. Enter title: "Test task"
2. Enter description: "This is a test"
3. Click Create

**Expected**:
- ✅ Modal closes immediately
- ✅ Toast appears (top-right): "Task created successfully" (green)
- ✅ Task appears at TOP of list instantly (optimistic update)
- ✅ Task shows title and description preview

---

### 5. Task List Display
**After creating 3 tasks, verify**:

```
┌──────────────────────────────────────┐
│ ☐ Test task 3                    ⋮⋮  │  ← Hover shows edit/delete
│   This is a test                     │
│   Jan 11, 2026                       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ ☐ Test task 2                    ⋮⋮  │
│   Another test                       │
│   Jan 11, 2026                       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ ☐ Test task 1                    ⋮⋮  │
│   Jan 11, 2026                       │
└──────────────────────────────────────┘
```

**Verify**:
- ✅ Tasks in reverse chronological order (newest first)
- ✅ Staggered fade-in animation (each task appears with delay)
- ✅ Checkbox on left
- ✅ Edit/Delete buttons hidden initially
- ✅ Hover on task → card shadow increases
- ✅ Hover on task → edit/delete buttons fade in

---

### 6. Toggle Complete
**Action**: Click checkbox on first task

**Animation Sequence**:
1. ✅ Checkbox animates to checked state (smooth fill)
2. ✅ Title gets strikethrough
3. ✅ Description gets strikethrough
4. ✅ Text color changes to gray/muted
5. ✅ Toast: "Task completed!" (green)

**Visual**:
```
Before:
┌──────────────────────────────────────┐
│ ☐ Test task                      ⋮⋮  │
│   This is a test                     │
└──────────────────────────────────────┘

After:
┌──────────────────────────────────────┐
│ ☑ Test task                      ⋮⋮  │  ← Checked + strikethrough
│   This is a test                     │  ← Strikethrough + gray
└──────────────────────────────────────┘
```

**Action**: Click checkbox again
**Expected**:
- ✅ Checkbox unchecks
- ✅ Strikethrough removed
- ✅ Color restored to dark
- ✅ Toast: "Task reopened" (green)

---

### 7. Edit Task
**Action**:
1. Hover on task → Edit button (pencil icon) appears
2. Click Edit button

**Modal Appearance**:
```
┌─────────────────────────────────────┐
│ Edit Task                        [×]│
│ Update your task details below.     │
│                                     │
│ Title *                             │
│ ┌─────────────────────────────────┐ │
│ │ Test task                       │ │  ← PRE-FILLED
│ └─────────────────────────────────┘ │
│                                     │
│ Description (optional)              │
│ ┌─────────────────────────────────┐ │
│ │ This is a test                  │ │  ← PRE-FILLED
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│                    [Cancel] [Update]│
└─────────────────────────────────────┘
```

**Verify**:
- ✅ Title shows "Edit Task" (not "Create New Task")
- ✅ Button shows "Update Task" (not "Create Task")
- ✅ Title field pre-filled with existing title
- ✅ Description field pre-filled with existing description

**Action**:
1. Change title to "Updated task"
2. Change description to "Updated description"
3. Click Update Task

**Expected**:
- ✅ Modal closes
- ✅ Toast: "Task updated successfully" (green)
- ✅ Task title updates immediately (optimistic)
- ✅ Task description updates immediately

---

### 8. Delete Task with Confirmation
**Action**:
1. Hover on task → Delete button (trash icon) appears
2. Click Delete button

**Confirmation Dialog**:
```
┌─────────────────────────────────────┐
│ Delete Task                         │
│                                     │
│ Are you sure you want to delete     │
│ this task? This action cannot be    │
│ undone.                             │
│                                     │
│                    [Cancel] [Delete]│
└─────────────────────────────────────┘
```

**Verify**:
- ✅ Dialog centered with dark overlay
- ✅ Delete button is RED (destructive)
- ✅ Cancel button is gray/outline

**Action**: Click Cancel
**Expected**:
- ✅ Dialog closes
- ✅ Task still in list (not deleted)

**Action**:
1. Click Delete button again
2. Click Delete (red button) in confirmation

**Expected**:
- ✅ Dialog closes
- ✅ Toast: "Task deleted successfully" (green)
- ✅ Task removed from list immediately (optimistic)
- ✅ Remaining tasks reposition smoothly

---

### 9. Empty State (if all tasks deleted)
**Action**: Delete all tasks

**Expected Display**:
```
┌──────────────────────────────────────┐
│                                      │
│           [Illustration]             │  ← SVG or icon
│                                      │
│     No tasks yet!                    │  ← Large heading
│     Create your first task to        │
│     get started.                     │
│                                      │
│        [+ Create Task]               │  ← Primary button
│                                      │
└──────────────────────────────────────┘
```

**Verify**:
- ✅ Empty state shows when no tasks
- ✅ "Create Task" button opens modal
- ✅ FAB still visible in bottom-right

---

### 10. Responsive Design Tests

#### Mobile (320px - 480px)
**Action**: Resize browser to mobile width

**Verify**:
- ✅ FAB still visible and accessible (bottom-right)
- ✅ FAB is large enough to tap (56x56px minimum)
- ✅ Modal fits screen (no horizontal scroll)
- ✅ Form inputs are readable
- ✅ Task cards stack properly
- ✅ Edit/Delete buttons are accessible

#### Tablet (768px - 1024px)
**Verify**:
- ✅ Layout adjusts smoothly
- ✅ Task cards maintain readable width
- ✅ Modal centered and sized appropriately

#### Desktop (1920px)
**Verify**:
- ✅ Content max-width prevents excessive stretching
- ✅ FAB stays in bottom-right (not center)
- ✅ Spacing looks balanced

---

### 11. Loading States

#### Button Loading
**Action**: Slow network simulation
1. Open DevTools → Network tab
2. Throttle to "Slow 3G"
3. Create/Edit/Delete task

**Expected**:
- ✅ Create button text: "Creating..." (with disabled state)
- ✅ Update button text: "Updating..." (with disabled state)
- ✅ Optimistic update still shows immediately
- ✅ Button re-enables after API response

---

### 12. Keyboard Navigation
**Test**: Navigate with keyboard only (no mouse)

1. **Tab** to FAB → **Enter** to open modal
   - ✅ Modal opens, focus on title input

2. Type title → **Tab** to description → Type description
   - ✅ Tab moves between fields

3. **Tab** to Create button → **Enter** to submit
   - ✅ Task created

4. **Tab** through task checkboxes
   - ✅ Can toggle with **Space** key

5. **Tab** to Edit button → **Enter** to open
   - ✅ Modal opens

6. **Esc** to close modal
   - ✅ Modal closes, focus returns to trigger

---

### 13. Error Handling

#### Network Error Simulation
**Action**:
1. Stop backend API server
2. Try to create a task

**Expected**:
- ✅ Optimistic update shows task briefly
- ✅ Error toast appears: "Failed to create task" (red)
- ✅ Task removed from list (rollback)

**Action**:
1. Restart backend
2. Create task again

**Expected**:
- ✅ Works normally

---

### 14. Dark Mode (if implemented)
**Action**: Toggle dark mode in OS/browser

**Verify**:
- ✅ All modals have dark backgrounds
- ✅ Text remains readable (proper contrast)
- ✅ FAB visible against dark background
- ✅ Confirmation dialog styled for dark mode

---

## Quick Pass/Fail Checklist

### Create Flow
- [ ] FAB visible and clickable
- [ ] Modal opens with empty form
- [ ] Validation works (empty title shows error)
- [ ] Valid task creates successfully
- [ ] Task appears in list immediately
- [ ] Toast notification shows
- [ ] Modal closes after creation

### Edit Flow
- [ ] Edit button appears on hover
- [ ] Modal opens with pre-filled data
- [ ] Changes save successfully
- [ ] Updates appear immediately
- [ ] Toast notification shows

### Delete Flow
- [ ] Delete button appears on hover
- [ ] Confirmation dialog shows
- [ ] Cancel works (task remains)
- [ ] Confirm deletes task
- [ ] Task removed immediately
- [ ] Toast notification shows

### Toggle Flow
- [ ] Checkbox toggles smoothly
- [ ] Strikethrough animation works
- [ ] Color changes appropriately
- [ ] Toast notification shows

### Responsive
- [ ] Works on mobile (320px)
- [ ] Works on tablet (768px)
- [ ] Works on desktop (1920px)
- [ ] Touch targets large enough on mobile

### Accessibility
- [ ] Keyboard navigation works
- [ ] ARIA labels present
- [ ] Focus management correct
- [ ] Color contrast sufficient

---

## Common Issues & Fixes

### Issue: Modal doesn't open
**Check**: Console for errors, verify state management

### Issue: Form doesn't validate
**Check**: Zod schema imported, zodResolver configured

### Issue: Optimistic update doesn't show
**Check**: SWR mutate called, swrKey correct

### Issue: FAB not visible
**Check**: z-index (should be 50), position fixed, bottom/right values

### Issue: Tasks don't appear
**Check**: Backend running, API endpoint correct, JWT token valid

---

## Success Criteria
✅ All create/edit/delete operations work smoothly
✅ Optimistic updates provide instant feedback
✅ Validation prevents invalid data
✅ Confirmations prevent accidental deletions
✅ Animations are smooth and delightful
✅ Responsive design works across devices
✅ Keyboard navigation is fully functional
✅ Error handling is graceful

---

**Testing Duration**: ~10 minutes for full pass
**Next**: Demo to stakeholders or proceed to Phase 5 polish
