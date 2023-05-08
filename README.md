# Solving LSAT Logic Games using Propositional Logic and Backtracking
Nora Baccam, INFO 550 Spring 2023 Final Project

## Files
- `solver.py` is the main script. Run this file in the command line with one of the following arguments - e.g., `python solver.py [-g1, -g2, -g3] [-backtrack, -fwdcheck]`. `-g1` is the Film Festival game, `-g2` is the Five Digit Code game, and `-g3` is the Recycling Center game. Will print out the valid assignments found through backtracking, and how long it took to run.
- `product_code.py`, `films.py` and `recycle.py` store the code that build the KB and variables.


## References
- LSAT Logic Game scenarios taken from here: https://www.trainertestprep.com/lsat/blog/sample-lsat-logic-games 
- Satispy GitHub repo: https://github.com/netom/satispy
