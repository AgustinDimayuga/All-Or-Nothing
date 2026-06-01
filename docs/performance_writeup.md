# Performance Write up

Link to the python file

https://github.com/AgustinDimayuga/All-Or-Nothing/blob/V5_Million_rows/alembic/versions/4157d2058e87_1_million_rows.py


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

The slowest endpoint we have is `GET /games/` at 268.20 ms

### Running explain analyze gives us this

```text
Limit  (cost=4065.74..4065.74 rows=1 width=144) (actual time=61.222..62.995 rows=20.00 loops=1)
  Buffers: shared hit=121347
  ->  Sort  (cost=4065.73..4065.74 rows=2 width=144) (actual time=61.197..62.986 rows=220.00 loops=1)
        Sort Key: games.date
        Sort Method: top-N heapsort  Memory: 80kB
        Buffers: shared hit=121347
        ->  Gather  (cost=1000.74..4065.72 rows=2 width=144) (actual time=0.307..58.094 rows=19958.00 loops=1)
              Workers Planned: 1
              Workers Launched: 1
              Buffers: shared hit=121347
              ->  Nested Loop  (cost=0.74..3065.52 rows=1 width=144) (actual time=0.050..53.849 rows=9979.00 loops=2)
                    Buffers: shared hit=121347
                    ->  Nested Loop  (cost=0.45..3061.02 rows=1 width=106) (actual time=0.042..37.995 rows=9979.00 loops=2)
                          Buffers: shared hit=61473
                          ->  Nested Loop  (cost=0.16..3056.52 rows=1 width=100) (actual time=0.031..21.783 rows=9979.00 loops=2)
                                Buffers: shared hit=1598
                                ->  Parallel Seq Scan on games  (cost=0.00..3047.59 rows=294 width=72) (actual time=0.010..7.500 rows=50000.00 loops=2)
                                      Filter: (CASE WHEN (now() < date) THEN 'upcoming'::text WHEN (now() < (date + '02:00:00'::interval)) THEN 'live'::text ELSE 'finished'::text END = 'finished'::text)
                                      Rows Removed by Filter: 0
                                      Buffers: shared hit=1577
                                ->  Memoize  (cost=0.16..0.28 rows=1 width=36) (actual time=0.000..0.000 rows=0.20 loops=100000)
                                      Cache Key: games.league_id
                                      Cache Mode: logical
                                      Hits: 48874  Misses: 5  Evictions: 0  Overflows: 0  Memory Usage: 1kB
                                      Buffers: shared hit=21
                                      Worker 0:  Hits: 51116  Misses: 5  Evictions: 0  Overflows: 0  Memory Usage: 1kB
                                      ->  Index Scan using leagues_pkey on leagues  (cost=0.15..0.27 rows=1 width=36) (actual time=0.003..0.003 rows=0.20 loops=10)
                                            Index Cond: (id = games.league_id)
                                            Filter: ((name)::text = 'nlb'::text)
                                            Rows Removed by Filter: 1
                                            Index Searches: 10
                                            Buffers: shared hit=21
                          ->  Index Scan using teams_pkey on teams home_team  (cost=0.29..4.49 rows=1 width=14) (actual time=0.001..0.001 rows=1.00 loops=19958)
                                Index Cond: (id = games.home_team_id)
                                Index Searches: 19958
                                Buffers: shared hit=59875
                    ->  Index Scan using teams_pkey on teams away_team  (cost=0.29..4.49 rows=1 width=14) (actual time=0.001..0.001 rows=1.00 loops=19958)
                          Index Cond: (id = games.away_team_id)
                          Index Searches: 19958
                          Buffers: shared hit=59874

```                          
Planning:
Buffers: shared hit=12
Planning Time: 0.307 ms
Execution Time: 63.027 ms


Indexes added to speed up the query 

CREATE INDEX idx_games_date
ON games (date);

CREATE INDEX idx_games_league_id
ON games (league_id);

### After adding the indexes

```text
Limit  (cost=239.28..263.12 rows=20 width=112) (actual time=15.127..15.810 rows=20.00 loops=1)
  Buffers: shared hit=2510 read=4
  ->  Nested Loop  (cost=0.88..23828.93 rows=19990 width=112) (actual time=0.842..15.769 rows=220.00 loops=1)
        Buffers: shared hit=2510 read=4
        ->  Nested Loop  (cost=0.59..17245.20 rows=19990 width=106) (actual time=0.454..8.871 rows=220.00 loops=1)
              Buffers: shared hit=1850 read=4
              ->  Nested Loop  (cost=0.30..10661.47 rows=19990 width=100) (actual time=0.391..2.043 rows=220.00 loops=1)
                    Join Filter: (games.league_id = leagues.id)
                    Rows Removed by Join Filter: 969
                    Buffers: shared hit=1190 read=4
                    ->  Index Scan using idx_games_date on games  (cost=0.30..9161.17 rows=99949 width=72) (actual time=0.291..1.475 rows=1189.00 loops=1)
                          Index Cond: (date <= (now() - '02:00:00'::interval))
                          Index Searches: 1
                          Buffers: shared hit=1189 read=4
                    ->  Materialize  (cost=0.00..1.07 rows=1 width=36) (actual time=0.000..0.000 rows=1.00 loops=1189)
                          Storage: Memory  Maximum Storage: 17kB
                          Buffers: shared hit=1
                          ->  Seq Scan on leagues  (cost=0.00..1.06 rows=1 width=36) (actual time=0.069..0.070 rows=1.00 loops=1)
                                Filter: ((name)::text = 'nlb'::text)
                                Rows Removed by Filter: 4
                                Buffers: shared hit=1
              ->  Index Scan using teams_pkey on teams home_team  (cost=0.29..0.33 rows=1 width=14) (actual time=0.030..0.030 rows=1.00 loops=220)
                    Index Cond: (id = games.home_team_id)
                    Index Searches: 220
                    Buffers: shared hit=660
        ->  Index Scan using teams_pkey on teams away_team  (cost=0.29..0.33 rows=1 width=14) (actual time=0.031..0.031 rows=1.00 loops=220)
              Index Cond: (id = games.away_team_id)
              Index Searches: 220
              Buffers: shared hit=660
```


Planning:
Buffers: shared hit=48 read=4
Planning Time: 5.629 ms
Execution Time: 16.167 ms








