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

## Flow 2: Engaged Bettor Tracks Active Bets, Game Resolves, and Checks Notifications

Sofia is a returning bettor who placed three bets earlier in the day on different NFL games. She wants to monitor how her picks are doing, and later finds out the results when the games finish.

Sofia logs back in to check her active bets:

- She calls `POST /auth/tokens` and receives a fresh JWT token.
- She calls `GET /users/u_7b9d1e3f/bets?status=active`. The response lists her three active bets across different games, showing each team she backed, the amounts wagered, and potential payouts.

She checks her balance to see how much she has left to wager:

- She calls `GET /users/u_7b9d1e3f/balance`. The response shows she has **$620.00** remaining.

Sofia wants details on one of her games that just went live:

- She calls `GET /games/g_5e6f7g8h`. The response shows the game is now `"status": "live"` with a current score of Chiefs 14, Eagles 10 — her bet is on the Chiefs, so things are looking good.

Later that evening, the Chiefs game concludes. The system automatically resolves all bets:

- The backend triggers `POST /bets/resolve` internally with `game_id: g_5e6f7g8h` and `winning_team: "Chiefs"`. The server resolves 98 bets, pays out winners, and creates a notification for every affected user including Sofia.

Sofia opens the app and checks her notifications:

- She calls `GET /users/u_7b9d1e3f/notifications?read=false`. The response includes a notification: *"Your bet on the Chiefs won! You earned $175.00."*
- She marks it as read by calling `PATCH /users/u_7b9d1e3f/notifications/n_3c5e7a9b` with `"read": true`.

Sofia checks her updated balance:

- She calls `GET /users/u_7b9d1e3f/balance`. Her balance is now **$795.00**, reflecting the payout. She heads to the leaderboard to see if she climbed the rankings.

---

## Flow 3: Competitive Player Reviews Past Performance and Climbs the Leaderboard

Derek has been using All-Or-Nothing for two weeks and considers himself a strategic bettor. He wants to review his betting history to spot patterns, then check where he stands on the leaderboard.

Derek logs in:

- He calls `POST /auth/tokens` and receives his JWT token.

He pulls up his full betting history to analyze his wins and losses:

- He calls `GET /users/u_9a1c3e5f/bets?status=won` to see all his winning bets. The response shows 14 wins, mostly on underdog picks in the NBA.
- He calls `GET /users/u_9a1c3e5f/bets?status=lost` to review his mistakes. He notices he tends to lose when betting on Monday night football — a pattern he'll factor into future decisions.

Feeling confident, Derek checks the weekly leaderboard:

- He calls `GET /leaderboard?period=weekly&limit=25`. The response ranks the top 25 users by net earnings this week. Derek sees he is currently sitting at **rank 4** with net earnings of **$430.00**, just behind the top three.

Derek decides to make a bold move to climb the rankings. He browses for a high-value game:

- He calls `GET /games?status=upcoming` and spots a college football game with favorable odds.
- He calls `GET /games/g_8b2d4f6a` to review the details — odds, teams, and start time.
- He calls `POST /bets` with a larger wager of **$200.00** on the home team.

After the game resolves in his favor, Derek checks the leaderboard again:

- He calls `GET /leaderboard?period=weekly`. He has jumped to **rank 2** with net earnings of **$790.00**. He's within striking distance of the top spot.

---

## Flow 4: Social Fan Comments on a Live Game (with Error Handling)

Priya is watching a live soccer match on TV and wants to join the conversation on All-Or-Nothing. She also tries to place a late bet and encounters an error.

Priya logs in and finds the live game:

- She calls `POST /auth/tokens` to get her token.
- She calls `GET /games?status=live&sport=soccer`. She finds the match with `game_id: g_3c5a7e9b`.

She reads what other users are saying:

- She calls `GET /games/g_3c5a7e9b/comments`. She sees 23 comments debating which team will score next.

Priya wants to join in:

- She calls `POST /games/g_3c5a7e9b/comments` with `"body": ""` — she accidentally submits an empty comment. The server returns `400 Bad Request` with error code `INVALID_COMMENT`, prompting her to enter valid content.
- She tries again with `"body": "No way Real Madrid holds this lead in the second half!"`. This time the server responds `201 Created` and her comment appears in the feed.

Excited, Priya tries to place a bet on the match mid-game:

- She calls `POST /bets` with `game_id: g_3c5a7e9b`, `team: "Real Madrid"`, and `amount: 75.00`. The server returns `403 Forbidden` with error code `BETTING_CLOSED`, informing her that the game has already started and betting is no longer accepted.

Priya realizes she missed her window. She deletes her comment after changing her mind about the prediction:

- She calls `DELETE /games/g_3c5a7e9b/comments/c_6d8f0b2e`. The server responds `204 No Content` confirming the deletion.

She makes a note to place her bets before kickoff next time.
