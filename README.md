# HyperTicTacToe

A game using tic-tac-toe board of tic-tac-toe boards

---

## Rules

To win the game, a player must complete the big tic-tac-toe grid in one of the 8 standard ways a tic-tac-toe board can be solved. 
A player can win one of the big boxes (one of the 9 boxes on the board with a tic-tac-toe board inside of it) by winning the smaller grid contained inside of it.
The catch is that, for example, if a player makes a move in the lower right corner of whichever little box they get to move in, the next move made by the other player must take place within the big box in the lower right corner of the big grid.
If that box is already taken, another suitable box will be chosen by iterating through past big boxes in which moves were to be played and checking if they can be moved in or not.

## Navigating the Repository
### Local

This directory contains working code for a local version of HyperTicTacToe with the ability to play a game with two players on the same computer and also with a bot.

**Run `Game.py` using python in order to run the game**

### Online

As of now, this directory contains unfinished code for an online version of HyperTicTacToe with the ability to connect to other players using the internet and a cloud server

**Don't run any file in this directory or you're likely to experience errors and timeouts**








