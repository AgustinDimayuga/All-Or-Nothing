# All-Or-Nothing Curl Commands for Flow 1

**Project:** All-Or-Nothing — Sports Betting Simulator  
**Base URL:** `/api/v1`

---

## Flow 1: New User Registers, Browses Games, and Places a Bet

Marco is a first-time sports fan who heard about All-Or-Nothing from a friend. He wants to create an account and place his first bet on an upcoming NBA game.

Marco starts by creating his account:

- He calls `POST /users` with his username, email, and password. The server responds with his new `user_id` of `u_4f8a2c1b` and a starting balance of **$1000.00** in virtual currency.

Since he now has an account, Marco logs in:

- He calls `POST /auth/tokens` with his email and password. The server returns a JWT token and confirms his `user_id` is `u_4f8a2c1b`. Marco's client saves both the token and user_id for future requests.

Marco wants to see what games are available to bet on:

- He calls `GET /games?status=upcoming&sport=basketball`. The response lists several upcoming NBA games. He notices one entry for **Lakers vs Warriors** with `game_id: g_1a2b3c4d`, starting at 7:30 PM, with home odds of 1.85 and away odds of 2.10.

Marco wants more details before committing:

- He calls `GET /games/g_1a2b3c4d`. The response confirms the game is still open for betting (`"betting_open": true`), shows the venue as Crypto.com Arena, and displays the current odds.

Marco decides to bet $50 on the Lakers:

- He calls `POST /bets` with `game_id: g_1a2b3c4d`, `team: "Lakers"`, and `amount: 50.00`. The server validates that Marco has enough balance, that the game hasn't started yet, and that this isn't a duplicate submission. The response confirms the bet with `bet_id: b_9c3e7d2a`, a potential payout of **$92.50**, and shows his new balance of **$950.00**.

Marco is now in the game. He drinks his pre-game coffee and waits for tip-off.

---

## Curl commands

1.
```bash
  curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/auth/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "Marco",
  "name": "Marco",
  "email": "test@email.com",
  "phone": "1234567890",
  "password": "password"
}'
```

It should respond with a code 200 and 

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJuYW1lIjoiTWFyY28iLCJleHAiOjE3Nzc5NjI4Mzd9.AF-xzOttBMSD9526w-YC8ED6ddBIKPp_pvyLl1iaLTg",
  "token_type": "bearer"
}
```

---

2. 
```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/auth/tokens' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=Marco&password=password&scope=&client_id=string&client_secret=********'
```
It should respond with a code 200 and 
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJuYW1lIjoiTWFyY28iLCJleHAiOjE3Nzc5NjI5Mzd9.ij90zdGw6aEFOgLDisaaJ02t8tXAXNPy6DMLztLYbXc",
  "token_type": "bearer"
}
```
It is similar to the previous call

---

3. 
```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/games/get_games?sport=Basketball&status=upcoming&page=1&limit=20' \
  -H 'accept: application/json'
```
It should respond with a code 200 and
```bash
[
  {
    "id": 2,
    "sport": "Basketball",
    "home_team": "Spurs",
    "away_team": "Wolves",
    "date": "2026-05-05T05:36:35.529799Z",
    "location": "LA"
  },
  {
    "id": 1,
    "sport": "Basketball",
    "home_team": "Lakers",
    "away_team": "Warriors",
    "date": "2026-05-05T05:36:35.529799Z",
    "location": "LA"
  }
]
```
There are multiple games

---

4. 
```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/games/game_details?id=1' \
  -H 'accept: application/json'
```
It should respond with a code 200 and

```json
{
  "game_id": 2,
  "league_id": 1,
  "home_team": "Lakers",
  "away_team": "Warriors",
  "date": "2026-05-05T05:36:35.529799Z",
  "location": "LA",
  "home_odds": 1.85,
  "away_odds": 2.1
}
```
---

5. 
```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/bets/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJuYW1lIjoiTWFyY28iLCJleHAiOjE3Nzc5NjM2Nzd9.3_bxOt0O-E_3DDO5F9SjbAJDYUy7ZM8Y2vKZ4EBcb1o' \
  -H 'Content-Type: application/json' \
  -d '{
  "game_id": 1,
  "team": "Lakers",
  "amount": 50
}'
```

It should response with a code 200 and

```json
{
  "bet_id": 1,
  "game_id": 1,
  "team_bet_on": "Lakers",
  "amount": 50,
  "odds": 1.85,
  "potential_payout": 92.5,
  "status": "active",
  "placed_at": "2026-05-05 06:03:00.508997+00:00",
  "new_balance": 50
}
```


