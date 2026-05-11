
## Example WorkFlow 2
## Example WorkFlow 3

Derek has been using All-Or-Nothing for two weeks and considers himself a strategic bettor. He wants to review his betting history to spot patterns, then check where he stands on the leaderboard.

Derek logs in:

- He calls `POST /auth/tokens` and receives his JWT token.

He pulls up his full betting history to analyze his wins and losses:

- He calls `GET /users/u_9a1c3e5f/bets?status=won` to see all his winning bets. The response shows 14 wins, mostly on underdog picks in the NBA.
- He calls `GET /users/u_9a1c3e5f/bets?status=lost` to review his mistakes. He notices he tends to lose when betting on Monday night football — a pattern he'll factor into future decisions.

Feeling confident, Derek checks the weekly leaderboard:

- He calls `GET /leaderboard?period=weekly&limit=25`. The response ranks the top 25 users by net earnings this week. Derek sees he is currently sitting at rank 4 with net earnings of $430.00, just behind the top three.

Derek decides to make a bold move to climb the rankings. He browses for a high-value game:

- He calls `GET /games?status=upcoming` and spots a college football game with favorable odds.
- He calls `GET /games/g_8b2d4f6a` to review the details — odds, teams, and start time.
- He calls `POST /bets` with a larger wager of $200.00 on the home team.

After the game resolves in his favor, Derek checks the leaderboard again:

- He calls `GET /leaderboard?period=weekly`. He has jumped to rank 2 with net earnings of $790.00. He's within striking distance of the top spot.

## Testing Results
> [!WARNING]
> Please note some changes were done to the example WorkFlow since when writing these we had a different structure in mind. When actually implementing it we changed a few things please follow all the steps below step by step.

1. First call `POST /auth/tokens` to get his token.

```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/auth/tokens' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=_____&password=string&scope=&client_id=string&client_secret='
```
You will recieve a response code 200 and something like this 
```json
{

  "access_token":"eyJhbGUzI1NiIsInR5cCI6IkpXVCJ9eyJ1cXkIjo0LCJuWjoicHJpeWiLeHAiOjE3Nzg1MjQ2NjF9.xa6JJhL-PfcRQn_5Qpz5ZyGzs_7e8D9Texh-Cy4uI",
  "token_type": "bearer"
}
```

> [!NOTE]
> Please note you will not recieve the same access token as the example response above. Copy your unique JWT and use it accordingly as explained below



2. You will now call `GET /leaderboard?period=weekly&limit=25` to check the leaderboard and compare his net earnings to everyone else betting. This checks everyone's net earnings and ranks them from the top 25 within a week span.

```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/leaderboard/?period=weekly&limit=25' \
  -H 'accept: application/json'
```

You will recieve a response code 200 and something like this
```json
{
  "period": "weekly",
  "limit": 25,
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 3,
      "username": "FaZe_FBI1137",
      "net_earnings": -10
    },
    {
      "rank": 2,
      "user_id": 1,
      "username": "Osmotic_pole",
      "net_earnings": -94
    },
    {
      "rank": 3,
      "user_id": 2,
      "username": "hello",
      "net_earnings": -100
    }
  ]
}
```

3. Now you want to place a bet on upcoming games to climb the leaderboard. So now he will calls `GET /games` with filters depending on what league he wants to browse to
climb the leaderboard. 

```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/games/?league=nlb&status=upcoming&page=1&limit=20' \
  -H 'accept: application/json'
```

You will recieve a response code 200 and something like this
```json
[
  {
    "id": 395,
    "sport": "baseball",
    "home_team": "Orioles",
    "away_team": "Yankees",
    "date": "2026-05-11T22:35:00Z",
    "location": "Oriole Park at Camden Yards"
  },
  {
    "id": 169,
    "sport": "baseball",
    "home_team": "Blue Jays",
    "away_team": "Rays",
    "date": "2026-05-11T23:07:00Z",
    "location": "Rogers Centre"
  },
  {
    "id": 1378,
    "sport": "baseball",
    "home_team": "Rangers",
    "away_team": "Diamondbacks",
    "date": "2026-05-12T00:05:00Z",
    "location": "Globe Life Field"
  }
]
```

4. You will now view game details on a specific game you want to bet on with good odds of winning with `GET /games/game_details?id=____`
> [!NOTE]
> Please note games end and begin at different times so you have to choose a game that is upcoming to look at the details and the use that unique id

```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/games/game_details?id=395' \
  -H 'accept: application/json'
```

You will recieve a response code 200 and something like this

```json
{
  "game_id": 1378,
  "league_id": 2,
  "home_team": "Rangers",
  "away_team": "Diamondbacks",
  "date": "2026-05-12T00:05:00Z",
  "location": "Globe Life Field",
  "home_odds": 2.96007821847731,
  "away_odds": 0.817560472887645
}
```

5. Now we will place a bet on an upcoming game. Don't forget your JWT. 

> [!NOTE]
> Again as a reminder, place a bet on a different game since this game will most likely be resolved when you look at this. 

```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/bets/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer PLACE_JWT_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{
  "game_id": 1378,
  "team": "Rangers",
  "amount": 200
}'
```

You will recieve a response code 200 and something like this
```json
{
  "bet_id": 7,
  "game_id": 1378,
  "team_bet_on": "Rangers",
  "amount": 200,
  "odds": 2.96007821847731,
  "potential_payout": 592.0156436954619,
  "status": "active",
  "placed_at": "2026-05-11 23:06:28.222152+00:00",
  "new_balance": 800
}
```

6. Now after the game has resolved check the leaderboard to see if you increased or decreased in ranking. 

```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/leaderboard/?period=weekly&limit=25' \
  -H 'accept: application/json'
```

You will recieve a response code 200 and something like this 

```json
{
  "period": "weekly",
  "limit": 25,
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 3,
      "username": "FaZe_FBI1137",
      "net_earnings": -10
    },
    {
      "rank": 2,
      "user_id": 1,
      "username": "Osmotic_pole",
      "net_earnings": -94
    },
    {
      "rank": 3,
      "user_id": 2,
      "username": "hello",
      "net_earnings": -100
    },
    {
      "rank": 4,
      "user_id": 8,
      "username": "Derek",
      "net_earnings": -200
    }
  ]
}
```
Congratulations you have finished this flow!!!

## Example WorkFlow 4
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

## Testing Results
> [!WARNING]
> Please note some changes were done to the example WorkFlow since when writing these we had a different structure in mind. When actually implementing it we changed a few things please follow all the steps below step by step.

1. You will call `POST /auth/tokens` and will be signing in as priya. A premade account for you to act as priya.


```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/auth/tokens' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=priya&password=string&scope=&client_id=string&client_secret='
```
You will recieve a response code 200 and something like this 
```json
{

  "access_token":"eyJhbGUzI1NiIsInR5cCI6IkpXVCJ9eyJ1cXkIjo0LCJuWjoicHJpeWiLeHAiOjE3Nzg1MjQ2NjF9.xa6JJhL-PfcRQn_5Qpz5ZyGzs_7e8D9Texh-Cy4uI",
  "token_type": "bearer"
}
```


> [!NOTE]
> Please note you will not recieve the same access token as the example response above. Copy your unique JWT and use it accordingly as explained below

2. You will now call `GET /games?league=nlb&status=finished&page=1&limit=20`. See how the query parameter used here is status=finished. This is to ensure you get a GAME_STARTED error, since we cannot ensure a game is live when you are grading. 

```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/games/?league=nlb&status=finished&page=1&limit=20' \
  -H 'accept: application/json'
```

You will recieve a response code 200 and something like this
```json
[
  {
    "id": 1398,
    "sport": "baseball",
    "home_team": "Giants",
    "away_team": "Yankees",
    "date": "2026-03-26T00:05:00Z",
    "location": "Oracle Park"
  },
  {
    "id": 1198,
    "sport": "baseball",
    "home_team": "Mets",
    "away_team": "Pirates",
    "date": "2026-03-26T17:15:00Z",
    "location": "Citi Field"
  },
  {
    "id": 1389,
    "sport": "baseball",
    "home_team": "Brewers",
    "away_team": "White Sox",
    "date": "2026-03-26T18:10:00Z",
    "location": "American Family Field"
  },
]
```

3. We will now grab the id 1398 and work with the Giants vs. Yankees game. So  you will now call `GET /comments/` which note is a game that has already started.
```bash
curl -X 'GET' \
  'https://all-or-nothing-r35u.onrender.com/games/1398/comments?page=1&limit=20' \
  -H 'accept: application/json'
```

You will recieve a 200 code and all the comments for the game 

```json
[
  {
    "comment_id": 3,
    "user_id": 5,
    "username": "Dummy",
    "body": "I love baseball!",
    "posted_at": "2026-05-11T18:14:14.881178Z"
  },
  {
    "comment_id": 4,
    "user_id": 5,
    "username": "Dummy",
    "body": "Basball works!",
    "posted_at": "2026-05-11T18:14:21.249514Z"
  },
  {
    "comment_id": 5,
    "user_id": 5,
    "username": "Dummy",
    "body": "Yankees on top I love NYC!!!",
    "posted_at": "2026-05-11T18:14:35.823425Z"
  }
]
```

4. You will now attempt to post an empty comment as priya. Using the JWT recieved you will call 
```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/games/1398/comments?body=' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer PLACE_JWT_TOKEN_HERE' \
  -d ''
```
You should recieve INVALID_COMMENT ERROR. 

```json
{
  "detail": {"error_code":"INVALID_COMMENT", "message":"Body cannot be empty"}
}
```

5. You will now write a valid comment. Don't forget your JWT.
```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/games/1398/comments?body=Yankees%20suck%20bro%21' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer PLACE_JWT_TOKEN_HERE' \
  -d ''
```

You should get a response like so 

```json
{
  "comment_id": 8, */ this will be different comment_id make sure to store it */
  "posted_at": "2026-05-11T18:25:52.807323Z",
  "body": "this is a test"
}
```

6. You will now place a bet on an ongoing game. Don't forget your JWT.
```bash
curl -X 'POST' \
  'https://all-or-nothing-r35u.onrender.com/bets/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer PLACE_JWT_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{
  "game_id": 1398,
  "team": "Yankees",
  "amount": 30
}'
```

You should get the following response, since the game already started

```json
{
  "detail": "Team is not playing or Game Already Started"
}
```

7. You will now delete the comment. Don't forget your JWT and Your comment_id!
```bash
curl -X 'DELETE' \
  'https://all-or-nothing-r35u.onrender.com/games/1398/comments/REPLACE_ME_WITH_COMMENT_ID' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer REPLACE_ME_WITH_JWT_TOKEN'
```

You will recieve a 204 response and you have finished this example flow!
