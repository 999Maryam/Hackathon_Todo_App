---
name: frontend-page-builder
description: Build complete frontend pages using reusable components, responsive layouts, and modern styling practices.
---

# Frontend Page & Component Builder

## Instructions

1. **Page structure**
   - Semantic HTML layout (`header`, `main`, `section`, `footer`)
   - Clear content hierarchy
   - Reusable page sections

2. **Component design**
   - Modular UI components (buttons, cards, navbars)
   - Props-driven structure (where applicable)
   - Consistent spacing and typography

3. **Layout system**
   - Responsive grid or flexbox layout
   - Mobile-first breakpoints
   - Fluid containers and alignment

4. **Styling**
   - Utility-first or component-scoped styles
   - Theme-based colors and fonts
   - Hover, focus, and active states

5. **Responsiveness**
   - Mobile, tablet, and desktop support
   - Adaptive typography and spacing
   - Touch-friendly interactions

## Best Practices
- Use semantic HTML for accessibility
- Keep components small and reusable
- Follow a consistent naming convention
- Avoid hard-coded sizes; prefer relative units
- Ensure visual consistency across pages

## Example Structure
```html
<header class="site-header">
  <nav class="navbar">
    <div class="logo">Brand</div>
    <ul class="nav-links">
      <li>Home</li>
      <li>Features</li>
      <li>Contact</li>
    </ul>
  </nav>
</header>

<main class="page-layout">
  <section class="content-section">
    <h1 class="page-title">Page Title</h1>
    <p class="page-description">
      This section represents reusable, styled content.
    </p>
    <button class="primary-button">Action</button>
  </section>
</main>

<footer class="site-footer">
  <p>© 2026 Your Company</p>
</footer>
