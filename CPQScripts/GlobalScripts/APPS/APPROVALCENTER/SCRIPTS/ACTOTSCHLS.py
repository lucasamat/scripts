# =========================================================================================================================================
#   __script_name : ACTOTSCHLS.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE THE APPROVAL DATES IN APPROVAL CNETER MASTER TABLE
#   __primary_author__ : VIJAYAKUMAR THANGARASU
#   __create_date : 08/09/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# [CPQ-COM] CATEGORY (AND SUBCATEGORY)
import Webcom.Configurator.Scripting.Test.TestProduct
from datetime import datetime
from SYDATABASE import SQL

Sql = SQL()

datetime_value = datetime.now()
GetALlRecord = Sql.GetList("SELECT * FROM ACAPMA (NOLOCK) ")
for eachRecord in GetALlRecord:
    Totaldays = Sql.GetFirst(
        """SELECT * FROM ACAPMA (NOLOCK) WHERE APPROVAL_RECORD_ID = '{approvalrecId}' 
    AND APRSTAMAP_APPROVALSTATUS = 'REQUESTED'  """.format(
            approvalrecId=str(eachRecord.APPROVAL_RECORD_ID)
        )
    )
    if Totaldays is not None:
        # if str(Totaldays.FIN_APPROVE_DATE) =='' and str(Totaldays.REJECT_DATE) =='':
        RequestedDate = str(Totaldays.REQUEST_DATE)
        datetimeconvert = datetime_value.strftime("%m/%d/%Y")
        changeRequestdate = datetime.strptime(RequestedDate, "%m/%d/%Y")
        Changecurrentdate = datetime.strptime(datetimeconvert, "%m/%d/%Y")
        remaindatesubForTotal = str(Changecurrentdate - changeRequestdate)
        Totalremaindate = str(remaindatesubForTotal.split(" ")[0])
        if str(Totalremaindate).startswith("0:00:", 0) == True:
            Totalremaindate = "0"

        CurrentsepEntry = str(Totaldays.CUR_APRCHNSTP_ENTRYDATE).split(" ")[0]
        changeCurrentsepEntry = datetime.strptime(CurrentsepEntry, "%m/%d/%Y")
        remaindatesubforStep = str(Changecurrentdate - changeCurrentsepEntry)
        Stepremaindate = str(remaindatesubforStep.split(" ")[0])
        if str(Stepremaindate).startswith("0:00:", 0) == True:
            Stepremaindate = "0"
        
        QueryStatement = """update ACAPMA set TOTALDAYS_IN_APPROVAL='{Totalremaindate}',TOTALDAYS_IN_APRCHNSTP='{Stepremaindate}' WHERE APPROVAL_RECORD_ID = '{approvalrecId}'  """.format(
            approvalrecId=str(eachRecord.APPROVAL_RECORD_ID), Totalremaindate=Totalremaindate, Stepremaindate=Stepremaindate
        )
        Sql.RunQuery(QueryStatement)
