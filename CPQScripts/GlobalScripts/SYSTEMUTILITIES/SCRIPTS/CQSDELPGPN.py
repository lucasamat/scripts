#===================================================================================================================#======================
#   __script_name : CQSDELPGPN.PY
#   __script_description : THIS SCRIPT IS USED TRIGGER EMAIL WHEN QUOTE WORKFLOW STATUS IN PRICING REVIEW  .
#   __primary_author__ : PONVEL SELVAM
#   __create_date :02/25/2022
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# #====================================================================================================================#======================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQ
from datetime import *
import sys
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
Sql = SQL()
# Param = Param


class qt_pricing_review_mail_trigger:
    def __init__(self, Quote):
        self.quote = Quote

    def mailtrigger(self,QUOTE_ID,QTEREV_ID,ACTION):
        
        
        #for quotes in pricing_review:
        pricing_review = Sql.GetFirst("SELECT MEMBER_ID,MEMBER_NAME,EMAIL,QUOTE_ID FROM SAQDLT WHERE  QUOTE_RECORD_ID = '"+str(QUOTE_ID)+"' AND C4C_PARTNERFUNCTION_ID = 'PRICING PERSON'")
        Subject = "Pricing Review Status Notification"
        mailBody = """
                    Dear """+str(pricing_review.MEMBER_NAME)+""",<br><br>
                    This is to notify that the Following Quote Number """+str(pricing_review.QUOTE_ID)+""" is in Pricing Review Status.
                    <br><br>
                    Thank You
                    """
        try:
            LOGIN_CRE = Sql.GetFirst("SELECT USER_NAME,PASSWORD FROM SYCONF (NOLOCK) where Domain ='SUPPORT_MAIL'")
            mailClient = SmtpClient()
            mailClient.Host = "smtp.gmail.com"
            mailClient.Port = 587
            mailClient.EnableSsl = "true"
            mailCred = NetworkCredential()
            mailCred.UserName = str(LOGIN_CRE.USER_NAME)
            mailCred.Password = str(LOGIN_CRE.PASSWORD)
            mailClient.Credentials = mailCred
            toEmail = MailAddress(str(recepient))
            fromEmail = MailAddress(str(LOGIN_CRE.USER_NAME))
            msg = MailMessage(fromEmail, toEmail)
            msg.Subject = Subject
            msg.IsBodyHtml = True
            msg.Body = mailBody  
            mailClient.Send(msg)
        except Exception as e:
            self.exceptMessage = "SYCONUPDAL : mailtrigger : EXCEPTION : UNABLE TO TRIGGER E-EMAIL : EXCEPTION E : "+str(e)



try:
    QUOTE_ID = Param.QUOTE_ID
except:
    QUOTE_ID = ''
try:
    QTEREV_ID = Param.QTEREV_ID
except:
    QTEREV_ID = ''
try:
    ACTION = Param.ACTION
except:
    ACTION = ''
obj = qt_pricing_review_mail_trigger(Quote)   

obj.mailtrigger(QUOTE_ID,QTEREV_ID,ACTION)
