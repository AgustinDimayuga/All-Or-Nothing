
## Example WorkFlow 2
## Example WorkFlow 3
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
