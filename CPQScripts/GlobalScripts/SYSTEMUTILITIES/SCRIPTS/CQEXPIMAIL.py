from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQ
from datetime import *
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
Sql = SQL()
# Param = Param


class qt_expiration_mail_trigger:
    def __init__(self, Quote):
        self.quote = Quote

    def mailtrigger(self,expired_quotes):
        Trace.Write("Mail Sending Function"+str(expired_quotes))
        for quotes in expired_quotes:
            getting_quotes = Sql.GetList("SELECT OWNER_NAME,QUOTE_ID,CONTRACT_VALID_TO,QUOTE_EXPIRE_DATE FROM SAQTMT (NOLOCK) WHERE QUOTE_ID = '"+str(quotes)+"'")
            for quote in getting_quotes:
                employee_table = Sql.GetFirst("SELECT EMAIL FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_NAME = '"+str(quote.OWNER_NAME)+"'")
                expiration_date = str(quote.QUOTE_EXPIRE_DATE).split(" ")[0].strip()
                Subject = "Your Quote is going to Expire in 7 Days"
                mailBody = """
                            Dear """+str(quote.OWNER_NAME)+""",<br><br>
                                This is to notify that the Quote Number """+str(quote.QUOTE_ID)+""" will be expired on """+str(expiration_date)+"""
                            <br><br>
                            Thank You 
                            """
                try:
                    recepient = str(employee_table.EMAIL)
                except:
                    Trace.Write("Mail not sent to "+str(quote.OWNER_NAME))
                Trace.Write("Mail sent to "+str(quote.OWNER_NAME))
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
                    Trace.Write("Mail Sent Successfully")
                    #Quote.GetCustomField("quote_expiration_mail").Content = "FALSE"
                except Exception as e:
                    self.exceptMessage = "SYCONUPDAL : mailtrigger : EXCEPTION : UNABLE TO TRIGGER E-EMAIL : EXCEPTION E : "+str(e)
                    Trace.Write(self.exceptMessage)
        return True


expiration_obj = qt_expiration_mail_trigger(Quote)

now = datetime.datetime.now()
current_date_obj = str(now).split(" ")[0].strip()
today_date_obj = datetime.datetime.strptime(str(current_date_obj),"%Y-%m-%d")
today_date_string = str(today_date_obj).split(" ")[0].strip()
target_mail_date_obj = today_date_obj + timedelta(days=7)
target_mail_date_obj= target_mail_date_obj.strftime('%m-%d-%Y')
target_mail_date = str(target_mail_date_obj).split(" ")[0].strip()
target_mail_date = target_mail_date.replace("-","/")
target_mail_date = "10/15/2022"
today_date_string ="12/9/2022"


expired_quotes_query = SqlHelper.GetList("SELECT QUOTE_ID,QUOTE_EXPIRE_DATE FROM SAQTMT where QUOTE_EXPIRE_DATE != '' AND OWNER_ID = 'X0123347'")


expired_quotes = []
if expired_quotes_query is not None:
    for quotes in expired_quotes_query:   
        expire_date = str(quotes.QUOTE_EXPIRE_DATE).split(" ")[0]

        Log.Info("Entered ---today_date_string"+str(today_date_string))
        Log.Info("Entered expire_date"+str(expire_date))
        if str(today_date_string) == str(expire_date):
            Log.Info("Entered QUOTE_ID"+str(quotes.QUOTE_ID))
            updatesaqtmtexpire = (""" UPDATE SAQTMT SET EXPIRED = '1' WHERE QUOTE_ID = '{quoteid}' """.format(quoteid = quotes.QUOTE_ID))
            #Sql.RunQuery(updatesaqtmtexpire)
        if str(target_mail_date) == str(expire_date):
            expired_quotes.append(quotes.QUOTE_ID)
if expired_quotes is not None:
    expiration_obj.mailtrigger(expired_quotes)
