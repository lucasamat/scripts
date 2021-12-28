# =========================================================================================================================================
#   __script_name : CQC4CWBCPQ.PY
#   __script_description : TO UPDATE THE SAQDLT TABLE DATA IN CPQ WHEN THE USER IS CHANGING THE SALES TEAM DETAILS IN C4C.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :24-11-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import sys
import datetime 
Sql = SQL()

def salesteam_insert(employee,quote_object,quote_rev_id,quote_revision_record_id,quote_record_id):
    Sql.RunQuery("""INSERT SAQDLT (
                            C4C_PARTNERFUNCTION_ID,
                            CRM_PARTNERFUNCTION_ID,
                            PARTNERFUNCTION_DESC,
                            PARTNERFUNCTION_ID,
                            PARTNERFUNCTION_RECORD_ID,
                            EMAIL,
                            MEMBER_ID,
                            MEMBER_NAME,
                            MEMBER_RECORD_ID,
                            QUOTE_ID,
                            QUOTE_RECORD_ID,
                            QTEREV_ID,
                            QTEREV_RECORD_ID,
                            QUOTE_REV_DEAL_TEAM_MEMBER_ID,
                            CPQTABLEENTRYADDEDBY,
                            CPQTABLEENTRYDATEADDED,
                            CpqTableEntryModifiedBy, 
                            CpqTableEntryDateModified
                            ) SELECT emp.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_DEAL_TEAM_MEMBER_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                            SELECT DISTINCT  
                            (SELECT TOP 1 C4C_PARTNER_FUNCTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION =
                            CASE '{C4c_partner_function}' 
                            WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                            WHEN '46' THEN 'SALES EMPLOYEE'
                            WHEN '213' THEN 'PARTNER CONTACT'
                            WHEN 'Z1' THEN 'BD'
                            WHEN 'Z2' THEN 'BD MANAGER'
                            WHEN 'Z3' THEN 'SALES ADMIN'
                            WHEN 'Z4' THEN 'SALES MANAGER'
                            WHEN 'Z5' THEN 'SALES REP'
                            WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                            WHEN 'ZFM' THEN 'FINANCE MANAGER'
                            ELSE 'FOB'
                            END ) AS C4C_PARTNERFUNCTION_ID,
                            (SELECT TOP 1 CRM_PARTNERFUNCTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = CASE '{C4c_partner_function}' 
                            WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                            WHEN '46' THEN 'SALES EMPLOYEE'
                            WHEN '213' THEN 'PARTNER CONTACT'
                            WHEN 'Z1' THEN 'BD'
                            WHEN 'Z2' THEN 'BD MANAGER'
                            WHEN 'Z3' THEN 'SALES ADMIN'
                            WHEN 'Z4' THEN 'SALES MANAGER'
                            WHEN 'Z5' THEN 'SALES REP'
                            WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                            WHEN 'ZFM' THEN 'FINANCE MANAGER'
                            ELSE 'FOB'
                            END ) AS CRM_PARTNERFUNCTION_ID,
                            (SELECT TOP 1 PARTNERFUNCTION_DESCRIPTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = CASE '{C4c_partner_function}' 
                            WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                            WHEN '46' THEN 'SALES EMPLOYEE'
                            WHEN '213' THEN 'PARTNER CONTACT'
                            WHEN 'Z1' THEN 'BD'
                            WHEN 'Z2' THEN 'BD MANAGER'
                            WHEN 'Z3' THEN 'SALES ADMIN'
                            WHEN 'Z4' THEN 'SALES MANAGER'
                            WHEN 'Z5' THEN 'SALES REP'
                            WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                            WHEN 'ZFM' THEN 'FINANCE MANAGER'
                            ELSE 'FOB'
                            END ) AS PARTNERFUNCTION_DESC,
                            (SELECT TOP 1 PARTNERFUNCTION_ID FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = CASE '{C4c_partner_function}' 
                            WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                            WHEN '46' THEN 'SALES EMPLOYEE'
                            WHEN '213' THEN 'PARTNER CONTACT'
                            WHEN 'Z1' THEN 'BD'
                            WHEN 'Z2' THEN 'BD MANAGER'
                            WHEN 'Z3' THEN 'SALES ADMIN'
                            WHEN 'Z4' THEN 'SALES MANAGER'
                            WHEN 'Z5' THEN 'SALES REP'
                            WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                            WHEN 'ZFM' THEN 'FINANCE MANAGER'
                            ELSE 'FOB'
                            END ) AS PARTNERFUNCTION_ID,
                            (SELECT TOP 1 PARTNERFUNCTION_RECORD_ID FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = CASE '{C4c_partner_function}' 
                            WHEN '39' THEN 'EMPLOYEE RESPONSIBLE'
                            WHEN '46' THEN 'SALES EMPLOYEE'
                            WHEN '213' THEN 'PARTNER CONTACT'
                            WHEN 'Z1' THEN 'BD'
                            WHEN 'Z2' THEN 'BD MANAGER'
                            WHEN 'Z3' THEN 'SALES ADMIN'
                            WHEN 'Z4' THEN 'SALES MANAGER'
                            WHEN 'Z5' THEN 'SALES REP'
                            WHEN 'ZCM' THEN 'CONTRACT MANAGER'
                            WHEN 'ZFM' THEN 'FINANCE MANAGER'
                            ELSE 'FOB'
                            END ) AS PARTNERFUNCTION_RECORD_ID,
                            SAEMPL.EMAIL,
                            SAEMPL.EMPLOYEE_ID,
                            SAEMPL.EMPLOYEE_NAME,
                            SAEMPL.EMPLOYEE_RECORD_ID,
                            '{QuoteId}' as QUOTE_ID,
                            '{QuoteRecordId}' as QUOTE_RECORD_ID,
                            '{RevisionId}' as QTEREV_ID,
                            '{RevisionRecordId}' as QTEREV_RECORD_ID
                            FROM SAEMPL WHERE EMPLOYEE_ID = '{EmployeeId}'
                            ) emp """.format(
                            UserId = User.Id,
                            EmployeeId = employee.get("EMPLOYEE_ID"),
                            C4c_partner_function = employee.get("C4C_PARTNER_FUNCTION"),
                            UserName=User.Name,
                            QuoteId = quote_object.QUOTE_ID,
                            QuoteRecordId=quote_object.MASTER_TABLE_QUOTE_RECORD_ID,
                            RevisionId=quote_rev_id,
                            RevisionRecordId=quote_revision_record_id,
                            )
                        )
    created_by_master_rec = None
    created_by_master_rec = Sql.GetFirst("SELECT C4C_PARTNER_FUNCTION,PARTNERFUNCTION_DESCRIPTION,PARTNERFUNCTION_ID,PARTNERFUNCTION_RECORD_ID FROM SYPFTY (NOLOCK) WHERE C4C_PARTNER_FUNCTION = 'CREATED BY'")
    if created_by_master_rec:
        salesteam_object = Sql.GetFirst("SELECT C4C_PARTNERFUNCTION_ID FROM SAQDLT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND C4C_PARTNERFUNCTION_ID = 'CREATED BY'".format(quote_object.MASTER_TABLE_QUOTE_RECORD_ID))
        if not salesteam_object:
            quote_employee_obj = Sql.GetFirst("SELECT MEMBER_ID FROM SAQDLT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND C4C_PARTNERFUNCTION_ID = 'EMPLOYEE RESPONSIBLE' ".format(quote_object.MASTER_TABLE_QUOTE_RECORD_ID))
            if quote_employee_obj is not None:
                employee_object = Sql.GetFirst("SELECT EMAIL,EMPLOYEE_ID,EMPLOYEE_NAME,EMPLOYEE_RECORD_ID FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_ID = '{EmployeeId}'".format(EmployeeId = quote_employee_obj.MEMBER_ID))
                sales_team_table = Sql.GetTable("SAQDLT")
                sales_team_createdby_insert ={
                    "QUOTE_REV_DEAL_TEAM_MEMBER_ID": str(Guid.NewGuid()).upper(),
                    "C4C_PARTNERFUNCTION_ID": created_by_master_rec.C4C_PARTNER_FUNCTION,
                    "PARTNERFUNCTION_DESC": created_by_master_rec.PARTNERFUNCTION_DESCRIPTION,
                    "PARTNERFUNCTION_ID": created_by_master_rec.PARTNERFUNCTION_ID,
                    "PARTNERFUNCTION_RECORD_ID": created_by_master_rec.PARTNERFUNCTION_RECORD_ID,
                    "EMAIL": employee_object.EMAIL,
                    "MEMBER_ID": employee_object.EMPLOYEE_ID,
                    "MEMBER_NAME": employee_object.EMPLOYEE_NAME,
                    "MEMBER_RECORD_ID": employee_object.EMPLOYEE_RECORD_ID,
                    "QUOTE_ID": quote_object.QUOTE_ID,
                    "QUOTE_RECORD_ID": quote_object.MASTER_TABLE_QUOTE_RECORD_ID,
                    "QTEREV_ID": quote_rev_id,
                    "QTEREV_RECORD_ID": quote_revision_record_id,
                }
                sales_team_table.AddRow(sales_team_createdby_insert)
                Sql.Upsert(sales_team_table)

#try:
if 'Param' in globals(): 	
    if hasattr(Param, 'CPQ_Columns'):
        for values in Param.CPQ_Columns:
            Key = str(values.Key)
            if str(Key).upper() == "QUOTE_ID":
                quote_id = str(values.Value)
                if quote_id:
                    payload_json_obj = Sql.GetFirst("SELECT INTEGRATION_PAYLOAD, CpqTableEntryId FROM SYINPL (NOLOCK) WHERE INTEGRATION_KEY = '{}' AND ISNULL(STATUS,'') = '' ORDER BY CpqTableEntryId DESC".format(quote_id))
                    Log.Info("CpqTableEntryId  ---------------"+str(payload_json_obj.CpqTableEntryId))
                    if payload_json_obj:
                        payload_json = eval(payload_json_obj.INTEGRATION_PAYLOAD)
                        payload_json = eval(payload_json.get('Param'))
                        payload_json = payload_json.get('CPQ_Columns')
                        if payload_json.get('C4C_Opportunity_Object_ID'):
                            ##To get the opportunity id from the opportunity table by passing opportunity object id receiving from the c4c...
                            opportunity_object =Sql.GetFirst("SELECT OPPORTUNITY_ID FROM SAOPPR(NOLOCK) WHERE C4C_OPPOBJ_ID = '{c4c_opppbj_id}'".format(c4c_opppbj_id = payload_json.get('C4C_Opportunity_Object_ID')) )
                            
                            ##To get the quote record id and revision record id for the c4c opportunity id...
                            revision_object = Sql.GetFirst("SELECT SAQTRV.QUOTE_RECORD_ID ,SAQTRV.QTEREV_RECORD_ID,SAQTRV.QTEREV_ID FROM SAQTRV(NOLOCK) JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID JOIN SAOPPR ON SAOPPR.OPPORTUNITY_ID = SAOPQT.OPPORTUNITY_ID WHERE SAOPPR.C4C_OPPOBJ_ID = '{c4c_opppbj_id}'".format(c4c_opppbj_id = payload_json.get('C4C_Opportunity_Object_ID')))
                            
                            ##To get the quote details for the sales team update(SAQDLT table insert)...
                            quote_object = Sql.GetFirst("SELECT QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(revision_object.QUOTE_RECORD_ID))
                            
                            ##To delete the SAQDLT table before insert the updated record from c4c...
                            Sql.RunQuery("DELETE FROM SAQDLT WHERE QUOTE_RECORD_ID = '{}'".format(revision_object.QUOTE_RECORD_ID))
                        if payload_json.get('SAEMPL'):
                            employee = payload_json.get('SAEMPL')
                            if type(employee) is dict:
                                employee_obj = SqlHelper.GetFirst("select EMPLOYEE_ID from SAEMPL(nolock) where EMPLOYEE_ID = '{employee_id}'".format(employee_id = employee.get("EMPLOYEE_ID")))
                                if employee_obj is None:
                                    country_obj = SqlHelper.GetFirst("select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(country = employee.get("COUNTRY")))
                                    salesorg_obj = SqlHelper.GetFirst("select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(state = employee.get("STATE")))
                                    employee_dict = {}
                                    employee_dict["EMPLOYEE_RECORD_ID"] = str(Guid.NewGuid()).upper()
                                    employee_dict["ADDRESS_1"] = employee.get("ADDRESS1")
                                    employee_dict["ADDRESS_2"] = employee.get("ADDRESS2")
                                    employee_dict["CITY"] = employee.get("CITY")
                                    employee_dict["COUNTRY"] = employee.get("COUNTRY")
                                    employee_dict["COUNTRY_RECORD_ID"] = country_obj.COUNTRY_RECORD_ID  if country_obj else ""
                                    employee_dict["EMAIL"] = employee.get("EMAIL")
                                    employee_dict["EMPLOYEE_ID"] = employee.get("EMPLOYEE_ID")
                                    employee_dict["EMPLOYEE_NAME"] = employee.get("EMPLOYEE_NAME")
                                    employee_dict["EMPLOYEE_STATUS"] = employee.get("EMPLOYEE_STATUS")
                                    employee_dict["FIRST_NAME"] = employee.get("FIRST_NAME")
                                    employee_dict["LAST_NAME"] = employee.get("LAST_NAME")
                                    employee_dict["PHONE"] = employee.get("PHONE")
                                    employee_dict["POSTAL_CODE"] = employee.get("POSTAL_CODE")
                                    employee_dict["STATE"] = employee.get("STATE")
                                    employee_dict["STATE_RECORD_ID"] = salesorg_obj.STATE_RECORD_ID  if salesorg_obj else ""
                                    employee_dict["CRM_EMPLOYEE_ID"] = employee.get("CRM_EMPLOYEE_ID")
                                    employee_dict["C4C_EMPLOYEE_ID"] = employee.get("C4C_EMPLOYEE_ID")
                                    employee_dict["CPQTABLEENTRYADDEDBY"] = User.UserName
                                    employee_dict["CpqTableEntryModifiedBy"] = User.Id
                                    employee_dict["ADDUSR_RECORD_ID"] = User.Id
                                    tableInfo = Sql.GetTable("SAEMPL")
                                    tablerow = employee_dict
                                    tableInfo.AddRow(tablerow)
                                    Sql.Upsert(tableInfo)
                                else:
                                    c4c_employee_update = "UPDATE SAEMPL SET C4C_EMPLOYEE_ID = '{c4c_employee_id}' WHERE EMPLOYEE_ID = '{employee_id}'".format(c4c_employee_id= employee.get("C4C_EMPLOYEE_ID"),employee_id= employee.get("EMPLOYEE_ID"))
                                    Sql.RunQuery(c4c_employee_update)
                                salesteam_insert(employee,quote_object,revision_object.QTEREV_ID,revision_object.QTEREV_RECORD_ID,quote_object.MASTER_TABLE_QUOTE_RECORD_ID)
                            else:
                                for employee in payload_json.get('SAEMPL'):
                                    employee_obj = SqlHelper.GetFirst("select EMPLOYEE_ID from SAEMPL(nolock) where EMPLOYEE_ID = '{employee_id}'".format(employee_id = employee.get("EMPLOYEE_ID")))
                                    if employee_obj is None:
                                        country_obj = SqlHelper.GetFirst("select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(country = employee.get("COUNTRY")))
                                        salesorg_obj = SqlHelper.GetFirst("select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(state = employee.get("STATE")))
                                        employee_dict = {}
                                        employee_dict["EMPLOYEE_RECORD_ID"] = str(Guid.NewGuid()).upper()
                                        employee_dict["ADDRESS_1"] = employee.get("ADDRESS1")
                                        employee_dict["ADDRESS_2"] = employee.get("ADDRESS2")
                                        employee_dict["CITY"] = employee.get("CITY")
                                        employee_dict["COUNTRY"] = employee.get("COUNTRY")
                                        employee_dict["COUNTRY_RECORD_ID"] = country_obj.COUNTRY_RECORD_ID  if country_obj else ""
                                        employee_dict["EMAIL"] = employee.get("EMAIL")
                                        employee_dict["EMPLOYEE_ID"] = employee.get("EMPLOYEE_ID")
                                        employee_dict["EMPLOYEE_NAME"] = employee.get("EMPLOYEE_NAME")
                                        employee_dict["EMPLOYEE_STATUS"] = employee.get("EMPLOYEE_STATUS")
                                        employee_dict["FIRST_NAME"] = employee.get("FIRST_NAME")
                                        employee_dict["LAST_NAME"] = employee.get("LAST_NAME")
                                        employee_dict["PHONE"] = employee.get("PHONE")
                                        employee_dict["POSTAL_CODE"] = employee.get("POSTAL_CODE")
                                        employee_dict["STATE"] = employee.get("STATE")
                                        employee_dict["STATE_RECORD_ID"] = salesorg_obj.STATE_RECORD_ID  if salesorg_obj else ""
                                        employee_dict["CRM_EMPLOYEE_ID"] = employee.get("CRM_EMPLOYEE_ID")
                                        employee_dict["C4C_EMPLOYEE_ID"] = employee.get("C4C_EMPLOYEE_ID")
                                        employee_dict["CPQTABLEENTRYADDEDBY"] = User.UserName
                                        employee_dict["CpqTableEntryModifiedBy"] = User.Id
                                        employee_dict["ADDUSR_RECORD_ID"] = User.Id
                                        tableInfo = Sql.GetTable("SAEMPL")
                                        tablerow = employee_dict
                                        tableInfo.AddRow(tablerow)
                                        Sql.Upsert(tableInfo)
                                    else:
                                        c4c_employee_update = "UPDATE SAEMPL SET C4C_EMPLOYEE_ID = '{c4c_employee_id}' WHERE EMPLOYEE_ID = '{employee_id}'".format(c4c_employee_id= employee.get("C4C_EMPLOYEE_ID"),employee_id= employee.get("EMPLOYEE_ID"))
                                        Sql.RunQuery(c4c_employee_update)
                                    salesteam_insert(employee,quote_object,revision_object.QTEREV_ID,revision_object.QTEREV_RECORD_ID,quote_object.MASTER_TABLE_QUOTE_RECORD_ID) 