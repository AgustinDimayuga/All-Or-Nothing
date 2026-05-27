# Concurrency Control in All-Or-Nothing
 
## Case 1 — Lost Update: Double Spend on `POST /bets`
 
### Phenomenon: Lost Update
 
Two concurrent bet requests from the same user both read the balance before either commits. Both see a sufficient balance. Both proceed to deduct. One deduction overwrites the other, and the user effectively spends the same money twice, therefore balance goes negative, or one update is gone and data shows as if only 1 bet was placed. 

 
