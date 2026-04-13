---
name: frontend
description: >
  Use this skill whenever building, reviewing, or debugging frontend web applications,
  UI components, or web interfaces. Triggers include any mention of HTML, CSS, JavaScript,
  TypeScript, React, Vue, Svelte, Angular, Tailwind CSS, responsive design, accessibility,
  web performance, Core Web Vitals, component architecture, state management, or frontend
  testing. Also use when the user asks to "build a website", "create a UI", "make it responsive",
  "improve accessibility", "optimize performance", or any web frontend work. This skill covers
  modern frontend development fundamentals: semantic HTML, CSS architecture, TypeScript,
  component patterns, accessibility (WCAG 2.2), performance optimization, responsive design,
  state management, testing, and build tooling for 2025–2026.
---

# Frontend Skill — Modern Frontend Development (2025–2026)

This skill covers the fundamentals and advanced patterns of frontend web development that apply across frameworks. For framework-specific guidance (Next.js, etc.), combine this with the relevant framework skill.

---

## 1. HTML: Semantic & Accessible by Default

Semantic HTML is the foundation of accessible, SEO-friendly, and maintainable interfaces.

### Use the right element for the job

```html
<!-- ✅ Semantic -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h1>Article Title</h1>
    <time datetime="2026-04-10">April 10, 2026</time>
    <p>Content...</p>
  </article>
  <aside aria-label="Related articles">...</aside>
</main>
<footer>...</footer>

<!-- ❌ Div soup -->
<div class="header">
  <div class="nav">
    <div class="link" onclick="goto('/about')">About</div>
  </div>
</div>
```

### Semantic element quick reference

| Element     | Use for                                     |
|:------------|:--------------------------------------------|
| `<header>`  | Introductory content, navigation            |
| `<nav>`     | Major navigation blocks                     |
| `<main>`    | Primary content (one per page)              |
| `<article>` | Self-contained, redistributable content     |
| `<section>` | Thematic grouping with a heading            |
| `<aside>`   | Tangentially related content                |
| `<footer>`  | Footer content, metadata                    |
| `<figure>`  | Self-contained media with `<figcaption>`    |
| `<time>`    | Machine-readable dates/times                |
| `<dialog>`  | Modal/non-modal dialogs (native)            |
| `<details>` | Disclosure widget (accordion)               |

### Head essentials

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Clear, concise page description" />
  <title>Page Title — Site Name</title>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="canonical" href="https://example.com/page" />
</head>
```

---

## 2. CSS Architecture

### Modern layout: Grid + Flexbox

Use CSS Grid for two-dimensional layouts and Flexbox for one-dimensional alignment.

```css
/* Grid for page layout */
.page {
  display: grid;
  grid-template-columns: 1fr min(65ch, 100%) 1fr;
  gap: var(--space-lg);
}
.page > * { grid-column: 2; }
.page > .full-bleed { grid-column: 1 / -1; }

/* Flexbox for component-level alignment */
.card-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
}
```

### Design tokens via CSS custom properties

```css
:root {
  /* Colors */
  --color-primary: oklch(55% 0.2 260);
  --color-surface: oklch(98% 0.005 260);
  --color-text: oklch(20% 0.02 260);
  --color-text-muted: oklch(45% 0.02 260);
  --color-border: oklch(85% 0.01 260);

  /* Spacing scale (based on 4px grid) */
  --space-xs: 0.25rem;    /* 4px */
  --space-sm: 0.5rem;     /* 8px */
  --space-md: 1rem;       /* 16px */
  --space-lg: 1.5rem;     /* 24px */
  --space-xl: 2rem;       /* 32px */
  --space-2xl: 3rem;      /* 48px */

  /* Typography */
  --font-body: 'Inter', system-ui, sans-serif;
  --font-heading: 'Plus Jakarta Sans', var(--font-body);
  --font-mono: 'JetBrains Mono', monospace;

  /* Fluid type scale */
  --text-sm: clamp(0.8rem, 0.75rem + 0.25vw, 0.875rem);
  --text-base: clamp(1rem, 0.93rem + 0.35vw, 1.125rem);
  --text-lg: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-xl: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem);
  --text-2xl: clamp(2rem, 1.5rem + 2.5vw, 3.5rem);

  /* Shadows */
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0% 0 0 / 0.07);
  --shadow-lg: 0 10px 25px oklch(0% 0 0 / 0.1);

  /* Transitions */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 150ms;
  --duration-normal: 250ms;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: oklch(72% 0.18 260);
    --color-surface: oklch(15% 0.01 260);
    --color-text: oklch(90% 0.01 260);
    --color-text-muted: oklch(65% 0.01 260);
    --color-border: oklch(30% 0.01 260);
  }
}
```

### Container queries (2026 standard)

```css
.card-container { container-type: inline-size; }

@container (min-width: 400px) {
  .card { flex-direction: row; }
}
@container (max-width: 399px) {
  .card { flex-direction: column; }
}
```

Container queries let components adapt to their parent's size rather than the viewport — critical for truly reusable components.

### CSS layers for specificity control

```css
@layer base, components, utilities;

@layer base {
  h1 { font-size: var(--text-2xl); }
}

@layer components {
  .btn { padding: var(--space-sm) var(--space-md); }
}

@layer utilities {
  .sr-only {
    position: absolute;
    width: 1px; height: 1px;
    clip: rect(0, 0, 0, 0);
    overflow: hidden;
  }
}
```

---

## 3. Responsive Design

### Mobile-first approach

```css
/* Base styles = mobile */
.grid { display: grid; gap: var(--space-md); }

/* Tablet */
@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}

/* Large screens */
@media (min-width: 1440px) {
  .grid { grid-template-columns: repeat(4, 1fr); }
}
```

### Fluid typography (no breakpoints needed)

```css
h1 { font-size: clamp(2rem, 1.5rem + 2.5vw, 3.5rem); }
```

### Other responsive patterns

- Use `min()`, `max()`, `clamp()` for fluid sizing without breakpoints.
- Use `aspect-ratio` for media containers.
- Test on real devices or throttled network — DevTools alone is insufficient.
- Ensure touch targets are at least 44×44px.

---

## 4. Accessibility (WCAG 2.2)

Accessibility is not optional — it's a legal requirement in many jurisdictions and a moral imperative.

### Core requirements

**Perceivable:**
- Color contrast: 4.5:1 for body text, 3:1 for large text (AA).
- All images have meaningful `alt` text (or `alt=""` for decorative).
- Don't rely on color alone to convey information.
- Support `prefers-reduced-motion` and `prefers-color-scheme`.

**Operable:**
- All interactive elements reachable and usable via keyboard.
- Visible focus indicators on all focusable elements (never `outline: none` without replacement).
- Skip-to-content link as the first focusable element.
- No keyboard traps — users can always Tab away.

**Understandable:**
- Use clear, consistent labels for form inputs (`<label>` linked to `<input>`).
- Provide error messages inline, associated with the field via `aria-describedby`.
- Use `aria-live` regions for dynamic content updates.

**Robust:**
- Valid HTML (use semantic elements over ARIA where possible).
- Test with screen readers (VoiceOver, NVDA).
- Test keyboard-only navigation end-to-end.

### Focus management

```css
/* Visible focus ring */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove default outline only for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### ARIA patterns

```html
<!-- Accessible modal -->
<dialog aria-labelledby="modal-title" aria-modal="true">
  <h2 id="modal-title">Confirm Action</h2>
  <p>Are you sure?</p>
  <button autofocus>Confirm</button>
  <button>Cancel</button>
</dialog>

<!-- Live region for notifications -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <!-- Inject status messages here -->
</div>

<!-- Accessible loading state -->
<div aria-busy="true" aria-label="Loading content">
  <span class="spinner" />
</div>
```

### Forms

```html
<form novalidate>
  <div class="field">
    <label for="email">Email address</label>
    <input
      id="email"
      type="email"
      required
      aria-describedby="email-error"
      aria-invalid="false"
    />
    <p id="email-error" role="alert" class="error" hidden>
      Please enter a valid email address.
    </p>
  </div>
</form>
```

---

## 5. TypeScript

TypeScript is the industry standard for any non-trivial frontend project in 2026.

### Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "noUncheckedIndexedAccess": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

### Key patterns

```typescript
// Discriminated unions for state
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// Exhaustive switch
function render<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'idle': return <Placeholder />;
    case 'loading': return <Spinner />;
    case 'success': return <Data data={state.data} />;
    case 'error': return <ErrorDisplay error={state.error} />;
  }
}

// Utility types
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Component props
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}
```

---

## 6. Component Architecture (React-centric, principles apply broadly)

### Component organization

```
src/components/
├── ui/                     # Primitives (Button, Input, Card, Modal)
│   ├── Button.tsx
│   ├── Button.test.tsx
│   └── index.ts           # Barrel export
├── features/               # Business logic components
│   ├── UserProfile/
│   │   ├── UserProfile.tsx
│   │   ├── UserAvatar.tsx
│   │   └── index.ts
│   └── Dashboard/
│       ├── Dashboard.tsx
│       ├── MetricsCard.tsx
│       └── index.ts
└── layouts/                # Page layouts
    ├── AppLayout.tsx
    └── AuthLayout.tsx
```

### Component design principles

1. **Single responsibility**: Each component does one thing well.
2. **Props down, events up**: Data flows down via props; actions flow up via callbacks.
3. **Composition over configuration**: Prefer composable children over massive prop APIs.
4. **Controlled vs uncontrolled**: Default to controlled components for form inputs.
5. **Co-location**: Keep styles, tests, and types next to the component they belong to.

### Custom hooks for logic reuse

```typescript
// src/hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}
```

---

## 7. State Management

### Decision tree

1. **Local UI state** (toggle, form input, modal open) → `useState` / `useReducer`
2. **Server state** (API data, caching, revalidation) → TanStack Query (React Query) or SWR
3. **Shared client state** (theme, auth, cart) → React Context or Zustand
4. **Complex global state** (large app, time-travel debugging) → Zustand or Redux Toolkit

### Server state with TanStack Query

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateUserInput) =>
      fetch('/api/users', { method: 'POST', body: JSON.stringify(data) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
}
```

### Lightweight global state with Zustand

```typescript
import { create } from 'zustand';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clear: () => void;
}

const useCart = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((s) => ({ items: [...s.items, item] })),
  removeItem: (id) => set((s) => ({ items: s.items.filter(i => i.id !== id) })),
  clear: () => set({ items: [] }),
}));
```

---

## 8. Performance Optimization

### Core Web Vitals targets

| Metric | Good | Measures |
|:-------|:-----|:---------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | Loading performance |
| INP (Interaction to Next Paint) | ≤ 200ms | Responsiveness |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | Visual stability |

### Key optimization techniques

**Reduce JavaScript:**
- Code-split by route (frameworks do this automatically).
- Lazy-load below-the-fold components with `React.lazy()` + `Suspense`.
- Audit bundle size with tools like `bundlephobia` and bundle analyzers.
- Set a performance budget: ≤400KB gzipped JS total.

**Optimize images:**
- Use modern formats: WebP or AVIF.
- Serve responsive images with `srcset` and `sizes`.
- Lazy-load below-the-fold images (`loading="lazy"`).
- Set explicit `width` and `height` to prevent layout shift.
- Use framework image components (e.g., `next/image`) when available.

**Optimize fonts:**
- Self-host fonts or use framework-level font optimization.
- Use `font-display: swap` to prevent invisible text.
- Subset fonts to include only needed characters.
- Preload critical fonts: `<link rel="preload" as="font" crossorigin>`.

**Reduce CSS:**
- Inline critical CSS or use framework-level extraction.
- Purge unused CSS (Tailwind does this by default).
- Use `content-visibility: auto` for off-screen sections.

**Network:**
- Preconnect to required origins: `<link rel="preconnect">`.
- Use HTTP/2 or HTTP/3 for multiplexing.
- Set proper cache headers for static assets.
- Use a CDN for static assets.

### Measuring performance

- **Lab testing**: Lighthouse, WebPageTest, Chrome DevTools Performance tab.
- **Field data (RUM)**: Chrome UX Report (CrUX), Vercel Analytics, or custom RUM.
- Test on real devices, especially mid-range Android phones on 3G/4G.

---

## 9. Security

### Frontend security essentials

- **Content Security Policy (CSP)**: Restrict script/style sources to prevent XSS.
- **Never store secrets in frontend code** — including API keys in environment variables prefixed for client exposure.
- **Sanitize user-generated HTML** before rendering. Use DOMPurify or equivalent.
- **CSRF protection**: Use `SameSite=Lax` or `Strict` cookies + anti-CSRF tokens for mutations.
- **Subresource Integrity (SRI)**: Add `integrity` attributes for CDN scripts.
- **HTTPS everywhere**: No exceptions.
- **Input validation**: Validate on both client (for UX) and server (for security). Client-side validation is never a security boundary.

---

## 10. Testing Strategy

### Testing pyramid

1. **Unit tests** (many): Individual functions, hooks, utilities.
2. **Component tests** (moderate): Render components, test behavior and output.
3. **Integration tests** (some): Test feature workflows with mocked APIs.
4. **E2E tests** (few): Full user flows in a real browser.

### Tools

| Layer | Tool |
|:------|:-----|
| Unit + Component | Vitest + React Testing Library |
| E2E | Playwright (preferred) or Cypress |
| Visual regression | Chromatic / Percy |
| Accessibility | axe-core, jest-axe, Lighthouse CI |

### Testing philosophy

```typescript
// ✅ Test behavior, not implementation
test('shows error when email is invalid', async () => {
  render(<SignupForm />);
  await userEvent.type(screen.getByLabelText('Email'), 'not-an-email');
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }));
  expect(screen.getByRole('alert')).toHaveTextContent('valid email');
});

// ❌ Don't test implementation details
test('sets emailError state', () => {
  // Testing internal state is brittle and couples tests to implementation
});
```

---

## 11. Build Tooling (2026)

| Tool | Purpose |
|:-----|:--------|
| **Vite** | Dev server + bundler (fast HMR, Rollup-based production builds) |
| **Turbopack** | Next.js dev bundler (Rust-based, replacing Webpack) |
| **esbuild** | Ultra-fast JS/TS transpilation |
| **Biome** | Linter + formatter (Rust-based, replaces ESLint + Prettier for speed) |
| **ESLint + Prettier** | Still widely used; Biome is the modern alternative |
| **Tailwind CSS** | Utility-first CSS framework (v4 uses Rust engine) |
| **PostCSS** | CSS transforms (autoprefixer, nesting) |

### Package management

- **pnpm**: Fast, disk-efficient, strict dependency resolution. Recommended for monorepos.
- **npm**: The default. Good enough for most projects.
- **bun**: Fast JS runtime + package manager. Growing ecosystem.

---

## 12. Error Handling

### React error boundaries

```tsx
'use client';
import { Component, ErrorInfo, ReactNode } from 'react';

class ErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Report to error tracking service (Sentry, etc.)
    console.error('Caught by boundary:', error, info);
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}
```

### API error handling pattern

```typescript
class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiError(response.status, body.detail || 'Request failed');
  }

  return response.json();
}
```

---

## 13. Internationalization (i18n)

For multi-language apps:
- Use established libraries: `next-intl` (Next.js), `react-i18next`, or `@formatjs/intl`.
- Store translations in structured JSON files per locale.
- Use ICU message syntax for plurals, gender, and interpolation.
- Set `lang` attribute on `<html>`.
- Use `dir="rtl"` for right-to-left languages.
- Format dates, numbers, and currencies with `Intl` APIs.

---

## 14. Common Pitfalls

| Pitfall | Fix |
|:--------|:----|
| Div soup with click handlers | Use semantic HTML (`<button>`, `<a>`, `<nav>`) |
| `outline: none` with no replacement | Use `:focus-visible` for visible focus rings |
| Images without `width`/`height` | Always set dimensions to prevent CLS |
| Testing implementation details | Test user-visible behavior instead |
| Giant monolithic components | Split into small, composable pieces |
| Client-side validation as security | Always validate on the server too |
| Ignoring `prefers-reduced-motion` | Wrap animations in `@media (prefers-reduced-motion: no-preference)` |
| Using `px` for everything | Use `rem` for text, `em` for component spacing, `px` for borders |
| No loading/error states | Always handle idle, loading, success, and error states |
| Bundling entire libraries | Import only what you need; use tree-shakeable packages |
