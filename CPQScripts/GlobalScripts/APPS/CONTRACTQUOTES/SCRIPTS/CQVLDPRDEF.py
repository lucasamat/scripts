# =========================================================================================================================================
#   __script_name : CQVLDPRDEF.PY
#   __script_description : THIS SCRIPT IS USED FOR PREDEFINED VALUES IN VALUE DRIVER (GETS TRIGGERED AFTER IFLOW SCRIPT - CQTVLDRIFW.py)
#   __primary_author__ : 
#   __create_date :06-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL

Sql = SQL()

Log.Info("hitted----->")
try:
    Qt_rec_id = Param.CPQ_Columns['Quote'] 
except:
    Qt_rec_id = ""
try:
    LEVEL = Param.CPQ_Columns['Level']
except:
    LEVEL = ""
#Log.Info("LEVEL ->"+str(LEVEL))
try:
    TreeParam = Param.CPQ_Columns['TreeParam']
    TreeParentParam = Param.CPQ_Columns['TreeParentParam'].replace("$$","'")
    TreeSuperParentParam = Param.CPQ_Columns['TreeSuperParentParam'].replace("$$","'")
    TreeTopSuperParentParam = Param.CPQ_Columns['TreeTopSuperParentParam']
    userId = Param.CPQ_Columns['Userid']
    userName = Param.CPQ_Columns['Username']
    quote_revision_record_id = Param.CPQ_Columns['quote_revision_record_id']
except: 
    TreeParam = ""
    TreeParentParam = ""
    TreeSuperParentParam = ""
    TreeTopSuperParentParam = ""
    userId = ""
    userName = ""
    quote_revision_record_id = ""

##fn call