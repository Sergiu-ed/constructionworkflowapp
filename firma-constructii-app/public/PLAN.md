# Construct Pro - Development Plan

## Overview
Construct Manager Pro is a construction site management application for managing projects, quotes, team attendance, and timekeeping.

## Current Architecture
- **Frontend**: Static HTML/CSS/JavaScript with TailwindCSS
- **Data Storage**: localStorage (client-side persistence)
- **Pages**: 
  - `index.html` - Main dashboard (calendar, projects, timekeeping, tasks)
  - `oferta.html` - Quote/Offer creation and preview
  - `settings.html` - Company profile, categories, pricing configuration

## Data Models

### Company Settings
- Name, slogan, address, city, phone, email, logo
- Quote categories with items
- Pricing: currency, hourly rate, material markup

### Projects
- Client info, phone, email
- Tasks with progress tracking
- Scheduled team members
- Active days calendar

### Quotes (Oferta)
- Client information (name, address, city, phone, email, job type)
- Dimensions (length, width, height, wall area, floor area)
- Work items across categories (demolition, preparation, waterproofing, etc.)
- Client-provided materials checkboxes
- Notes

### Timekeeping
- Work timer (start/stop)
- Work mode (site/transport)
- Team attendance tracking
- Elapsed time persistence

## Phase 1: Backend Infrastructure (CURRENT)
- [x] Setup project structure with `/backend`, `/api`, `/lib` directories
- [ ] Create RESTful API endpoints
- [ ] Set up serverless functions on Modal
- [ ] Data persistence layer (file-based or database)

## Phase 2: API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/settings` | GET/PUT | Company settings CRUD |
| `/api/projects` | GET/POST/PUT/DELETE | Project management |
| `/api/quotes` | GET/POST/PUT/DELETE | Quote management |
| `/api/timekeeping` | GET/POST | Timer state and logs |
| `/api/team` | GET/POST/DELETE | Team member management |

## Phase 3: Frontend Integration
- Replace localStorage calls with API calls
- Add loading states and error handling
- Offline fallback with localStorage sync

## Phase 4: Enhanced Features
- PDF export for quotes
- Email integration
- Multi-user support
- Real-time sync

---
*Last Updated: 2026-01-15*
*Status: Phase 1 - Backend Infrastructure*
