# PostgreSQL Schema

Core tables:
- `accounts_user`: UUID users, unique username/email, profile URL, bio, timestamps.
- `connections_friendrequest`, `connections_friend`: friend lifecycle and reciprocal graph edges.
- `trips_currency`, `trips_trip`, `trips_tripmember`, `trips_tripinvitation`: currencies, trips, role-based members, invitations.
- `expenses_category`, `expenses_expense`, `expenses_expenseparticipant`, `expenses_expensecomment`, `expenses_expenseaudit`: expense domain, participant balances, comments, edit history.
- `payments_payment`: settlement records.
- `notifications_notification`: in-app notification inbox.
- `activity_activitylog`: audit timeline.

## ER Diagram
```mermaid
erDiagram
  accounts_user ||--o{ connections_friendrequest : sends
  accounts_user ||--o{ connections_friend : has
  accounts_user ||--o{ trips_tripmember : joins
  trips_trip ||--o{ trips_tripmember : contains
  trips_trip ||--o{ trips_tripinvitation : invites
  trips_trip ||--o{ expenses_expense : has
  expenses_expense ||--o{ expenses_expenseparticipant : splits
  expenses_category ||--o{ expenses_expense : categorizes
  trips_trip ||--o{ payments_payment : settles
  accounts_user ||--o{ notifications_notification : receives
```
