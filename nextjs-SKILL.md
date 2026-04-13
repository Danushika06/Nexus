---
name: nextjs
description: >
  Use this skill whenever building, scaffolding, debugging, or reviewing Next.js applications.
  Triggers include any mention of Next.js, App Router, Server Components, Server Actions,
  React Server Components (RSC), next.config, Vercel deployment, or file-based routing.
  Also use when the user asks to build a full-stack React app, SSR/SSG/ISR application,
  or mentions pages like layout.tsx, page.tsx, loading.tsx, error.tsx, route.ts, or middleware.ts.
  Use this skill even if the user just says "build me a web app" and the context suggests Next.js,
  or when migrating from Pages Router to App Router. Covers Next.js 15+ with App Router patterns,
  React 19 Server Components, caching, streaming, and production deployment.
---

# Next.js Skill — Production Patterns for Next.js 15+

This skill covers building production-grade Next.js applications using the **App Router** (the default since Next.js 13, stable since 14, and the only recommended approach for new projects). The Pages Router is in maintenance mode — always default to App Router for new work.

---

## 1. Project Structure

Organize by **feature/domain**, not by file type. The App Router uses a file-system-based routing convention inside the `app/` directory.

```
my-app/
├── app/                    # App Router (routes + layouts)
│   ├── layout.tsx          # Root layout (required)
│   ├── page.tsx            # Home route (/)
│   ├── loading.tsx         # Root loading UI
│   ├── error.tsx           # Root error boundary
│   ├── not-found.tsx       # 404 page
│   ├── global-error.tsx    # Catches errors in root layout
│   ├── (auth)/             # Route group (no URL segment)
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/
│   │   ├── layout.tsx      # Nested layout for /dashboard/*
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   └── settings/page.tsx
│   └── api/
│       └── webhooks/route.ts  # API route handler
├── src/                    # Application source (non-route code)
│   ├── components/
│   │   ├── ui/             # Shared design-system components
│   │   └── features/       # Feature-specific components
│   ├── lib/                # Utilities, helpers, constants
│   ├── actions/            # Server Actions (grouped by domain)
│   ├── hooks/              # Custom React hooks
│   ├── types/              # Shared TypeScript types
│   └── styles/             # Global CSS / Tailwind config
├── public/                 # Static assets (served at /)
├── .env.local              # Local environment variables
├── next.config.ts          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── package.json
```

### Key file conventions inside `app/`

| File            | Purpose                                    |
|:----------------|:-------------------------------------------|
| `layout.tsx`    | Shared UI wrapper; persists across navigations within its scope |
| `page.tsx`      | Unique UI for a route; makes the route publicly accessible |
| `loading.tsx`   | Instant loading skeleton (wraps page in `<Suspense>`)  |
| `error.tsx`     | Error boundary for the route segment (`'use client'` required) |
| `not-found.tsx` | UI for `notFound()` calls                  |
| `route.ts`      | API endpoint (GET, POST, etc.) — no UI     |
| `template.tsx`  | Like layout but re-mounts on every navigation |
| `default.tsx`   | Fallback for parallel route slots           |

### Route groups and organization

- `(groupName)/` — Parenthesized folders create logical groups without affecting the URL.
- `[param]/` — Dynamic segments. `[...slug]/` for catch-all. `[[...slug]]/` for optional catch-all.
- `@slot/` — Parallel routes for rendering multiple pages simultaneously in one layout.
- `(.)segment` / `(..)segment` — Intercepting routes for modal patterns.

---

## 2. Server Components vs Client Components

**Server Components are the default.** Every component in the App Router is a Server Component unless you add `'use client'` at the top of the file.

### Server Components (default)

- Run only on the server. Ship zero JavaScript to the browser.
- Can directly access databases, file systems, environment variables, and secrets.
- Can `await` async operations directly in the component body.
- Cannot use `useState`, `useEffect`, `useRef`, event handlers, or browser APIs.

### Client Components (`'use client'`)

- Render on the server first (for HTML), then hydrate on the client.
- Can use hooks, event handlers, browser APIs.
- Should be as small and leaf-level as possible — "islands" of interactivity.

### The golden pattern: server-first with client islands

```tsx
// app/dashboard/page.tsx — Server Component (default)
import { getMetrics } from '@/lib/data';
import InteractiveChart from '@/components/features/InteractiveChart';

export default async function DashboardPage() {
  const metrics = await getMetrics(); // Direct DB/API call on server

  return (
    <main>
      <h1>Dashboard</h1>
      {/* Pass server-fetched data DOWN to a client island */}
      <InteractiveChart data={metrics} />
    </main>
  );
}
```

```tsx
// src/components/features/InteractiveChart.tsx
'use client';
import { useState } from 'react';

export default function InteractiveChart({ data }: { data: Metric[] }) {
  const [filter, setFilter] = useState('all');
  // Client-side interactivity here
  return <div>...</div>;
}
```

### Composition pattern for context providers

Wrap client providers around server children using the `children` prop:

```tsx
// src/components/providers.tsx
'use client';
import { ThemeProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  return <ThemeProvider attribute="class">{children}</ThemeProvider>;
}

// app/layout.tsx — Server Component
import { Providers } from '@/components/providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

## 3. Data Fetching

In the App Router, data fetching happens **on the server by default** — no `getServerSideProps` or `getStaticProps`.

### Fetch in Server Components

```tsx
// Fetch with time-based revalidation
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 60, tags: ['products'] },
  });
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}
```

### Direct database access

```tsx
import { db } from '@/lib/db';

export default async function UsersPage() {
  const users = await db.user.findMany({ take: 20 });
  return <UserList users={users} />;
}
```

### Parallel data fetching (avoid waterfalls)

```tsx
export default async function DashboardPage() {
  // Fire all requests simultaneously
  const [users, revenue, orders] = await Promise.all([
    getUsers(),
    getRevenue(),
    getRecentOrders(),
  ]);
  return <Dashboard users={users} revenue={revenue} orders={orders} />;
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <main>
      <h1>Dashboard</h1>
      <Suspense fallback={<RevenueCardSkeleton />}>
        <RevenueCard />  {/* Streams in when data resolves */}
      </Suspense>
      <Suspense fallback={<OrdersTableSkeleton />}>
        <OrdersTable />
      </Suspense>
    </main>
  );
}
```

---

## 4. Server Actions

Server Actions replace many traditional API routes. They are async functions marked with `'use server'` that execute on the server and can be called from forms or client code.

### Defining and using Server Actions

```tsx
// src/actions/todo.ts
'use server';

import { revalidatePath } from 'next/cache';
import { db } from '@/lib/db';
import { z } from 'zod';

const CreateTodoSchema = z.object({
  title: z.string().min(1).max(200),
});

export async function createTodo(formData: FormData) {
  const parsed = CreateTodoSchema.safeParse({
    title: formData.get('title'),
  });

  if (!parsed.success) {
    return { error: 'Invalid input' };
  }

  await db.todo.create({ data: { title: parsed.data.title } });
  revalidatePath('/todos');
}
```

```tsx
// app/todos/page.tsx — Server Component
import { createTodo } from '@/actions/todo';

export default function TodosPage() {
  return (
    <form action={createTodo}>
      <input name="title" placeholder="New todo..." />
      <button type="submit">Add</button>
    </form>
  );
}
```

### Security rules for Server Actions

- Always validate inputs with Zod or similar inside each action.
- Always check authentication and authorization inside the action body.
- Never trust that layout-level or middleware-level auth checks are sufficient — actions are callable endpoints.
- Use `revalidatePath()` or `revalidateTag()` for surgical cache invalidation after mutations.

---

## 5. Caching Strategy

Next.js 15 changed caching defaults: **GET Route Handlers and client navigations are no longer cached by default.**

### Cache invalidation patterns

```tsx
import { revalidateTag, revalidatePath } from 'next/cache';

// Tag-based: invalidate all fetches tagged 'products'
revalidateTag('products');

// Path-based: revalidate a specific route
revalidatePath('/products');
revalidatePath('/products/[id]', 'page');
```

### For non-fetch data (e.g., direct DB calls)

```tsx
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (userId: string) => db.user.findUnique({ where: { id: userId } }),
  ['user'],
  { revalidate: 300, tags: ['users'] }
);
```

### Static vs Dynamic rendering

- Static by default when no dynamic functions are used (`cookies()`, `headers()`, `searchParams`).
- Force static: `export const dynamic = 'force-static'`
- Force dynamic: `export const dynamic = 'force-dynamic'`

---

## 6. Async APIs (Breaking Change in Next.js 15)

Dynamic route parameters (`params`) and search parameters (`searchParams`) are now **Promises** in Next.js 15. You must `await` them:

```tsx
// CORRECT in Next.js 15+
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const product = await getProduct(id);
  return <ProductDetail product={product} />;
}
```

Similarly, `cookies()` and `headers()` are now async:

```tsx
import { cookies } from 'next/headers';

export default async function Page() {
  const cookieStore = await cookies();
  const theme = cookieStore.get('theme');
  // ...
}
```

---

## 7. Middleware

Middleware runs at the edge **before every request**. Keep it lightweight — no heavy computation or database calls.

```tsx
// middleware.ts (root of project)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

Best uses: auth guards, redirects, A/B testing, geolocation routing, header manipulation.  
Avoid: database queries, heavy computation (use Server Components or API routes instead).

---

## 8. Metadata & SEO

Use the Metadata API for SEO. It works at the layout or page level.

```tsx
// Static metadata
export const metadata: Metadata = {
  title: 'My App',
  description: 'A production-grade Next.js application',
  openGraph: { title: 'My App', description: '...', images: ['/og.png'] },
};

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params;
  const product = await getProduct(id);
  return {
    title: product.name,
    description: product.description,
  };
}
```

Generate sitemaps and robots.txt using `app/sitemap.ts` and `app/robots.ts`.

---

## 9. Error Handling

```tsx
// app/dashboard/error.tsx — MUST be a client component
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

- `error.tsx` catches errors within its route segment and its children.
- `global-error.tsx` (in `app/`) catches errors in the root layout itself.
- `not-found.tsx` handles `notFound()` calls.
- `loading.tsx` provides instant skeleton UIs via automatic `<Suspense>`.

---

## 10. Image & Font Optimization

```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={630}
  priority           // For above-the-fold images
  placeholder="blur" // If using imported static images
/>
```

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

---

## 11. Environment Variables

- `.env.local` — local secrets (gitignored)
- Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.
- Server-only secrets (DB URLs, API keys) must NOT have the `NEXT_PUBLIC_` prefix.
- Validate env vars at build time using `@t3-oss/env-nextjs` or a Zod schema.

---

## 12. TypeScript Best Practices

- Always use TypeScript. Next.js has first-class TS support.
- Enable `strict: true` in `tsconfig.json`.
- Type Server Action return values explicitly.
- Use `satisfies` for metadata objects and route configs.
- Prefer Zod for runtime validation at API/action boundaries.

---

## 13. Testing

- **Unit tests**: Vitest or Jest + React Testing Library for component logic.
- **Integration tests**: Test Server Components by testing their output, not their internals.
- **E2E tests**: Playwright or Cypress for full user-flow testing.
- **API Route tests**: Use `next/test` utilities or direct handler testing.

---

## 14. Production Checklist

Before deploying:
1. Run `next build` and check for warnings.
2. Verify all `NEXT_PUBLIC_` variables are safe for the browser.
3. Enable Content Security Policy headers.
4. Add `loading.tsx` and `error.tsx` to critical routes.
5. Use `<Image>` for all images (automatic optimization).
6. Use `next/font` for all fonts (no layout shift).
7. Set up OG images via `opengraph-image.tsx`.
8. Generate `sitemap.ts` and `robots.ts`.
9. Review bundle size with `@next/bundle-analyzer`.
10. Test on real devices/networks with throttled connections.

---

## 15. Common Pitfalls

| Pitfall | Fix |
|:--------|:----|
| Putting `'use client'` on everything | Default to Server Components; add `'use client'` only on interactive leaves |
| Not awaiting `params`/`searchParams` in Next.js 15 | They are Promises now — always `await` them |
| Blocking I/O in Server Components | Use `Promise.all()` for parallel fetches; wrap in `<Suspense>` |
| Relying on layout-level auth for Server Actions | Validate auth inside each Server Action individually |
| Using `localStorage`/`sessionStorage` for server data | Use cookies or server-side sessions instead |
| Huge Client Components | Break into smaller client islands; keep data fetching on the server |
| Ignoring `loading.tsx` | Add loading skeletons for perceived performance |
