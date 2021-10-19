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

def replace_account(repalce_values,acct_rec_id,table_name):
    Trace.Write("repalce_values===="+str(repalce_values))
    Trace.Write("acct_rec_id===="+str(acct_rec_id))
    Trace.Write("table_name===="+str(table_name))


try:
    repalce_values = Param.repalce_values
    acct_rec_id = Param.acct_rec_id
    table_name = Param.table_name
except:
    repalce_values ='' 
    acct_rec_id = '' 
    table_name = '' 
replace_account(repalce_values,acct_rec_id,table_name)
