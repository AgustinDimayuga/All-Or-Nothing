# Performance Write up

Link to the python file

https://github.com/AgustinDimayuga/All-Or-Nothing/blob/V5_Million_rows/alembic/versions/4157d2058e87_1_million_rows.py

Final row counts:

Final row counts:

| Table | Rows |
|---------|---------:|
| bets | 998,085 |
| wallet | 100,000 |
| users | 100,000 |
| games | 100,000 |
| teams | 50,000 |
| leagues | 5 |
| Total | 1,348,090 |

# Justification

We all agreed our largest table in the database had to be bets since many players could place multiple bets, so we decided on close to 1 million bets. 

The users


# Performance results of hitting endpoints

`POST /bets` 7.65ms

```Bash
curl -X 'POST' \
  'http://127.0.0.1:3000/bets/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDAwMDEsIm5hbWUiOiJOaWMiLCJleHAiOjE3ODAyOTUxOTF9.4k7eHDVBO63hUvgjPbtd1QwhiacFUgr44iMd_kJzGVE' \
  -H 'Content-Type: application/json' \
  -d '{
  "game_id": 100002,
  "team": "Team_2271",
  "amount": 1
}'
```

`POST /bets/early` 91.06 ms

```Bash
curl -X 'POST' \
  'http://127.0.0.1:3000/bets/early?bet_id=998090' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDAwMDEsIm5hbWUiOiJOaWMiLCJleHAiOjE3ODAyOTUxOTF9.4k7eHDVBO63hUvgjPbtd1QwhiacFUgr44iMd_kJzGVE' \
  -d ''
```

`POST /auth/users` 202.56 ms

```Bash
curl -X 'POST' \
  'http://127.0.0.1:3000/auth/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "Storm2",
  "name": "Nice",
  "email": "l;askjf@gmail.com",
  "phone": "911111111",
  "password": "lmaoo"
}'
```

`POST /auth/tokens` 168.97 ms

```Bash
curl -X 'POST' \
  'http://127.0.0.1:3000/auth/tokens' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=Storm&password=lmao&scope=&client_id=string&client_secret=********'
```

`GET /games/` 268.20 ms

```Bash
curl -X 'GET' \
  'http://127.0.0.1:3000/games/?league=nlb&status=finished&page=1&limit=20' \
  -H 'accept: application/json'
```

`GET /games/game_details` 58.04 ms

```Bash
curl -X 'GET' \
  'http://127.0.0.1:3000/games/game_details?id=37200' \
  -H 'accept: application/json'
```

`GET /leaderboard` 190.92 ms

```Bash
curl -X 'GET' \
  'http://127.0.0.1:3000/leaderboard/?period=weekly&limit=100' \
  -H 'accept: application/json'
```

`GET /users/balance` 38.29 ms

```Bash
curl -X 'GET' \
  'http://127.0.0.1:3000/users/balance' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDAwMDEsIm5hbWUiOiJOaWMiLCJleHAiOjE3ODAyOTgxMTJ9.-LWF6NYTRRzVlyrhrPoZ4voGb2JRR_kCn-cgnZDEw-I'
```

`GET/users/me/` 0.00ms

```Bash
curl -X 'GET' \
  'http://127.0.0.1:3000/users/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDAwMDEsIm5hbWUiOiJOaWMiLCJleHAiOjE3ODAyOTgxMTJ9.-LWF6NYTRRzVlyrhrPoZ4voGb2JRR_kCn-cgnZDEw-I'
```

`GET/users/me/bets/` 103.71 ms

```Bash

curl -X 'GET' \
  'http://127.0.0.1:3000/users/me/bets?status=all&page=1&limit=20' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDAwMDEsIm5hbWUiOiJOaWMiLCJleHAiOjE3ODAzMDUxNzd9.uPODql9aMzynoe1YuC9xj1ogGhcjRN0GDvFXcs8LBoA'
```

`GET/users/me/withdraw` 32.68 ms

```Bash
curl -X 'POST' \
  'http://127.0.0.1:3000/users/me/withdraw' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDAwMDEsIm5hbWUiOiJOaWMiLCJleHAiOjE3ODAzMDY0NTJ9.rOUEM-dCSnUgfEeKnjV9oyPTy6QoF4rpP7ttyBIS4Nw' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 0
}'
```




