# All-Or-Nothing API Specification

**Project:** All-Or-Nothing — Sports Betting Simulator  
**Contributors:** Agustin Xocua Dimayuga, Fabian Ballesteros-Limon, Miguel Medina, Nicolas Rosetes Beltran  
**Base URL:** `/api/v1`  
**Format:** All requests and responses use `application/json`

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Users](#2-users)
3. [Games](#3-games)
4. [Bets](#4-bets)
5. [Leaderboard](#5-leaderboard)
6. [Comments](#6-comments)
7. [Notifications](#7-notifications)
8. [Error Responses](#8-error-responses)

---

## 1. Authentication

### `POST /auth/users`

Creates a new user account with a starting balance of virtual currency.

**Request:**
```json
{
  "username": "sportzfan99",
  "email": "sportzfan99@example.com",
  "password": "SecurePass123!"
}
```

**Response `201 Created`:**
```json
{
  "user_id": "u_4f8a2c1b",
  "username": "sportzfan99",
  "email": "sportzfan99@example.com",
  "balance": 1000.00,
  "created_at": "2025-04-15T10:30:00Z"
}
```

**Errors:**
- `409 Conflict` — username or email already in use
- `422 Unprocessable Entity` — missing or malformed fields

---

### `POST /auth/tokens`

Authenticates an existing user and returns a session token used in the `Authorization` header for all protected endpoints.

**Request:**
```json
{
  "email": "sportzfan99@example.com",
  "password": "SecurePass123!"
}
```

**Response `200 OK`:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "u_4f8a2c1b",
  "username": "sportzfan99",
  "expires_at": "2025-04-16T10:30:00Z"
}
```

**Errors:**
- `401 Unauthorized` — invalid credentials
- `422 Unprocessable Entity` — missing fields

---

### `DELETE /auth/tokens`

Invalidates the current session token.

**Headers:** `Authorization: Bearer <token>`

**Response `204 No Content`**

---

## 2. Users

### `GET /users/{user_id}`

Returns the profile and current balance for a specific user. Users may only access their own profile unless they are an admin.

**Headers:** `Authorization: Bearer <token>`

**Response `200 OK`:**
```json
{
  "user_id": "u_4f8a2c1b",
  "username": "sportzfan99",
  "balance": 850.00,
  "total_bets": 12,
  "wins": 7,
  "losses": 5,
  "win_rate": 0.583,
  "member_since": "2025-04-15T10:30:00Z"
}
```

**Errors:**
- `403 Forbidden` — attempting to access another user's profile
- `404 Not Found` — user does not exist

---

### `GET /users/{user_id}/balance`

Returns only the current virtual currency balance for the authenticated user. Useful for lightweight balance checks before placing a bet.

**Headers:** `Authorization: Bearer <token>`

**Response `200 OK`:**
```json
{
  "user_id": "u_4f8a2c1b",
  "balance": 850.00
}
```

---

### `GET /users/{user_id}/bets`

Returns the full bet history for the authenticated user, including active, resolved, and pending bets. Supports pagination.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type   | Default | Description                              |
|-----------|--------|---------|------------------------------------------|
| `status`  | string | all     | Filter by `active`, `won`, `lost`, `pending` |
| `page`    | int    | 1       | Page number                              |
| `limit`   | int    | 20      | Results per page (max 100)               |

**Response `200 OK`:**
```json
{
  "user_id": "u_4f8a2c1b",
  "page": 1,
  "limit": 20,
  "total": 12,
  "bets": [
    {
      "bet_id": "b_9c3e7d2a",
      "game_id": "g_1a2b3c4d",
      "game_summary": "Lakers vs Warriors",
      "team_bet_on": "Lakers",
      "amount": 50.00,
      "odds": 1.85,
      "potential_payout": 92.50,
      "status": "won",
      "placed_at": "2025-04-14T18:00:00Z",
      "resolved_at": "2025-04-14T22:10:00Z"
    }
  ]
}
```

---

## 3. Games

### `GET /games`

Returns a list of live and upcoming games available for betting. Optionally filter by sport or status.

**Query Parameters:**
| Parameter | Type   | Default  | Description                               |
|-----------|--------|----------|-------------------------------------------|
| `sport`   | string | all      | Filter by sport (e.g. `basketball`, `football`) |
| `status`  | string | upcoming | Filter by `live`, `upcoming`, `finished`  |
| `page`    | int    | 1        | Page number                               |
| `limit`   | int    | 20       | Results per page (max 100)                |

**Response `200 OK`:**
```json
{
  "page": 1,
  "limit": 20,
  "total": 3,
  "games": [
    {
      "game_id": "g_1a2b3c4d",
      "sport": "basketball",
      "home_team": "Lakers",
      "away_team": "Warriors",
      "start_time": "2025-04-15T19:30:00Z",
      "status": "upcoming",
      "home_odds": 1.85,
      "away_odds": 2.10,
      "venue": "Crypto.com Arena"
    },
    {
      "game_id": "g_5e6f7g8h",
      "sport": "football",
      "home_team": "Chiefs",
      "away_team": "Eagles",
      "start_time": "2025-04-15T20:00:00Z",
      "status": "live",
      "home_score": 14,
      "away_score": 10,
      "home_odds": 1.60,
      "away_odds": 2.40,
      "venue": "Arrowhead Stadium"
    }
  ]
}
```

**Errors:**
- `503 Service Unavailable` — live game data source is unreachable

---

### `GET /games/{game_id}`

Returns full details for a single game including current scores (if live), odds, and betting eligibility status.

**Response `200 OK`:**
```json
{
  "game_id": "g_1a2b3c4d",
  "sport": "basketball",
  "home_team": "Lakers",
  "away_team": "Warriors",
  "start_time": "2025-04-15T19:30:00Z",
  "status": "upcoming",
  "home_odds": 1.85,
  "away_odds": 2.10,
  "venue": "Crypto.com Arena",
  "betting_open": true,
  "total_bets_placed": 134,
  "total_wagered": 4520.00
}
```

**Errors:**
- `404 Not Found` — game does not exist
- `503 Service Unavailable` — game data temporarily unavailable

---

## 4. Bets

### `POST /bets`

Places a new bet on behalf of the authenticated user. Deducts the wager amount from the user's balance immediately. Bets cannot be placed once a game has started.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "game_id": "g_1a2b3c4d",
  "team": "Lakers",
  "amount": 50.00
}
```

**Response `201 Created`:**
```json
{
  "bet_id": "b_9c3e7d2a",
  "game_id": "g_1a2b3c4d",
  "game_summary": "Lakers vs Warriors",
  "team_bet_on": "Lakers",
  "amount": 50.00,
  "odds": 1.85,
  "potential_payout": 92.50,
  "status": "active",
  "placed_at": "2025-04-15T14:22:00Z",
  "new_balance": 800.00
}
```

**Errors:**
- `400 Bad Request` — amount is zero or negative
- `403 Forbidden` — betting has closed (game already started)
- `404 Not Found` — game does not exist
- `409 Conflict` — duplicate bet submission detected
- `422 Unprocessable Entity` — insufficient balance

---

### `GET /bets/{bet_id}`

Returns the current status and details for a single bet. Only accessible by the user who placed the bet.

**Headers:** `Authorization: Bearer <token>`

**Response `200 OK`:**
```json
{
  "bet_id": "b_9c3e7d2a",
  "game_id": "g_1a2b3c4d",
  "game_summary": "Lakers vs Warriors",
  "team_bet_on": "Lakers",
  "amount": 50.00,
  "odds": 1.85,
  "potential_payout": 92.50,
  "status": "active",
  "placed_at": "2025-04-15T14:22:00Z",
  "resolved_at": null
}
```

**Errors:**
- `403 Forbidden` — bet belongs to another user
- `404 Not Found` — bet does not exist

---

### `POST /bets/resolve` *(Internal / System Use)*

Triggered automatically by the system when a game concludes. Resolves all pending bets for the finished game, updates user balances, and emits notifications. This endpoint is not intended for direct user access.

**Request:**
```json
{
  "game_id": "g_1a2b3c4d",
  "winning_team": "Lakers"
}
```

**Response `200 OK`:**
```json
{
  "game_id": "g_1a2b3c4d",
  "bets_resolved": 134,
  "total_paid_out": 8350.00,
  "resolved_at": "2025-04-15T22:15:00Z"
}
```

**Errors:**
- `404 Not Found` — game not found
- `409 Conflict` — game results already processed
- `503 Service Unavailable` — game result data unavailable; bets remain pending

---

## 5. Leaderboard

### `GET /leaderboard`

Returns a ranked list of users by net virtual currency earnings (total winnings minus total wagered). Encourages competition by surfacing top performers.

**Query Parameters:**
| Parameter  | Type   | Default | Description                               |
|------------|--------|---------|-------------------------------------------|
| `period`   | string | all     | Filter by `daily`, `weekly`, `monthly`, `all` |
| `limit`    | int    | 25      | Number of users to return (max 100)       |

**Response `200 OK`:**
```json
{
  "period": "weekly",
  "generated_at": "2025-04-15T14:00:00Z",
  "leaderboard": [
    {
      "rank": 1,
      "user_id": "u_4f8a2c1b",
      "username": "sportzfan99",
      "net_earnings": 620.00,
      "total_bets": 12,
      "win_rate": 0.583
    },
    {
      "rank": 2,
      "user_id": "u_7b9d1e3f",
      "username": "betmaster42",
      "net_earnings": 490.00,
      "total_bets": 20,
      "win_rate": 0.600
    }
  ]
}
```

---

## 6. Comments

### `GET /games/{game_id}/comments`

Returns all comments posted on a specific game, ordered by most recent first. Supports pagination.

**Query Parameters:**
| Parameter | Type | Default | Description        |
|-----------|------|---------|--------------------|
| `page`    | int  | 1       | Page number        |
| `limit`   | int  | 30      | Results per page   |

**Response `200 OK`:**
```json
{
  "game_id": "g_1a2b3c4d",
  "page": 1,
  "limit": 30,
  "total": 47,
  "comments": [
    {
      "comment_id": "c_2d4f6a8b",
      "user_id": "u_4f8a2c1b",
      "username": "sportzfan99",
      "body": "Lakers are going to dominate tonight!",
      "posted_at": "2025-04-15T14:05:00Z"
    }
  ]
}
```

---

### `POST /games/{game_id}/comments`

Posts a new comment on a game. Empty or whitespace-only comments are rejected.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "body": "Lakers are going to dominate tonight!"
}
```

**Response `201 Created`:**
```json
{
  "comment_id": "c_2d4f6a8b",
  "game_id": "g_1a2b3c4d",
  "user_id": "u_4f8a2c1b",
  "username": "sportzfan99",
  "body": "Lakers are going to dominate tonight!",
  "posted_at": "2025-04-15T14:05:00Z"
}
```

**Errors:**
- `400 Bad Request` — body is empty or only whitespace
- `404 Not Found` — game does not exist

---

### `DELETE /games/{game_id}/comments/{comment_id}`

Deletes a comment. Users may only delete their own comments.

**Headers:** `Authorization: Bearer <token>`

**Response `204 No Content`**

**Errors:**
- `403 Forbidden` — comment belongs to another user
- `404 Not Found` — comment does not exist

---

## 7. Notifications

### `GET /users/{user_id}/notifications`

Returns a list of notifications for the authenticated user, such as bet resolution results (win/loss) and balance updates.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type    | Default | Description                    |
|-----------|---------|---------|--------------------------------|
| `read`    | boolean | false   | Filter to only unread if `false` |
| `page`    | int     | 1       | Page number                    |
| `limit`   | int     | 20      | Results per page               |

**Response `200 OK`:**
```json
{
  "user_id": "u_4f8a2c1b",
  "page": 1,
  "limit": 20,
  "total_unread": 2,
  "notifications": [
    {
      "notification_id": "n_3c5e7a9b",
      "type": "bet_resolved",
      "message": "Your bet on the Lakers won! You earned $92.50.",
      "bet_id": "b_9c3e7d2a",
      "read": false,
      "created_at": "2025-04-15T22:16:00Z"
    }
  ]
}
```

---

### `PATCH /users/{user_id}/notifications/{notification_id}`

Marks a single notification as read.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "read": true
}
```

**Response `200 OK`:**
```json
{
  "notification_id": "n_3c5e7a9b",
  "read": true
}
```

---

## 8. Error Responses

All errors follow a consistent envelope format:

```json
{
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Your balance of $30.00 is less than the requested wager of $50.00.",
    "status": 422
  }
}
```

### Standard Error Codes

| HTTP Status | Code                      | Description                                              |
|-------------|---------------------------|----------------------------------------------------------|
| 400         | `INVALID_AMOUNT`          | Bet amount is zero, negative, or non-numeric             |
| 400         | `INVALID_COMMENT`         | Comment body is empty or invalid                         |
| 401         | `UNAUTHORIZED`            | Missing or invalid authentication token                  |
| 403         | `FORBIDDEN`               | Authenticated user lacks permission for this resource    |
| 403         | `BETTING_CLOSED`          | Game has already started; bets are no longer accepted    |
| 404         | `GAME_NOT_FOUND`          | The specified game does not exist                        |
| 404         | `BET_NOT_FOUND`           | The specified bet does not exist                         |
| 404         | `USER_NOT_FOUND`          | The specified user does not exist                        |
| 409         | `DUPLICATE_ACCOUNT`       | Email or username is already registered                  |
| 409         | `DUPLICATE_BET`           | An identical bet was already submitted                   |
| 409         | `ALREADY_RESOLVED`        | Game results have already been processed                 |
| 422         | `INSUFFICIENT_BALANCE`    | User does not have enough virtual currency to place bet  |
| 500         | `INTERNAL_SERVER_ERROR`   | Unexpected server-side error; try again later            |
| 503         | `GAME_DATA_UNAVAILABLE`   | Live sports data source is temporarily unreachable       |

---
