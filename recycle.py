from satispy import Variable, Cnf
from satispy.solver import Minisat


def set_rules_vars():
    KB = Cnf()
    #There are exactly three recycling centers in Rivertown: Center 1, Center 2, and Center 3. 
    #Exactly five kinds of material are recycled at these recycling centers: glass, newsprint, plastic, tin, and wood. 
    c1_glass = Variable("C1_G")
    c1_newsprint = Variable("C1_N")
    c1_plastic = Variable("C1_P")
    c1_tin = Variable("C1_T")
    c1_wood = Variable("C1_W")

    c2_glass = Variable("C2_G")
    c2_newsprint = Variable("C2_N")
    c2_plastic = Variable("C2_P")
    c2_tin = Variable("C2_T")
    c2_wood = Variable("C2_W")

    c3_glass = Variable("C3_G")
    c3_newsprint = Variable("C3_N")
    c3_plastic = Variable("C3_P")
    c3_tin = Variable("C3_T")
    c3_wood = Variable("C3_W")

    #Only one of the recycling centers recycles plastic, and that recycling center does not recycle glass.
    KB &= (c3_plastic & -c2_plastic & -c1_plastic & -c3_glass)

    #Each recycling center recycles at least two but no more than three of these kinds of material. 
    KB &= ((c1_glass & c1_tin & -c1_plastic & -c1_wood & -c1_newsprint) \
        | (c1_newsprint & c1_wood & -c1_glass & -c1_tin & -c1_plastic) \
        | (c1_tin & c1_plastic & -c1_glass & -c1_wood & -c1_newsprint) \
        | (c1_glass & c1_newsprint & c1_wood & -c1_tin & -c1_plastic) \
        | (c1_newsprint & c1_wood & c1_tin & -c1_plastic & -c1_glass) \
        | (c1_plastic & c1_wood & c1_newsprint & -c1_glass & -c1_tin))

    KB &= ((c2_glass & c2_tin & -c2_plastic & -c2_wood & -c2_newsprint) \
        | (c2_newsprint & c2_wood & -c2_glass & -c2_tin & -c2_plastic) \
        | (c2_tin & c2_plastic & -c2_glass & -c2_wood & -c2_newsprint) \
        | (c2_glass & c2_newsprint & c2_wood & -c2_tin & -c2_plastic) \
        | (c2_newsprint & c2_wood & c2_tin & -c2_plastic & -c2_glass) \
        | (c2_plastic & c2_wood & c2_newsprint & -c2_glass & -c2_tin))

    KB &= ((c3_glass & c3_tin & -c3_plastic & -c3_wood & -c3_newsprint) \
        | (c3_newsprint & c3_wood & -c3_glass & -c3_tin & -c3_plastic) \
        | (c3_tin & c3_plastic & -c3_glass & -c3_wood & -c3_newsprint) \
        | (c3_glass & c3_newsprint & c3_wood & -c3_tin & -c3_plastic) \
        | (c3_newsprint & c3_wood & c3_tin & -c3_plastic & -c3_glass) \
        | (c3_plastic & c3_wood & c3_newsprint & -c3_glass & -c3_tin))

    # The following conditions must hold:
    #Any recycling center that recycles wood also recycles newsprint.
    KB &= c1_wood >> c1_newsprint
    KB &= c2_wood >> c2_newsprint
    KB &= c3_wood >> c3_newsprint

    #Every kind of material that Center 2 recycles is also recycled at Center 1.
    KB &= c2_glass >> c1_glass
    KB &= c2_newsprint >> c1_newsprint
    KB &= c2_plastic >> c1_plastic
    KB &= c2_tin >> c1_tin
    KB &= c2_wood >> c1_wood

    c1 = [c1_glass, c1_newsprint, c1_plastic, c1_tin, c1_wood]
    c2 = [c2_glass, c2_newsprint, c2_plastic, c2_tin, c2_wood]
    c3 = [c3_glass, c3_newsprint, c3_plastic, c3_tin, c3_wood]

    variables = [c1, c2, c3]

    return KB, variables