# Secret Santa Probability Tracker

### In traditional Secret Santa, names are drawn from a hat in a circle.
### If you pull your own name, you put your name back in the hat and pull a new one.
### If the last player chooses his own name, he swaps with the second to last player.
### If the order in which participants draw names is known, there's a bias in this system.

### This program takes that bias in mind and calculates the probability matrix of any player being assigned to any other given player using recursive logic.
For small groups, exact probabilities are calculated.
For larger groups, probabilities are found via a Monte Carlo simulation to save processing time
(the difference between this method and exact calculations is negligible for large groups).

Watch this Numberphile video to learn more about Secret Santa's bias:
https://www.youtube.com/watch?v=5kC5k5QBqcc

## Use this program if you want to gain an upper hand in guessing who you or your friends' Secret Santa gifters are! (the bias is most noticable in small groups)

# How to use:

## Requirements
- Python 3.x
- matplotlib

## Run
1. Open your terminal or command prompt
2. Navigate to your project folder:
  cd <file-path-to-your-project-folder>
3. Install required packages:
  pip install -r requirements.txt
4. Run the program:
  python main.py