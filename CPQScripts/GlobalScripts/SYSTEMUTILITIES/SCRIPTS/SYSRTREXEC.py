# =========================================================================================================================================
#   __script_name : SYSRTREXEC.PY
#   __script_description :  THIS SCRIPT IS USED ACROSS ALL THE APPS DURING THE ONPRODUCTLOADED EVENT TO DO THE SEARCH FUNCTIONALITY IN CONTAINER
#   __primary_author__ : LEO JOSEPH
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
if Product.PartNumber =="QT" and Product.Attributes.GetByName('Services') is not None:
	#Log.Info('script called--87-inside script---')
	#ServiceProducts=['Z0090','Z0091','Z0092','Z0006','Z0007','Z0035','Z0110','Z0108','Z0009','Z0010','Z0046']
	ServiceProducts=['Z0091','Z0092','Z0007','Z0110','Z0010','Z0009','Z0046','Z0100','Z0090','Z0006','Z0103','Z0113','Z0114','Z0068','Z0115','Z0111']
	for prd in ServiceProducts:
		#Log.Info('script called--90--service id-----'+str(prd))
		Product.GetContainerByName('Services').AddNewRow(str(prd),False)
# Added this list and conduction for pricing calculation in Segment tab
def enable_disable_execute_rules():
	sql_obj_cnt = Sql.GetFirst(
		"SELECT count(Q.RECORD_ID) as cnt FROM SYSEFL Q (NOLOCK) INNER JOIN  SYOBJD D (NOLOCK) ON Q.API_NAME=D.OBJECT_NAME INNER JOIN SYSECT S (NOLOCK) ON S.RECORD_ID=Q.SECTION_RECORD_ID INNER JOIN SYPAGE SP (NOLOCK) ON SP.RECORD_ID = S.PAGE_RECORD_ID INNER JOIN SYTABS T (NOLOCK) ON T.RECORD_ID=SP.TAB_RECORD_ID WHERE T.APP_LABEL='"
		+ Product.Name
		+ "' AND D.DATA_TYPE!='FORMULA' "
	)
	
	sql_cnt = sql_obj_cnt.cnt

	if sql_cnt > 1000:
		modVal = (sql_cnt / 1000) + 1
	else:
		modVal = 1
	j = 1
	DivVal = 1
	for i in range(modVal):
		EndCount = 1000 * j
		sql_obj = Sql.GetList(
			"select top 1000 * from (SELECT Q.SAPCPQ_ATTRIBUTE_NAME as RECORD_ID,D.DATA_TYPE, ROW_NUMBER() OVER( order by Q.RECORD_ID) AS ROW FROM SYSEFL Q (NOLOCK) INNER JOIN  SYOBJD D (NOLOCK) ON Q.API_NAME=D.OBJECT_NAME INNER JOIN SYSECT S (NOLOCK) ON S.RECORD_ID=Q.SECTION_RECORD_ID INNER JOIN SYPAGE SP (NOLOCK) ON SP.RECORD_ID = S.PAGE_RECORD_ID INNER JOIN SYTABS T (NOLOCK) ON T.RECORD_ID=SP.TAB_RECORD_ID WHERE T.APP_LABEL='"
			+ Product.Name
			+ "' AND D.DATA_TYPE!='FORMULA' "
			+ ") m where m.ROW BETWEEN "
			+ str(DivVal)
			+ " and "
			+ str(EndCount)
			+ " "
		)
		DivVal = EndCount
		j += 1
		if sql_obj is not None:
			for sql in sql_obj:
				if str(sql.DATA_TYPE) == "LONG TEXT AREA":
					QSTN_ID = "QSTN_" + str(sql.RECORD_ID).replace("-", "_") + "_LONG"
				else:
					QSTN_ID = "QSTN_" + str(sql.RECORD_ID).replace("-", "_")
				if Product.Attributes.GetByName(QSTN_ID) is not None:
					Product.Attributes.GetByName(QSTN_ID).ExecuteRulesOnChange = False

	sql_obj_R_cnt = Sql.GetFirst("SELECT count(RECORD_ID) as cnt FROM SYOBJR (NOLOCK)")
	sqlR_cnt = sql_obj_R_cnt.cnt

	if sqlR_cnt > 1000:
		modRVal = (sqlR_cnt / 1000) + 1
	else:
		modRVal = 1
	jR = 1
	DivValR = 1
	for i in range(modRVal):
		EndRCount = 1000 * jR
		sql_obj_R = Sql.GetList(
			"select top 1000 * from (SELECT SAPCPQ_ATTRIBUTE_NAME as RECORD_ID, ROW_NUMBER() OVER( order by RECORD_ID) AS ROW FROM SYOBJR (NOLOCK) )m where m.ROW BETWEEN "
			+ str(DivVal)
			+ " and "
			+ str(EndCount)
			+ " "
		)
		DivValR = EndRCount
		jR += 1
		if sql_obj_R is not None:
			for sql in sql_obj_R:
				QSTN_ID = "QSTN_R_" + str(sql.RECORD_ID).replace("-", "_")
				if Product.Attributes.GetByName(QSTN_ID) is not None:
					Product.Attributes.GetByName(QSTN_ID).ExecuteRulesOnChange = False
	return 'data'


enable_disable_execute_rules()
"""
if Product.PartNumber =="QT" and Product.Attributes.GetByName('Services') is not None:
	Log.Info('script called--87--')
	ServiceProducts=['Z0090','Z0091','Z0092','Z0006','Z0007','Z0035','Z0110','Z0108','Z0009','Z0010','Z0046']
	for prd in ServiceProducts:
		Log.Info('script called--90-----')
		Product.GetContainerByName('Services').AddNewRow(str(prd),False)
		#Product.GetContainerByName('Services').AddNewRow('Z0092',False)"""