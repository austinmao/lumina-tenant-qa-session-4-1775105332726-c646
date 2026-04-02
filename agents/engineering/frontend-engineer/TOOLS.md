# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Skills I Use

| Skill | Trigger | Purpose |
|---|---|---|
| `email-design-system` | any email template work | Tenant email tokens + React Email patterns |
| `marketing/email-sequences` | email campaign sequences | Campaign copy + structure |
| `resend/log-to-attio` | after sending any email | Log send to Attio CRM |

## Project Paths

- **Email templates:** `templates/email/` (onboarding/, marketing/, sales/)
- **Render script:** `templates/email/render.ts`
- **Brand logos:** `assets/brand/logos/`
- **Brand guide:** `brands/<tenant>/brand-guide.md` (active tenant)
- **Design tokens:** see `skills/email-design-system/SKILL.md` → Design Tokens section

## Dev Commands

```bash
# Email template development
cd templates/email && pnpm dev        # start preview server
cd templates/email && pnpm build      # build all templates

# Next.js app (if applicable)
pnpm dev                              # start dev server
pnpm build && pnpm start              # production build check
pnpm lint                             # ESLint
pnpm type-check                       # tsc --noEmit
```

## shadcn/ui Component Registry

When adding a new shadcn component:
```bash
pnpm dlx shadcn@latest add <component-name>
```
Check `components/ui/` before adding — component may already exist.

## Environment Variables Needed

- `NEXT_PUBLIC_*` — public vars (safe to expose to browser)
- Check `.env.example` for the full list before starting a new feature
