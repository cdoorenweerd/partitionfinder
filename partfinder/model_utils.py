# Copyright (C) 2012 Robert Lanfear and Brett Calcott
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# PartitionFinder also includes the PhyML program, the RAxML program, and the
# PyParsing library, all of which are protected by their own licenses and
# conditions, using PartitionFinder implies that you agree with those licences
# and conditions as well.

import logtools
import pandas as pd
import os
from config import the_config

log = logtools.get_logger()
from util import PartitionFinderError

def get_num_params(modelstring):
    """
    Input a model string like HKY+I+G or LG+G+F, and get the number of
    parameters
    """

    m = the_config.available_models.query("name=='%s'" %modelstring).matrix_params.values[0]
    b = the_config.available_models.query("name=='%s'" %modelstring).basefreq_params.values[0]
    r = the_config.available_models.query("name=='%s'" %modelstring).ratevar_params.values[0]

    total = m+b+r

    log.debug("Model: %s Params: %d" % (modelstring, total))

    return total

def get_raxml_protein_modelstring(modelstring):
    """Start with a model like this: LG+I+G+F, return a model in raxml format like this:
    LGF. This is only used for printing out RAxML partition files
    NB. In RAxML you can't specify different rate hetero parameters in each protein model
    you have to choose either ALL +G or ALL +I+G. PartitionFinder allows you to mix and 
    match here, but if you're going to use RAxML downstream, you will need to be smarter
    and run two analyses - one with just +I+G models, and one with +G models. 

    So really all we do is add an F/X to the model name if it used +F.
    """

    elements = modelstring.split("+")
    model_name = elements[0]
    extras = elements[1:]

    raxmlstring = model_name
    if "F" in extras:
        raxmlstring = ''.join([raxmlstring, "F"])
    elif "X" in extras:
        raxmlstring = ''.join([raxmlstring, "X"])    

    return raxmlstring


