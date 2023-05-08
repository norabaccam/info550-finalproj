'''
LSAT Logic Game solver
Logic Game scenarios from: https://www.trainertestprep.com/lsat/blog/sample-lsat-logic-games
'''

from satispy import Variable, Cnf
from satispy.solver import Minisat
import time, sys
import films, product_code, recycle # KB and variables code
import numpy as np

def print_assignments(solution):
    '''
    Prints out each variable and the truth value assigned to it.
    params
    - solution: a dictionary mapping variable:truthVal assignments
    '''
    for variable, truth_val in solution.items():
        print(f"{variable} is {truth_val}")

def select_unassigned_var(sol, variables):
    '''
    Selects variable that has not been assigned a truth value.
    params
    - sol: a dictionary mapping variable:truthVal assignments
    - variables: list of Variable objects
    returns 
    - var if it is not in the sol dictionary, None otherwise
    '''
    for var in variables:
        if var not in sol:
            return var
    return None

def backtrack(sol, variables, KB, solver):
    '''
    Implements backtracking to find value assignments for each variable
    that are consistent with the KB.
    params
    - sol: a dictionary mapping variable:truthVal assignments
    - variables: list of Variable objects
    - KB: knowledge base storing sentences
    - solver: Minisat() object to check validity
    returns
    - if a valid solution is found, returns the solution dictionary and KB,
    otherwise false
    '''
    if len(sol) == len(variables):
        for var, truth_val in sol.items():
            if truth_val:
                KB &= var
            else:
                KB &= -var
        is_valid = solver.solve(KB)
        if is_valid.success:
            return sol, KB
    var = select_unassigned_var(sol, variables)
    if var:
        for truth_val in [True, False]:
            if truth_val:
                assign = var
            else:
                assign = -var
            if solver.solve(KB & assign).success:
                sol[var] = truth_val
                result = backtrack(sol, variables, KB, solver)
                if result:
                    return result
            if var in sol:
                del sol[var]
    return False

def fwd_check(sol, variables, domains, KB, solver):
    '''
    Implements forward-checking - removes values from the domains
    of future variables to maintain consistency.
    params
    - sol: a dictionary mapping variable:truthVal assignments
    - variables: list of Variable objects
    - domains: dictionary mapping variables to a list of values in the domain 
    - KB: knowledge base storing sentences
    - solver: Minisat() object to check validity
    '''
    for var in variables:
        if var not in sol:
            for truth_val in domains[var]:
                if truth_val:
                    assign = var
                else:
                    assign = -var
                if not solver.solve(KB & assign).success:
                    domains[var].remove(truth_val)

def backtrack_fwdcheck(sol, variables, domains, KB, solver):
    '''
    Implements backtracking w/ forward-checking
    params
    - sol: a dictionary mapping variable:truthVal assignments
    - variables: list of Variable objects
    - domains: dictionary mapping variables to a list of values in the domain 
    - KB: knowledge base storing sentences
    - solver: Minisat() object to check validity
    returns
    - if a valid solution is found, returns the solution dictionary and KB,
    otherwise false
    '''
    if len(sol) == len(variables):
        for var, truth_val in sol.items():
            if truth_val:
                KB &= var
            else:
                KB &= -var
        is_valid = solver.solve(KB)
        if is_valid.success:
            return sol, KB, domains
    var = select_unassigned_var(sol, variables)
    if var:
        for truth_val in domains[var]:
            if truth_val:
                assign = var
            else:
                assign = -var
            if solver.solve(KB & assign).success:
                sol[var] = truth_val
                fwd_check(sol, variables, domains, KB, solver)
                result = backtrack_fwdcheck(sol, variables, domains, KB, solver)
                if result:
                    return result
            if var in sol:
                del sol[var]
    return False

def set_rules_vars_helper(game):
    '''
    Adds sentences to KB and defines variables depending on logic game.
    params
    - game: string of which logic game to work through
    returns
    - KB, the knowledge base and variables, list of variables.
    '''
    if game == '-g1':
        KB, variables = films.set_rules_vars()
    elif game == '-g2':
        KB, variables = product_code.set_rules_vars()
    elif game == '-g3':
        KB, variables = recycle.set_rules_vars()
    return KB, variables

def solve(algorithm, KB, variables):
    '''
    Finds a valid solution to the logic game using backtracking w/ w/o forward-checking.
    params:
    - algorithm: string of which algorithm to use
    - KB: knowledge base
    - variables: list of variables
    '''
    solver = Minisat()
    domains = {var:[True, False] for var in list(np.concatenate(variables).flat)}
    for vars in variables:
        if algorithm == '-backtrack':
            sol, updated_KB = backtrack({}, vars, KB, solver)
        else:
            sol, updated_KB, updated_domains = backtrack_fwdcheck({}, vars, domains, KB, solver)
            domains = updated_domains
        KB = updated_KB
        print_assignments(sol)

def main():
    '''
    Parses arguments. Solves corresponding logic game with backtracking.
    '''
    args = sys.argv
    if len(args) == 3:
        if args[1] not in ['-g1', '-g2', '-g3']:
            exit("not valid logic game number.")
        elif args[2] not in ['-backtrack', '-fwdcheck']:
            exit("not valid algorithm.")
        game, algorithm = args[1], args[2]
        KB, variables = set_rules_vars_helper(game)
        start_time = time.time()
        solve(algorithm, KB, variables)
        print(f"My program took {round(time.time() - start_time, 2)} seconds to find a solution.")
    else:
        exit("please enter one logic game and one valid algorithm.")

main()