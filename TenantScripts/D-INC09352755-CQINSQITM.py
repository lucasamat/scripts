import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import CQPARTIFLW
import CQCPQC4CWB
import time
import re
import datetime
import time
import System.Net
from System import Convert
from System.Text.Encoding import UTF8
Sql = SQL()


try:
    contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
    contract_quote_rec_id = ''
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")	
except:
    quote_revision_record_id =  ""

quote_revision_obj = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,QUOTE_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
check_contract_obj = Sql.GetFirst("SELECT COUNT(*) as CNT FROM SAQCYR (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
if quote_revision_obj and check_contract_obj.CNT == 0:
            contract_header_start_date = quote_revision_obj.CONTRACT_VALID_FROM
            contract_header_start_datetime = datetime.datetime.strptime(str(quote_revision_obj.CONTRACT_VALID_FROM).split(' ')[0], '%m/%d/%Y')
            contract_header_end_datetime = datetime.datetime.strptime(str(quote_revision_obj.CONTRACT_VALID_TO).split(' ')[0], '%m/%d/%Y')
            contract_header_end_date = contract_header_end_datetime
            contract_datediff = contract_header_end_datetime - contract_header_start_datetime
            avgyear = 365.2425       # pedants definition of a year length with leap years
            avgmonth = 365.2425/12.0  # even leap years have 12 months
            years, remainder = divmod(contract_datediff.days, avgyear)
            years, months = int(years), (remainder / avgmonth) #INC08814916 - M
            if months > 0:
                years += 1 
            yearwise_dates_dict = {}
            for year in range(1, years+1):
                # Find yearwise start and end date till contract end - start
                date_obj = Sql.GetFirst("""SELECT DATEADD(day,-1,DATEADD(year, {YearIncrement}, '{DateString}')) AS EndDate, DATEADD(year, {YearIncrement}, '{DateString}') AS StartDate""".format(DateString=contract_header_start_date, YearIncrement=year))
                yearwise_start_date = datetime.datetime.strptime(str(date_obj.StartDate).split(' ')[0], '%m/%d/%Y')
                yearwise_end_date = datetime.datetime.strptime(str(date_obj.EndDate).split(' ')[0], '%m/%d/%Y')
                if year == 1:
                    yearwise_dates_dict[year] = {'YEAR':'YEAR '+str(year),'start_date':contract_header_start_datetime.date()}
                year_end_date = yearwise_end_date.date()
                if contract_header_end_date.date() < year_end_date:
                    year_end_date = contract_header_end_date.date()
                    yearwise_dates_dict[year].update({'end_date':contract_header_end_datetime.date()})
                else:
                    yearwise_dates_dict[year].update({'end_date':yearwise_end_date})
                if year+1 <= years:
                    yearwise_dates_dict[year+1] = {'YEAR':'YEAR '+str(year+1),'start_date':yearwise_start_date}
                # Find yearwise start and end date till contract end - end
            datas = []
            modified_date = str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            columns = 'CONTRACT_END_DATE,CONTRACT_START_DATE,CNTYER,QUOTE_RECORD_ID,QUOTE_ID,QTEREV_RECORD_ID,QTEREV_ID,CpqTableEntryModifiedBy,CpqTableEntryDateModified'
            for val in yearwise_dates_dict.Values:
                datas.append([str(val['end_date']),str(val['start_date']),val['YEAR'],contract_quote_rec_id,quote_revision_obj.QUOTE_ID,quote_revision_record_id,quote_revision_obj.QTEREV_ID,modified_date])
            dates_temp = (", ".join(map(str,[str(tuple(data)) for data in datas],)).replace("None", "null").replace("'", "''"))
#insert = SqlHelper.GetFirst("sp_executesql @T=N'INSERT INTO SAQCYR ("+str(columns)+") SELECT DISTINCT "+str(columns)+" FROM (VALUES "+str(dates_temp)+") AS TEMP("+str(columns)+") ' ")