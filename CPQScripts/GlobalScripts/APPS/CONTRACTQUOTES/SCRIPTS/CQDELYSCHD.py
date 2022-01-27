# =========================================================================================================================================
#   __script_name : CQDELYSCHD.PY
#   __script_description : THIS SCRIPT IS USED TO  update,delete, insert in delivery schedule based on quantiy and delivery schedule change
#   __create_date : 27/01/2022
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import sys
import System.Net
import datetime
import time
from datetime import timedelta , date

Sql = SQL()

#A055S000P01-14051 start
def insert_deliveryschedule_request(rec_id,QuoteRecordId,rev_rec_id):
    Trace.Write('rec_id--'+str(rec_id))

    return 'Data'


Action =Param.Action
rec_id =Param.rec_id
QuoteRecordId = Param.QuoteRecordId
rev_rec_id = Param.rev_rec_id
if Action == "INSERT":
    insert_deliverydetails = insert_deliveryschedule_request(rec_id,QuoteRecordId,rev_rec_id)