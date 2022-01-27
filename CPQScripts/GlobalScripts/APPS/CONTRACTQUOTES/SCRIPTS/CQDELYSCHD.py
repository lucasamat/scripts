# =========================================================================================================================================
#   __script_name : CQDELYSCHD.PY
#   __script_description : THIS SCRIPT IS USED TO  update,delete, insert in delivery schedule based on quantiy and delivery schedule change
#   __create_date : 27/01/2022
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
import sys
import System.Net

Sql = SQL()