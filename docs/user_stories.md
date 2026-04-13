# User Stories & Exceptions  
**Project:** All-Or-Nothing (Sports Betting Simulator API)  

---

## User Stories

1. As a new sports fan, I want to create an account, so that I can start participating in the betting simulator.

2. As a returning bettor, I want to log into my account, so that I can access my balance and continue placing bets.

3. As a casual viewer, I want to browse live and upcoming games, so that I can find interesting matches to bet on.

4. As a strategic bettor, I want to view detailed game information like teams, odds, and start times, so that I can make smarter betting decisions.

5. As a competitive player, I want to place bets using virtual currency, so that I can test my predictions against real-world outcomes.

6. As an engaged user, I want to track my active bets in real time, so that I can see how my predictions are performing.

7. As a reflective bettor, I want to review my past bets and results, so that I can improve my betting strategy over time.

8. As a careful player, I want to check my virtual currency balance, so that I can manage how much I wager.

9. As a hands-off user, I want my bets to be automatically resolved when games finish, so that I don’t have to manually track results.

10. As a competitive player, I want to view a leaderboard, so that I can see how I rank against other users.

11. As a social sports fan, I want to comment on games and bets, so that I can share opinions and interact with others.

12. As an active bettor, I want to receive updates when my bets are resolved, so that I can stay informed about my wins and losses.

---

## Exceptions / Error Scenarios

1. **Exception: Invalid login credentials**  
   If a user enters incorrect login information when trying to sign in, an error message is returned and they are asked to try again.

2. **Exception: Duplicate account creation**  
   If a user tries to create an account with an email or username that already exists, the request is rejected and they are prompted to use a different one.

3. **Exception: Insufficient balance for bet**  
   If a user attempts to place a bet without enough virtual currency, the bet is not placed and a message is shown asking them to lower the amount.

4. **Exception: Bet placed after game start**  
   If a user tries to place a bet after the game has already started, the bet is rejected and they are informed that betting is closed.

5. **Exception: Invalid bet amount**  
   If a user enters a bet amount that is zero or negative, the request is denied and they are asked to enter a valid amount.

6. **Exception: Live game data unavailable**  
   If live game data cannot be retrieved, the affected games are temporarily unavailable for betting and a notice is shown to the user.

7. **Exception: Duplicate bet submission**  
   If the same bet is submitted multiple times, only one is accepted and the duplicates are ignored with a message shown.

8. **Exception: Bet resolution failure**  
   If game results are delayed or unavailable, the bet remains pending and is updated once the results are received.

9. **Exception: Unauthorized data access**  
   If a user attempts to access another user’s information, access is denied and an authorization error is returned.

10. **Exception: Internal server error**  
   If something unexpected goes wrong, a generic error message is returned and the user is asked to try again later.

11. **Exception: Invalid game selection**  
   If a user tries to place a bet on a game that does not exist, the request is rejected and an error message is shown.

12. **Exception: Invalid comment submission**  
   If a user submits an empty or invalid comment, it is not posted and they are prompted to enter valid content.
