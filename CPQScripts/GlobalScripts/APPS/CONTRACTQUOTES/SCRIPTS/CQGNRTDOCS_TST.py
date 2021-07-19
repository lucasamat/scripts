import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler
import Webcom.Configurator.Scripting.Test.TestProduct
import System
import sys
from System import IO
from System import Web
import System.Net
from System.Net import WebClient
import re


primaryQueryItems = SqlHelper.GetList("Select * from SAQDOC")
tableInfo = SqlHelper.GetTable("SAQDOC")
for primaryItem in primaryQueryItems:
    tableInfo.AddRow(primaryItem)
SqlHelper.Delete(tableInfo)

if "Param" in globals():
    recid = Param.quoterecid
    Log.Info("recid--"+str(recid))
else:
    recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()

quoteid = SqlHelper.GetFirst("SELECT QUOTE_ID, QUOTE_NAME FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"'")
#Log.Info("SELECT QUOTE_ID, QUOTE_NAME FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"'")

Quote=QuoteHelper.Edit('01340018')
if Quote.CompositeNumber == '01340018':
    Quote.GenerateDocument('AMAT Quote', GenDocFormat.PDF)
    fileName = Quote.GetLatestGeneratedDocumentFileName()
    GDB = Quote.GetLatestGeneratedDocumentInBytes()
    List = Quote.GetGeneratedDocumentList('AMAT Quote')
    for doc in List:
        doc_id = doc.Id
        doc_name = doc.FileName
        quote_id = quoteid.QUOTE_ID
        quote_name = quoteid.QUOTE_NAME
        guid = str(Guid.NewGuid()).upper()
        qt_rec_id = recid
        date_added = doc.DateCreated
        tableInfo = SqlHelper.GetTable('SAQDOC')
        row = {}
        row['QUOTE_DOCUMENT_RECORD_ID'] = guid
        row['DOCUMENT_ID'] = doc_id
        row['DOCUMENT_NAME'] = doc_name
        row['QUOTE_ID'] = quote_id
        row['QUOTE_NAME'] = quote_name
        row['QUOTE_RECORD_ID'] = qt_rec_id
        row['CPQTABLEENTRYDATEADDED'] = date_added
        tableInfo.AddRow(row)
        SqlHelper.Upsert(tableInfo)





