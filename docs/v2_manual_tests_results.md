
## Example WorkFlow 2
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


Sofia checks her updated balance after the game is over:

- She calls `GET /users/u_7b9d1e3f/balance`. Her balance is now **$795.00**, reflecting the payout. 
## Testing Results
1. You will call `POST /auth/tokens and will be signing in as Sofia. A premade account for you to act as Sofia.
   ```Bash
    curl -X 'POST' \
    'https://all-or-nothing-r35u.onrender.com/auth/tokens' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=password&username=Sofia&password=string&scope=&client_id=string&client_secret=********'
   ```
   You will receive a response code 200 and something like this

   ```json
    {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJuYW1lIjoiU29maWEiLCJleHAiOjE3Nzg1NTU5NTN9.ZGprxn_8JBMr_4hXhz4-ds0y3gOV8ra_z5ptBQV3iEA",
    "token_type": "bearer"
    }
   ```
>[!NOTE]
> Please not you will not recieve the same acess token as the example ressponse above.Copy your unique JWT and use it accordingly as explained below.

2. Sofia is then ready for a brand new of betting
   - so she places a bet using `POST/bets`
>[!NOTE]
> NOTE TO GRADER: Replace [REPLACE IWTH YOUR TOKEN] with the access toke from step 1
> The other paramaters and results will be up to you based on what games are available through the get games endpoint with the "upcoming" filter.
   
   ```bash
    curl -X 'POST' \
    'https://all-or-nothing-r35u.onrender.com/bets/' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer [REPLACE WITH YOUR TOKEN] \
    -H 'Content-Type: application/json' \
    -d '{
    "game_id": 1731,
    "team": "Brewers",
    "amount": 100
    }
   ```
   You should receive something like this:
   ``` json
    {
    "bet_id": 8,
    "game_id": 1731,
    "team_bet_on": "Brewers",
    "amount": 100,
    "odds": 2.06364422354296,
    "potential_payout": 206.364422354296,
    "status": "active",
    "placed_at": "2026-05-12 02:42:28.486169+00:00",
    "new_balance": 900
    }
   ```
Just to make sure her bet was processed correctly she runs `GET /users/u_7b9d1e3f/bets?status=active` to check her active bets
   ```Bash
   curl -X 'GET' \
    'https://all-or-nothing-r35u.onrender.com/users/me/bets?status=pending&page=1&limit=20' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJuYW1lIjoiU29maWEiLCJleHAiOjE3Nzg1NTg1OTd9.KsCiyIEM4Gfl762_9IOLcm7orMLPn5r5HIJuvt2YgCI'
   ```
You should recieve something like this:
   ```json
    {
    "user_id": 7,
    "status": "pending",
    "page": 1,
    "limit": 20,
    "total": 1,
    "returned": 1,
    "bets": [
      {
        "bet_id": 8,
        "game_id": 1731,
        "team_id": 64,
        "team_bet_on": "Brewers",
        "amount": 100,
        "odds": 2.06364422354296,
        "potential_payout": 206.364422354296,
        "status": "pending",
        "placed_at": "2026-05-12T02:42:28.486169Z"
      }
      ]
    }
   ```
3. After an hour of working on her potion shop, Sofia decides to check up on the game she bet on 
  - So she runs `GET /games/g_5e6f7g8h` with the `"status: "live"`
    ```bash
    curl -X 'GET' \
    'https://all-or-nothing-r35u.onrender.com/games/?league=nlb&status=live&page=1&limit=20' \
    -H 'accept: application/json'
    ```
  - And the output should look something like:
    ```json
    [
      {
        "id": 862,
        "sport": "baseball",
        "home_team": "Dodgers",
        "away_team": "Giants",
        "date": "2026-05-12T02:10:00Z",
        "location": "UNIQLO Field at Dodger Stadium"
      }
    ]
    ```
>[!WARNING]
>This is not something that the Grader has to do.
>
>Currently in our code there is a cronjob that randomly chooses the winning team after the game has ended (this runs every 2 hours)
>
>There is also a second cronjob that updates wallet based on the first cronjob's results (This runs every hour)

While she continues working on her potion shop, the game she bet on ends. Shortly afer the 2 hour/ cronjob takes into affects and runs 
`POST /bets/resolve` which updates her wallet based on the game outcome.

After finishing her homework Sofia realizes the game ended hours ago and decides to check her balance 
  - So she runs `GET /users/u_7b9d1e3f/balance`
    ```bash
      curl -X 'GET' \
    'https://all-or-nothing-r35u.onrender.com/users/balance' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer [INSERT USER TOKEN HERE]'
    ```
  - And recieves something like:
    ```json
    {
    "balance": 900
    }

    ```
Unfortnately her total did'nt increase meaning she lost the bet :(
     
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
  -d 'grant_type=password&username=Priya&password=string&scope=&client_id=string&client_secret='
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
