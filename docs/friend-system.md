# Friend System and Trip Invitations

This module provides JWT-protected APIs and React pages for user search, friend requests, friend lists, trip invitations, and in-app notifications. PostgreSQL is configured via `DATABASE_URL` and Cloudinary profile pictures are stored as secure URLs on the user record.

## API Highlights
- `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/logout/`
- `GET /api/friends/search/?search=alice`
- `POST /api/friends/requests/send/`, `POST /api/friends/requests/{id}/accept/`, `reject/`, `cancel/`
- `GET /api/friends/`, `DELETE /api/friends/{id}/remove/`
- `POST /api/trips/{id}/invite/`, `POST /api/trips/invitations/{id}/accept/`, `reject/`, `cancel/`
- `GET /api/notifications/`, `POST /api/notifications/mark_all_read/`, `POST /api/notifications/{id}/mark_read/`

All list endpoints use DRF pagination, search, filtering, and ordering where applicable. Mutating friend and invitation workflows use transactions where membership edges or notifications are created.
