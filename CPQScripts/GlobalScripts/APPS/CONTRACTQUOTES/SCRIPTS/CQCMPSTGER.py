#===================================================================================================================#======================
#   __script_name : CQCMPSTGER.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY ERROR MESSAGE BASED ON SCENARIO WHILE CLICKING COMPLETE STAGE.
#   __primary_author__ : Joe Ebenezer
#   __create_date :03/30/2022
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# #====================================================================================================================#======================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQ
from datetime import *
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
Sql = SQL()

def complete_stage_error():
    Trace.Write("Complete Stage Error")


ApiResponse = ApiResponseFactory.JsonResponse(complete_stage_error())