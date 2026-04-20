# All-Or-Nothing Example Flows

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
