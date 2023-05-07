from satispy import Variable, Cnf
from satispy.solver import Minisat

def set_rules_vars():
    KB = Cnf()
    #The codes use the digits 0, 1, 2, 3, and 4, and no others.
    d1_zero = Variable("D1_0")
    d1_one = Variable("D1_1")
    d1_two = Variable("D1_2")
    d1_three = Variable("D1_3")
    d1_four = Variable("D1_4")

    d2_zero = Variable("D2_0")
    d2_one = Variable("D2_1")
    d2_two = Variable("D2_2")
    d2_three = Variable("D2_3")
    d2_four = Variable("D2_4")

    d3_zero = Variable("D3_0")
    d3_one = Variable("D3_1")
    d3_two = Variable("D3_2")
    d3_three = Variable("D3_3")
    d3_four = Variable("D3_4")

    d4_zero = Variable("D4_0")
    d4_one = Variable("D4_1")
    d4_two = Variable("D4_2")
    d4_three = Variable("D4_3")
    d4_four = Variable("D4_4")

    d5_zero = Variable("D5_0")
    d5_one = Variable("D5_1")
    d5_two = Variable("D5_2")
    d5_three = Variable("D5_3")
    d5_four = Variable("D5_4")
    #Each digit occurs exactly once in any code.
    #each index can only have on value assigned to it

    # the digit in the first place can only be one or two
    KB &= (-d1_zero & -d1_three & -d1_four)
    KB &= (d1_one >> (-d2_one & -d3_one & -d4_one & -d5_one & -d1_two))
    KB &= (d1_two >> (-d2_two & -d3_two & -d4_two & -d5_two & -d1_one))

    # the digit in the second place can only be two or four
    KB &= (-d2_zero & -d2_one & -d2_three)
    KB &= (d2_two >> (-d2_four & -d1_two & -d3_two & -d4_two & -d5_two))
    KB &= (d2_four >> (-d2_two & -d1_four & -d3_four & -d4_four & -d5_four))

    # the digit in third place cannot be four
    KB &= -d3_four
    KB &= d3_zero >> (-d2_zero & -d1_zero & -d4_zero & -d5_zero & -d3_one & -d3_two & -d3_three)
    KB &= d3_one >> (-d2_one & -d1_one & -d4_one & -d5_one & -d3_zero & -d3_two & -d3_three)
    KB &= d3_two >> (-d2_two & -d1_two & -d4_two & -d5_two & -d3_zero & -d3_one & -d3_three)
    KB &= d3_three >> (-d2_three & -d1_three & -d4_three & -d5_three & -d3_zero & -d3_two & -d3_one)

    KB &= d4_zero >> (-d2_zero & -d3_zero & -d1_zero & -d5_zero & -d4_one & -d4_two & -d4_three & -d4_four)
    KB &= d4_one >> (-d2_one & -d3_one & -d1_one & -d5_one & -d4_zero & -d4_two & -d4_three & -d4_four)
    KB &= d4_two >> (-d2_two & -d3_two & -d1_two & -d5_two & -d4_one & -d4_zero & -d4_three & -d4_four)
    KB &= d4_three >> (-d2_three & -d3_three & -d1_three & -d5_three & -d4_one & -d4_two & -d4_zero & -d4_four)
    KB &= d4_four >> (-d2_four & -d3_four & -d1_four & -d5_four & -d4_one & -d4_two & -d4_three & -d4_zero)

    #the digit in the fifth place cannot be zero
    KB &= (-d5_zero)
    KB &= d5_one >> (-d2_one & -d3_one & -d4_one & -d1_one & -d5_two & -d5_three & -d5_four)
    KB &= d5_two >> (-d2_two & -d3_two & -d4_two & -d1_two & -d5_one & -d5_three & -d5_four)
    KB &= d5_three >> (-d2_three & -d3_three & -d4_three & -d1_three & -d5_two & -d5_one & -d5_four)
    KB &= d5_four >> (-d2_four & -d3_four & -d4_four & -d1_four & -d5_two & -d5_three & -d5_one)

    #The second digit has a value exactly twice that of the first digit.
    KB &= (d1_one >> d2_two)
    KB &= (d1_two >> d2_four)

    #The value of the third digit is less than the value of the fifth digit.
    KB &= d5_four >> (d3_three ^ d3_two ^ d3_one ^ d3_zero)
    KB &= d5_three >> (d3_two ^ d3_one ^ d3_zero)
    KB &= d5_two >> (d3_one ^ d3_zero)
    KB &= d5_one >> d3_zero

    digit_one = [d1_zero, d1_one, d1_two, d1_three, d1_four]
    digit_two = [d2_zero, d2_one, d2_two, d2_three, d2_four]
    digit_three = [d3_zero, d3_one, d3_two, d3_three, d3_four]
    digit_four = [d4_zero, d4_one, d4_two, d4_three, d4_four]
    digit_five = [d5_zero, d5_one, d5_two, d5_three, d5_four]

    variables = [digit_one, digit_two, digit_three, digit_four, digit_five]
  
    return KB, variables
