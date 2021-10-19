# =========================================================================================================================================
#   __script_name : CQRPLACTCT.PY
#   __script_description : THIS SCRIPT IS USED TO REPLACE ACCOUNT AND CONTACT WHEN USER CLICKS ON REPLACE BUTTON ON A RELATED LIST RECORD.
#   __primary_author__ : WASIM ABDUL
#   __create_date : 19/10/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
#from datetime import datetime
#from datetime import datetime
#import time
Sql = SQL()
ScriptExecutor = ScriptExecutor

def replace_account(Values,acctid):
    Trace.Write("q"+str(Values))
    Trace.Write("q2"+str(acctid))


try:
    Values = Param.Values
    acctid = Param.acctid
except:
    Values ='' 
    acctid = ''  
update_document_type(Values,acctid)
