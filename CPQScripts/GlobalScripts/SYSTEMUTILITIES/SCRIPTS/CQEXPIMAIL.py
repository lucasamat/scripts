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
            getting_quotes = Sql.GetFirst("SELECT OWNER_NAME,OWNER_ID,QUOTE_ID,CONTRACT_VALID_TO,QUOTE_EXPIRE_DATE FROM SAQTMT (NOLOCK) WHERE QUOTE_ID = '"+str(quotes)+"'")
            # for quote in getting_quotes:
            employee_table = Sql.GetFirst("SELECT EMAIL FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_ID = '"+str(getting_quotes.OWNER_ID)+"'")
            expiration_date = str(getting_quotes.QUOTE_EXPIRE_DATE).split(" ")[0].strip()
            Subject = "Your Quote is going to Expire in 7 Days"
            mailBody = """
                        Dear """+str(getting_quotes.OWNER_NAME)+""",<br><br>
                            This is to notify that the Quote Number """+str(getting_quotes.QUOTE_ID)+""" will be expired on """+str(expiration_date)+"""
                        <br><br>
                        Thank You 
                        """
            try:
                recepient = str(employee_table.EMAIL)
            except:
                Trace.Write("Mail not sent to "+str(getting_quotes.OWNER_NAME))
            Trace.Write("Mail sent to "+str(getting_quotes.OWNER_NAME))
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
today_current_date = now.strftime('%m/%d/%Y')
current_date_obj = str(now).split(" ")[0].strip()
today_date_obj = datetime.datetime.strptime(str(current_date_obj),"%Y-%m-%d")
today_date_string = str(today_date_obj).split(" ")[0].strip()
target_mail_date_obj = today_date_obj + timedelta(days=7)
target_mail_date_obj= target_mail_date_obj
target_mail_date = str(target_mail_date_obj).split(" ")[0].strip()
#target_mail_date = target_mail_date.replace("-","/")

expired_quotes_query = Sql.GetList("SELECT QUOTE_ID,CONVERT(nvarchar(10),QUOTE_EXPIRE_DATE,120) as QUOTE_EXPIRE_DATE FROM SAQTMT where CONVERT(nvarchar(10),QUOTE_EXPIRE_DATE,120) = '{target_mail_date}'".format(target_mail_date=target_mail_date))
###A055S000P01-12558
updatesaqtmtexpire = (""" UPDATE SAQTMT SET EXPIRED = '1' WHERE  QUOTE_EXPIRE_DATE = '{today_current_date}' AND QTEREV_STATUS NOT IN ('SUBMITTED FOR BOOKING') """.format(today_current_date = today_current_date ))
Sql.RunQuery(updatesaqtmtexpire)


expired_quotes = []
if expired_quotes_query is not None:
    for quotes in expired_quotes_query:   
        expire_date = str(quotes.QUOTE_EXPIRE_DATE).split(" ")[0]     
        #Trace.Write(" sjdhjksadhjds  "+str(target_mail_date)+ "  -  " +str(expire_date))
        if str(target_mail_date) == str(expire_date):
            expired_quotes.append(quotes.QUOTE_ID)
if expired_quotes is not None:
    expiration_obj.mailtrigger(expired_quotes)

