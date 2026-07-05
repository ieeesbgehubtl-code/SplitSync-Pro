# API Documentation

All endpoints are rooted at `/api/` and require JWT auth except register/login/refresh.

## Auth
- `POST /auth/register/`
- `POST /auth/login/`
- `POST /auth/refresh/`
- `POST /auth/logout/`
- `GET/PATCH /auth/me/`
- `POST /auth/change-password/`
- `DELETE /auth/delete-account/`

## Friends
- `GET /friends/search/?search=`
- `POST /friends/requests/send/`
- `POST /friends/requests/{id}/accept|reject|cancel/`
- `GET /friends/`
- `DELETE /friends/{id}/remove/`

## Trips
- `GET/POST /trips/`
- `POST /trips/{id}/invite/`
- `GET /trips/{id}/members/`
- `POST /trips/{id}/close|archive|transfer_ownership/`
- `POST /trips/{id}/members/{member_id}/remove/`

## Expenses and Settlements
- `GET/POST /expenses/`
- `GET/POST /expenses/categories/`
- `GET /expenses/trip-settlements/{trip_id}/balances/`
- `GET /expenses/trip-settlements/{trip_id}/simplify/`

## Payments, Reports, Notifications
- `GET/POST /payments/`
- `GET /reports/dashboard/`
- `GET /notifications/`
- `POST /notifications/{id}/mark_read/`
- `POST /notifications/mark_all_read/`
