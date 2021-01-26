# HyperTicTacToe

A game using tic-tac-toe board of tic-tac-toe boards

---

## Rules

Below is a blank board where the bold lines indicate where the big boxes start and stop and where the thinner lines indicate where the small grid boxes start and stop:

![Blank Board Image](gameImages/blankBoard.png?raw=true "Blank Board")

To win the game, a player must win three consecutive big boxes (in a row, in a column, or on a diagonal). 
A player can win one of the big boxes (one of the 9 boxes on the board with a tic-tac-toe board inside of it) by winning the smaller grid contained inside of it.
The catch is that, for example, if a player makes a move in the lower right corner of whichever little box they get to move in, the next move made by the other player must take place within the big box in the lower right corner of the big grid (see location of red box). 

![Illustration of move rule](gameImages/randomMove2.png?raw=true)

Basically, each move determines where the next move must be played by taking the relative location of a move (for instance, top right corner of a small grid) and making it so that the opponent must move in the corresponding big box (in this case, the top right big box).

If that box is already taken, another suitable box will be chosen by iterating through prevous big boxes in which moves were to be played (the ones colored in red) and checking if they can be moved in or not.

## Navigating the Repository
### Local

This directory contains working code for a local version of HyperTicTacToe with the ability to play a game with two players on the same computer and also with a bot.

This game was written using Python 3.7.9 so please make sure your Python version is 3.7.9+

In order to play this game, you will need to have `pygame` installed. If it isn't already installed, you can easily install it by going to your command line and typing the following command: `pip install pygame`

To play the game, run the `Run.bat` file in the directory in the Local folder

### Online

As of now, this directory contains unfinished code for an online version of HyperTicTacToe with the ability to connect to other players using the internet and a cloud server

**Don't run any file in this directory or you're likely to experience errors and timeouts**








