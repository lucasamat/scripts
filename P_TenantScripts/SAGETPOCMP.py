 # =========================================================================================================================================
#   __script_name : SAGETPOCMP.PY
#   __script_description : THIS SCRIPT IS RECEIVED C4C DATA  AND SEND TO C4C SYSTEM
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential

clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

Log.Info("SAGETPOCMP Starts ---->Hitting")

try:
	if 'Param' in globals():    
		if hasattr(Param, 'CPQ_Columns'): 
			PRODUCTOFFERING_ID = ''
			POES = ''
			SALESORG_ID = ''
			DISTRIBUTIONCHANNEL_ID = ''
			primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")       
			for table_dict in Param.CPQ_Columns: 
				tbl = str(table_dict.Key)
				if str(tbl).upper() == "PRODUCTOFFERING_ID":
					PRODUCTOFFERING_ID = str(table_dict.Value)
				if str(tbl).upper() == "POES":
					POES = str(table_dict.Value)
				if str(tbl).upper() == "SALESORG_ID":
					SALESORG_ID = str(table_dict.Value)
				if str(tbl).upper() == "DISTRIBUTIONCHANNEL_ID":
					DISTRIBUTIONCHANNEL_ID = str(table_dict.Value)    
			  
			RESULT = ''
			
			Log.Info("4444 PRODUCTOFFERING_ID--->"+str(PRODUCTOFFERING_ID))
			Log.Info("4444 POES----> "+str(POES))
			Log.Info("4444 SALESORG_ID --->"+str(SALESORG_ID))
			Log.Info("4444 DISTRIBUTIONCHANNEL_ID---->"+str(DISTRIBUTIONCHANNEL_ID))
			
			#PRODUCTOFFERING_ID is empty
			if PRODUCTOFFERING_ID == '':
				
				table = SqlHelper.GetList("SELECT DISTINCT A.SAP_PART_NUMBER AS ProductOffering,A.DOCTYP_ID AS DocumentType,A.MATERIAL_NAME AS ProductOfferingName FROM MAMADT A(NOLOCK) JOIN MAMSOP (NOLOCK) B ON A.SAP_PART_NUMBER = b.SAP_PART_NUMBER JOIN MAADPR C(NOLOCK) ON A.SAP_PART_NUMBER = C.PRDOFR_ID WHERE B.SALESORG_ID ='"+ str(SALESORG_ID) +"' AND B.DISTRIBUTIONCHANNEL_ID ='"+ str(DISTRIBUTIONCHANNEL_ID) + "' AND ISNULL(A.POES,'FALSE') = '"+str(POES)+"' " )
				
				prod_offering_lst = []
				
				for data in table:
					dt={}
					dt['ProductOffering'] = data.ProductOffering
					dt['DocumentType'] = data.DocumentType
					dt['ProductOfferingName'] = data.ProductOfferingName
					prod_offering_lst.append(dt)
				
				
				RESULT = {'ProductOfferingArray' : prod_offering_lst}
				
			
			#PRODUCTOFFERING_ID is not empty
			if PRODUCTOFFERING_ID != '':           
				
				table = SqlHelper.GetList("SELECT DISTINCT A.COMP_PRDOFR_ID AS CompatibleProductOffering ,A.COMP_PRDOFR_DOCTYP AS DocumentType,A.PRDOFR_ID as ProductOffering,A.COMP_PRDOFR_NAME as CompatibleProductOfferingName FROM MAADPR A(NOLOCK) JOIN MAMSOP (NOLOCK) B ON A.COMP_PRDOFR_ID = b.SAP_PART_NUMBER WHERE A.PRDOFR_ID ='"+ str(PRODUCTOFFERING_ID) +"' AND B.SALESORG_ID ='"+ str(SALESORG_ID) +"' AND B.DISTRIBUTIONCHANNEL_ID ='"+ str(DISTRIBUTIONCHANNEL_ID) + "' AND ISNULL(A.POES,'FALSE') = '"+str(POES)+"' AND ISNULL(VISIBLE_INCONFIG,'FALSE')='TRUE' ")
				
				prod_offering_lst = []
				
				for data in table:
					dt={}
					dt['CompatibleProductOffering'] = data.CompatibleProductOffering
					dt['DocumentType'] = data.DocumentType
					dt['ProductOffering'] = data.ProductOffering
					dt['CompatibleProductOfferingName'] = data.CompatibleProductOfferingName
					prod_offering_lst.append(dt)            
				
				RESULT = {'ProductOfferingArray' : prod_offering_lst}               
				
				
			if str(RESULT) != '':
				ApiResponse = ApiResponseFactory.JsonResponse( RESULT)  

			else:
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})                
							
except:
	Log.Info("SAGETPOCMP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAGETPOCMP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})