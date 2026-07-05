# TripSplit

TripSplit is a production-oriented trip expense splitting app built with Django REST Framework, PostgreSQL, JWT authentication, React, Vite, TypeScript, Tailwind, TanStack Query, React Hook Form, Zod, Framer Motion, Recharts, and Cloudinary URL storage.

## Features
- JWT register/login/logout, profile update, change password, and soft account deletion.
- Friend discovery, friend requests, reciprocal friends, and trip invitations.
- Trips with destinations, images, currencies, roles, owner/admin permissions, archive/close/delete, transfer ownership, and active members.
- Expenses with Equal, Exact, Percentage, Share Units, and Custom splits using `Decimal` math only.
- Settlement simplification that minimizes payment edges between debtors and creditors.
- Cash/online payment recording and in-app notifications.
- Dashboard reports for trips, friends, recent expenses, monthly spending, and category spending.

## Local setup
1. Create PostgreSQL database `tripsplit`.
2. Copy `.env.example` to `.env` and fill database/Cloudinary values.
3. Install backend packages: `python -m pip install -r backend/requirements.txt`.
4. Run migrations: `cd backend && python manage.py migrate`.
5. Start backend: `python manage.py runserver`.
6. Install frontend packages: `cd frontend && npm install`.
7. Start frontend: `npm run dev`.

## Cloudinary
Upload profile, trip, and receipt images directly from the client or trusted upload service to Cloudinary. Store only the returned secure URL in PostgreSQL; backend validators reject non-Cloudinary image URLs.
