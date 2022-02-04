# =========================================================================================================================================
#   __script_name : CQDOCUGENR.PY
#   __script_description : DOCUMENT GENERATION IN CONTRACT QUOTES APP (GETS TRIGGERED AFTER IFLOW SCRIPT - CQDOCIFLOW.py)
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date :24-11-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import datetime
from datetime import date
from SYDATABASE import SQL

Sql = SQL()
UserId = str(User.Id)
UserName = str(User.UserName)

def englishdoc():
	Log.Info("enlgish doc RECID------")
	quoteid = SqlHelper.GetFirst("SELECT QUOTE_ID, MASTER_TABLE_QUOTE_RECORD_ID,QUOTE_NAME,C4C_QUOTE_ID, QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	Quote=QuoteHelper.Edit(quoteid.C4C_QUOTE_ID)
	qtqdoc="""INSERT SAQDOC (
						QUOTE_DOCUMENT_RECORD_ID,
						DOCUMENT_ID,
						DOCUMENT_NAME,
						DOCUMENT_PATH,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						LANGUAGE_ID,
						LANGUAGE_NAME,
						LANGUAGE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						STATUS,
						QTEREV_ID,
						QTEREV_RECORD_ID
						)SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
						'Pending' AS DOCUMENT_ID,
						'' AS DOCUMENT_NAME,
						'' AS DOCUMENT_PATH,
						'{quoteid}' AS QUOTE_ID,
						'{quotename}' AS QUOTE_NAME,
						'{quoterecid}' AS QUOTE_RECORD_ID,
						'EN' AS LANGUAGE_ID,
						'English' AS LANGUAGE_NAME,
						MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY,
						'{dateadded}' as CPQTABLEENTRYDATEADDED,
						'{UserId}' as CpqTableEntryModifiedBy,
						'{date}' as CpqTableEntryDateModified,
						'PENDING' as STATUS
						FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'English'""".format(quoteid=quoteid.QUOTE_ID,quotename=quoteid.QUOTE_NAME,quoterecid=recid,UserName=UserName,dateadded=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
	#Log.Info(qtqdoc)
	Sql.RunQuery(qtqdoc)
	
	SUM_YEAR1 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '1' AND BILLING_INTERVAL IS NULL" +" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR2 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '2' AND BILLING_INTERVAL IS NULL" +" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR3 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '3' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR4 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '4' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR5 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '5' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")


	M1_Y1 = SUM_YEAR1.MONTH_1
	Quote.SetGlobal('M1_Y1', str(M1_Y1))
	M2_Y1 = SUM_YEAR1.MONTH_2
	Quote.SetGlobal('M2_Y1', str(M2_Y1))
	M3_Y1 = SUM_YEAR1.MONTH_3
	Quote.SetGlobal('M3_Y1', str(M3_Y1))
	M4_Y1 = SUM_YEAR1.MONTH_4
	Quote.SetGlobal('M4_Y1', str(M4_Y1))
	M5_Y1 = SUM_YEAR1.MONTH_5
	Quote.SetGlobal('M5_Y1', str(M5_Y1))
	M6_Y1 = SUM_YEAR1.MONTH_6
	Quote.SetGlobal('M6_Y1', str(M6_Y1))
	M7_Y1 = SUM_YEAR1.MONTH_7
	Quote.SetGlobal('M7_Y1', str(M7_Y1))
	M8_Y1 = SUM_YEAR1.MONTH_8
	Quote.SetGlobal('M8_Y1', str(M8_Y1))
	M9_Y1 = SUM_YEAR1.MONTH_9
	Quote.SetGlobal('M9_Y1', str(M9_Y1))
	M10_Y1 = SUM_YEAR1.MONTH_10
	Quote.SetGlobal('M10_Y1', str(M10_Y1))
	M11_Y1 = SUM_YEAR1.MONTH_11
	Quote.SetGlobal('M11_Y1', str(M11_Y1))
	M12_Y1 = SUM_YEAR1.MONTH_12
	Quote.SetGlobal('M12_Y1', str(M12_Y1))

	M1_Y2 = SUM_YEAR2.MONTH_1
	Quote.SetGlobal('M1_Y2', str(M1_Y2))
	M2_Y2 = SUM_YEAR2.MONTH_2
	Quote.SetGlobal('M2_Y2', str(M2_Y2))
	M3_Y2 = SUM_YEAR2.MONTH_3
	Quote.SetGlobal('M3_Y2', str(M3_Y2))
	M4_Y2 = SUM_YEAR2.MONTH_4
	Quote.SetGlobal('M4_Y2', str(M4_Y2))
	M5_Y2 = SUM_YEAR2.MONTH_5
	Quote.SetGlobal('M5_Y2', str(M5_Y2))
	M6_Y2 = SUM_YEAR2.MONTH_6
	Quote.SetGlobal('M6_Y2', str(M6_Y2))
	M7_Y2 = SUM_YEAR2.MONTH_7
	Quote.SetGlobal('M7_Y2', str(M7_Y2))
	M8_Y2 = SUM_YEAR2.MONTH_8
	Quote.SetGlobal('M8_Y2', str(M8_Y2))
	M9_Y2 = SUM_YEAR2.MONTH_9
	Quote.SetGlobal('M9_Y2', str(M9_Y2))
	M10_Y2 = SUM_YEAR2.MONTH_10
	Quote.SetGlobal('M10_Y2', str(M10_Y2))
	M11_Y2 = SUM_YEAR2.MONTH_11
	Quote.SetGlobal('M11_Y2', str(M11_Y2))
	M12_Y2 = SUM_YEAR2.MONTH_12
	Quote.SetGlobal('M12_Y2', str(M12_Y2))

	M1_Y3 = SUM_YEAR3.MONTH_1
	Quote.SetGlobal('M1_Y3', str(M1_Y3))
	M2_Y3 = SUM_YEAR3.MONTH_2
	Quote.SetGlobal('M2_Y3', str(M2_Y3))
	M3_Y3 = SUM_YEAR3.MONTH_3
	Quote.SetGlobal('M3_Y3', str(M3_Y3))
	M4_Y3 = SUM_YEAR3.MONTH_4
	Quote.SetGlobal('M4_Y3', str(M4_Y3))
	M5_Y3 = SUM_YEAR3.MONTH_5
	Quote.SetGlobal('M5_Y3', str(M5_Y3))
	M6_Y3 = SUM_YEAR3.MONTH_6
	Quote.SetGlobal('M6_Y3', str(M6_Y3))
	M7_Y3 = SUM_YEAR3.MONTH_7
	Quote.SetGlobal('M7_Y3', str(M7_Y3))
	M8_Y3 = SUM_YEAR3.MONTH_8
	Quote.SetGlobal('M8_Y3', str(M8_Y3))
	M9_Y3 = SUM_YEAR3.MONTH_9
	Quote.SetGlobal('M9_Y3', str(M9_Y3))
	M10_Y3 = SUM_YEAR3.MONTH_10
	Quote.SetGlobal('M10_Y3', str(M10_Y3))
	M11_Y3 = SUM_YEAR3.MONTH_11
	Quote.SetGlobal('M11_Y3', str(M10_Y3))
	M12_Y3 = SUM_YEAR3.MONTH_12
	Quote.SetGlobal('M12_Y3', str(M12_Y3))

	M1_Y4 = SUM_YEAR4.MONTH_1
	Quote.SetGlobal('M1_Y4', str(M1_Y4))
	M2_Y4 = SUM_YEAR4.MONTH_2
	Quote.SetGlobal('M2_Y4', str(M2_Y4))
	M3_Y4 = SUM_YEAR4.MONTH_3
	Quote.SetGlobal('M3_Y4', str(M3_Y4))
	M4_Y4 = SUM_YEAR4.MONTH_4
	Quote.SetGlobal('M4_Y4', str(M4_Y4))
	M5_Y4 = SUM_YEAR4.MONTH_5
	Quote.SetGlobal('M5_Y4', str(M5_Y4))
	M6_Y4 = SUM_YEAR4.MONTH_6
	Quote.SetGlobal('M6_Y4', str(M6_Y4))
	M7_Y4 = SUM_YEAR4.MONTH_7
	Quote.SetGlobal('M7_Y4', str(M7_Y4))
	M8_Y4 = SUM_YEAR4.MONTH_8
	Quote.SetGlobal('M8_Y4', str(M8_Y4))
	M9_Y4 = SUM_YEAR4.MONTH_9
	Quote.SetGlobal('M9_Y4', str(M9_Y4))
	M10_Y4 = SUM_YEAR4.MONTH_10
	Quote.SetGlobal('M10_Y4', str(M10_Y4))
	M11_Y4 = SUM_YEAR4.MONTH_11
	Quote.SetGlobal('M11_Y4', str(M11_Y4))
	M12_Y4 = SUM_YEAR4.MONTH_12
	Quote.SetGlobal('M12_Y4', str(M12_Y4))

	M1_Y5 = SUM_YEAR5.MONTH_1
	Quote.SetGlobal('M1_Y5', str(M1_Y5))
	M2_Y5 = SUM_YEAR5.MONTH_2
	Quote.SetGlobal('M2_Y5', str(M2_Y5))
	M3_Y5 = SUM_YEAR5.MONTH_3
	Quote.SetGlobal('M3_Y5', str(M3_Y5))
	M4_Y5 = SUM_YEAR5.MONTH_4
	Quote.SetGlobal('M4_Y5', str(M4_Y5))
	M5_Y5 = SUM_YEAR5.MONTH_5
	Quote.SetGlobal('M5_Y5', str(M5_Y5))
	M6_Y5 = SUM_YEAR5.MONTH_6
	Quote.SetGlobal('M6_Y5', str(M6_Y5))
	M7_Y5 = SUM_YEAR5.MONTH_7
	Quote.SetGlobal('M7_Y5', str(M7_Y5))
	M8_Y5 = SUM_YEAR5.MONTH_8
	Quote.SetGlobal('M8_Y5', str(M8_Y5))
	M9_Y5 = SUM_YEAR5.MONTH_9
	Quote.SetGlobal('M9_Y5', str(M9_Y5))
	M10_Y5 = SUM_YEAR5.MONTH_10
	Quote.SetGlobal('M10_Y5', str(M10_Y5))
	M11_Y5 = SUM_YEAR5.MONTH_11
	Quote.SetGlobal('M11_Y5', str(M11_Y5))
	M12_Y5 = SUM_YEAR5.MONTH_12
	Quote.SetGlobal('M12_Y5', str(M12_Y5))

	GetYear1EndDate = SqlHelper.GetFirst("""SELECT
   ID,
   (SELECT MAX(convert(date, LastUpdateDate))
      FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
   AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '1' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")

	#DATES_YEAR_1 = SqlHelper.GetFirst("SELECT MONTH_1, MONTH_1, MONTH_2, MONTH_3, MONTH_4, MONTH_5, MONTH_6, MONTH_7, MONTH_8, MONTH_9, MONTH_10, MONTH_10, MONTH_11, MONTH_12 FROM #QT__Billing_Matrix_Header(NOLOCK) WHERE QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '4'")

	GetYear2EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '2' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	GetYear3EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '3' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	GetYear4EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '4' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	GetYear5EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '5' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")

	try:
		Y1ED = GetYear1EndDate.LastUpdateDate
		d1 = '{}-{}-{}'.format(Y1ED.Month, Y1ED.Day, Y1ED.Year)
		Quote.SetGlobal('Year1EndDate', str(d1))		
	except:
		pass
	try:
		Y2ED = GetYear2EndDate.LastUpdateDate
		d2 = '{}-{}-{}'.format(Y2ED.Month, Y2ED.Day, Y2ED.Year)
		Quote.SetGlobal('Year2EndDate', str(d2))		
	except:
		pass
	try:
		Y3ED = GetYear3EndDate.LastUpdateDate
		d3 = '{}-{}-{}'.format(Y3ED.Month, Y3ED.Day, Y3ED.Year)
		Quote.SetGlobal('Year3EndDate', str(d3))		
	except:
		pass
	try:
		Y4ED = GetYear4EndDate.LastUpdateDate
		d4 = '{}-{}-{}'.format(Y4ED.Month, Y4ED.Day, Y4ED.Year)
		Quote.SetGlobal('Year4EndDate', str(d4))		
	except:
		pass
	try:
		Y5ED = GetYear5EndDate.LastUpdateDate
		d5 = '{}-{}-{}'.format(Y5ED.Month, Y5ED.Day, Y5ED.Year)
		Quote.SetGlobal('Year5EndDate', str(d5))		
	except:
		pass

	try:
		Payment_Term = SqlHelper.GetFirst(" SELECT PAYMENTTERM_NAME FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
		Quote.GetCustomField('PaymentTermName').Content = str(Payment_Term.PAYMENTTERM_NAME)
		PO_n = SqlHelper.GetFirst(" SELECT PO_NUMBER FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
		Quote.GetCustomField('CustomerPO').Content = str(PO_n.PO_NUMBER)
	except:
		pass
	
	#to insert in SAQIFP for tool base quote start
	extifp_price = fptotal = fptax =  0.00
	QuoteproductTotals = Quote.QuoteTables["SAQIFP"]
	for i in QuoteproductTotals.Rows:
		#Log.Info('inside SAQIFP for tool base quote')
		extifp_price += float(i['UNIT_PRICE'])
		fptotal += float(i['EXTENDED_PRICE'] +(i['TAX']))
		fptax += float(i['TAX'])
		Quote.SetGlobal('Subtotaltoolsdoc', str(extifp_price))
		Quote.SetGlobal('taxtoolsdoc', str(fptax))
		#Log.Info('inside SAQIFP for tool base quote---Subtotaltoolsdoc-----'+str(extifp_price))
		Quote.SetGlobal('totalspareToolsdoc', str(fptotal))
		#Log.Info('inside SAQIFP for tool base quote---totalspareToolsdoc-----'+str(fptotal))
	#to insert in SAQIFP for tool base quote end
	# offerings_total = 0.00
	# decimal_place ="2"
	# oft = tax = totalprice = unoft = 0.00
	# QuoteproductTotal = Quote.QuoteTables["SAQITM"]
	# for i in QuoteproductTotal.Rows:
		
	# 	oft += float(i['EXTENDED_UNIT_PRICE'])
	# 	unoft += float(i['UNIT_PRICE'])
		
	# 	tax +=  float(i['TAX'])
	# 	totalprice += float(i['EXTENDED_UNIT_PRICE'] +(i['TAX']))
	# 	Quote.SetGlobal('Total_price', str(oft))
	# 	#offerings_total = str(round(offerings_total + oft))
		
	# 	#offerings_total = round(offerings_total + float(i['EXTENDED_UNIT_PRICE'],2))
	# 	#Quote.GetCustomField('Total_Offerings').Content = str(offerings_total)
		
	# 	Quote.SetGlobal('Total_Offerings', str(unoft))
	# 	Quote.SetGlobal('Total_tax', str(tax))
	# 	#Quote.SetGlobal('Total_Offerings', str(offerings_total))
	Quote.GenerateDocument('AMAT Quote', GenDocFormat.PDF)
	
	''' if Quote is not None and Quote.CompositeNumber == str(quoteid.C4C_QUOTE_ID):
		login = SqlHelper.GetFirst("SELECT USER_NAME,PASSWORD,DOMAIN FROM SYCONF (NOLOCK)")
	if login is not None:
		Login_Username = str(login.USER_NAME)
		Login_Password = str(login.PASSWORD)
		Login_Domain = str(login.DOMAIN)
	#example of url service
		url = 'https://sandbox.webcomcpq.com/customapi/executescript?scriptName=CQGNRTDOCS_ENGLISH&username='+str(Login_Username)+'&password='+str(Login_Password)+'&domain='+str(Login_Domain)+''
		#quoterecid=Product.Attributes.GetByName('QSTN_SYSEFL_QT_00001').GetValue()
		#example of user autorization header
		headers = { 'authorization': RestClient.GetBasicAuthenticationHeader(Login_Username, Login_Password+"#"+Login_Domain) }

	#example of input JSON data
	#data = '[{"quoterecid": '+quoterecid+'}]'
	#data = '{"quoterecid": '+quoterecid+'}'
	#data =  '{"Param": "{\'Service\':\'SapReject\',\'QuoteNumber\': [\'66620797\']}"}'
		data='{"Param":"{\'quoterecid\':\''+recid+'\'}"}'

	#make HTTPS POST and receive response in form of dynamic entity
		Data = RestClient.Post(url, data)
		Trace.Write(Data) '''
		#QuoteHelper.Edit(quoteid.C4C_QUOTE_ID, True)

	# '''for action in Quote.Actions:
	# 	if action.Name == "Reprice" and action.IsPrimaryAction:
	# 		Quote.ExecuteAction(action.Id)
	# 		Quote.QuoteTables["SAQITM"].Save()
	# 		Quote.QuoteTables["SAQICO"].Save()
	# 		Quote.QuoteTables["SAQIFP"].Save()'''
		#QuoteproductTotals = Quote.QuoteTables["SAQITM"]
		#QuoteproductTotals.AddNewRow()
		#Quote.QuoteTables["SAQITM"].Save()
		#Quote.GenerateDocument('AMAT Quote', GenDocFormat.PDF)
	fileName = Quote.GetLatestGeneratedDocumentFileName()
	GDB = Quote.GetLatestGeneratedDocumentInBytes()
	List = Quote.GetGeneratedDocumentList('AMAT Quote')
	for doc in List:
		doc_id = doc.Id
		doc_name = doc.FileName
		if fileName==doc_name:
			# quote_id = quoteid.QUOTE_ID
			# quote_name = quoteid.QUOTE_NAME
			#added_by = audit_fields.USERNAME
			#modified_by = audit_fields.CpqTableEntryModifiedBy
			#modified_date = audit_fields.CpqTableEntryDateModified
			# guid = str(Guid.NewGuid()).upper()
			# qt_rec_id = recid
			# date_added = doc.DateCreated
			""" tableInfo = SqlHelper.GetTable('SAQDOC')
			row = {}	
			row['QUOTE_DOCUMENT_RECORD_ID'] = guid
			row['DOCUMENT_ID'] = doc_id
			row['DOCUMENT_NAME'] = doc_name
			row['QUOTE_ID'] = quote_id
			row['QUOTE_NAME'] = quote_name
			row['QUOTE_RECORD_ID'] = qt_rec_id
			row['CPQTABLEENTRYDATEADDED'] = date_added
			row['LANGUAGE_ID'] = 'EN'
			row['LANGUAGE_NAME'] = 'English'
			row['LANGUAGE_RECORD_ID'] = 'CE9C0F91-36EB-45D8-9B12-505E6B6B9A37'
			row['CPQTABLEENTRYADDEDBY'] = UserName
			row['CpqTableEntryModifiedBy'] = UserId
			row['CpqTableEntryDateModified'] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
			tableInfo.AddRow(row)
			SqlHelper.Upsert(tableInfo) """
			update_query = """UPDATE SAQDOC SET DOCUMENT_ID = '{docid}', DOCUMENT_NAME = '{docname}', STATUS = 'ACQUIRED' WHERE SAQDOC.DOCUMENT_ID = 'Pending' AND SAQDOC.LANGUAGE_ID = 'EN' AND SAQDOC.STATUS = 'PENDING' AND SAQDOC.QUOTE_RECORD_ID = '{recid}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(recid=recid,docid=doc_id,docname=doc_name,quote_revision_record_id=quote_revision_record_id)			
			Sql.RunQuery(update_query)
			''' qtqdoc="""INSERT SAQDOC (
						QUOTE_DOCUMENT_RECORD_ID,
						DOCUMENT_ID,
						DOCUMENT_NAME,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						LANGUAGE_ID,
						LANGUAGE_NAME,
						LANGUAGE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						STATUS
						)SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
						'{docid}' AS DOCUMENT_ID,
						'{docname}' AS DOCUMENT_NAME,
						'{quoteid}' AS QUOTE_ID,
						'{quotename}' AS QUOTE_NAME,
						'{quoterecid}' AS QUOTE_RECORD_ID,
						'EN' AS LANGUAGE_ID,
						'English' AS LANGUAGE_NAME,
						MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY,
						'{dateadded}' as CPQTABLEENTRYDATEADDED,
						'{UserId}' as CpqTableEntryModifiedBy,
						'{date}' as CpqTableEntryDateModified,
						'ACQUIRED' as STATUS
						FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'English'""".format(docid=doc_id,docname=doc_name,quoteid=quote_id,quotename=quote_name,quoterecid=qt_rec_id,UserName=UserName,dateadded=date_added,UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
			#Log.Info(qtqdoc)
			Sql.RunQuery(qtqdoc) '''

def chinesedoc():
	quoteid = SqlHelper.GetFirst("SELECT QUOTE_ID, QUOTE_NAME,C4C_QUOTE_ID, QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	Quote=QuoteHelper.Edit(quoteid.C4C_QUOTE_ID)
	qtqdoc="""INSERT SAQDOC (
						QUOTE_DOCUMENT_RECORD_ID,
						DOCUMENT_ID,
						DOCUMENT_NAME,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						LANGUAGE_ID,
						LANGUAGE_NAME,
						LANGUAGE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						STATUS
						)SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
						'Pending' AS DOCUMENT_ID,
						'' AS DOCUMENT_NAME,
						'{quoteid}' AS QUOTE_ID,
						'{quotename}' AS QUOTE_NAME,
						'{quoterecid}' AS QUOTE_RECORD_ID,
						'ZH' AS LANGUAGE_ID,
						'Chinese' AS LANGUAGE_NAME,
						MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY,
						'{dateadded}' as CPQTABLEENTRYDATEADDED,
						'{UserId}' as CpqTableEntryModifiedBy,
						'{date}' as CpqTableEntryDateModified,
						'PENDING' as STATUS
						FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'Chinese'""".format(quoteid=quoteid.QUOTE_ID,quotename=quoteid.QUOTE_NAME,quoterecid=recid,UserName=UserName,dateadded=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
	#Log.Info(qtqdoc)
	Sql.RunQuery(qtqdoc)
	
	SUM_YEAR1 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '1' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR2 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '2' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR3 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '3' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR4 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '4' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	SUM_YEAR5 = SqlHelper.GetFirst("SELECT convert(varchar,FORMAT(cast(SUM(MONTH_1) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_1, convert(varchar,FORMAT(cast(SUM(MONTH_2) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_2, convert(varchar,FORMAT(cast(SUM(MONTH_3) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_3, convert(varchar,FORMAT(cast(SUM(MONTH_4) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_4, convert(varchar,FORMAT(cast(SUM(MONTH_5) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_5, convert(varchar,FORMAT(cast(SUM(MONTH_6) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_6, convert(varchar,FORMAT(cast(SUM(MONTH_7) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_7, convert(varchar,FORMAT(cast(SUM(MONTH_8) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_8, convert(varchar,FORMAT(cast(SUM(MONTH_9) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_9, convert(varchar,FORMAT(cast(SUM(MONTH_10) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_10, convert(varchar,FORMAT(cast(SUM(MONTH_11) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_11, convert(varchar,FORMAT(cast(SUM(MONTH_12) as numeric(10,2)),'###,###,##0.00','en-US'))  AS MONTH_12 FROM QT__BM_YEAR_1(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND YEAR = '5' AND BILLING_INTERVAL IS NULL"+" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")


	M1_Y1 = SUM_YEAR1.MONTH_1
	Quote.SetGlobal('M1_Y1', str(M1_Y1))
	M2_Y1 = SUM_YEAR1.MONTH_2
	Quote.SetGlobal('M2_Y1', str(M2_Y1))
	M3_Y1 = SUM_YEAR1.MONTH_3
	Quote.SetGlobal('M3_Y1', str(M3_Y1))
	M4_Y1 = SUM_YEAR1.MONTH_4
	Quote.SetGlobal('M4_Y1', str(M4_Y1))
	M5_Y1 = SUM_YEAR1.MONTH_5
	Quote.SetGlobal('M5_Y1', str(M5_Y1))
	M6_Y1 = SUM_YEAR1.MONTH_6
	Quote.SetGlobal('M6_Y1', str(M6_Y1))
	M7_Y1 = SUM_YEAR1.MONTH_7
	Quote.SetGlobal('M7_Y1', str(M7_Y1))
	M8_Y1 = SUM_YEAR1.MONTH_8
	Quote.SetGlobal('M8_Y1', str(M8_Y1))
	M9_Y1 = SUM_YEAR1.MONTH_9
	Quote.SetGlobal('M9_Y1', str(M9_Y1))
	M10_Y1 = SUM_YEAR1.MONTH_10
	Quote.SetGlobal('M10_Y1', str(M10_Y1))
	M11_Y1 = SUM_YEAR1.MONTH_11
	Quote.SetGlobal('M11_Y1', str(M11_Y1))
	M12_Y1 = SUM_YEAR1.MONTH_12
	Quote.SetGlobal('M12_Y1', str(M12_Y1))

	M1_Y2 = SUM_YEAR2.MONTH_1
	Quote.SetGlobal('M1_Y2', str(M1_Y2))
	M2_Y2 = SUM_YEAR2.MONTH_2
	Quote.SetGlobal('M2_Y2', str(M2_Y2))
	M3_Y2 = SUM_YEAR2.MONTH_3
	Quote.SetGlobal('M3_Y2', str(M3_Y2))
	M4_Y2 = SUM_YEAR2.MONTH_4
	Quote.SetGlobal('M4_Y2', str(M4_Y2))
	M5_Y2 = SUM_YEAR2.MONTH_5
	Quote.SetGlobal('M5_Y2', str(M5_Y2))
	M6_Y2 = SUM_YEAR2.MONTH_6
	Quote.SetGlobal('M6_Y2', str(M6_Y2))
	M7_Y2 = SUM_YEAR2.MONTH_7
	Quote.SetGlobal('M7_Y2', str(M7_Y2))
	M8_Y2 = SUM_YEAR2.MONTH_8
	Quote.SetGlobal('M8_Y2', str(M8_Y2))
	M9_Y2 = SUM_YEAR2.MONTH_9
	Quote.SetGlobal('M9_Y2', str(M9_Y2))
	M10_Y2 = SUM_YEAR2.MONTH_10
	Quote.SetGlobal('M10_Y2', str(M10_Y2))
	M11_Y2 = SUM_YEAR2.MONTH_11
	Quote.SetGlobal('M11_Y2', str(M11_Y2))
	M12_Y2 = SUM_YEAR2.MONTH_12
	Quote.SetGlobal('M12_Y2', str(M12_Y2))

	M1_Y3 = SUM_YEAR3.MONTH_1
	Quote.SetGlobal('M1_Y3', str(M1_Y3))
	M2_Y3 = SUM_YEAR3.MONTH_2
	Quote.SetGlobal('M2_Y3', str(M2_Y3))
	M3_Y3 = SUM_YEAR3.MONTH_3
	Quote.SetGlobal('M3_Y3', str(M3_Y3))
	M4_Y3 = SUM_YEAR3.MONTH_4
	Quote.SetGlobal('M4_Y3', str(M4_Y3))
	M5_Y3 = SUM_YEAR3.MONTH_5
	Quote.SetGlobal('M5_Y3', str(M5_Y3))
	M6_Y3 = SUM_YEAR3.MONTH_6
	Quote.SetGlobal('M6_Y3', str(M6_Y3))
	M7_Y3 = SUM_YEAR3.MONTH_7
	Quote.SetGlobal('M7_Y3', str(M7_Y3))
	M8_Y3 = SUM_YEAR3.MONTH_8
	Quote.SetGlobal('M8_Y3', str(M8_Y3))
	M9_Y3 = SUM_YEAR3.MONTH_9
	Quote.SetGlobal('M9_Y3', str(M9_Y3))
	M10_Y3 = SUM_YEAR3.MONTH_10
	Quote.SetGlobal('M10_Y3', str(M10_Y3))
	M11_Y3 = SUM_YEAR3.MONTH_11
	Quote.SetGlobal('M11_Y3', str(M10_Y3))
	M12_Y3 = SUM_YEAR3.MONTH_12
	Quote.SetGlobal('M12_Y3', str(M12_Y3))

	M1_Y4 = SUM_YEAR4.MONTH_1
	Quote.SetGlobal('M1_Y4', str(M1_Y4))
	M2_Y4 = SUM_YEAR4.MONTH_2
	Quote.SetGlobal('M2_Y4', str(M2_Y4))
	M3_Y4 = SUM_YEAR4.MONTH_3
	Quote.SetGlobal('M3_Y4', str(M3_Y4))
	M4_Y4 = SUM_YEAR4.MONTH_4
	Quote.SetGlobal('M4_Y4', str(M4_Y4))
	M5_Y4 = SUM_YEAR4.MONTH_5
	Quote.SetGlobal('M5_Y4', str(M5_Y4))
	M6_Y4 = SUM_YEAR4.MONTH_6
	Quote.SetGlobal('M6_Y4', str(M6_Y4))
	M7_Y4 = SUM_YEAR4.MONTH_7
	Quote.SetGlobal('M7_Y4', str(M7_Y4))
	M8_Y4 = SUM_YEAR4.MONTH_8
	Quote.SetGlobal('M8_Y4', str(M8_Y4))
	M9_Y4 = SUM_YEAR4.MONTH_9
	Quote.SetGlobal('M9_Y4', str(M9_Y4))
	M10_Y4 = SUM_YEAR4.MONTH_10
	Quote.SetGlobal('M10_Y4', str(M10_Y4))
	M11_Y4 = SUM_YEAR4.MONTH_11
	Quote.SetGlobal('M11_Y4', str(M11_Y4))
	M12_Y4 = SUM_YEAR4.MONTH_12
	Quote.SetGlobal('M12_Y4', str(M12_Y4))

	M1_Y5 = SUM_YEAR5.MONTH_1
	Quote.SetGlobal('M1_Y5', str(M1_Y5))
	M2_Y5 = SUM_YEAR5.MONTH_2
	Quote.SetGlobal('M2_Y5', str(M2_Y5))
	M3_Y5 = SUM_YEAR5.MONTH_3
	Quote.SetGlobal('M3_Y5', str(M3_Y5))
	M4_Y5 = SUM_YEAR5.MONTH_4
	Quote.SetGlobal('M4_Y5', str(M4_Y5))
	M5_Y5 = SUM_YEAR5.MONTH_5
	Quote.SetGlobal('M5_Y5', str(M5_Y5))
	M6_Y5 = SUM_YEAR5.MONTH_6
	Quote.SetGlobal('M6_Y5', str(M6_Y5))
	M7_Y5 = SUM_YEAR5.MONTH_7
	Quote.SetGlobal('M7_Y5', str(M7_Y5))
	M8_Y5 = SUM_YEAR5.MONTH_8
	Quote.SetGlobal('M8_Y5', str(M8_Y5))
	M9_Y5 = SUM_YEAR5.MONTH_9
	Quote.SetGlobal('M9_Y5', str(M9_Y5))
	M10_Y5 = SUM_YEAR5.MONTH_10
	Quote.SetGlobal('M10_Y5', str(M10_Y5))
	M11_Y5 = SUM_YEAR5.MONTH_11
	Quote.SetGlobal('M11_Y5', str(M11_Y5))
	M12_Y5 = SUM_YEAR5.MONTH_12
	Quote.SetGlobal('M12_Y5', str(M12_Y5))

	GetYear1EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '1' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")

	#DATES_YEAR_1 = SqlHelper.GetFirst("SELECT MONTH_1, MONTH_1, MONTH_2, MONTH_3, MONTH_4, MONTH_5, MONTH_6, MONTH_7, MONTH_8, MONTH_9, MONTH_10, MONTH_10, MONTH_11, MONTH_12 FROM #QT__Billing_Matrix_Header(NOLOCK) WHERE QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '4'")

	GetYear2EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '2'AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	GetYear3EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '3'AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	GetYear4EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '4' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	GetYear5EndDate = SqlHelper.GetFirst("""SELECT
	ID,
	(SELECT MAX(convert(date, LastUpdateDate))
		FROM (VALUES (MONTH_1),(MONTH_2),(MONTH_3),(MONTH_4),(MONTH_5),(MONTH_6),(MONTH_7),(MONTH_8),(MONTH_9),(MONTH_10),(MONTH_11),(MONTH_12)) AS UpdateDate(LastUpdateDate))
	AS LastUpdateDate
	FROM QT__Billing_Matrix_Header
	where QUOTE_RECORD_ID = '"""+str(recid)+"""' AND YEAR = '5' AND QTEREV_RECORD_ID = '"""+str(quote_revision_record_id)+"""'""")
	try:
		Y1ED = GetYear1EndDate.LastUpdateDate
		d1 = '{}-{}-{}'.format(Y1ED.Month, Y1ED.Day, Y1ED.Year)
		Quote.SetGlobal('Year1EndDate', str(d1))		
	except:
		pass
	try:
		Y2ED = GetYear2EndDate.LastUpdateDate
		d2 = '{}-{}-{}'.format(Y2ED.Month, Y2ED.Day, Y2ED.Year)
		Quote.SetGlobal('Year2EndDate', str(d2))		
	except:
		pass
	try:
		Y3ED = GetYear3EndDate.LastUpdateDate
		d3 = '{}-{}-{}'.format(Y3ED.Month, Y3ED.Day, Y3ED.Year)
		Quote.SetGlobal('Year3EndDate', str(d3))		
	except:
		pass
	try:
		Y4ED = GetYear4EndDate.LastUpdateDate
		d4 = '{}-{}-{}'.format(Y4ED.Month, Y4ED.Day, Y4ED.Year)
		Quote.SetGlobal('Year4EndDate', str(d4))		
	except:
		pass
	try:
		Y5ED = GetYear5EndDate.LastUpdateDate
		d5 = '{}-{}-{}'.format(Y5ED.Month, Y5ED.Day, Y5ED.Year)
		Quote.SetGlobal('Year5EndDate', str(d5))		
	except:
		pass
	
	try:
		PO_n = SqlHelper.GetFirst(" SELECT PO_NUMBER FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"'AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
		Quote.GetCustomField('CustomerPO').Content = str(PO_n.PO_NUMBER)
	except:
		pass
	# offerings_total = 0
	# decimal_place ="2"
	# oft = tax = totalprice =unoft =  0.00
	
	# QuoteproductTotal = Quote.QuoteTables["SAQITM"]
	# for i in QuoteproductTotal.Rows:
	# 	oft += float(i['EXTENDED_UNIT_PRICE'])
	# 	tax += float(i['TAX'])
	# 	unoft += float(i['UNIT_PRICE'])
	# 	totalprice += float(i['EXTENDED_UNIT_PRICE'] +(i['TAX']))
	# 	#offerings_total = round(offerings_total + i['EXTENDED_UNIT_PRICE'],2)
	# 	#Quote.GetCustomField('Total_Offerings').Content = str(offerings_total)
	# 	Quote.SetGlobal('Total_Offerings', str(unoft))
	# 	Quote.SetGlobal('Total_tax', str(tax))
	# 	Quote.SetGlobal('Total_price', str(oft))

	Quote.GenerateDocument('AMAT Quote Chinese', GenDocFormat.PDF)
	""" if Quote is not None and Quote.CompositeNumber == str(quoteid.C4C_QUOTE_ID):
		LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME,PASSWORD,DOMAIN FROM SYCONF (NOLOCK)")
	if LOGIN_CREDENTIALS is not None:
		Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
		Login_Password = str(LOGIN_CREDENTIALS.PASSWORD)
		Login_Domain = str(LOGIN_CREDENTIALS.DOMAIN)
	#example of url service
		url = 'https://sandbox.webcomcpq.com/customapi/executescript?scriptName=CQGNRTDOCS_CHINESE&username='+str(Login_Username)+'&password='+str(Login_Password)+'&domain='+str(Login_Domain)+''
		quoterecid=Product.Attributes.GetByName('QSTN_SYSEFL_QT_00001').GetValue()
		#example of user autorization header
		headers = { 'authorization': RestClient.GetBasicAuthenticationHeader(Login_Username, Login_Password+"#"+Login_Domain) }

	#example of input JSON data
	#data = '[{"quoterecid": '+quoterecid+'}]'
	#data = '{"quoterecid": '+quoterecid+'}'
	#data =  '{"Param": "{\'Service\':\'SapReject\',\'QuoteNumber\': [\'66620797\']}"}'
		data='{"Param":"{\'quoterecid\':\''+quoterecid+'\'}"}'

	#make HTTPS POST and receive response in form of dynamic entity
		Data = RestClient.Post(url, data)
		Trace.Write(Data) """
		#Quote.GenerateDocument('AMAT Quote Chinese', GenDocFormat.PDF)
	fileName = Quote.GetLatestGeneratedDocumentFileName()
	GDB = Quote.GetLatestGeneratedDocumentInBytes()
	List = Quote.GetGeneratedDocumentList('AMAT Quote Chinese')
	for doc in List:
		doc_id = doc.Id
		doc_name = doc.FileName
		if fileName==doc_name:
			# quote_id = quoteid.QUOTE_ID
			# quote_name = quoteid.QUOTE_NAME
			#added_by = audit_fields.USERNAME
			#modified_by = audit_fields.CpqTableEntryModifiedBy
			#modified_date = audit_fields.CpqTableEntryDateModified
			# guid = str(Guid.NewGuid()).upper()
			# qt_rec_id = recid
			# date_added = doc.DateCreated
			""" tableInfo = SqlHelper.GetTable('SAQDOC')
			row = {}
			row['QUOTE_DOCUMENT_RECORD_ID'] = guid
			row['DOCUMENT_ID'] = doc_id
			row['DOCUMENT_NAME'] = doc_name
			row['QUOTE_ID'] = quote_id
			row['QUOTE_NAME'] = quote_name
			row['QUOTE_RECORD_ID'] = qt_rec_id
			row['CPQTABLEENTRYDATEADDED'] = date_added
			row['LANGUAGE_ID'] = 'ZH'
			row['LANGUAGE_NAME'] = 'Chinese'
			row['LANGUAGE_RECORD_ID'] = '1A92BC4C-CBB3-4412-BE54-6C28A06C71FE'
			row['CPQTABLEENTRYADDEDBY'] = UserName
			row['CpqTableEntryModifiedBy'] = UserId
			row['CpqTableEntryDateModified'] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
			tableInfo.AddRow(row)
			SqlHelper.Upsert(tableInfo) """
			update_query = """UPDATE SAQDOC SET DOCUMENT_ID = '{docid}', DOCUMENT_NAME = '{docname}', STATUS = 'ACQUIRED' WHERE SAQDOC.DOCUMENT_ID = 'Pending' AND SAQDOC.LANGUAGE_ID = 'ZH' AND SAQDOC.STATUS = 'PENDING' AND SAQDOC.QUOTE_RECORD_ID = '{recid}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(recid=recid,docid=doc_id,docname=doc_name)
			Sql.RunQuery(update_query)
			''' qtqdoc="""INSERT SAQDOC (
						QUOTE_DOCUMENT_RECORD_ID,
						DOCUMENT_ID,
						DOCUMENT_NAME,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						LANGUAGE_ID,
						LANGUAGE_NAME,
						LANGUAGE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						STATUS
						)SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
						'{docid}' AS DOCUMENT_ID,
						'{docname}' AS DOCUMENT_NAME,
						'{quoteid}' AS QUOTE_ID,
						'{quotename}' AS QUOTE_NAME,
						'{quoterecid}' AS QUOTE_RECORD_ID,
						'ZH' AS LANGUAGE_ID,
						'Chinese' AS LANGUAGE_NAME,
						MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY,
						'{dateadded}' as CPQTABLEENTRYDATEADDED,
						'{UserId}' as CpqTableEntryModifiedBy,
						'{date}' as CpqTableEntryDateModified,
						'ACQUIRED' AS STATUS
						FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'Chinese' AND MALANG.LANGUAGE_ID='ZH'""".format(docid=doc_id,docname=doc_name,quoteid=quote_id,quotename=quote_name,quoterecid=qt_rec_id,UserName=UserName,dateadded=date_added,UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
			#Log.Info(qtqdoc)
			Sql.RunQuery(qtqdoc) '''

def fpmdoc():
	quoteid = SqlHelper.GetFirst("SELECT QUOTE_ID, QUOTE_NAME,C4C_QUOTE_ID, QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	Quote=QuoteHelper.Edit(quoteid.C4C_QUOTE_ID)	
	qtqdoc="""INSERT SAQDOC (
						QUOTE_DOCUMENT_RECORD_ID,
						DOCUMENT_ID,
						DOCUMENT_NAME,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						LANGUAGE_ID,
						LANGUAGE_NAME,
						LANGUAGE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						STATUS
						)SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
						'Pending' AS DOCUMENT_ID,
						'' AS DOCUMENT_NAME,
						'{quoteid}' AS QUOTE_ID,
						'{quotename}' AS QUOTE_NAME,
						'{quoterecid}' AS QUOTE_RECORD_ID,
						'EN' AS LANGUAGE_ID,
						'English' AS LANGUAGE_NAME,
						MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY,
						'{dateadded}' as CPQTABLEENTRYDATEADDED,
						'{UserId}' as CpqTableEntryModifiedBy,
						'{date}' as CpqTableEntryDateModified,
						'PENDING' as STATUS
						FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'English'""".format(quoteid=quoteid.QUOTE_ID,quotename=quoteid.QUOTE_NAME,quoterecid=recid,UserName=UserName,dateadded=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))	
	Sql.RunQuery(qtqdoc)
	
	try:
		PO_n = SqlHelper.GetFirst(" SELECT PO_NUMBER FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
		Quote.GetCustomField('CustomerPO').Content = str(PO_n.PO_NUMBER)
	except:
		pass

	# offerings_total = 0
	# decimal_place ="2"
	# oft = tax = totalprice = unoft = 0.00
	
	# QuoteproductTotal = Quote.QuoteTables["SAQITM"]
	# for i in QuoteproductTotal.Rows:
	# 	#Log.Info(i['EXTENDED_UNIT_PRICE'])
	# 	oft += float(i['EXTENDED_UNIT_PRICE'])
	# 	tax += float(i['TAX'])
	# 	unoft += float(i['UNIT_PRICE'])
	# 	totalprice += float(i['EXTENDED_UNIT_PRICE'] +(i['TAX']))
	# 	#offerings_total = round(offerings_total + i['EXTENDED_UNIT_PRICE'],2)
	# 	#Quote.GetCustomField('Total_Offerings').Content = str(offerings_total)
		
	# 	Quote.SetGlobal('Total_Offerings', str(unoft))
	# 	Quote.SetGlobal('Total_tax', str(tax))
	# 	Quote.SetGlobal('Total_price', str(oft))
		
	Quote.GenerateDocument('FPM Quote', GenDocFormat.PDF)
	fileName = Quote.GetLatestGeneratedDocumentFileName()
	GDB = Quote.GetLatestGeneratedDocumentInBytes()
	List = Quote.GetGeneratedDocumentList('FPM Quote')
	for doc in List:
		doc_id = doc.Id
		doc_name = doc.FileName
		if fileName==doc_name:
			# quote_id = quoteid.QUOTE_ID
			# quote_name = quoteid.QUOTE_NAME
			#added_by = audit_fields.USERNAME
			#modified_by = audit_fields.CpqTableEntryModifiedBy
			#modified_date = audit_fields.CpqTableEntryDateModified
			# guid = str(Guid.NewGuid()).upper()
			# qt_rec_id = recid
			# date_added = doc.DateCreated
			""" tableInfo = SqlHelper.GetTable('SAQDOC')
			row = {}
			row['QUOTE_DOCUMENT_RECORD_ID'] = guid
			row['DOCUMENT_ID'] = doc_id
			row['DOCUMENT_NAME'] = doc_name
			row['QUOTE_ID'] = quote_id
			row['QUOTE_NAME'] = quote_name
			row['QUOTE_RECORD_ID'] = qt_rec_id
			row['CPQTABLEENTRYDATEADDED'] = date_added
			row['LANGUAGE_ID'] = 'EN'
			row['LANGUAGE_NAME'] = 'English'
			row['LANGUAGE_RECORD_ID'] = 'CE9C0F91-36EB-45D8-9B12-505E6B6B9A37'
			row['CPQTABLEENTRYADDEDBY'] = UserName
			row['CpqTableEntryModifiedBy'] = UserId
			row['CpqTableEntryDateModified'] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
			tableInfo.AddRow(row)
			SqlHelper.Upsert(tableInfo) """
			update_query = """UPDATE SAQDOC SET DOCUMENT_ID = '{docid}', DOCUMENT_NAME = '{docname}', STATUS = 'ACQUIRED' WHERE SAQDOC.DOCUMENT_ID = 'Pending' AND SAQDOC.LANGUAGE_ID = 'EN' AND SAQDOC.STATUS = 'PENDING' AND SAQDOC.QUOTE_RECORD_ID = '{recid}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(recid=recid,docid=doc_id,docname=doc_name,quote_revision_record_id=quote_revision_record_id)
			Sql.RunQuery(update_query)
			''' qtqdoc="""INSERT SAQDOC (
						QUOTE_DOCUMENT_RECORD_ID,
						DOCUMENT_ID,
						DOCUMENT_NAME,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						LANGUAGE_ID,
						LANGUAGE_NAME,
						LANGUAGE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						STATUS
						)SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
						'{docid}' AS DOCUMENT_ID,
						'{docname}' AS DOCUMENT_NAME,
						'{quoteid}' AS QUOTE_ID,
						'{quotename}' AS QUOTE_NAME,
						'{quoterecid}' AS QUOTE_RECORD_ID,
						'EN' AS LANGUAGE_ID,
						'English' AS LANGUAGE_NAME,
						MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY,
						'{dateadded}' as CPQTABLEENTRYDATEADDED,
						'{UserId}' as CpqTableEntryModifiedBy,
						'{date}' as CpqTableEntryDateModified,
						'ACQUIRED' AS STATUS
						FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'English'""".format(docid=doc_id,docname=doc_name,quoteid=quote_id,quotename=quote_name,quoterecid=qt_rec_id,UserName=UserName,dateadded=date_added,UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
			#Log.Info(qtqdoc)
			Sql.RunQuery(qtqdoc) '''

def popup():
	sec_str = ""
	sec_str += """<div class="drop-box" style="display: none;">
				<div class="col-md-3 pl-0 rolling_popup">
				<div class="col-md-2 p-0">
					<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
				</div>
				<div class="col-md-10 p-0">
					<h3>Generating Document</h3>
				<p>The Quote document is currently being generated. You will receive an email notification when the document is generated.</p>
				</div>
				</div>
				</div>"""
	return sec_str

def warning():
	sec_str = ""
	sec_str += """<div id="Headerbnr" class="mart_col_back disp_blk"><div class="col-md-12" id="PageAlert"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio6" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down"></i><i class="pull-right fa fa-chevron-up"></i></div><div id="Alert_notifcatio6" class="col-md-12 alert-notification brdr collapse in"><div class="col-md-12 alert-warning"><label title=" Warning: Please select a valid document language from the list before generating."><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Info"> Warning: Please select a valid document language from the list before generating.</label></div></div></div></div>"""
	return sec_str

def submit_to_customer(doc_rec_id):
	Trace.Write("cm to this function=====")		
	quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
	update_submitted_date = Sql.RunQuery("""UPDATE SAQDOC SET DATE_SUBMITTED = '{submitted_date}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'""".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,doc_rec_id,submitted_date = date.today().strftime("%m/%d/%Y")))
	Sql.RunQuery(update_submitted_date)	
	return True

def customer_accepted(doc_rec_id):
	Trace.Write("cm to this acceptedfunction=====")		
	quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
	update_submitted_date = Sql.RunQuery("""UPDATE SAQDOC SET ACCEPTED = 'TRUE', DATE_ACCEPTED = '{submitted_date}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'""".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,doc_rec_id,submitted_date = date.today().strftime("%m/%d/%Y"),))
	Sql.RunQuery(update_submitted_date)
	output_doc_query = Sql.GetFirst(" SELECT * FROM SAQDOC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,doc_rec_id))
	if output_doc_query:
		if str(output_doc_query.DATE_ACCEPTED) != "":			
			update_revision_status = "UPDATE SAQTRV SET REVISION_STATUS = 'CUSTOMER ACCEPTED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
			Sql.RunQuery(update_revision_status)	
	return True

def customer_rejected(doc_rec_id,REJECT_COMMENT):
	Trace.Write("cm to this rejectedfunction=====")
	quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")

	update_submitted_date = Sql.RunQuery("""UPDATE SAQDOC SET DATE_REJECTED = '{submitted_date}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'""".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,doc_rec_id,submitted_date = date.today().strftime("%m/%d/%Y")))
	Sql.RunQuery(update_submitted_date)

	output_doc_query = Sql.GetFirst(" SELECT * FROM SAQDOC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,doc_rec_id))
	if output_doc_query:
		if str(output_doc_query.DATE_REJECTED) != "":
			Trace.Write("DATE_REJ"+str(output_doc_query.DATE_REJECTED))
			update_revision_status = "UPDATE SAQTRV SET REVISION_STATUS = 'CUSTOMER REJECTED',MEMO = '{memo}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id",memo=REJECT_COMMENT))
			Sql.RunQuery(update_revision_status)	
	return True

def save_document_description(doc_desc_val,doc_rec_id):
	Trace.Write("cm to this savefunction=====")	
	quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")	
	update_document_description = Sql.RunQuery("""UPDATE SAQDOC SET DOCUMENT_DESCRIPTION = '{description}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'""".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,doc_rec_id,description = doc_desc_val))
	Sql.RunQuery(update_document_description)
	return True

try:
	recid = Param.CPQ_Columns['Quote']
	language = Param.CPQ_Columns['Language']
	a = language.split(",")
	UserId = a[1]
	UserName = a[2]
except:
	recid = ""
	language = ""
try:
	quote_revision_record_id = Param.CPQ_Columns['QuoteRevision']
except:
	quote_revision_record_id = ""
try: 
	ACTION = Param.ACTION
except:
	ACTION = ""
try:
	doc_rec_id = Param.doc_rec_id
except:
	doc_rec_id = ""
try:
	doc_desc_val = Param.doc_desc_val
except:
	doc_desc_val = ""
try: 
	REJECT_COMMENT = Param.REJECT_COMMENT
except:
	REJECT_COMMENT = ""
# if 'ENGLISH DOC' in language:
# 	ApiResponse = ApiResponseFactory.JsonResponse(englishdoc())
# elif 'CHINESE DOC' in language:
# 	ApiResponse = ApiResponseFactory.JsonResponse(chinesedoc())
# elif 'FPM DOC' in language:
# 	ApiResponse = ApiResponseFactory.JsonResponse(fpmdoc())
# elif ACTION == 'POPUP':
# 	ApiResponse = ApiResponseFactory.JsonResponse(popup())
# elif ACTION == 'WARNING':
# 	ApiResponse = ApiResponseFactory.JsonResponse(warning())
if ACTION == 'SUBMIT_TO_CUSTOMER':
	ApiResponse = ApiResponseFactory.JsonResponse(submit_to_customer(doc_rec_id))
elif ACTION == 'CUSTOMER_ACCEPTED':
	ApiResponse = ApiResponseFactory.JsonResponse(customer_accepted(doc_rec_id))
elif ACTION == 'CUSTOMER_REJECTED':
	ApiResponse = ApiResponseFactory.JsonResponse(customer_rejected(doc_rec_id,REJECT_COMMENT))
elif ACTION == 'SAVE_DESC':
	ApiResponse = ApiResponseFactory.JsonResponse(save_document_description(doc_desc_val,doc_rec_id))



