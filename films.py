from satispy import Variable, Cnf
from satispy.solver import Minisat

import time
import numpy as np
start_time = time.time()

def set_rules_vars():
    # THURSDAY
    # any movie can be shown on thursday, as long as harvest is shown last.
    # ex: they are showing harvest first on thursday
    th_harvest_first = Variable("TH_H_F")
    th_harvest_sec = Variable("TH_H_S")
    th_harvest_third = Variable("TH_H_TH")
    # ex: they are showing greed first on thursday
    th_greed_first = Variable("TH_G_F")
    th_greed_sec = Variable("TH_G_S")
    th_greed_third = Variable("TH_G_TH") 
    # ex: they are showing limelight first on thursday
    th_ll_first = Variable("TH_LL_F")
    th_ll_sec = Variable("TH_LL_S")
    th_ll_third = Variable("TH_LL_TH") 

    # FRIDAY
    #harvest can be shown first, greed can be shown first/second, limelight can be shown first/second
    # ex: they are showing harvest first on friday
    f_harvest_first = Variable("F_H_F")
    f_harvest_sec = Variable("F_H_S") 
    f_harvest_third = Variable("F_H_TH") 
    # ex: they are showing greed first on friday
    f_greed_first = Variable("F_G_F")
    f_greed_sec = Variable("F_G_S")
    f_greed_third = Variable("F_G_TH") 
    # ex: they are showing limelight first on friday
    f_ll_first = Variable("F_LL_F")
    f_ll_sec = Variable("F_LL_S")
    f_ll_third = Variable("F_LL_TH")

    # SATURDAY
    #On Saturday either Greed or Harvest, but not both, is shown, and no film is shown after it on that day.
    # limelight can be shown first, greed can be shown first/sec, harvest can be shown first/sec
    s_harvest_first = Variable("S_H_F")
    s_harvest_sec = Variable("S_H_S")
    s_harvest_third = Variable("S_H_TH") 
    # ex: they are showing greed first on saturday
    s_greed_first = Variable("S_G_F")
    s_greed_sec = Variable("S_G_S")
    s_greed_third = Variable("S_G_TH") 
    # ex: they are showing limelight first on saturday
    s_ll_first = Variable("S_LL_F")
    s_ll_sec = Variable("S_LL_S")
    s_ll_third = Variable("S_LL_TH") 

    KB = Cnf()

    #These films will never be shown on this day and this order based on other rules.
    KB &= (-th_greed_third & -th_ll_third & -f_harvest_sec & -f_harvest_third & -f_greed_third & -f_ll_third \
        & -s_harvest_third & -s_greed_third & -s_ll_sec & -s_ll_third)

    #Each film is shown at least once during the festival but never more than once on a given day. 
    #film is either shown on thurs, fri, or sat, but not more than once on that day.
    KB &= (((th_harvest_first ^ th_harvest_sec ^ th_harvest_third) | (f_harvest_first) | (s_harvest_first ^ s_harvest_sec)) \
        & ((th_greed_first ^ th_greed_sec) | (f_greed_first ^ f_greed_sec) | (s_greed_first ^ s_greed_sec)) \
        & ((th_ll_first ^ th_ll_sec) | (f_ll_first ^ f_ll_sec) | (s_ll_first)))

    # Maintain the order of movies
    #If a movie is shown second, there has to be a movie shown first.
    #If a movie is shown third, there has to be a first and second movie.
    KB &= (th_harvest_sec >> (th_greed_first | th_ll_first))
    KB &= (th_greed_sec >> th_ll_first)
    KB &= (th_harvest_third >> ((th_ll_first ^ th_greed_first) & (th_greed_sec ^ th_ll_sec)))

    #On Friday either Greed or Limelight, but not both, is shown, and no film is shown after it on that day.
    KB &= (f_harvest_first >> (f_ll_sec ^ f_greed_sec))

    #On Saturday either Greed or Harvest, but not both, is shown, and no film is shown after it on that day.
    KB &= (s_ll_first >> (s_greed_sec ^ s_harvest_sec))

    #On each day at least one film is shown. 
    KB &= (th_greed_first | th_greed_sec | th_harvest_first | th_harvest_sec | th_harvest_third | th_ll_first | th_ll_sec) \
        & (f_greed_first | f_greed_sec | f_harvest_first | f_ll_first | f_ll_sec) \
        & (s_greed_first | s_greed_sec | s_harvest_first | s_harvest_sec | s_ll_first)

    #Films are shown one at a time.
    KB &= (th_greed_first >> (-th_harvest_first & -th_ll_first))
    KB &= (th_harvest_first >> (-th_greed_first & -th_ll_first))
    KB &= (th_ll_first >> (-th_greed_first & -th_harvest_first))

    KB &= (th_greed_sec >> (-th_harvest_sec & -th_ll_sec))
    KB &= (th_harvest_sec >> (-th_greed_sec & -th_ll_sec))
    KB &= (th_ll_sec >> (-th_greed_sec & -th_harvest_sec))

    KB &= (f_greed_first >> (-f_harvest_first & -f_ll_first))
    KB &= (f_harvest_first >> (-f_greed_first & -f_ll_first))
    KB &= (f_ll_first >> (-f_greed_first & -f_harvest_first))

    KB &= (f_greed_sec >> f_harvest_first)
    KB &= (f_ll_sec >> f_harvest_first)

    KB &= (s_greed_first >> (-s_harvest_first & -s_ll_first))
    KB &= (s_harvest_first >> (-s_greed_first & -s_ll_first))
    KB &= (s_ll_first >> (-s_greed_first & -s_harvest_first))

    KB &= (s_greed_sec >> s_ll_first)
    KB &= (s_harvest_sec >> s_ll_first)

    #On Thursday Harvest is shown, and no film is shown after it on that day.
    KB &= (th_harvest_first ^ th_harvest_third ^ th_harvest_sec)
    KB &= (th_harvest_first >> (-th_greed_sec & -th_ll_sec))

    #On Saturday either Greed or Harvest, but not both, is shown, and no film is shown after it on that day.
    KB &= (s_greed_first >> -s_harvest_sec)
    KB &= (s_greed_sec >> s_ll_first)

    KB &= (s_harvest_first >> -s_greed_first)
    KB &= (s_harvest_sec >> s_ll_first)

    th_variables = [th_harvest_first, th_harvest_sec, th_harvest_third, 
                th_greed_first, th_greed_sec, th_greed_third,
                th_ll_first, th_ll_sec, th_ll_third]
    f_variables = [f_harvest_first, f_harvest_sec, f_harvest_third,
                f_greed_first, f_greed_sec, f_greed_third,
                f_ll_first, f_ll_sec, f_ll_third]
    s_variables = [s_harvest_first, s_harvest_sec, s_harvest_third,
                s_greed_first, s_greed_sec, s_greed_third,
                s_ll_first, s_ll_sec, s_ll_third]

    variables = [th_variables, f_variables, s_variables]
    return KB, variables
