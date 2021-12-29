"""Using for Approval Center Actions."""

# =========================================================================================================================================
#   __script_name : ACSECTACTN.PY
#   __script_description : THIS SCRIPT IS USED TO PERFORM SECTION BASED ACTIONS
#   __primary_author__ : VIJAYAKUMAR THANGARASU
#   __create_date :14-02-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import re
import sys
import datetime
import CQCPQC4CWB
import CQREVSTSCH
import clr

import SYCNGEGUID as CPQID
import ACVIORULES

from SYDATABASE import SQL
from datetime import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage


violationruleInsert = ACVIORULES.ViolationConditions()
Sql = SQL()
clr.AddReference("System.Net")
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
#CurrentTabName = TestProduct.CurrentTab
try:
	CurrentTabName = TestProduct.CurrentTab
except:
	CurrentTabName = "Quotes"
class approvalCenter:
	"""Using for Approval Center."""

	def __init__(self, QuoteNumber):
		"""Approvalcenter initializer."""
		self.QuoteNumber = QuoteNumber
		self.UserId = str(User.Id)
		self.UserName = str(User.Name)
		now = datetime.now()
		self.datetime_value = now.strftime("%m/%d/%Y %H:%M:%S")
		self.exceptMessage = ""
		try:
			self.quote_revision_record_id = Quote.GetGlobal('quote_revision_record_id')
		except:
			Trace.Write("EXCEPT: quote_revision_record_id")
			# quote_revision_record_id_query = Sql.GetFirst("SELECT QTEREV_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(self.QuoteNumber)+"'")
			self.quote_revision_record_id = ""
		LOGIN_CREDENTIALS = Sql.GetFirst("SELECT top 1 Domain FROM SYCONF (nolock) order by CpqTableEntryId")
		if LOGIN_CREDENTIALS is not None:
			Login_Domain = str(LOGIN_CREDENTIALS.Domain)
		self.ImagePath = "/mt/" + str(Login_Domain) + "/Additionalfiles/"

	def ApproveVoilationRule(self, AllParams, ACTION, ApproveDesc, CurrentTransId):
		"""Approve and Reject Function."""
		#try:
		Trace.Write("@59")
		Product.SetGlobal("ApprovalMasterRecId", str(self.QuoteNumber))
		if CurrentTabName == 'Quotes':
			quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT (NOLOCK) where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=self.quote_revision_record_id))
			quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID

			if quote_obj is not None:
				approval_queue_obj = Sql.GetFirst("SELECT ACAPMA.APPROVAL_RECORD_ID FROM ACAPMA (NOLOCK) JOIN ACAPTX (NOLOCK) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID and ACAPMA.APRCHN_RECORD_ID = ACAPTX.APRCHN_RECORD_ID where APRSTAMAP_APPROVALSTATUS <> 'RECALLED' AND ACAPTX.APPROVAL_TRANSACTION_RECORD_ID ='{CurrentTransId}'".format(CurrentTransId=CurrentTransId))
				self.QuoteNumber = approval_queue_obj.APPROVAL_RECORD_ID 
			# APRTRXOBJ_RECORD_ID = '{quote_record_id}' AND
		else:
			transaction_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPTX where APPROVAL_TRANSACTION_RECORD_ID = '{TransactionId}'".format(TransactionId = self.QuoteNumber))
			self.QuoteNumber = transaction_obj.APPROVAL_RECORD_ID
		if str(ACTION) == "APPROVE":
			Getchaintype = Sql.GetFirst(
				"""SELECT APPROVAL_METHOD FROM ACAPMA (NOLOCK) INNER JOIN ACAPCH (NOLOCK)
				ON ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID
				WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
					QuoteNumber=str(self.QuoteNumber),
				)
			)                
			if ApproveDesc == '':                    
				ApproveDesc ='Approved '+ str(self.datetime_value)
			else:
				ApproveDesc = str(ApproveDesc)+" "+str(self.datetime_value)
			Transupdate = """UPDATE ACAPTX
					SET APPROVALSTATUS = 'APPROVED',
					APPROVED_BY = '{UserName}',
					APPROVEDBY_RECORD_ID = '{UserId}',
					RECIPIENT_COMMENTS = '{ApproveDesc}'
					WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
					and APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' 
					AND ARCHIVED = 0""".format(
				UserId=str(self.UserId),
				UserName=str(self.UserName),
				ApproveDesc=str(ApproveDesc),
				QuoteNumber=str(self.QuoteNumber),
				getCpqId=str(CurrentTransId),
			)
			##Finding the UNANIMOUS_CONSENT value from the chain step code starts....
			transaction_obj = Sql.GetFirst("""SELECT APRCHN_ID,APRCHNSTP_RECORD_ID,APPROVAL_ID FROM ACAPTX WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' and APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}'""".format(QuoteNumber=str(self.QuoteNumber),getCpqId=str(CurrentTransId)))
			chain_step_obj = Sql.GetFirst("""select UNANIMOUS_CONSENT from ACACST where APRCHN_ID = '{approval_chain_id}' and APPROVAL_CHAIN_STEP_RECORD_ID = '{approval_chain_step_record_id}'""".format(approval_chain_id = transaction_obj.APRCHN_ID,approval_chain_step_record_id = transaction_obj.APRCHNSTP_RECORD_ID))
			if str(chain_step_obj.UNANIMOUS_CONSENT).upper() == 'FALSE':
				Transaction_update = """UPDATE ACAPTX
					SET APPROVALSTATUS = 'APPROVAL NO LONGER REQUIRED',
					APPROVED_BY = '{UserName}',
					APPROVEDBY_RECORD_ID = '{UserId}',
					RECIPIENT_COMMENTS = 'Approval No Longer Required'
					WHERE APRCHNSTP_RECORD_ID = '{chain_step_record_id}'
					AND APRCHN_ID = '{chain_id}'
					AND APPROVAL_ID LIKE '%{approval_id}'
					AND ARCHIVED = 0""".format(
				UserId=str(self.UserId),
				UserName=str(self.UserName),
				ApproveDesc=str(ApproveDesc),
				chain_step_record_id=str(transaction_obj.APRCHNSTP_RECORD_ID),
				chain_id = transaction_obj.APRCHN_ID,
				approval_id = transaction_obj.APPROVAL_ID
				)        
				a = Sql.RunQuery(Transaction_update)
			##Finding the UNANIMOUS_CONSENT value from the chain step code ends....
			UpdateApproverv = """UPDATE ACAPMA
					SET CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}'
					WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
				QuoteNumber=str(self.QuoteNumber), datetime_value=self.datetime_value
			)
			a = Sql.RunQuery(Transupdate)
			b = Sql.RunQuery(UpdateApproverv)
			approvetresponse = self.sendmailNotification("Approve", CurrentTransId)
			Notificationresponse = self.sendmailNotification("Notification",CurrentTransId)
			GetCurStatus = Sql.GetFirst(
				"""SELECT APPROVAL_RECORD_ID,ACACST.WHERE_CONDITION_01,
						SYOBJH.OBJECT_NAME,ACAPTX.APPROVAL_ID,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,
						ACAPTX.REQUESTOR_COMMENTS
						FROM ACAPTX (NOLOCK)
						INNER JOIN ACACST (NOLOCK) ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
						INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
						WHERE ACAPTX.APPROVAL_RECORD_ID = '{QuoteNumber}'
						AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' 
						AND ACAPTX.ARCHIVED = 0""".format(
					QuoteNumber=str(self.QuoteNumber), UserId=str(self.UserId)
				)
			)
			if GetCurStatus:
				targetObj = str(GetCurStatus.OBJECT_NAME)
				wherecond = str(GetCurStatus.WHERE_CONDITION_01)
				currentObj = str(GetCurStatus.APPROVAL_ID).split("-")
				ObjectName = str(currentObj[0])
				#GettingSnapshot = violationruleInsert.SnapshotDataInsert(str(targetObj), str(wherecond), ObjectName)
				Wherecond1 = """ WHERE ACAPTX.APPROVAL_RECORD_ID = '{secCondi}' AND
					ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '{CurTransid}' """.format(
					secCondi=str(self.QuoteNumber), CurTransid=str(GetCurStatus.APPROVAL_TRANSACTION_RECORD_ID),
				)
				#SnapshorQuery = GettingSnapshot + Wherecond1
				#Snapshotinsert = Sql.RunQuery(SnapshorQuery)
			round_approve_status = Sql.GetList("SELECT DISTINCT APPROVALSTATUS FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{secCondi}'".format(secCondi=str(self.QuoteNumber)))
			round_status = []
			for i in round_approve_status:
				round_status.append(i.APPROVALSTATUS)
			if ('APPROVED' in round_status and ('APPROVAL REQUIRED' not in round_status and 'REQUESTED' not in round_status and 'REJECTED' not in round_status) ):
				completed_date = "True"
			else:
				completed_date = 'False'
			
			if completed_date == "True":
				UPDATE_ACACHR = """ UPDATE ACACHR SET ACACHR.COMPLETED_BY = '{UserName}',ACACHR.COMPLETEDBY_RECORD_ID='{UserId}', COMPLETED_DATE = '{datetime_value}' WHERE ACACHR.APPROVAL_RECORD_ID='{QuoteNumber}'""".format(UserId=self.UserId,UserName=self.UserName,datetime_value=self.datetime_value,QuoteNumber=self.QuoteNumber)
			else:
				UPDATE_ACACHR = """ UPDATE ACACHR SET ACACHR.COMPLETED_BY = '{UserName}',ACACHR.COMPLETEDBY_RECORD_ID='{UserId}',COMPLETED_DATE = NULL WHERE ACACHR.APPROVAL_RECORD_ID='{QuoteNumber}'""".format(UserId=self.UserId,UserName=self.UserName,datetime_value=self.datetime_value,QuoteNumber=self.QuoteNumber)
			Sql.RunQuery(UPDATE_ACACHR)
			if str(Getchaintype.APPROVAL_METHOD).upper() == "PARALLEL STEP APPROVAL":
				Curapprovestep = Sql.GetFirst(
					" SELECT ACAPTX.* FROM ACAPTX (NOLOCK) WHERE APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' AND ARCHIVED = 0".format(
						QuoteNumber=str(QuoteNumber), getCpqId=str(CurrentTransId),
					)
				)
				lateststepId = Sql.GetFirst(
					"""SELECT * FROM ACAPMA (NOLOCK) WHERE
					ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
					AND CUR_APRCHNSTP<{ids} AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
						QuoteNumber=str(self.QuoteNumber), ids=int(Curapprovestep.APRCHNSTP_ID)
					)
				)
				if lateststepId is not None:
					Currsteprecordcheck = Sql.GetFirst(
						"""SELECT * FROM ACAPTX (NOLOCK) WHERE APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' AND ARCHIVED = 0
						AND APRCHNSTP_RECORD_ID IN ( SELECT APRCHNSTP_RECORD_ID FROM ACAPMA(NOLOCK)
						WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED') """.format(
							QuoteNumber=str(QuoteNumber), getCpqId=str(CurrentTransId)
						)
					)
					if Currsteprecordcheck is None:
						Getcurrentapprovestep = Sql.GetFirst(
							""" SELECT * FROM ACAPTX (NOLOCK) INNER JOIN ACACST(NOLOCK)
							ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
							INNER JOIN ACACSA (NOLOCK) ON
							ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
							WHERE APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' AND ARCHIVED = 0""".format(
								QuoteNumber=str(QuoteNumber), getCpqId=str(CurrentTransId),
							)
						)
						ChangeStepApproverv = """UPDATE ACAPMA SET CUR_APPCHNSTP_APPROVER_ID = '{approverId}'
									,CUR_APRCHNSTP_APPROVER_RECORD_ID = '{ApproverRecId}',CUR_APRCHNSTP = '{ChaindStep}'
									,CUR_APRCHNSTP_ENTRYDATE = '{datetime_value}',
									CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}',
									APRCHNSTP_RECORD_ID = '{ChainStepRecId}' WHERE
									APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
							approverId=str(Getcurrentapprovestep.APRCHNSTP_APPROVER_ID),
							ApproverRecId=str(Getcurrentapprovestep.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID),
							ChaindStep=str(Getcurrentapprovestep.APRCHNSTP_NUMBER),
							datetime_value=self.datetime_value,
							ChainStepRecId=str(Getcurrentapprovestep.APPROVAL_CHAIN_STEP_RECORD_ID),
							QuoteNumber=str(self.QuoteNumber),
						)
						a1 = Sql.RunQuery(ChangeStepApproverv)
				statusupdate = True

				not_approved_transaction_obj = Sql.GetFirst(
					"""SELECT count(CpqTableEntryId) as cnt FROM ACAPTX (NOLOCK)
						WHERE APRTRXOBJ_ID = '{QuoteId}' AND ARCHIVED = 0 AND APPROVALSTATUS not in ('APPROVED','APPROVAL NO LONGER REQUIRED')""".format(
						QuoteId=str(quote_obj.QUOTE_ID)
					)
				)
				if not_approved_transaction_obj.cnt > 0:
					statusupdate = False
				
				Checkunanimous = Sql.GetList(
					"""SELECT * FROM ACAPTX (NOLOCK) WHERE UNANIMOUS_CONSENT = 'True' AND ARCHIVED = 0
					AND APPROVALSTATUS <> 'APPROVED' AND APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
						QuoteNumber=str(self.QuoteNumber)
					)
				)
				if statusupdate == True and len(Checkunanimous) <= 0:
					GetCurStatus = Sql.GetFirst(
						"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
								ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
								FROM ACACSS (NOLOCK)
								INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID = SYOBJD.PARENT_OBJECT_RECORD_ID
								INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
								INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
								WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
								AND APPROVALSTATUS = 'APPROVED' AND ACAPMA.APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
							QuoteNumber=str(self.QuoteNumber)
						)
					)
					if GetCurStatus:
						
						MainObjUpdateQuery = """UPDATE SAQTRV SET
							REVISION_STATUS = 'APPROVED'
							WHERE {primaryKey} = '{Primaryvalue}' """.format(
							statusUpdate = str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
							ObjName=str(GetCurStatus.OBJECT_NAME),
							ApiName=str(GetCurStatus.API_NAME),
							Primaryvalue=str(GetCurStatus.APRTRXOBJ_RECORD_ID),
							primaryKey = str(GetCurStatus.RECORD_NAME )
						)
						b = Sql.RunQuery(MainObjUpdateQuery)
						UpdateApproverv = """UPDATE ACAPMA SET APRSTAMAP_APPROVALSTATUS = 'APPROVED',
							APROBJ_STATUSFIELD_VALUE = 'APPROVED FOR PUBLISHING',
							CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}',
							FIN_APPROVE_DATE = '{datetime_value}',
							FIN_APPROVE_USER_ID = '{UserName}',FIN_APPROVE_USER_RECORD_ID = '{UserId}'
							WHERE APPROVAL_RECORD_ID = '{approvalId}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
							approvalId=(self.QuoteNumber),
							datetime_value=self.datetime_value,
							UserId=str(self.UserId),
							UserName=str(self.UserName),
						)
						c = Sql.RunQuery(UpdateApproverv)
						response = self.cbcmailtrigger()
						getQuote = Sql.GetFirst(
							"SELECT QUOTE_ID,QUOTE_STATUS FROM SAQTMT WHERE QTEREV_RECORD_ID = '{}'".format(self.quote_revision_record_id)
						)
						if getQuote.QUOTE_STATUS == "APPROVED":
							
							result = ScriptExecutor.ExecuteGlobal("QTPOSTACRM", {"QUOTE_ID": getQuote.QUOTE_ID, 'Fun_type':'cpq_to_crm'})
			else:
				
				GetCurrentTranStatus = Sql.GetFirst(
					"""SELECT ACAPTX.* FROM ACAPMA (NOLOCK) INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_ID =
						ACAPTX.APPROVAL_ID AND ACAPMA.APRCHNSTP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID AND ACAPTX.APPROVAL_RECORD_ID = ACAPMA.APPROVAL_RECORD_ID WHERE APPROVALSTATUS = 'REQUESTED' AND ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ACAPMA.APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
						QuoteNumber=str(self.QuoteNumber)
					)
				)
				if GetCurrentTranStatus is None:
					GetCurrentStrpId = Sql.GetFirst(
						"SELECT APRCHN_ID,CUR_APRCHNSTP,APRCHN_RECORD_ID,ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_ID FROM ACAPMA (nolock)"
						+ " WHERE ACAPMA.APPROVAL_RECORD_ID = '"
						+ str(self.QuoteNumber)
						+ "' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'"
					)
					restrictstepList = ""
					##check smart approval starts
					smart_approval = Sql.GetFirst("""SELECT DISTINCT ACACST.APRCHNSTP_NUMBER FROM ACAPTX (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTX.APRCHN_RECORD_ID = ACACST.APRCHN_RECORD_ID AND ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID WHERE ACAPTX.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ACACST.ENABLE_SMARTAPPROVAL = 1 AND ACAPTX.APPROVALSTATUS IN ('APPROVED','APPROVAL NO LONGER REQUIRED')""".format(QuoteNumber = str(self.QuoteNumber) ))
					if smart_approval is not None and int(GetCurrentStrpId.CUR_APRCHNSTP) <= int(smart_approval.APRCHNSTP_NUMBER):
						
						currentStep = int(smart_approval.APRCHNSTP_NUMBER)    
					else:
						currentStep = int(GetCurrentStrpId.CUR_APRCHNSTP)
					##checking smart approval ends
					for restrict in range(1, currentStep + 1):
						restrictstepList += "'" + str(restrict) + "'"
						if restrict != currentStep:
							restrictstepList += ","
					result = Sql.GetFirst(
						"SELECT TOP 1  * FROM ACACST (NOLOCK) WHERE APRCHN_RECORD_ID = '"
						+ str(GetCurrentStrpId.APRCHN_RECORD_ID)
						+ "' AND WHERE_CONDITION_01 <> '' AND APRCHNSTP_NUMBER NOT IN ("
						+ str(restrictstepList)
						+ ") ORDER BY ACACST.APRCHNSTP_NUMBER "
					)
					if result:
						GetObjName = Sql.GetFirst(
							"SELECT OBJECT_NAME FROM SYOBJH (NOLOCK) WHERE RECORD_ID = '"
							+ str(result.TSTOBJ_RECORD_ID)
							+ "'"
						)
						Select_Query = (
							"SELECT * FROM "
							+ str(GetObjName.OBJECT_NAME)
							+ " (NOLOCK) WHERE "
							+ str(result.WHERE_CONDITION_01)
						)
						getObjSplit = str(GetCurrentStrpId.APPROVAL_ID).split("-")
						ObjectName = getObjSplit[0]
						if ObjectName != str(GetObjName.OBJECT_NAME):
							TargeobjRelation = Sql.GetFirst(
								"SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE DATA_TYPE = 'LOOKUP' AND LOOKUP_OBJECT = '"
								+ str(ObjectName)
								+ "' AND OBJECT_NAME = '"
								+ str(GetObjName.OBJECT_NAME)
								+ "' "
							)
							PrimaryValue = str(GetCurrentStrpId.APRTRXOBJ_RECORD_ID)
							Select_Query += " AND " + str(TargeobjRelation.API_NAME) + " = '" + str(PrimaryValue) + "' "
						else:
							TargeobjRelation = Sql.GetFirst(
								"SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '"                                   
								+ str(GetObjName.OBJECT_NAME)
								+ "' "
							)
							Select_Query += " AND " + str(TargeobjRelation.API_NAME) + " = '" + str(GetCurrentStrpId.APRTRXOBJ_RECORD_ID) + "' "
						SqlQuery = Sql.GetFirst(Select_Query)
						if SqlQuery:
							GetApproveretail = Sql.GetFirst(
								"""SELECT APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,APRCHNSTP_APPROVER_ID,
								APPROVAL_CHAIN_STEP_RECORD_ID,ACACST.APRCHNSTP_NUMBER
								FROM ACACST (NOLOCK)
								INNER JOIN ACACSA (NOLOCK)
								ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
								WHERE ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = '{ChainRecordId}' """.format(
									ChainRecordId=str(result.APPROVAL_CHAIN_STEP_RECORD_ID)
								)
							)
							if GetApproveretail:
								ChangeStepApproverv = """UPDATE ACAPMA SET CUR_APPCHNSTP_APPROVER_ID = '{approverId}'
								,CUR_APRCHNSTP_APPROVER_RECORD_ID = '{ApproverRecId}',CUR_APRCHNSTP = '{ChaindStep}'
								,CUR_APRCHNSTP_ENTRYDATE = '{datetime_value}',
								CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}',
								APRCHNSTP_RECORD_ID = '{ChainStepRecId}' WHERE
								APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
									approverId=str(GetApproveretail.APRCHNSTP_APPROVER_ID),
									ApproverRecId=str(GetApproveretail.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID),
									ChaindStep=str(GetApproveretail.APRCHNSTP_NUMBER),
									datetime_value=self.datetime_value,
									ChainStepRecId=str(GetApproveretail.APPROVAL_CHAIN_STEP_RECORD_ID),
									QuoteNumber=str(self.QuoteNumber),
								)
								GetStatus = Sql.GetFirst(
									"""SELECT ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHNSTP_RECORD_ID
										FROM ACACSS (NOLOCK)
										INNER JOIN ACAPMA (NOLOCK) ON ACACSS.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
										WHERE ACACSS.APPROVALSTATUS = 'REQUESTED'
										AND APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
										QuoteNumber=str(self.QuoteNumber)
									)
								)
								if GetStatus:
									UpdateTrans = """UPDATE ACAPTX SET
										APPROVALSTATUS = 'REQUESTED',
										REQUESTOR_COMMENTS = '{RequestDesc}'
										WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
										AND APRCHNSTP_RECORD_ID = '{stepRecordId}' AND ARCHIVED = 0""".format(
										QuoteNumber=str(self.QuoteNumber),
										RequestDesc=str(GetCurStatus.REQUESTOR_COMMENTS),
										stepRecordId=str(GetApproveretail.APPROVAL_CHAIN_STEP_RECORD_ID),
									)
								c = Sql.RunQuery(ChangeStepApproverv)
								d = Sql.RunQuery(UpdateTrans)
								approvetresponse = self.sendmailNotification("Request")
					else:
						Trace.Write('###393')
						GetCurStatus = Sql.GetFirst(
							"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
								ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
								FROM ACACSS (NOLOCK)
								INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID = SYOBJD.PARENT_OBJECT_RECORD_ID
								INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
								INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
								WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
								AND APPROVALSTATUS = 'APPROVED' AND ACAPMA.APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
								QuoteNumber=str(self.QuoteNumber)
							)
						)
						if GetCurStatus:
							 
							##updating main table only if the all chains are approved starts
							statusupdate = True
							not_approved_transaction_obj = Sql.GetFirst(
								"""SELECT count(CpqTableEntryId) as cnt FROM ACAPTX (NOLOCK)
								WHERE APRTRXOBJ_ID = '{QuoteId}' AND ARCHIVED = 0 AND APPROVALSTATUS NOT IN ('APPROVED','APPROVAL NO LONGER REQUIRED')""".format(
								QuoteId=str(quote_obj.QUOTE_ID)
								)
							)
							if not_approved_transaction_obj and not_approved_transaction_obj.cnt > 0:
								statusupdate = False
							
							if statusupdate == True:
								MainObjUpdateQuery = """UPDATE SAQTRV SET
									REVISION_STATUS = 'APPROVED' 
									WHERE {primaryKey} = '{Primaryvalue}' """.format(
									statusUpdate = str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
									ObjName=str(GetCurStatus.OBJECT_NAME),
									ApiName=str(GetCurStatus.API_NAME),
									Primaryvalue=str(GetCurStatus.APRTRXOBJ_RECORD_ID),
									primaryKey = str(GetCurStatus.RECORD_NAME )
								)
								b = Sql.RunQuery(MainObjUpdateQuery)
							###updating main table only if the all chains are approved ends
							UpdateApproverv = """UPDATE ACAPMA SET APRSTAMAP_APPROVALSTATUS = 'APPROVED',
								APROBJ_STATUSFIELD_VALUE = 'APPROVED FOR PUBLISHING',
								CUR_APRCHNSTP_LASTACTIONDATE= '{datetime_value}',
								FIN_APPROVE_DATE = '{datetime_value}',
								FIN_APPROVE_USER_ID = '{UserName}',FIN_APPROVE_USER_RECORD_ID = '{UserId}'
								WHERE APPROVAL_RECORD_ID = '{approvalId}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
								approvalId=(self.QuoteNumber),
								datetime_value=self.datetime_value,
								UserId=str(self.UserId),
								UserName=str(self.UserName),
							)
							c = Sql.RunQuery(UpdateApproverv)
							response = self.cbcmailtrigger()
							getQuote = Sql.GetFirst(
								"SELECT QUOTE_ID,QUOTE_STATUS FROM SAQTMT WHERE QTEREV_RECORD_ID = '{}'".format(self.quote_revision_record_id)
							)
							if getQuote.QUOTE_STATUS == "APPROVED":
								
								result = ScriptExecutor.ExecuteGlobal("QTPOSTACRM", {"QUOTE_ID": getQuote.QUOTE_ID, 'Fun_type':'cpq_to_crm'})
		elif str(ACTION) == "REJECT":
			if ApproveDesc == '':                    
				ApproveDesc = str(self.datetime_value)
			else:
				ApproveDesc = str(ApproveDesc)+" "+str(self.datetime_value)
			Transupdate = """UPDATE ACAPTX SET
					APPROVALSTATUS = 'REJECTED',
					REJECTED_BY = '{UserName}',
					REJECTBY_RECORD_ID = '{UserId}',
					RECIPIENT_COMMENTS = '{ApproveDesc}'
					WHERE APPROVAL_RECIPIENT_RECORD_ID = '{UserId}'
					AND APPROVAL_RECORD_ID = '{QuoteNumber}'
					AND APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' AND ARCHIVED = 0""".format(
				UserId=str(self.UserId),
				UserName=str(self.UserName),
				ApproveDesc=str(ApproveDesc),
				QuoteNumber=str(self.QuoteNumber),
				getCpqId=str(CurrentTransId),
			)

			UpdateApprovere = """UPDATE ACAPMA SET APRSTAMAP_APPROVALSTATUS = 'REJECTED',APROBJ_STATUSFIELD_VALUE =
			'APPROVAL REJECTED',CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}',
			REJECT_DATE = '{datetime_value}',FIN_REJECT_USER_ID = '{UserName}',
			FIN_REJECT_USER_RECORD_ID = '{UserId}'
			WHERE APPROVAL_RECORD_ID = '{approvalId}' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
				approvalId=(self.QuoteNumber),
				datetime_value=self.datetime_value,
				UserId=str(self.UserId),
				UserName=str(self.UserName),
			)

			a = Sql.RunQuery(Transupdate)
			b = Sql.RunQuery(UpdateApprovere)

			GetCurStatus = Sql.GetFirst(
				"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
					ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHN_RECORD_ID
					FROM ACACSS (NOLOCK)
					INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID = SYOBJD.PARENT_OBJECT_RECORD_ID
					INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
					INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
					WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ACACSS.APPROVALSTATUS = 'REJECTED' AND ACAPMA.APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
					QuoteNumber=str(self.QuoteNumber)
				)
			)
			if GetCurStatus:
				
				MainObjUpdateQuery = """UPDATE {ObjName} SET
					{ApiName} = '{statusUpdate}'
					WHERE {primaryKey} = '{Primaryvalue}' """.format(
					statusUpdate = "REJECTED",
					ObjName="SAQTRV",
					ApiName="REVISION_STATUS",
					Primaryvalue=str(GetCurStatus.APRTRXOBJ_RECORD_ID),
					primaryKey = "QUOTE_REVISION_RECORD_ID"
				)

				b = Sql.RunQuery(MainObjUpdateQuery)
				##Calling the iflow script to insert the records into SAQRSH custom table(Capture Date/Time for Quote Revision Status update.)
				CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
				##update ARCHIVED as True If one step user rejected the transactn starts
				Trans_update_archive = Sql.RunQuery("""UPDATE ACAPTX SET ARCHIVED = 1 WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
					AND APRCHN_RECORD_ID = '{chainRecordId}'  """.format(
					QuoteNumber=str(self.QuoteNumber), chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID)
					)
				)
				##update ARCHIVED as True If one step user rejected the transactn ends
			try:
				##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
				CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
				CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
			except Exception, e:
				Trace.Write("EXCEPTION: QUOTE WRITE BACK "+str(e))

			rejecttresponse = self.sendmailNotification("Reject", CurrentTransId)
			Notificationresponse = self.sendmailNotification("Notification",CurrentTransId)
			UPDATE_ACACHR = """ UPDATE ACACHR SET ACACHR.COMPLETED_BY = '{UserName}',ACACHR.COMPLETEDBY_RECORD_ID='{UserId}', COMPLETED_DATE = '{datetime_value}' WHERE ACACHR.APPROVAL_RECORD_ID='{QuoteNumber}'""".format(UserId=self.UserId,UserName=self.UserName,datetime_value=self.datetime_value,QuoteNumber=self.QuoteNumber)
			Sql.RunQuery(UPDATE_ACACHR)
			Snapshotreject = Sql.GetFirst(
				"""SELECT APPROVAL_RECORD_ID,ACACST.WHERE_CONDITION_01,
						SYOBJH.OBJECT_NAME,ACAPTX.APPROVAL_ID,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,
						ACAPTX.REQUESTOR_COMMENTS
						FROM ACAPTX (NOLOCK)
						INNER JOIN ACACST (NOLOCK) ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
						INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
						WHERE ACAPTX.APPROVAL_RECORD_ID = '{QuoteNumber}'
						AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' AND ACAPTX.ARCHIVED = 0""".format(
					QuoteNumber=str(self.QuoteNumber), UserId=str(self.UserId)
				)
			)
			if Snapshotreject:
				targetObj = str(Snapshotreject.OBJECT_NAME)
				wherecond = str(Snapshotreject.WHERE_CONDITION_01)
				currentObj = str(Snapshotreject.APPROVAL_ID).split("-")
				ObjectName = str(currentObj[0])
				#GettingSnapshot = violationruleInsert.SnapshotDataInsert(str(targetObj), str(wherecond), ObjectName)
				Wherecond1 = """ WHERE ACAPTX.APPROVAL_RECORD_ID = '{secCondi}' AND
					ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '{CurTransid}' """.format(
					secCondi=str(self.QuoteNumber), CurTransid=str(Snapshotreject.APPROVAL_TRANSACTION_RECORD_ID),
				)
					#SnapshorQuery = GettingSnapshot + Wherecond1
					#Snapshotinsert = Sql.RunQuery(SnapshorQuery)
			
		# except Exception, e:
		#     self.exceptMessage = (
		#         "ACSECTACTN : ApproveVoilationRule : EXCEPTION : UNABLE TO APPROVE OR REJECT : EXCEPTION E : " + str(e)
		#     )
		#     Trace.Write(self.exceptMessage)
		return "True"

	# A043S001P01-13245 start
	# def BulkAction(self, ACTION, ApproveDesc):
	#     """for bulk action"""
	#     Trace.Write("coming to this bulkaction-----")
	#     BulkQuery = Sql.GetList(
	#         """ SELECT* FROM ACAPTX WHERE APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' AND APPROVALSTATUS = 'REQUESTED'
	#         AND APRCHN_RECORD_ID = '{QuoteNumber}' """.format(
	#             QuoteNumber=str(self.QuoteNumber), UserId=str(self.UserId)
	#         )
	#     )
	#     Trace.Write(
	#         str(
	#             """ SELECT* FROM ACAPTX WHERE APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' AND APPROVALSTATUS = 'REQUESTED'
	#             AND APRCHN_RECORD_ID = '{QuoteNumber}' """.format(
	#                 QuoteNumber=str(self.QuoteNumber), UserId=str(self.UserId)
	#             )
	#         )
	#     )
	#     if str(ACTION) == "BULKAPPROVE":
	#         for Bulk in BulkQuery:
	#             self.QuoteNumber = str(Bulk.APPROVAL_RECORD_ID)
	#             CurrentTransId = str(Bulk.APPROVAL_TRANSACTION_RECORD_ID)
	#             Getchaintype = Sql.GetFirst(
	#                 """SELECT APPROVAL_METHOD FROM ACAPMA (NOLOCK) INNER JOIN ACAPCH (NOLOCK)
	#                 ON ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID
	#                 WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                     QuoteNumber=str(self.QuoteNumber),
	#                 )
	#             )
	#             Transupdate = """UPDATE ACAPTX
	#                     SET APPROVALSTATUS = 'APPROVED',
	#                     APPROVED_BY = '{UserName}',
	#                     APPROVEDBY_RECORD_ID = '{UserId}',
	#                     RECIPIENT_COMMENTS = '{ApproveDesc}'
	#                     WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                     and APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' """.format(
	#                 UserId=str(self.UserId),
	#                 UserName=str(self.UserName),
	#                 ApproveDesc=str(ApproveDesc),
	#                 QuoteNumber=str(self.QuoteNumber),
	#                 getCpqId=str(CurrentTransId),
	#             )
	#             UpdateApproverv = """UPDATE ACAPMA
	#                     SET CUR_APRCHNSTP_LASTACTIONDATE = convert(VARCHAR(10), '{datetime_value}',101)
	#                     WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                 QuoteNumber=str(self.QuoteNumber), datetime_value=self.datetime_value
	#             )
	#             a = Sql.RunQuery(Transupdate)
	#             b = Sql.RunQuery(UpdateApproverv)
	#             approvetresponse = self.sendmailNotification("Approve", CurrentTransId)
	#             GetCurStatus = Sql.GetFirst(
	#                 """SELECT APPROVAL_RECORD_ID,ACACST.WHERE_CONDITION_01,
	#                         SYOBJH.OBJECT_NAME,ACAPTX.APPROVAL_ID,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,
	#                         ACAPTX.REQUESTOR_COMMENTS
	#                         FROM ACAPTX (NOLOCK)
	#                         INNER JOIN ACACST (NOLOCK) ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
	#                         INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
	#                         WHERE ACAPTX.APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                         AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' """.format(
	#                     QuoteNumber=str(self.QuoteNumber), UserId=str(self.UserId)
	#                 )
	#             )
	#             if GetCurStatus:
	#                 targetObj = str(GetCurStatus.OBJECT_NAME)
	#                 wherecond = str(GetCurStatus.WHERE_CONDITION_01)
	#                 currentObj = str(GetCurStatus.APPROVAL_ID).split("-")
	#                 ObjectName = str(currentObj[0])
	#                 #GettingSnapshot = violationruleInsert.SnapshotDataInsert(str(targetObj), str(wherecond), ObjectName)
	#                 Wherecond1 = """ WHERE ACAPTX.APPROVAL_RECORD_ID = '{secCondi}' AND
	#                     ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '{CurTransid}' """.format(
	#                     secCondi=str(self.QuoteNumber), CurTransid=str(GetCurStatus.APPROVAL_TRANSACTION_RECORD_ID),
	#                 )
	#                 #SnapshorQuery = GettingSnapshot + Wherecond1
	#                 #Snapshotinsert = Sql.RunQuery(SnapshorQuery)
	#             if str(Getchaintype.APPROVAL_METHOD).upper() == "TRUE":
	#                 Curapprovestep = Sql.GetFirst(
	#                     " SELECT ACAPTX.* FROM ACAPTX (NOLOCK) WHERE APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}'".format(
	#                         QuoteNumber=str(QuoteNumber), getCpqId=str(CurrentTransId),
	#                     )
	#                 )
	#                 lateststepId = Sql.GetFirst(
	#                     """SELECT * FROM ACAPMA(NOLOCK) WHERE
	#                     ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                     AND CUR_APRCHNSTP<{ids}""".format(
	#                         QuoteNumber=str(self.QuoteNumber), ids=int(Curapprovestep.APRCHNSTP_ID)
	#                     )
	#                 )
	#                 if lateststepId is not None:
	#                     Currsteprecordcheck = Sql.GetFirst(
	#                         """SELECT * FROM ACAPTX(NOLOCK) WHERE APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}'
	#                         AND APRCHNSTP_RECORD_ID IN ( SELECT APRCHNSTP_RECORD_ID FROM ACAPMA(NOLOCK)
	#                         WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' ) """.format(
	#                             QuoteNumber=str(QuoteNumber), getCpqId=str(CurrentTransId)
	#                         )
	#                     )
	#                     if Currsteprecordcheck is None:
	#                         Getcurrentapprovestep = Sql.GetFirst(
	#                             """ SELECT * FROM ACAPTX (NOLOCK) INNER JOIN ACACST(NOLOCK)
	#                             ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
	#                             INNER JOIN ACACSA (NOLOCK) ON
	#                             ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
	#                             WHERE APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}'""".format(
	#                                 QuoteNumber=str(QuoteNumber), getCpqId=str(CurrentTransId),
	#                             )
	#                         )
	#                         ChangeStepApproverv = """UPDATE ACAPMA SET CUR_APPCHNSTP_APPROVER_ID = '{approverId}'
	#                                     ,CUR_APRCHNSTP_APPROVER_RECORD_ID = '{ApproverRecId}',CUR_APRCHNSTP = '{ChaindStep}'
	#                                     ,CUR_APRCHNSTP_ENTRYDATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#                                     CUR_APRCHNSTP_LASTACTIONDATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#                                     APRCHNSTP_RECORD_ID = '{ChainStepRecId}' WHERE
	#                                     APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                             approverId=str(Getcurrentapprovestep.APRCHNSTP_APPROVER_ID),
	#                             ApproverRecId=str(Getcurrentapprovestep.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID),
	#                             ChaindStep=str(Getcurrentapprovestep.APRCHNSTP_NUMBER),
	#                             datetime_value=self.datetime_value,
	#                             ChainStepRecId=str(Getcurrentapprovestep.APPROVAL_CHAIN_STEP_RECORD_ID),
	#                             QuoteNumber=str(self.QuoteNumber),
	#                         )
	#                         a1 = Sql.RunQuery(ChangeStepApproverv)
	#                 statusupdate = "True"
	#                 GetAllStepRecId = Sql.GetList(
	#                     """SELECT DISTINCT APRCHNSTP_RECORD_ID FROM ACAPTX (NOLOCK)
	#                         WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                         QuoteNumber=str(self.QuoteNumber)
	#                     )
	#                 )
	#                 for GetEachStepRecId in GetAllStepRecId:
	#                     CheckEach = Sql.GetFirst(
	#                         """SELECT * FROM ACAPTX (NOLOCK) WHERE APRCHNSTP_RECORD_ID = '{StepRecirdId}'
	#                             AND APPROVALSTATUS = 'APPROVED' """.format(
	#                             StepRecirdId=str(GetEachStepRecId.APRCHNSTP_RECORD_ID)
	#                         )
	#                     )
	#                     if CheckEach is None:
	#                         statusupdate = "False"
	#                 Checkunanimous = Sql.GetList(
	#                     """SELECT * FROM ACAPTX (NOLOCK) WHERE UNANIMOUS_CONSENT = 'True' AND ARCHIVED <>'True'
	#                     AND APPROVALSTATUS <> 'APPROVAL REQUIRED' AND APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                         QuoteNumber=str(self.QuoteNumber)
	#                     )
	#                 )
	#                 if statusupdate == "True" and len(Checkunanimous) <= 0:
	#                     GetCurStatus = Sql.GetFirst(
	#                         """SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
	#                                 ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
	#                                 FROM ACACSS (NOLOCK)
	#                                 INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_STATUSFIELD_RECORD_ID = SYOBJD.RECORD_ID
	#                                 INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
	#                                 INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
	#                                 WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                                 AND APPROVALSTATUS = 'APPROVED' """.format(
	#                             QuoteNumber=str(self.QuoteNumber)
	#                         )
	#                     )
	#                     if GetCurStatus:
	#                         if (GetCurStatus.OBJECT_NAME) == "PASGRV":
	#                             SegmentIds = str(GetCurStatus.APRTRXOBJ_RECORD_ID)
	#                             MainObjUpdateQuery = """UPDATE {ObjName} SET {ApiName} = '{ApiVal}'
	#                             WHERE AGMREV_ID = '{RevId}' """.format(
	#                                 ObjName=str(GetCurStatus.OBJECT_NAME),
	#                                 ApiName=str(GetCurStatus.API_NAME),
	#                                 RevId=str(SegmentIds),
	#                                 ApiVal=str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
	#                             )
	#                             b = Sql.RunQuery(MainObjUpdateQuery)
	#                         UpdateApproverv = """UPDATE ACAPMA SET APRSTAMAP_APPROVALSTATUS = 'APPROVED',
	#                             APROBJ_STATUSFIELD_VALUE = 'APPROVED FOR PUBLISHING',
	#                             CUR_APRCHNSTP_LASTACTIONDATE= convert(VARCHAR(10), '{datetime_value}', 101),
	#                             FIN_APPROVE_DATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#                             FIN_APPROVE_USER_ID = '{UserName}',FIN_APPROVE_USER_RECORD_ID = '{UserId}'
	#                             WHERE APPROVAL_RECORD_ID = '{approvalId}' """.format(
	#                             approvalId=(self.QuoteNumber),
	#                             datetime_value=self.datetime_value,
	#                             UserId=str(self.UserId),
	#                             UserName=str(self.UserName),
	#                         )
	#                         c = Sql.RunQuery(UpdateApproverv)
	#             else:
	#                 GetCurrentTranStatus = Sql.GetFirst(
	#                     """SELECT ACAPTX.* FROM ACAPMA (NOLOCK) INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_ID =
	#                         ACAPTX.APPROVAL_ID AND ACAPMA.APRCHNSTP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID AND
	#                         APPROVALSTATUS = 'REQUESTED' AND ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                         QuoteNumber=str(self.QuoteNumber)
	#                     )
	#                 )
	#                 if GetCurrentTranStatus is None:
	#                     GetCurrentStrpId = Sql.GetFirst(
	#                         "SELECT APRCHN_ID,CUR_APRCHNSTP,APRCHN_RECORD_ID,ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_ID FROM ACAPMA"
	#                         + " WHERE ACAPMA.APPROVAL_RECORD_ID = '"
	#                         + str(self.QuoteNumber)
	#                         + "' "
	#                     )
	#                     restrictstepList = ""
	#                     currentStep = int(GetCurrentStrpId.CUR_APRCHNSTP)
	#                     for restrict in range(1, currentStep + 1):
	#                         restrictstepList += "'" + str(restrict) + "'"
	#                         if restrict != currentStep:
	#                             restrictstepList += ","
	#                     result = Sql.GetFirst(
	#                         "SELECT TOP 1  * FROM ACACST (NOLOCK) WHERE APRCHN_RECORD_ID = '"
	#                         + str(GetCurrentStrpId.APRCHN_RECORD_ID)
	#                         + "' AND WHERE_CONDITION_01 <> '' AND APRCHNSTP_NUMBER NOT IN ("
	#                         + str(restrictstepList)
	#                         + ") ORDER BY ACACST.APRCHNSTP_NUMBER "
	#                     )
	#                     if result:
	#                         GetObjName = Sql.GetFirst(
	#                             "SELECT OBJECT_NAME FROM SYOBJH (NOLOCK) WHERE RECORD_ID = '"
	#                             + str(result.TSTOBJ_RECORD_ID)
	#                             + "'"
	#                         )
	#                         Select_Query = (
	#                             "SELECT * FROM "
	#                             + str(GetObjName.OBJECT_NAME)
	#                             + " (NOLOCK) WHERE "
	#                             + str(result.WHERE_CONDITION_01)
	#                         )
	#                         getObjSplit = str(GetCurrentStrpId.APPROVAL_ID).split("-")
	#                         ObjectName = getObjSplit[0]
	#                         TargeobjRelation = Sql.GetFirst(
	#                             "SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE DATA_TYPE = 'LOOKUP' AND LOOKUP_OBJECT = '"
	#                             + str(ObjectName)
	#                             + "' AND OBJECT_NAME = '"
	#                             + str(GetObjName.OBJECT_NAME)
	#                             + "' "
	#                         )
	#                         if str(ObjectName) == "PASGRV":
	#                             SegmentIds = str(GetCurrentStrpId.APRTRXOBJ_RECORD_ID)
	#                             GetRevPrimary = Sql.GetFirst(
	#                                 "SELECT PRICEAGREEMENT_REVISION_RECORD_ID FROM PASGRV (NOLOCK) "
	#                                 + " WHERE AGMREV_ID = '{}' ".format(str(SegmentIds))
	#                             )
	#                             RecordId = str(GetRevPrimary.PRICEAGREEMENT_REVISION_RECORD_ID)
	#                         Select_Query += " AND " + str(TargeobjRelation.API_NAME) + " = '" + str(RecordId) + "' "
	#                         SqlQuery = Sql.GetFirst(Select_Query)
	#                         if SqlQuery:
	#                             GetApproveretail = Sql.GetFirst(
	#                                 """SELECT APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,APRCHNSTP_APPROVER_ID,
	#                                 APPROVAL_CHAIN_STEP_RECORD_ID,ACACST.APRCHNSTP_NUMBER
	#                                 FROM ACACST (NOLOCK)
	#                                 INNER JOIN ACACSA (NOLOCK)
	#                                 ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
	#                                 WHERE ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = '{ChainRecordId}' """.format(
	#                                     ChainRecordId=str(result.APPROVAL_CHAIN_STEP_RECORD_ID)
	#                                 )
	#                             )
	#                             if GetApproveretail:
	#                                 ChangeStepApproverv = """UPDATE ACAPMA SET CUR_APPCHNSTP_APPROVER_ID = '{approverId}'
	#                                 ,CUR_APRCHNSTP_APPROVER_RECORD_ID = '{ApproverRecId}',CUR_APRCHNSTP = '{ChaindStep}'
	#                                 ,CUR_APRCHNSTP_ENTRYDATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#                                 CUR_APRCHNSTP_LASTACTIONDATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#                                 APRCHNSTP_RECORD_ID = '{ChainStepRecId}' WHERE
	#                                 APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                                     approverId=str(GetApproveretail.APRCHNSTP_APPROVER_ID),
	#                                     ApproverRecId=str(GetApproveretail.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID),
	#                                     ChaindStep=str(GetApproveretail.APRCHNSTP_NUMBER),
	#                                     datetime_value=self.datetime_value,
	#                                     ChainStepRecId=str(GetApproveretail.APPROVAL_CHAIN_STEP_RECORD_ID),
	#                                     QuoteNumber=str(self.QuoteNumber),
	#                                 )
	#                                 GetStatus = Sql.GetFirst(
	#                                     """SELECT ACACSS.APPROVALSTATUS,ACAPMA.APRCHNSTP_RECORD_ID
	#                                         FROM ACACSS (NOLOCK)
	#                                         INNER JOIN ACAPMA (NOLOCK) ON ACACSS.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
	#                                         WHERE ACACSS.APROBJ_STATUSFIELD_VAL = 'APPROVAL REQUIRED'
	#                                         AND APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
	#                                         QuoteNumber=str(self.QuoteNumber)
	#                                     )
	#                                 )
	#                                 if GetStatus:
	#                                     UpdateTrans = """UPDATE ACAPTX SET
	#                                         APPROVALSTATUS = '{ApprovalStatus}',
	#                                         REQUESTOR_COMMENTS = '{RequestDesc}'
	#                                         WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                                         AND APRCHNSTP_RECORD_ID = '{stepRecordId}'""".format(
	#                                         ApprovalStatus=str(GetStatus.APPROVALSTATUS),
	#                                         QuoteNumber=str(self.QuoteNumber),
	#                                         RequestDesc=str(GetCurStatus.REQUESTOR_COMMENTS),
	#                                         stepRecordId=str(GetApproveretail.APPROVAL_CHAIN_STEP_RECORD_ID),
	#                                     )
	#                                 c = Sql.RunQuery(ChangeStepApproverv)
	#                                 d = Sql.RunQuery(UpdateTrans)
	#                                 approvetresponse = self.sendmailNotification("Request")
	#                     else:
	#                         GetCurStatus = Sql.GetFirst(
	#                             """SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
	#                                 ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
	#                                 FROM ACACSS (NOLOCK)
	#                                 INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_STATUSFIELD_RECORD_ID = SYOBJD.RECORD_ID
	#                                 INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
	#                                 INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
	#                                 WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                                 AND APPROVALSTATUS = 'APPROVED' """.format(
	#                                 QuoteNumber=str(self.QuoteNumber)
	#                             )
	#                         )
	#                         if GetCurStatus:
	#                             if (GetCurStatus.OBJECT_NAME) == "PASGRV":
	#                                 SegmentIds = str(GetCurStatus.APRTRXOBJ_RECORD_ID)
	#                                 MainObjUpdateQuery = """UPDATE {ObjName} SET {ApiName} = '{ApiVal}'
	#                                 WHERE AGMREV_ID = '{RevId}' """.format(
	#                                     ObjName=str(GetCurStatus.OBJECT_NAME),
	#                                     ApiName=str(GetCurStatus.API_NAME),
	#                                     RevId=str(SegmentIds),
	#                                     ApiVal=str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
	#                                 )
	#                                 b = Sql.RunQuery(MainObjUpdateQuery)
	#                             UpdateApproverv = """UPDATE ACAPMA SET APRSTAMAP_APPROVALSTATUS = 'APPROVED',
	#                                 APROBJ_STATUSFIELD_VALUE = 'APPROVED FOR PUBLISHING',
	#                                 CUR_APRCHNSTP_LASTACTIONDATE= convert(VARCHAR(10), '{datetime_value}', 101),
	#                                 FIN_APPROVE_DATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#                                 FIN_APPROVE_USER_ID = '{UserName}',FIN_APPROVE_USER_RECORD_ID = '{UserId}'
	#                                 WHERE APPROVAL_RECORD_ID = '{approvalId}' """.format(
	#                                 approvalId=(self.QuoteNumber),
	#                                 datetime_value=self.datetime_value,
	#                                 UserId=str(self.UserId),
	#                                 UserName=str(self.UserName),
	#                             )
	#                             c = Sql.RunQuery(UpdateApproverv)
	#             ScriptExecutor.ExecuteGlobal(
	#                 "SYALLTABOP",
	#                 {
	#                     "Primary_Data": str(self.QuoteNumber),
	#                     "TabNAME": "My Approval Queue",
	#                     "ACTION": "VIEW",
	#                     "RELATED": "",
	#                 },
	#             )
	#     if str(ACTION) == "BULKREJECT":
	#         for Bulk in BulkQuery:
	#             self.QuoteNumber = str(Bulk.APPROVAL_RECORD_ID)
	#             Transupdate = """UPDATE ACAPTX SET
	#                     APPROVALSTATUS = 'REJECTED',
	#                     REJECTED_BY = '{UserName}',
	#                     REJECTBY_RECORD_ID = '{UserId}',
	#                     RECIPIENT_COMMENTS = '{ApproveDesc}'
	#                     WHERE APPROVAL_RECIPIENT_RECORD_ID = '{UserId}'
	#                     AND APPROVAL_TRANSACTION_RECORD_ID = '{getCpqId}' """.format(
	#                 UserId=str(self.UserId),
	#                 UserName=str(self.UserName),
	#                 ApproveDesc=str(ApproveDesc),
	#                 getCpqId=str(Bulk.APPROVAL_TRANSACTION_RECORD_ID),
	#             )
	#             UpdateApprovere = """UPDATE ACAPMA SET APRSTAMAP_APPROVALSTATUS = 'REJECTED',APROBJ_STATUSFIELD_VALUE =
	#             'APPROVAL REJECTED',CUR_APRCHNSTP_LASTACTIONDATE = convert(VARCHAR(10), '{datetime_value}', 101),
	#             REJECT_DATE = convert(VARCHAR(10), '{datetime_value}', 101),FIN_REJECT_USER_ID = '{UserName}',
	#             FIN_REJECT_USER_RECORD_ID = '{UserId}'
	#             WHERE APPROVAL_RECORD_ID = '{approvalId}' """.format(
	#                 approvalId=(Bulk.APPROVAL_RECORD_ID),
	#                 datetime_value=self.datetime_value,
	#                 UserId=str(self.UserId),
	#                 UserName=str(self.UserName),
	#             )
	#             a = Sql.RunQuery(Transupdate)
	#             b = Sql.RunQuery(UpdateApprovere)
	#             GetCurStatus = Sql.GetFirst(
	#                 """SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
	#                     ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
	#                     FROM ACACSS (NOLOCK)
	#                     INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_STATUSFIELD_RECORD_ID = SYOBJD.RECORD_ID
	#                     INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
	#                     INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
	#                     WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND APPROVALSTATUS = 'REJECTED' """.format(
	#                     QuoteNumber=str(Bulk.APPROVAL_RECORD_ID)
	#                 )
	#             )
	#             if GetCurStatus:
	#                 if (GetCurStatus.OBJECT_NAME) == "PASGRV":
	#                     SegmentIds = str(GetCurStatus.APROBJ_ID)
	#                     MainObjUpdateQuery = """UPDATE {ObjName} SET {ApiName} = '{ApiVal}'
	#                         WHERE AGMREV_ID = '{SegmentIds}' """.format(
	#                         ObjName=str(GetCurStatus.OBJECT_NAME),
	#                         ApiName=str(GetCurStatus.API_NAME),
	#                         SegmentIds=str(SegmentIds),
	#                         ApiVal=str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
	#                     )
	#                     b = Sql.RunQuery(MainObjUpdateQuery)
	#             rejecttresponse = self.sendmailNotification("Reject", CurrentTransId)
	#             Snapshotreject = Sql.GetFirst(
	#                 """SELECT APPROVAL_RECORD_ID,ACACST.WHERE_CONDITION_01,
	#                         SYOBJH.OBJECT_NAME,ACAPTX.APPROVAL_ID,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,
	#                         ACAPTX.REQUESTOR_COMMENTS
	#                         FROM ACAPTX (NOLOCK)
	#                         INNER JOIN ACACST (NOLOCK) ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
	#                         INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
	#                         WHERE ACAPTX.APPROVAL_RECORD_ID = '{QuoteNumber}'
	#                         AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' """.format(
	#                     QuoteNumber=str(self.QuoteNumber), UserId=str(self.UserId)
	#                 )
	#             )
	#             if Snapshotreject:
	#                 targetObj = str(Snapshotreject.OBJECT_NAME)
	#                 wherecond = str(Snapshotreject.WHERE_CONDITION_01)
	#                 currentObj = str(Snapshotreject.APPROVAL_ID).split("-")
	#                 ObjectName = str(currentObj[0])
	#                 #GettingSnapshot = violationruleInsert.SnapshotDataInsert(str(targetObj), str(wherecond), ObjectName)
	#                 Wherecond1 = """ WHERE ACAPTX.APPROVAL_RECORD_ID = '{secCondi}' AND
	#                     ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '{CurTransid}' """.format(
	#                     secCondi=str(self.QuoteNumber), CurTransid=str(Snapshotreject.APPROVAL_TRANSACTION_RECORD_ID),
	#                 )
	#                 #SnapshorQuery = GettingSnapshot + Wherecond1
	#                 #Snapshotinsert = Sql.RunQuery(SnapshorQuery)
	#             ScriptExecutor.ExecuteGlobal(
	#                 "SYALLTABOP",
	#                 {
	#                     "Primary_Data": str(self.QuoteNumber),
	#                     "TabNAME": "My Approval Queue",
	#                     "ACTION": "VIEW",
	#                     "RELATED": "",
	#                 },
	#             )
	#     return "True"
	# A043S001P01-13245 end
	def RecallSmartApprovalAction(self):
		
		if self.QuoteNumber:
			GetCurStatus = Sql.GetFirst(
								"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
										ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHN_RECORD_ID,ACAPMA.APPROVAL_ID
										FROM ACACSS (NOLOCK)
										INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_STATUSFIELD_RECORD_ID = SYOBJD.RECORD_ID
										INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
										INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
										WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
										AND APPROVALSTATUS = 'REJECTED' """.format(
									QuoteNumber=str(self.QuoteNumber)
								)
							)
			if GetCurStatus:
				GetObjhRecId = Sql.GetFirst(
					"SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '"
					+ str(GetCurStatus.OBJECT_NAME)
					+ "' "
				)
				Objh_Id = str(GetObjhRecId.RECORD_ID)
				ObjPrimaryKey = str(GetCurStatus.APRTRXOBJ_RECORD_ID)
				""" retrunRecall = violationruleInsert.insertviolationtableafterRecall(
					str(GetCurStatus.APRCHN_RECORD_ID), str(ObjPrimaryKey), str(GetCurStatus.OBJECT_NAME), Objh_Id
				) """
				retrunRecall = violationruleInsert.InsertAction(
					Objh_Id, str(ObjPrimaryKey), str(GetCurStatus.OBJECT_NAME), "RECALL"
				)
				GetExplicit = Sql.GetFirst(
					"""SELECT * FROM ACACST (NOLOCK) WHERE APRCHN_RECORD_ID = '{chainRecordId}'
						AND REQUIRE_EXPLICIT_APPROVAL = 1 """.format(
						chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID)
					)
				)
				GetSmart = Sql.GetFirst(
					"""SELECT * FROM ACACST (NOLOCK) WHERE APRCHN_RECORD_ID = '{chainRecordId}'
						AND ENABLE_SMARTAPPROVAL = 1 """.format(
						chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID)
					)
				)
				GetQueryApprovaRecId = Sql.GetFirst(
					"""SELECT * FROM ACAPMA (NOLOCK) WHERE APRCHN_RECORD_ID = '{chainRecordId}'
					ORDER BY CpqTableEntryId DESC """.format(
						chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID)
					)
				)
				GetApprovaRecId = str(GetQueryApprovaRecId.APPROVAL_RECORD_ID)
				getstepId = []
				GetLatestStepRecId = ""
				if GetExplicit is not None and GetSmart is None:
					GetLatestStepRecId = str(GetExplicit.APPROVAL_CHAIN_STEP_RECORD_ID)
					for count in range(1, int(GetExplicit.APRCHNSTP_NUMBER)):
						getstepId.append(count)
				elif GetExplicit is None and GetSmart is not None:
					GetLatestStepRecId = str(GetSmart.APPROVAL_CHAIN_STEP_RECORD_ID)
					for count in range(1, int(GetSmart.APRCHNSTP_NUMBER)):
						getstepId.append(count)
				elif GetSmart is not None and GetExplicit is not None:
					if int(GetExplicit.APRCHNSTP_NUMBER) < int(GetSmart.APRCHNSTP_NUMBER):
						GetLatestStepRecId = str(GetExplicit.APPROVAL_CHAIN_STEP_RECORD_ID)
						for count in range(1, int(GetExplicit.APRCHNSTP_NUMBER)):
							getstepId.append(count)
					else:
						GetLatestStepRecId = str(GetSmart.APPROVAL_CHAIN_STEP_RECORD_ID)
						for count in range(1, int(GetSmart.APRCHNSTP_NUMBER)):
							getstepId.append(count)
				if GetLatestStepRecId != "":
					GetApproveretail = Sql.GetFirst(
						"""SELECT APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,APRCHNSTP_APPROVER_ID,
						APPROVAL_CHAIN_STEP_RECORD_ID,ACACST.APRCHNSTP_NUMBER
						FROM ACACST (NOLOCK)
						INNER JOIN ACACSA (NOLOCK)
						ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
						WHERE ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = '{ChainRecordId}' """.format(
							ChainRecordId=str(GetLatestStepRecId)
						)
					)
					if GetApproveretail:
						ChangeStepApproverv = """UPDATE ACAPMA SET CUR_APPCHNSTP_APPROVER_ID = '{approverId}'
						,CUR_APRCHNSTP_APPROVER_RECORD_ID = '{ApproverRecId}',CUR_APRCHNSTP = '{ChaindStep}'
						,CUR_APRCHNSTP_ENTRYDATE = '{datetime_value}',
						CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}',
						APRCHNSTP_RECORD_ID = '{ChainStepRecId}' WHERE
						APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
							approverId=str(GetApproveretail.APRCHNSTP_APPROVER_ID),
							ApproverRecId=str(GetApproveretail.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID),
							ChaindStep=str(GetApproveretail.APRCHNSTP_NUMBER),
							datetime_value=self.datetime_value,
							ChainStepRecId=str(GetApproveretail.APPROVAL_CHAIN_STEP_RECORD_ID),
							QuoteNumber=str(GetApprovaRecId),
						)
						approvalrun = Sql.RunQuery(ChangeStepApproverv)
				if len(getstepId) > 0:
					if len(getstepId) == 1:
						getstepIdtuple = "(" + str(getstepId[0]) + ")"
					else:
						getstepIdtuple = tuple(getstepId)
					Transarchiveupdate = """UPDATE ACAPTX SET ARCHIVED = 1 WHERE APRCHN_RECORD_ID = '{chainRecordId}'
					AND APRCHNSTP_ID IN {getstepIdtuple} """.format(
						chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID), getstepIdtuple=getstepIdtuple
					)
					d = Sql.RunQuery(Transarchiveupdate)
				
				#UPDATE_ACACHR = """ UPDATE ACACHR SET APPROVAL_ROUND = APPROVAL_ROUND + 1 WHERE ACACHR.APPROVAL_RECORD_ID='{QuoteNumber}' AND ACACHR.APRCHN_RECORD_ID = '{chainRecordId}'""".format(QuoteNumber=GetApprovaRecId,chainRecordId=GetCurStatus.APRCHN_RECORD_ID)
				#Sql.RunQuery(UPDATE_ACACHR)

				GetAllRecallViolatedRrecId = Sql.GetList(
					"""SELECT APPROVAL_RECORD_ID FROM ACAPMA (NOLOCK) WHERE APRTRXOBJ_RECORD_ID = '{ApprovalObject}'""".format(
						ApprovalObject=str(GetQueryApprovaRecId.APRTRXOBJ_RECORD_ID)
					)
				)
				for eachId in GetAllRecallViolatedRrecId:
					self.QuoteNumber = str(eachId.APPROVAL_RECORD_ID)
					recallresponse = self.sendmailNotification("Recall")

	def SmartApprovalAction(self):
		
		GetCurStatus = Sql.GetFirst(
								"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
										ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHN_RECORD_ID,ACAPMA.APPROVAL_ID, ACAPMA.REQUESTOR_COMMENTS
										FROM ACACSS (NOLOCK)
										INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID = SYOBJD.PARENT_OBJECT_RECORD_ID
										INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
										INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
										WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
										AND APPROVALSTATUS = 'REJECTED' AND ACAPMA.APRSTAMAP_APPROVALSTATUS = 'RECALLED' """.format(
									QuoteNumber=str(self.QuoteNumber)
								)
							)
		if GetCurStatus:
			GetObjhRecId = Sql.GetFirst(
				"SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '"
				+ str(GetCurStatus.OBJECT_NAME)
				+ "' "
			)
			Objh_Id = str(GetObjhRecId.RECORD_ID)
			ObjPrimaryKey = str(GetCurStatus.APRTRXOBJ_RECORD_ID)
			""" retrunRecall = violationruleInsert.insertviolationtableafterRecall(
				str(GetCurStatus.APRCHN_RECORD_ID), str(ObjPrimaryKey), str(GetCurStatus.OBJECT_NAME), Objh_Id
			) """
			retrunRecall = violationruleInsert.InsertAction(
				Objh_Id, str(ObjPrimaryKey), str(GetCurStatus.OBJECT_NAME), "RECALL"
			)
			
			approval_id_without_auto_inc = '-'.join((GetCurStatus.APPROVAL_ID).split('-')[0:-1])
			Sql.RunQuery("""UPDATE ACAPTX SET APPROVALSTATUS = IQ.APPROVALSTATUS, APPROVED_BY = IQ.APPROVED_BY,
												APPROVEDBY_RECORD_ID = IQ.APPROVEDBY_RECORD_ID,
												RECIPIENT_COMMENTS = IQ.RECIPIENT_COMMENTS
							FROM ACAPTX
							INNER JOIN (
										SELECT ACAPTX.APRCHN_RECORD_ID, ACAPTX.APRCHNSTP_RECORD_ID, ACAPTX.APRCHNSTP_APPROVER_RECORD_ID, 
												ACAPTX.APPROVALSTATUS, ACAPTX.APPROVED_BY, ACAPTX.APPROVEDBY_RECORD_ID, ACAPTX.RECIPIENT_COMMENTS
											FROM ACAPTX (NOLOCK)
											JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID
											WHERE ACAPTX.APPROVAL_ID LIKE '%{ApprovalId}%' AND 
													ACACST.ENABLE_SMARTAPPROVAL = 1 AND ACAPTX.APPROVALSTATUS = 'APPROVED' AND ACAPTX.ARCHIVED = 1
									) IQ ON IQ.APRCHN_RECORD_ID = ACAPTX.APRCHN_RECORD_ID AND IQ.APRCHNSTP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID 
											AND IQ.APRCHNSTP_APPROVER_RECORD_ID = ACAPTX.APRCHNSTP_APPROVER_RECORD_ID
							WHERE ACAPTX.ARCHIVED = 0 AND ACAPTX.APPROVALSTATUS = 'REQUESTED' AND ACAPTX.APPROVAL_ID LIKE '%{ApprovalId}%'""".format(
								ApprovalId=approval_id_without_auto_inc
							))
			quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=self.quote_revision_record_id))
			getMethod = Sql.GetList("SELECT DISTINCT ACAPTX.APPROVAL_RECORD_ID, ACAPCH.APPROVAL_METHOD FROM ACAPCH (NOLOCK) INNER JOIN ACAPTX ON ACAPCH.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_ID LIKE '%{quote}%' AND ACAPTX.ARCHIVED = 0 AND ACAPTX.APRCHN_RECORD_ID = '{chain_id}'".format(quote=quote_obj.QUOTE_ID,chain_id = str(GetCurStatus.APRCHN_RECORD_ID)))
			for ele in getMethod:
				#a = Sql.GetFirst("SELECT APPROVAL_RECORD_ID FROM ACAPTX WHERE CpqTableEntryId = '{}'".format(ele.CpqTableEntryId))
				if ele.APPROVAL_METHOD == 'SERIES STEP APPROVAL':
					##ENABLE_SMARTAPPROVAL condition is checked here
					Sql.RunQuery("""UPDATE ACAPTX SET APPROVALSTATUS = 'APPROVAL REQUIRED'
											FROM ACAPTX (NOLOCK) INNER JOIN ACACST (NOLOCK) 
											ON ACAPTX.APRCHN_RECORD_ID = ACACST.APRCHN_RECORD_ID 
											AND ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID 
											WHERE ACAPTX.APRTRXOBJ_ID = '{approval_rec_id}' AND ACACST.ENABLE_SMARTAPPROVAL = 0 AND ACAPTX.APRCHNSTP_ID != '1' AND ACAPTX.ARCHIVED = 0""".format(approval_rec_id = 
											Quote.CompositeNumber))
					a = Sql.GetFirst(""" SELECT ACAPTX.APPROVALSTATUS,ACAPTX.APPROVAL_RECIPIENT,ACAPTX.APRCHNSTP_ID FROM ACAPTX (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTX.APRCHN_RECORD_ID = ACACST.APRCHN_RECORD_ID AND ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID WHERE ACAPTX.APRTRXOBJ_ID = '{}' AND ACACST.ENABLE_SMARTAPPROVAL = 1 AND ACAPTX.APRCHNSTP_ID = '1' AND ACAPTX.ARCHIVED = 0""".format(Quote.CompositeNumber))
					if a.APPROVALSTATUS == "REQUESTED":
						Sql.RunQuery("""UPDATE ACAPTX SET APPROVALSTATUS = 'APPROVAL REQUIRED'
											FROM ACAPTX (NOLOCK) INNER JOIN ACACST (NOLOCK) 
											ON ACAPTX.APRCHN_RECORD_ID = ACACST.APRCHN_RECORD_ID 
											AND ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID 
											WHERE ACAPTX.APRTRXOBJ_ID = '{approval_rec_id}' AND ACACST.ENABLE_SMARTAPPROVAL = 1 AND ACAPTX.APRCHNSTP_ID != '1' AND ACAPTX.ARCHIVED = 0 AND APPROVALSTATUS != 'APPROVED'""".format(approval_rec_id = 
											Quote.CompositeNumber))
					Sql.RunQuery("""UPDATE ACAPTX SET RECIPIENT_COMMENTS = '' WHERE APPROVAL_RECORD_ID = '{}'
											AND APPROVALSTATUS = 'APPROVAL REQUIRED' AND ARCHIVED = 0""".format(
											ele.APPROVAL_RECORD_ID))
				##to update REQUESTOR_COMMENTS for recalled rounds starts
				Sql.RunQuery("""UPDATE ACAPMA SET REQUESTOR_COMMENTS = '{comment}' WHERE APPROVAL_RECORD_ID = '{approval_rec_id}'
							""".format(comment = str(RequestDesc),
							approval_rec_id = ele.APPROVAL_RECORD_ID))
				Sql.RunQuery("""UPDATE ACAPTX SET REQUESTOR_COMMENTS = '{comment}' WHERE APPROVAL_RECORD_ID = '{approval_rec_id}'
							AND ARCHIVED = 0""".format(comment = str(RequestDesc),
							approval_rec_id = ele.APPROVAL_RECORD_ID))
				##to update REQUESTOR_COMMENTS for recalled rounds ends
			Getcurrentapprovestep = Sql.GetFirst(
										""" SELECT * FROM ACAPTX (NOLOCK) INNER JOIN ACACST(NOLOCK)
										ON ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
										INNER JOIN ACACSA (NOLOCK) ON
										ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
										WHERE ACAPTX.ARCHIVED = 0 AND ACAPTX.APPROVALSTATUS = 'REQUESTED' AND ACAPTX.APPROVAL_ID LIKE '%{ApprovalId}%'""".format(
										ApprovalId=approval_id_without_auto_inc
										)
									)
			if Getcurrentapprovestep:
				ChangeStepApproverv = """UPDATE ACAPMA SET CUR_APPCHNSTP_APPROVER_ID = '{approverId}'
							,CUR_APRCHNSTP_APPROVER_RECORD_ID = '{ApproverRecId}',CUR_APRCHNSTP = '{ChaindStep}'
							,CUR_APRCHNSTP_ENTRYDATE = '{datetime_value}',
							CUR_APRCHNSTP_LASTACTIONDATE = '{datetime_value}',
							APRCHNSTP_RECORD_ID = '{ChainStepRecId}',REQUESTOR_COMMENTS='{Requestor_Comments}'  WHERE
							APPROVAL_ID LIKE '%{ApprovalId}%' AND APRSTAMAP_APPROVALSTATUS <> 'RECALLED'""".format(
					approverId=str(Getcurrentapprovestep.APRCHNSTP_APPROVER_ID),
					ApproverRecId=str(Getcurrentapprovestep.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID),
					ChaindStep=str(Getcurrentapprovestep.APRCHNSTP_NUMBER),
					datetime_value=self.datetime_value,
					ChainStepRecId=str(Getcurrentapprovestep.APPROVAL_CHAIN_STEP_RECORD_ID),
					ApprovalId=approval_id_without_auto_inc,
					Requestor_Comments=GetCurStatus.REQUESTOR_COMMENTS
				)
				Sql.RunQuery(ChangeStepApproverv)
				#UPDATE_ACACHR = """ UPDATE ACACHR SET APPROVAL_ROUND = APPROVAL_ROUND + 1 WHERE ACACHR.APPROVAL_RECORD_ID='{QuoteNumber}' AND ACACHR.APRCHN_RECORD_ID = '{chainRecordId}'""".format(QuoteNumber=GetApprovaRecId,chainRecordId=GetCurStatus.APRCHN_RECORD_ID)
				#Sql.RunQuery(UPDATE_ACACHR)
				UPDATE_ACACHR = """ UPDATE ACACHR SET INITIATED_DATE = '{datetime_value}', INTIATEDBY_RECORD_ID = '{UserId}', INITIATED_BY = '{UserName}' WHERE ACACHR.APPROVAL_RECORD_ID='{QuoteNumber}'""".format(UserId=self.UserId,UserName=self.UserName,datetime_value=self.datetime_value,QuoteNumber=self.QuoteNumber)
				Sql.RunQuery(UPDATE_ACACHR)

				submit=Sql.GetFirst("Select APPROVAL_METHOD FROM ACAPCH(NOLOCK) WHERE APPROVAL_CHAIN_RECORD_ID =  '"+str(Getcurrentapprovestep.APRCHN_RECORD_ID)+"'")
				GetCurStatus = Sql.GetFirst(
				"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
					ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
					FROM ACACSS (NOLOCK)
					INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID =SYOBJD.PARENT_OBJECT_RECORD_ID
					INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.OBJECT_NAME=SYOBJD.OBJECT_NAME
					INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL=SYOBJH.LABEL AND ACACSS.APRCHN_RECORD_ID =ACAPMA.APRCHN_RECORD_ID
					WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND APPROVALSTATUS = 'REQUESTED'  """.format(
					QuoteNumber=str(self.QuoteNumber)
				)
				)
				if GetCurStatus:
					
					MainObjUpdateQuery = """UPDATE SAQTRV SET
						REVISION_STATUS = 'APPROVAL PENDING'
						WHERE {primaryKey} = '{Primaryvalue}' """.format(
						statusUpdate = str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
						ObjName=str(GetCurStatus.OBJECT_NAME),
						ApiName=str(GetCurStatus.API_NAME),
						Primaryvalue=str(GetCurStatus.APRTRXOBJ_RECORD_ID),
						primaryKey = str(GetCurStatus.RECORD_NAME )
					)
					b = Sql.RunQuery(MainObjUpdateQuery)
					##Calling the iflow script to insert the records into SAQRSH custom table(Capture Date/Time for Quote Revision Status update.)
					CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
				
				try:
					##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
					CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
					CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
				except Exception, e:
					Trace.Write("EXCEPTION: QUOTE WRITE BACK "+str(e))

				if submit.APPROVAL_METHOD == "PARALLEL STEP APPROVAL":
					requestresponse = self.sendmailNotification("ParallelRequest")
				else:
					requestresponse = self.sendmailNotification("Request")
	
	def SubmitForApprovalAction(self, GetStatus=None, RequestDesc=''):
		UpdateTrans = ""
		Trace.Write("GetStatus "+str(GetStatus))
		if GetStatus:        
			# approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND APPROVAL_RECORD_ID = '{approval_rec_id}'".format(quote_revision_record_id=self.quote_revision_record_id,approval_rec_id = GetStatus.APPROVAL_RECORD_ID))
			# approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
			Sql.RunQuery("""UPDATE ACAPMA SET
				APROBJ_STATUSFIELD_VALUE = '{ApprovalStatus}',
				APRSTAMAP_APPROVALSTATUS = 'REQUESTED',
				REQUEST_USER_ID = '{UserName}',
				REQUEST_USER_RECORD_ID = '{UserId}',
				REQUESTOR_COMMENTS = '{RequestDesc}',
				REQUEST_DATE = '{datetime_value}',
				CUR_APRCHNSTP_ENTRYDATE = '{datetime_value}'
				WHERE APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
				ApprovalStatus=str(GetStatus.APROBJ_STATUSFIELD_VAL),
				QuoteNumber=str(self.QuoteNumber),
				UserName=str(self.UserName),
				UserId=str(self.UserId),
				datetime_value=str(self.datetime_value),
				RequestDesc=RequestDesc
			))
			if str(GetStatus.APPROVAL_METHOD).upper() == "PARALLEL STEP APPROVAL":
				
				parallel = "True"
				if CurrentTabName == 'Quotes':
					
					quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=self.quote_revision_record_id))
					quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
					if quote_obj is not None:
						approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND APPROVAL_RECORD_ID = '{approval_rec_id}'".format(quote_revision_record_id=self.quote_revision_record_id,approval_rec_id = GetStatus.APPROVAL_RECORD_ID))
						approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
						UpdateTrans = """UPDATE ACAPTX SET
							APPROVALSTATUS = 'REQUESTED',
							REQUESTOR_COMMENTS = '{RequestDesc}'
							WHERE APPROVAL_RECORD_ID = '{approval_record_id}'""".format(
							approval_record_id=approval_record_id,
							RequestDesc=str(RequestDesc),
						)
				else:
					approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND APPROVAL_RECORD_ID = '{approval_rec_id}'".format(quote_revision_record_id=self.quote_revision_record_id,approval_rec_id = GetStatus.APPROVAL_RECORD_ID))
					approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
					UpdateTrans = """UPDATE ACAPTX SET
						APPROVALSTATUS = 'REQUESTED',
						REQUESTOR_COMMENTS = '{RequestDesc}'
						WHERE APPROVAL_RECORD_ID = '{approval_record_id}' """.format(
						approval_record_id=str(approval_record_id),
						RequestDesc=str(RequestDesc),
					)
			else:
				
				parallel = "False"
				if CurrentTabName == 'Quotes':
					Trace.Write("Quote_Tab_J")
					quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=self.quote_revision_record_id))
					quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
					
					if quote_obj is not None:
						approval_queue_obj = Sql.GetList("select APPROVAL_RECORD_ID,APRCHNSTP_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND (APRSTAMAP_APPROVALSTATUS = 'REQUESTED' OR APRSTAMAP_APPROVALSTATUS = 'WAITING FOR APPROVAL') AND APRCHNSTP_RECORD_ID = '{chain_step_rec_id}'".format(quote_revision_record_id=self.quote_revision_record_id,chain_step_rec_id = GetStatus.APRCHNSTP_RECORD_ID))
						# (APRSTAMAP_APPROVALSTATUS = 'REQUESTED' OR APRSTAMAP_APPROVALSTATUS = 'WAITING FOR APPROVAL')
						for approval_queue in approval_queue_obj:
							approval_record_id = approval_queue.APPROVAL_RECORD_ID
							UpdateTrans = """UPDATE ACAPTX SET 
								APPROVALSTATUS = 'REQUESTED',
								REQUESTOR_COMMENTS = '{RequestDesc}'
								WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
								AND APRCHNSTP_ID = '1' """.format(
								QuoteNumber=str(self.QuoteNumber),
								RequestDesc=str(RequestDesc),
								#stepRecordId=str(GetStatus.APRCHNSTP_RECORD_ID),
							)
							##commented bcoz it is updating as approval required for both series and parallel
							#Sql.RunQuery("""UPDATE ACAPTX SET APPROVALSTATUS = 'APPROVAL REQUIRED'
							#        WHERE APRTRXOBJ_ID LIKE '{quote}'
							#        AND APRCHNSTP_ID != '1' AND ARCHIVED = 0""".format(
							#        quote=quote_obj.QUOTE_ID,
							#        RequestDesc=str(RequestDesc)
							#    #stepRecordId=str(GetStatus.APRCHNSTP_RECORD_ID),
							#))
				else:
					Trace.Write("Approval_Center_J")
					approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND APPROVAL_RECORD_ID = '{approval_rec_id}'".format(quote_revision_record_id=self.quote_revision_record_id,approval_rec_id = GetStatus.APPROVAL_RECORD_ID))
					approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
					UpdateTrans = """UPDATE ACAPTX SET
						APPROVALSTATUS = 'REQUESTED',
						REQUESTOR_COMMENTS = '{RequestDesc}'
						WHERE APPROVAL_RECORD_ID = '{approval_record_id}'
						AND APRCHNSTP_RECORD_ID = '{stepRecordId}' """.format(
						approval_record_id=str(approval_record_id),
						RequestDesc=str(RequestDesc),
						stepRecordId=str(GetStatus.APRCHNSTP_RECORD_ID),
					)
			##added runquery in update ACAPMA query
			#a = Sql.RunQuery(UpdateAppoval)
			b = Sql.RunQuery(UpdateTrans)
			approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND APPROVAL_RECORD_ID = '{approval_rec_id}'".format(quote_revision_record_id=self.quote_revision_record_id,approval_rec_id = GetStatus.APPROVAL_RECORD_ID))
			approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
			UPDATE_ACACHR = """ UPDATE ACACHR SET INITIATED_DATE = '{datetime_value}', INTIATEDBY_RECORD_ID = '{UserId}', INITIATED_BY = '{UserName}' WHERE ACACHR.APPROVAL_RECORD_ID='{approval_record_id}'""".format(UserId=self.UserId,UserName=self.UserName,datetime_value=self.datetime_value,approval_record_id=approval_record_id)
			Sql.RunQuery(UPDATE_ACACHR)

			GetCurStatus = Sql.GetFirst(
				"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
					ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL
					FROM ACACSS (NOLOCK)
					INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID =SYOBJD.PARENT_OBJECT_RECORD_ID
					INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.OBJECT_NAME=SYOBJD.OBJECT_NAME
					INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL=SYOBJH.LABEL
					WHERE ACAPMA.APPROVAL_RECORD_ID = '{approval_record_id}' AND ACACSS.APPROVALSTATUS = 'REQUESTED' """.format(
					approval_record_id=str(approval_record_id)
				)
			)
			if GetCurStatus:
				
				MainObjUpdateQuery = """UPDATE SAQTRV SET
					REVISION_STATUS = 'APPROVAL PENDING'
					WHERE QUOTE_REVISION_RECORD_ID = '{Primaryvalue}' """.format(
					statusUpdate = str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
					ObjName=str(GetCurStatus.OBJECT_NAME),
					ApiName=str(GetCurStatus.API_NAME),
					Primaryvalue=str(GetCurStatus.APRTRXOBJ_RECORD_ID),
					primaryKey = str(GetCurStatus.RECORD_NAME )
				)
				b = Sql.RunQuery(MainObjUpdateQuery)
				##Calling the iflow script to insert the records into SAQRSH custom table(Capture Date/Time for Quote Revision Status update.)
				CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))

				getQuote = Sql.GetFirst(
					"SELECT QUOTE_ID,REVISION_STATUS FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID = '"
					+ str(GetCurStatus.APRTRXOBJ_RECORD_ID)
					+ "' AND QTEREV_RECORD_ID = '"
					+str(self.quote_revision_record_id)
					+"'"
				)
				if getQuote.REVISION_STATUS == "APPROVED":
					
					result = ScriptExecutor.ExecuteGlobal("QTPOSTACRM", {"QUOTE_ID": getQuote.QUOTE_ID, 'Fun_type':'cpq_to_crm'})
			
			try:
				##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
				CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
				CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
			except Exception, e:
				Trace.Write("EXCEPTION: QUOTE WRITE BACK " +str(e))

			if parallel == "True":
				requestresponse = self.sendmailNotification("ParallelRequest")
			else:
				requestresponse = self.sendmailNotification("Request")
	
	def SubmitForApproval(self, RequestDesc, ACTION):
		"""Submt for approval and recall fucntion."""

		if str(ACTION) == "SUBMIT_FOR_APPROVAL":
			parallel = ""
			Trace.Write("@1336--"+ str(CurrentTabName))
			if CurrentTabName == 'Quotes':
				
				quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=self.quote_revision_record_id))
				quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
				if quote_obj is not None:
					##query is to get max distinct round APPROVAL_RECORD_ID 
					approval_queues_obj = Sql.GetList("""SELECT DISTINCT ACAPTX.APPROVAL_RECORD_ID from ACAPTX (NOLOCK) INNER JOIN ACAPMA (NOLOCK) on ACAPTX.APPROVAL_RECORD_ID = ACAPMA.APPROVAL_RECORD_ID and ACAPTX.APRTRXOBJ_ID = ACAPMA.APRTRXOBJ_ID INNER JOIN (select ACAPMA.APRCHN_ID,max(APPROVAL_ROUND) as round,ACAPMA.APRTRXOBJ_RECORD_ID from ACAPMA (NOLOCK) inner join ACAPTX (NOLOCK) ON ACAPTX.APPROVAL_RECORD_ID = ACAPMA.APPROVAL_RECORD_ID and ACAPTX.APRTRXOBJ_ID = ACAPMA.APRTRXOBJ_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '{quote_record_id}' GROUP BY ACAPMA.APRCHN_ID,ACAPMA.APRTRXOBJ_RECORD_ID) m on m.APRCHN_ID = ACAPTX.APRCHN_ID and m.round = ACAPTX.APPROVAL_ROUND and m.APRTRXOBJ_RECORD_ID = ACAPMA.APRTRXOBJ_RECORD_ID WHERE ACAPMA.APRSTAMAP_APPROVALSTATUS IN ('APPROVAL REQUIRED','RECALLED')""".format(quote_record_id = self.quote_revision_record_id))
					for approval_queue_obj in approval_queues_obj:
						approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
						self.QuoteNumber = approval_record_id
						archived_transaction_obj = Sql.GetFirst("SELECT count(*) as cnt FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{}' AND ARCHIVED = 1".format(self.QuoteNumber))
						explicit_approval = Sql.GetFirst(" SELECT CpqTableEntryId FROM ACAPTX WHERE REQUIRE_EXPLICIT_APPROVAL = 0 AND APPROVAL_RECORD_ID = '{}'".format(self.QuoteNumber))
						if archived_transaction_obj.cnt > 0 and explicit_approval is not None:
														
							self.SmartApprovalAction()
						else:
							
							GetStatus = Sql.GetFirst(
								"""SELECT ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHNSTP_RECORD_ID,ACAPCH.APPROVAL_METHOD,ACAPMA.APPROVAL_RECORD_ID
								FROM ACACSS (NOLOCK)
								INNER JOIN ACAPMA (NOLOCK) ON ACACSS.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
								INNER JOIN ACAPCH (NOLOCK) ON ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID
								WHERE ACACSS.APPROVALSTATUS = 'REQUESTED'
								AND APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
									QuoteNumber=str(self.QuoteNumber)
								)
							)
							# Trace.Write("RequestDescRequestDesc1--2004--"+str(RequestDesc)+str(GetStatus.APRCHNSTP_RECORD_ID)+str(GetStatus.APPROVAL_METHOD))
							self.SubmitForApprovalAction(GetStatus,RequestDesc)
			else:
				GetStatus = Sql.GetFirst(
					"""SELECT ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHNSTP_RECORD_ID,ACAPCH.APPROVAL_METHOD
					FROM ACACSS (NOLOCK)
					INNER JOIN ACAPMA (NOLOCK) ON ACACSS.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
					INNER JOIN ACAPCH (NOLOCK) ON ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID
					WHERE ACACSS.APPROVALSTATUS = 'REQUESTED'
					AND APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
						QuoteNumber=str(self.QuoteNumber)
					)
				)
				
				self.SubmitForApprovalAction(GetStatus, RequestDesc)
			
			
		elif str(ACTION) == "RECALL":
			#recallresponse = self.sendmailNotification("Recall")
			#try:
			if CurrentTabName == 'Quotes':
				quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=self.quote_revision_record_id))
				quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
				if quote_obj is not None:
					approval_queues_obj = Sql.GetList("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}' AND APRSTAMAP_APPROVALSTATUS = 'REJECTED'".format(quote_revision_record_id=self.quote_revision_record_id))
					#approval_record_id = 
					for approval_queue_obj in approval_queues_obj:
						self.QuoteNumber = str(approval_queue_obj.APPROVAL_RECORD_ID)
						#RecalledRecId = str(self.QuoteNumber)
						'''GetCurStatus1 = Sql.GetFirst(
							"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,SYOBJH.RECORD_ID,
								ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHN_RECORD_ID
								FROM ACACSS (NOLOCK)
								INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_STATUSFIELD_RECORD_ID = SYOBJD.RECORD_ID
								INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
								INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
								WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
								QuoteNumber=self.QuoteNumber
							)
						)
						if GetCurStatus1:
							if str(GetCurStatus.OBJECT_NAME) == "PASGRV":
								SegmentIds = str(GetCurStatus.APROBJ_ID)
								GetRevPrimary = Sql.GetFirst(
									"""SELECT PRICEAGREEMENT_REVISION_RECORD_ID
										FROM PASGRV (NOLOCK)
										WHERE AGMREV_ID = '{RevId}' """.format(
										RevId=str(SegmentIds)
									)
								)
								ObjPrimaryKey = str(GetRevPrimary.PRICEAGREEMENT_REVISION_RECORD_ID)'''
						GetCurStatus = Sql.GetFirst(
							"""SELECT DISTINCT SYOBJD.API_NAME,SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME,
									ACAPMA.APRTRXOBJ_RECORD_ID,ACACSS.APROBJ_STATUSFIELD_VAL,ACAPMA.APRCHN_RECORD_ID,ACAPMA.APPROVAL_ID
									FROM ACACSS (NOLOCK)
									INNER JOIN SYOBJD (NOLOCK) ON ACACSS.APROBJ_RECORD_ID = SYOBJD.PARENT_OBJECT_RECORD_ID
									INNER JOIN SYOBJH ON SYOBJH.OBJECT_NAME = SYOBJD.OBJECT_NAME
									INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
									WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'
									AND ACACSS.APPROVALSTATUS = 'RECALLED' """.format(
								QuoteNumber=str(self.QuoteNumber)
							)
						)
						if GetCurStatus:
							MainObjUpdateQuery = """UPDATE SAQTRV SET
							REVISION_STATUS = 'RECALLED'
							WHERE QUOTE_REVISION_RECORD_ID = '{Primaryvalue}' """.format(
									statusUpdate = str(GetCurStatus.APROBJ_STATUSFIELD_VAL),
									ObjName=str(GetCurStatus.OBJECT_NAME),
									ApiName=str(GetCurStatus.API_NAME),
									Primaryvalue=str(GetCurStatus.APRTRXOBJ_RECORD_ID),
									primaryKey = str(GetCurStatus.RECORD_NAME )
								)
							b = Sql.RunQuery(MainObjUpdateQuery)
							##Calling the iflow script to insert the records into SAQRSH custom table(Capture Date/Time for Quote Revision Status update.)
							CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
							
							UpdateAppoval = """UPDATE ACAPMA SET
								ACAPMA.APROBJ_STATUSFIELD_VALUE = ACACSS.APROBJ_STATUSFIELD_VAL,
								ACAPMA.APRSTAMAP_APPROVALSTATUS = ACACSS.APPROVALSTATUS
								FROM ACAPMA (NOLOCK)
								INNER JOIN ACACSS (NOLOCK) ON ACAPMA.APRCHN_RECORD_ID = ACACSS.APRCHN_RECORD_ID
								WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ACACSS.APPROVALSTATUS = 'RECALLED'
								AND ACAPMA.APRCHN_RECORD_ID = '{chainRecordId}' """.format(
								QuoteNumber=str(self.QuoteNumber), chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID)
							)
							Transupdate = """UPDATE ACAPTX SET ARCHIVED = 1 WHERE APPROVAL_RECORD_ID = '{QuoteNumber}'
							AND APRCHN_RECORD_ID = '{chainRecordId}' """.format(
								QuoteNumber=str(self.QuoteNumber), chainRecordId=str(GetCurStatus.APRCHN_RECORD_ID)
							)
							c = Sql.RunQuery(UpdateAppoval)
							d = Sql.RunQuery(Transupdate)
							#self.RecallSmartApprovalAction()
						try:
							##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
							CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
							CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
						except Exception, e:
							Trace.Write("EXCEPTION: QUOTE WRITE BACK "+str(e))

				#self.QuoteNumber = RecalledRecId
			#except Exception, e:
			#    self.exceptMessage = (
			#       "ACSECTACTN : SubmitForApproval : EXCEPTION : UNABLE TO SUBMIT OR RECALL : EXCEPTION E : " + str(e)
			#    )
			#    Trace.Write(self.exceptMessage)
		
	
		return True

	# A043S001P01 -  11384  Start
	def RichTextArea(self, value):
		"""Email template rich text area."""
		Product.SetGlobal("RichTextVaslue", value)
		return "True"

	# A043S001P01 -  11384  End
	# A043S001P01-12838 Start
	def PreviewApprovers(self, AllParams, FromSeg):        
		"""For preview option."""
		if 1:
			Htmlstr = data_list = ""
			recid = ""
			flag = 0
			complete = ""
			ApprovedIcon = self.ImagePath + "ApprovedCorrect.svg"
			UserIcon = self.ImagePath + "approval user icon.svg"
			RejectIcon = self.ImagePath + "close1.svg"
			PendingIcon = self.ImagePath + "clock.svg"
			ApproveWhiteIcon = self.ImagePath + "ApprovedCorrectwhite.svg"
			RejectWhiteIcon = self.ImagePath + "close1white.svg"
			LargeCrossRed = self.ImagePath + "Large Cross Red.svg"
			LargeTickgreen = self.ImagePath + "Large_Tick_green.svg"
			UserWhiteIcon = self.ImagePath + "usericonwhite.svg"
			clock_exe = self.ImagePath + "clock exe.svg"
			thumb_icon = self.ImagePath + "thumb_icon.svg"
			hour_glass = self.ImagePath + "hour_glass.svg"
			unanimous_consent = self.ImagePath + "unanimous_consent.svg"
			GroupUserIcon = self.ImagePath + "group_user_icon.svg"
			try:
				contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			except:
				Trace.Write("contract_quote_record_id !!!")
				contract_quote_record_id = ""
			steps_status = []
			headIcon_status = []
			get_chain_max_rounds = []
			##approval image based on chain step starts
			try:
				approval_chain = Param.approval_chain
			except:
				approval_chain = ""
			Trace.Write("Approval Chain---> "+str(approval_chain))
			##approval image based on chain step ends
			Trace.Write("CurrentTabName_J "+str(CurrentTabName))
			Trace.Write("From Seg "+str(FromSeg))
			if str(FromSeg) == "True" or CurrentTabName == 'Quotes' or CurrentTabName == 'Quote':
				ApiName = "APRTRXOBJ_RECORD_ID"
			else:
				if CurrentTabName == 'My Approval Queue':
					ApiName = "APPROVAL_RECORD_ID"
					getrecid = Sql.GetFirst("SELECT APPROVAL_RECORD_ID FROM ACAPTX WHERE APPROVAL_TRANSACTION_RECORD_ID = '{}'".format(self.QuoteNumber))
					recid = str(getrecid.APPROVAL_RECORD_ID)
				elif CurrentTabName == 'Team Approval Queue':
					ApiName = "APPROVAL_RECORD_ID"
					getrecid = Sql.GetFirst("SELECT APPROVAL_RECORD_ID FROM ACAPTX WHERE APPROVAL_TRANSACTION_RECORD_ID = '{}'".format(self.QuoteNumber))
					recid = str(getrecid.APPROVAL_RECORD_ID)
			if CurrentTabName == 'Quotes' or CurrentTabName == 'Quote':
				my_approval_queue_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID,QTEREV_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id=  self.quote_revision_record_id))
				quote_record_id = my_approval_queue_obj.MASTER_TABLE_QUOTE_RECORD_ID
				GetMaxStepsQuery = Sql.GetList(
					"""select ACAPCH.APRCHN_ID, ACAPCH.APRCHN_NAME,ACAPMA.CUR_APRCHNSTP, ACAPCH.APRCHN_DESCRIPTION, ACAPMA.APPROVAL_RECORD_ID,ACAPMA.APRTRXOBJ_ID,ACAPMA.APRCHN_RECORD_ID
						from ACAPCH (nolock)
						inner join ACAPMA (nolock) on ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID
						JOIN (SELECT ACAPCH.APRCHN_ID, ACAPMA.APRTRXOBJ_RECORD_ID,MAX(ACAPMA.CPQTABLEENTRYID) AS CPQTABLEENTRYID FROM ACAPMA(NOLOCK) JOIN ACAPCH(NOLOCK) ON ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID WHERE ACAPMA.APRTRXOBJ_RECORD_ID = '{revision_rec_id}'  GROUP BY ACAPCH.APRCHN_ID, ACAPMA.APRTRXOBJ_RECORD_ID) B ON ACAPMA.APRTRXOBJ_RECORD_ID = B.APRTRXOBJ_RECORD_ID AND ACAPCH.APRCHN_ID = B.APRCHN_ID AND ACAPMA.CPQTABLEENTRYID = B.CPQTABLEENTRYID 
						WHERE ACAPMA.APRTRXOBJ_RECORD_ID = '{revision_rec_id}'
						""".format(
						revision_rec_id=  self.quote_revision_record_id
					)
				)
			else:
				GetMaxStepsQuery = Sql.GetList(
					"""select ACAPCH.APRCHN_ID, ACAPCH.APRCHN_NAME, ACAPCH.APRCHN_DESCRIPTION, ACAPMA.APPROVAL_RECORD_ID
						from ACAPCH (nolock)
						inner join ACAPMA (nolock) on ACAPMA.APRCHN_RECORD_ID = ACAPCH.APPROVAL_CHAIN_RECORD_ID
						WHERE ACAPMA.{ApiName} = '{QuoteNumber}'
						group by ACAPCH.APRCHN_ID, ACAPCH.APRCHN_NAME, ACAPCH.APRCHN_DESCRIPTION, ACAPMA.APPROVAL_RECORD_ID
						""".format(
						QuoteNumber=recid, ApiName=ApiName
					)
				)
				my_queue_obj = Sql.GetFirst("""select APRTRXOBJ_RECORD_ID from ACAPMA where APPROVAL_RECORD_ID = '{QuoteNumber}'""".format(QuoteNumber=recid,revision_rec_id=  self.quote_revision_record_id))
				#my_approval_queue_obj = Sql.GetFirst("""select OWNER_NAME from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{quote_rec_id}'  AND QTEREV_RECORD_ID='{revision_rec_id}'""".format(quote_rec_id = my_queue_obj.APRTRXOBJ_RECORD_ID,revision_rec_id=  self.quote_revision_record_id))
				my_approval_queue_obj = Sql.GetFirst("""select OWNER_NAME from SAQTMT where QTEREV_RECORD_ID='{quote_rec_id}'""".format(quote_rec_id = my_queue_obj.APRTRXOBJ_RECORD_ID))
			if CurrentTabName == 'Quotes' or CurrentTabName == 'Quote':
				my_approval_queue_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID,OWNER_NAME from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id=  self.quote_revision_record_id))
				quote_record_id = my_approval_queue_obj.MASTER_TABLE_QUOTE_RECORD_ID
				GetMaxQuery = Sql.GetFirst(
					"""select max(ACAPTX.APRCHNSTP_ID) as MaxStep, ACAPTX.REQUESTOR_COMMENTS,max(ACAPTX.APPROVAL_ROUND) as appround 
						from ACAPTX (nolock)
						inner join ACAPMA (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
						where ACAPMA.APRTRXOBJ_RECORD_ID = '{revision_rec_id}' GROUP BY ACAPTX.REQUESTOR_COMMENTS""".format(
						revision_rec_id=  self.quote_revision_record_id
					)
				)
			else:
				GetMaxQuery = Sql.GetFirst(
					"""select max(ACAPTX.APRCHNSTP_ID) as MaxStep, ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND as appround
						from ACAPTX (nolock)
						inner join ACAPMA (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
						where ACAPMA.{ApiName} = '{QuoteNumber}' GROUP BY ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND""".format(
						QuoteNumber=recid, ApiName=ApiName
					)
				)    
			if GetMaxStepsQuery:
				data_list = GetMaxStepsQuery
				Htmlstr += '<div class="container-fluid">'
				Htmlstr += '<div class="row tabsmenu2" id="APPROVAL_TAB"><ul class="nav nav-tabs">'
				Htmlstr += '<li class="dropdown pull-right tabdrop hide">'
				Htmlstr += '<a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="icon-align-justify"></i>'
				Htmlstr += '<b class="caret"></b></a><ul class="dropdown-menu"></ul></li>'
				j = 0
				if str(FromSeg) == "True":
					Htmlstr += (
						'<li class="common_MyApprovalQueue active" onclick = "PriceApprovalHistory(this)" ><a data-toggle="tab">'
						+ '<abbr title="All">All</abbr></a></li>'
					)
					j += 1
				for GetMaxStep in GetMaxStepsQuery:
					if j == 0:
						active = "active"
						 ##approval image based on chain step starts
						if not approval_chain:
							approval_chain = str(GetMaxStep.APRCHN_ID)

						 ##approval image based on chain step ends
					else:
						active = ""
					##approval image based on chain step starts
					if approval_chain:
						if approval_chain == str(GetMaxStep.APRCHN_ID):
							active = "active"  
						else:
							active = ""  
					##approval image based on chain step ends
					appround = MaxStep = ""
					if GetMaxQuery:
						## to get max round of a particular chain in multi chain starts
						if CurrentTabName == 'Quotes' or CurrentTabName == 'Quote':
							GetMaxQuery = Sql.GetFirst(
								"""select max(ACAPTX.APRCHNSTP_ID) as MaxStep, max(ACAPTX.APPROVAL_ROUND) as appround,ACAPTX.APRCHN_ID,ACAPTX.REQUESTOR_COMMENTS 
									from ACAPTX (nolock)
									inner join ACAPMA (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
									where ACAPMA.APRTRXOBJ_RECORD_ID = '{revision_rec_id}' AND ACAPMA.APRCHN_NAME = '{chain_rec_id}' GROUP BY ACAPTX.APRCHN_ID,ACAPTX.REQUESTOR_COMMENTS""".format(
									revision_rec_id=  self.quote_revision_record_id,chain_rec_id = approval_chain
								)
							)
						get_chain_max_rounds.append(GetMaxQuery)   ##to get max rounds of all chains
						## to get max round of a particular chain in multi chain ends
						appround = GetMaxQuery.appround
						MaxStep = GetMaxQuery.MaxStep

					getaprovalsubtabname = 'Round '+str(appround)+" : "+str(GetMaxStep.APRCHN_ID)

					if Product.GetGlobal("TreeParentLevel1") != 'Approvals':
						Htmlstr += (
							'<li class="common_MyApprovalQueue '
							+ str(active)
							+ '"'
							+ 'id ="'
							+ str(GetMaxStep.APRCHN_ID)
							+ '"'
							+ ' onclick = "PriceApprovalHistory(this)"> <a data-toggle="tab"><abbr title="'
							+ str(GetMaxStep.APRCHN_DESCRIPTION)
							+ '">'
							+ str(getaprovalsubtabname)
							+ "</abbr></a></li>"
						)
						j += 1
				Htmlstr += "</ul></div>"
				if GetMaxQuery:  
					## REQUESTOR_COMMENTS is not in GetMaxQuery for quote tab
					if CurrentTabName != "Quotes" or CurrentTabName != 'Quote':                  
						requestor_comments = GetMaxQuery.REQUESTOR_COMMENTS
					## REQUESTOR_COMMENTS is not in GetMaxQuery for ends
					if Product.GetGlobal("TreeParentLevel1") == 'Approvals':                        
						GetMaxQuery = Sql.GetFirst(
						"""select max(ACAPTX.APRCHNSTP_ID) as MaxStep, ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND as appround
							from ACAPTX (nolock)
							inner join ACAPMA (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
							where ACAPMA.{ApiName} = '{QuoteNumber}' AND ACAPTX.APPROVAL_ROUND = {round} AND ACAPTX.APRCHN_ID = '{chain}' GROUP BY ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND""".format(
							QuoteNumber=self.quote_revision_record_id, ApiName="APRTRXOBJ_RECORD_ID",round=Product.GetGlobal("TreeParam").split(" ")[1],chain=Product.GetGlobal("TreeParentLevel0")
						)
						)
						GetComments = Sql.GetFirst(
						"""select ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND as appround
							from ACAPTX (nolock)
							inner join ACAPMA (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
							where ACAPMA.{ApiName} = '{QuoteNumber}' AND ACAPTX.APPROVAL_ROUND = {round} AND ACAPTX.APRCHN_ID = '{chain}' AND ACAPTX.REQUESTOR_COMMENTS != '' GROUP BY ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND""".format(
							QuoteNumber=self.quote_revision_record_id, ApiName="APRTRXOBJ_RECORD_ID",round=Product.GetGlobal("TreeParam").split(" ")[1],chain=Product.GetGlobal("TreeParentLevel0")
						)
						)
						if GetComments:
							requestor_comments = GetComments.REQUESTOR_COMMENTS
						else:
							requestor_comments = ""
					#A055S000P01-3376 - START    
					elif Product.GetGlobal("TreeParam") == 'Approvals' and (CurrentTabName == 'Quotes' or CurrentTabName == 'Quote'): 
						##to get REQUESTOR_COMMENTS of particular chain starts
						max_round = 1
						for get_chain_max_round in get_chain_max_rounds:
							if str(get_chain_max_round.APRCHN_ID) == str(approval_chain):
								max_round = get_chain_max_round.appround       
						## to get REQUESTOR_COMMENTS of particular chain starts         
						GetMinQuery = Sql.GetFirst(
						"""select ACAPTX.APRCHNSTP_ID, ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,ACAPTX.REQUESTOR_COMMENTS,ACAPTX.APPROVAL_ROUND as appround
							from ACAPTX (nolock)
							inner join ACAPMA (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
							where ACAPMA.{ApiName} = '{revision_rec_id}' AND ACAPTX.APPROVAL_ROUND = '{round}' AND ACAPTX.APRCHN_ID = '{approval_chain}'""".format(
							revision_rec_id=  self.quote_revision_record_id, ApiName="APRTRXOBJ_RECORD_ID",round=str(max_round),approval_chain= str(approval_chain)
						)
						)
						requestor_comments = GetMinQuery.REQUESTOR_COMMENTS
						if GetMinQuery:
							Product.SetGlobal("CurrentApprovalTransaction",GetMinQuery.APPROVAL_TRANSACTION_RECORD_ID)
						else:
							Product.SetGlobal("CurrentApprovalTransaction","")
					#A055S000P01-3376 - END      
				else:                    
					requestor_comments = ""
				Htmlstr += ('''
				<div class="row chainstep_fixed_Outer">
				<div class="chainstep_fixed_head col-md-12 p-0">
							<div class="col-md-6 border_rigt_cust">
								<p class="m-0">Requestor</p>
							</div>
							<div class="col-md-6">
								<p class="m-0">Requestor Comments</p>
							</div>
						</div>
				<div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
							<div class="col-md-1 p-0">
								<img title="'''+str(my_approval_queue_obj.OWNER_NAME)+'''" class="large_man_recp" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/approval_user_icon.svg" >
							</div>
							<div class="col-md-10 p-0">
								<p class="m-0"><span title="'''+str(my_approval_queue_obj.OWNER_NAME)+'''">'''+str(my_approval_queue_obj.OWNER_NAME)+'''</span></p>
							</div>
						</div>
						<div class="col-md-6 chainstep_sub_content p-0">                            
							<div class="col-md-12 p-0">
								<p class="m-0"><span>'''+str(requestor_comments)+'''</span></p>
							</div>
						</div>
				</div>''')


				Htmlstr += ('''<div class="row step_chain_outer_wrap">''')
				if CurrentTabName == "Quotes" or CurrentTabName == 'Quote':
					quote_record = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id = self.quote_revision_record_id))
					##Max_Round is commented and added below to get max round for particular chain
					#Max_Round = Sql.GetFirst("SELECT MAX(APPROVAL_ROUND) AS ROUND FROM ACAPTX (NOLOCK) WHERE APRTRXOBJ_ID = '{quote_record}'".format(quote_record = quote_record.QUOTE_ID))
				Trace.Write("max="+str(GetMaxQuery.MaxStep))
				for i in range(1, int(GetMaxQuery.MaxStep) + 1):
					Trace.Write("VALUE OF i="+str(i))
					if i > 1:
						if str(FromSeg) == "True":
							Htmlstr += '<div class="row dispflex">'
						# else:
							# Htmlstr += '<div class="row">'
						# for GetMaxStep in GetMaxStepsQuery:
						#     if str(FromSeg) == "True":
						#         Htmlstr += (
						#             '<div class="col-xs-6 stepicon minwid600 CommonHistoryPAApp '
						#             + str(GetMaxStep.APRCHN_NAME).replace(" ", "_")
						#             + '"></div>'
						#         )
						#     else:
						#         Htmlstr += '<div class="col-xs-3 col-xs-offset-5 stepicon"></div>'
						# Htmlstr += "</div>"
					# Htmlstr += '<div class="row vert-flexstart">'
					for GetMaxStep in GetMaxStepsQuery:
						if CurrentTabName == "Quotes" or CurrentTabName == 'Quote':
							##Max_Round is added to get max round for particular chain
							Max_Round = Sql.GetFirst("SELECT MAX(APPROVAL_ROUND) AS ROUND FROM ACAPTX (NOLOCK) WHERE APRTRXOBJ_ID = '{quote_record}' AND ACAPTX.APRCHN_RECORD_ID = '{chain_rec_id}'".format(quote_record = quote_record.QUOTE_ID, chain_rec_id = GetMaxStep.APRCHN_RECORD_ID))
							if Max_Round is not None:
								if str(TreeParam) == 'Approvals':
									##approval image based on chain step starts
									if approval_chain:
										approval_chain_name = "AND ACAPTX.APRCHN_ID = '{}'".format(str(approval_chain))

									else:
										approval_chain_name = ""
									##approval image based on chain step ends
									GetAllStep = Sql.GetList(
										"""select DISTINCT ACACST.ENABLE_SMARTAPPROVAL,ACAPTX.APRCHNSTP_ID,
											CASE
												when ACACSA.ROLE_ID != ''
													then 'ROLE'
												when ACACSA.PROFILE_ID != ''
													then 'PROFILE'
												else 'USER'
											END as ROLE, ACAPTX.APRCHNSTP_APPROVER_ID, ACACST.APRCHNSTP_NAME,
											ACACST.REQUIRE_EXPLICIT_APPROVAL,ACACST.UNANIMOUS_CONSENT
											from ACAPTX (NOLOCK)
											inner join ACACST (nolock) on ACACST.APRCHN_ID = ACAPTX.APRCHN_ID
											AND ACACST.APRCHNSTP_NUMBER = ACAPTX.APRCHNSTP_ID
											inner join ACACSA (nolock) on ACACSA.APRCHN_ID = ACACST.APRCHN_ID
											AND ACACST.APRCHNSTP_NUMBER = CAST(ACACSA.APRCHNSTP as FLOAT)
											WHERE ACAPTX.APPROVAL_RECORD_ID = '{ApprovalRecordId}' AND ACAPTX.APRCHNSTP_ID = '{StepId}' AND ACAPTX.APPROVAL_ROUND = '{Round}' AND ACAPTX.APRCHNSTP_ID IS NOT NULL {approval_cond}""".format(
											ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID), StepId=str(i), Round=str(Max_Round.ROUND),approval_cond = str(approval_chain_name)
										)
									)
								else:
									
									GetAllStep = Sql.GetList(
										"""select DISTINCT ACACST.ENABLE_SMARTAPPROVAL,ACAPTX.APRCHNSTP_ID,
											CASE
												when ACACSA.ROLE_ID != ''
													then 'ROLE'
												when ACACSA.PROFILE_ID != ''
													then 'PROFILE'
												else 'USER'
											END as ROLE, ACAPTX.APRCHNSTP_APPROVER_ID, ACACST.APRCHNSTP_NAME,
											ACACST.REQUIRE_EXPLICIT_APPROVAL,ACACST.UNANIMOUS_CONSENT
											from ACAPTX (NOLOCK)
											inner join ACACST (nolock) on ACACST.APRCHN_ID = ACAPTX.APRCHN_ID
											AND ACACST.APRCHNSTP_NUMBER = ACAPTX.APRCHNSTP_ID
											inner join ACACSA (nolock) on ACACSA.APRCHN_ID = ACACST.APRCHN_ID
											AND ACACST.APRCHNSTP_NUMBER = CAST(ACACSA.APRCHNSTP as FLOAT)
											WHERE
											ACAPTX.APRCHNSTP_ID = '{StepId}' AND ACAPTX.APPROVAL_ROUND = '{Round}' AND ACAPTX.APRCHNSTP_ID IS NOT NULL AND ACAPTX.APRTRXOBJ_ID LIKE '%{QuoteId}%'""".format(
											QuoteId=str(GetMaxStep.APRTRXOBJ_ID), StepId=str(i), Round=TreeParam.split(' ')[1].strip()
										)
									)

							else:
								
								GetAllStep = Sql.GetList(
									"""select DISTINCT ACACST.ENABLE_SMARTAPPROVAL,ACAPTX.APRCHNSTP_ID,
										CASE
											when ACACSA.ROLE_ID != ''
												then 'ROLE'
											when ACACSA.PROFILE_ID != ''
												then 'PROFILE'
											else 'USER'
										END as ROLE, ACAPTX.APRCHNSTP_APPROVER_ID, ACACST.APRCHNSTP_NAME,
										ACACST.REQUIRE_EXPLICIT_APPROVAL,ACACST.UNANIMOUS_CONSENT
										from ACAPTX (NOLOCK)
										inner join ACACST (nolock) on ACACST.APRCHN_ID = ACAPTX.APRCHN_ID
										AND ACACST.APRCHNSTP_NUMBER = ACAPTX.APRCHNSTP_ID
										inner join ACACSA (nolock) on ACACSA.APRCHN_ID = ACACST.APRCHN_ID
										AND ACACST.APRCHNSTP_NUMBER = CAST(ACACSA.APRCHNSTP as FLOAT)
										WHERE ACAPTX.APPROVAL_RECORD_ID = '{ApprovalRecordId}'
										AND ACAPTX.APRCHNSTP_ID = '{StepId}' AND ACAPTX.APRCHNSTP_ID IS NOT NULL """.format(
										ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID), StepId=str(i)
									)
								)
						else:
							GetAllStep = Sql.GetList(
								"""select DISTINCT ACACST.ENABLE_SMARTAPPROVAL,ACAPTX.APRCHNSTP_ID,
									CASE
										when ACACSA.ROLE_ID != ''
											then 'ROLE'
										when ACACSA.PROFILE_ID != ''
											then 'PROFILE'
										else 'USER'
									END as ROLE, ACAPTX.APRCHNSTP_APPROVER_ID, ACACST.APRCHNSTP_NAME,
									ACACST.REQUIRE_EXPLICIT_APPROVAL,ACACST.UNANIMOUS_CONSENT
									from ACAPTX (NOLOCK)
									inner join ACACST (nolock) on ACACST.APRCHN_ID = ACAPTX.APRCHN_ID
									AND ACACST.APRCHNSTP_NUMBER = ACAPTX.APRCHNSTP_ID
									inner join ACACSA (nolock) on ACACSA.APRCHN_ID = ACACST.APRCHN_ID
									AND ACACST.APRCHNSTP_NUMBER = CAST(ACACSA.APRCHNSTP as FLOAT)
									WHERE ACAPTX.APPROVAL_RECORD_ID = '{ApprovalRecordId}'
									AND ACAPTX.APRCHNSTP_ID = '{StepId}' AND ACAPTX.APRCHNSTP_ID IS NOT NULL """.format(
									ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID), StepId=str(i)
								)
							)
						
						if GetAllStep:
							chain = []


							for AllStep in GetAllStep:
								if str(FromSeg) == "True":
									Htmlstr += (
										'<div class="col-xs-6 previewapproval CommonHistoryPAApp '
										+ str(GetMaxStep.APRCHN_NAME).replace(" ", "_")
										+ '">'
									)
								else:
									# Htmlstr += '<div class="col-xs-12 previewapproval">'

									
									# Htmlstr += ('''<div class="row">''')
									if contract_quote_record_id != '' and self.quote_revision_record_id:
										quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID,OWNER_NAME from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"), revision_rec_id = self.quote_revision_record_id))
										
										if quote_obj is not None:
											quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
											
											if Product.GetGlobal("TreeParentLevel1") != 'Approvals':
												approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPTX where APRTRXOBJ_ID = '{quote_id}' AND APPROVAL_ROUND = '{roundd}'".format(quote_id = quote_obj.QUOTE_ID,roundd=Max_Round.ROUND))
											else:
												approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPTX where APRTRXOBJ_ID = '{quote_id}' AND APPROVAL_ROUND = '{roundd}' AND APRCHN_ID = '{chain}'".format(quote_id = quote_obj.QUOTE_ID,chain=Product.GetGlobal("TreeParentLevel0"),roundd=TreeParam.split(' ')[1]))
											approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
											Getchintype = Sql.GetFirst(
												"""SELECT APPROVAL_METHOD FROM ACAPCH (NOLOCK) INNER JOIN ACAPMA (NOLOCK)
												ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
												WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
													QuoteNumber=approval_record_id
												)
											)
											
											chain_Type = Sql.GetFirst("SELECT APPROVAL_METHOD FROM ACAPCH (NOLOCK) WHERE APRCHN_ID = '"+str(GetMaxStep.APRCHN_ID)+"'")
											if chain_Type.APPROVAL_METHOD == "SERIES STEP APPROVAL":
												parallel_icon = "/mt/APPLIEDMATERIALS_TST/Additionalfiles/parllel_arrow_icon.svg"
											elif chain_Type.APPROVAL_METHOD == "PARALLEL STEP APPROVAL":
												parallel_icon = "/mt/APPLIEDMATERIALS_TST/Additionalfiles/parllel_icon.svg"
										else:
											parallel_icon = "/mt/APPLIEDMATERIALS_TST/Additionalfiles/parllel_arrow_icon.svg"
									else:
										parallel_icon = "/mt/APPLIEDMATERIALS_TST/Additionalfiles/parllel_arrow_icon.svg"

									GetApproverQuery = Sql.GetList(
										"""select * from ACAPTX (NOLOCK)
											WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}'
											AND APRCHNSTP_ID = '{StepId}' AND APRCHN_ID = '{ChainId}' """.format(
											ApprovalRecordId=str(approval_queue_obj.APPROVAL_RECORD_ID) if Product.GetGlobal("TreeParentLevel1") == 'Approvals' else str(GetMaxStep.APPROVAL_RECORD_ID),
											StepId=str(AllStep.APRCHNSTP_ID),
											ChainId=str(GetMaxStep.APRCHN_ID),
										)
									)
									if GetApproverQuery:
										for GetApprover in GetApproverQuery:
											# BackgroundCss = ""
											# if str(GetApprover.APPROVALSTATUS) == "APPROVED":
											#     UserApproveIcon = LargeTickgreen
											#     BackgroundCss = "greenbg"
											# elif str(GetApprover.APPROVALSTATUS) == "REJECTED":
											#     UserApproveIcon = LargeCrossRed
											#     BackgroundCss = "redbg"
											# elif str(GetApprover.APPROVALSTATUS) == "REQUESTED":
											#     Trace.Write("User.IdUser.Id"+str(User.Id))
											#     Trace.Write("GetApprover.APPROVAL_RECIPIENT_RECORD_IDGetApprover.APPROVAL_RECIPIENT_RECORD_ID"+str(GetApprover.APPROVAL_RECIPIENT_RECORD_ID))
											#     if str(User.Id) == str(GetApprover.APPROVAL_RECIPIENT_RECORD_ID):
											#         Trace.Write("YEZZZ")
											#         UserApproveIcon =  '''<a id="approve" data-target="#preview_approval" onclick="approve_request()" data-toggle="modal"> <img class="iconsize" src="'''+ str(ApprovedIcon)+ '''" alt=""></a><a id="reject" data-target="#preview_approval" onclick="reject_request()" data-toggle="modal"> <img class="iconsize" src="'''+ str(RejectIcon)+ '''" alt=""></a>'''
											#     else:
											#         UserApproveIcon = '''<img src="'''+str(clock_exe)+'''">'''
											# else:
											#     UserApproveIcon = clock_exe


											# Trace.Write("UserApproveIcon"+str(UserApproveIcon))
											# Trace.Write("str(User.Id)"+str(User.Id))
											# if (
											#     str(GetApprover.APPROVAL_RECIPIENT_RECORD_ID) == str(User.Id)
											#     and str(FromSeg) != "True"
											# ):
											#     Trace.Write("APPROVAL_RECIPIENT_RECORD_ID")
											#     readonly = (
											#         '<a class="clrccc" id="'
											#         + str(GetApprover.APPROVAL_TRANSACTION_RECORD_ID)
											#         + '" onclick="ApprovalCommentEdit(this);" '
											#         + ' data-target="#preview_approval" data-toggle="modal">'
											#         + '<i class="fa fa-pencil" aria-hidden="true"></i>'
											#         + "</a>"
											#     )
											#     if str(GetApprover.APPROVALSTATUS) not in ["APPROVED", "REJECTED", "REQUESTED"]:
											#         Trace.Write("not in approval required--->"+str(GetApprover.APPROVALSTATUS))
											#         if str(FromSeg) == "True":
											#             colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
											#         else:
											#             colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
											#     elif (
											#         str(GetApprover.APPROVALSTATUS) == "REQUESTED"
											#         and str(GetApprover.ARCHIVED).upper() == "FALSE"
											#     ):  
											#         Trace.Write(" in REQUESTED--->"+str(GetApprover.APPROVALSTATUS))
											#         if str(FromSeg) == "True":
											#             colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
											#         else:
											#             colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
											#     else:
											#         Trace.Write("approvallllllllllllllllllllllllllllllll")
											#         if str(FromSeg) == "True":
											#             colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
											#         else:
											#             colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
											# else:
											#     readonly = (
											#         '<a class="clrccc" id="'
											#         + str(GetApprover.APPROVAL_TRANSACTION_RECORD_ID)
											#         + '" onclick="ApprovalCommentView(this);" '
											#         + ' data-target="#preview_approval" data-toggle="modal">'
											#         + '<i class="fa fa-eye" aria-hidden="true"></i>'
											#         + "</a>"
											#     )
											#     if str(GetApprover.APPROVALSTATUS) not in ["APPROVED", "REJECTED"]:
											#         if str(FromSeg) == "True":
											#             colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
											#         else:
											#             colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
											#     else:
											#         if str(FromSeg) == "True":
											#             colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
											#         else:
											#             colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
											# if str(FromSeg) == "True":
											#     colOneClass, colTwoClass, colThreeClass = "col-xs-5", "col-xs-7", "ellipsis_app"
											# else:
											#     colOneClass, colTwoClass, colThreeClass = "col-xs-4", "col-xs-8", ""
											# Trace.Write("HtmlstrHtmlstrHtmlstrHtmlstrHtmlstrHtmlstr")  

											# smart approval icon - starts

											if str(AllStep.ENABLE_SMARTAPPROVAL) == "True":
												thumb = ''' <img title="Smart Approval Enabled on Resubmission" class= "smart_approval_icon" src = "'''+ str(thumb_icon)+'''">'''
											else:
												thumb = ''
											# smart approval icon - ends
											##unanimous consent icon starts
											if str(AllStep.UNANIMOUS_CONSENT) == "True":
												unanimous = ''' <img title="Unanimous Consent Enabled" class="unanimous_consent_img" src="'''+str(unanimous_consent)+'''">'''
											else:
												unanimous = ""
											##unanimous consent icon ends


											if str(AllStep.APRCHNSTP_ID) not in chain:
												chain.append(str(AllStep.APRCHNSTP_ID))
												dynamic_icon = ''
												
												icon_status = Sql.GetList("SELECT DISTINCT APPROVALSTATUS FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}' AND APRCHNSTP_ID = '{StepId}'".format(ApprovalRecordId=str(approval_queue_obj.APPROVAL_RECORD_ID) if Product.GetGlobal("TreeParentLevel1") == 'Approvals' else str(GetMaxStep.APPROVAL_RECORD_ID), StepId= str(AllStep.APRCHNSTP_ID)))
												
												# rejection logic - starts
												
												for approval_status in icon_status:
													steps_status.append(approval_status.APPROVALSTATUS)
													headIcon_status.append(approval_status.APPROVALSTATUS)

												if "APPROVED" in headIcon_status and ("REQUESTED" not in headIcon_status and "APPROVAL REQUIRED" not in headIcon_status and "REJECTED" not in headIcon_status):
													dynamic_icon = '''<img title = 'Approved' src="'''+str(LargeTickgreen)+'''" class="center-block">'''
													dynamic_icon_1 = '''<img title = 'Approved' src="'''+str(LargeTickgreen)+'''" class="chainstep_collapse_img_top">'''
												elif "REJECTED" in headIcon_status and ("REQUESTED" not in headIcon_status and "APPROVAL REQUIRED" not in headIcon_status and "APPROVED" not in headIcon_status):
													dynamic_icon =  '''<img title = 'Rejected' src="'''+str(LargeCrossRed)+'''" class="center-block">'''
													dynamic_icon_1 =  '''<img title = 'Rejected' src="'''+str(LargeCrossRed)+'''" class="chainstep_collapse_img_top">'''
												elif "APPROVAL REQUIRED" in headIcon_status and ("REQUESTED" not in headIcon_status and "REJECTED" not in headIcon_status and "APPROVED" not in headIcon_status):
													dynamic_icon = ""
													dynamic_icon_1 = ""
												elif "REJECTED" in headIcon_status:
													dynamic_icon = '''<img title = 'Rejected' src="'''+str(LargeCrossRed)+'''" class="center-block">''' 
													dynamic_icon_1 = '''<img title = 'Rejected' src="'''+str(LargeCrossRed)+'''" class="chainstep_collapse_img_top">''' 
												else:
													dynamic_icon = '''<img title = 'Approval Required' src="'''+str(hour_glass)+'''" class="center-block">'''
													dynamic_icon_1 = '''<img title = 'Approval Required' 'REJECTED' src="'''+str(clock_exe)+'''" class="chainstep_collapse_img_top">'''
												Htmlstr += ('''    <div class="col-md-5 step_chain step-'''+str(AllStep.APRCHNSTP_ID)+'''">
														<div class="col-md-12 chainstep_head p-0">
															<div class="col-md-1">'''
															+str(dynamic_icon)+
															'''</div>
															<div class="col-md-11 p-0">
															<p class="m-0">Step '''+str(AllStep.APRCHNSTP_ID)+''' : '''+str(AllStep.APRCHNSTP_NAME) + str(thumb)+ str(unanimous)+ '''</p>
															</div>
													<img class="chain_step_right_img" src="'''+str(parallel_icon)+'''">
														</div>''')
												
												headIcon_status = []
												Htmlstr += (''' <div class="col-md-12 chainstep_sub_head_out p-0 ">
																	<div class="chainstep_sub_head col-md-12 p-0">
																		<div class="col-md-6 p-0">
																			<p class="m-0">RECIPIENT</p>
																		</div>
																		<div class="col-md-6 p-0">
																			<p class="m-0">RECIPIENT COMMENTS</p>
																		</div>
																	</div>
																	''')
												acaptx_data = Sql.GetList("SELECT DISTINCT * FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}' AND APRCHNSTP_ID = '{StepId}'".format(ApprovalRecordId=str(approval_queue_obj.APPROVAL_RECORD_ID) if Product.GetGlobal("TreeParentLevel1") == 'Approvals' else str(GetMaxStep.APPROVAL_RECORD_ID), StepId= str(AllStep.APRCHNSTP_ID)))
												# <button style="border:none;" class="fa fa-plus" id="approval-toggle" onclick="approval_toggle(this)"></button>
												apr_chn_stp = Sql.GetFirst("SELECT APRCHNSTP_APPROVER_ID FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}' AND APRCHNSTP_ID = '{StepId}'".format(ApprovalRecordId=str(approval_queue_obj.APPROVAL_RECORD_ID) if Product.GetGlobal("TreeParentLevel1") == 'Approvals' else str(GetMaxStep.APPROVAL_RECORD_ID), StepId= str(AllStep.APRCHNSTP_ID)))
												approver_id = apr_chn_stp.APRCHNSTP_APPROVER_ID
												# approval_grouping = Sql.GetList("SELECT APRCHNSTP_APPROVER_ID FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}' AND APRCHNSTP_ID = '{StepId}'".format(ApprovalRecordId=str(approval_queue_obj.APPROVAL_RECORD_ID) if Product.GetGlobal("TreeParentLevel1") == 'Approvals' else str(GetMaxStep.APPROVAL_RECORD_ID), StepId= str(AllStep.APRCHNSTP_ID)))
												# for group in approval_grouping:
												if (str(approver_id).startswith("PRO") or str(approver_id).startswith("ROL")):
													Htmlstr += ('''<div class="chainstep_arrow_out_collapse"> <div class="col-md-12 border_rigt_cust chainstep_sub_content p-0">  <a class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapse_'''+str(AllStep.APRCHNSTP_ID)+'''" id="approval-toggle"> <img title="'''+str(apr_chn_stp.APRCHNSTP_APPROVER_ID)+'''" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/group_3_user_icon.svg"> <span title="'''+str(apr_chn_stp.APRCHNSTP_APPROVER_ID)+'''">'''+str(apr_chn_stp.APRCHNSTP_APPROVER_ID)+'''</span> </a> '''+str(dynamic_icon_1)+''' </div> </div>''')
											
													Htmlstr += ('''<div id="collapse_'''+str(AllStep.APRCHNSTP_ID)+'''" class="panel-collapse collapse"> ''')
												for data in acaptx_data:
													if str(data.APPROVALSTATUS) == "REQUESTED":
														if (str(User.Id) == str(data.APPROVAL_RECIPIENT_RECORD_ID)):
															Trace.Write("CHKNG_ICON_CONDTN")
															if Product.GetGlobal("TreeParentLevel1") != 'Approvals':
																
																req_status = '''<a class ='' id="approve_'''+str(data.APPROVAL_TRANSACTION_RECORD_ID)+'''" data-target="#preview_approval" onclick="approve_request(this)" data-toggle="modal"> <img class="iconsize" src="'''+ str(ApprovedIcon)+ '''" alt=""></a><a class ='' id="reject_'''+str(data.APPROVAL_TRANSACTION_RECORD_ID)+'''" data-target="#preview_approval" onclick="reject_request(this)" data-toggle="modal"> <img class="iconsize" src="'''+ str(RejectIcon)+ '''" alt=""></a>'''
																
															else:
																req_status = '''<img title='Approval Required' src="'''+str(clock_exe)+'''">'''
														else:
															req_status = '''<img title='Approval Required' src="'''+str(clock_exe)+'''">'''
														if ('REJECTED' in steps_status):
															req_status = ""
													elif str(data.APPROVALSTATUS) == "APPROVED":
														req_status = '''<img title = 'Approved' src="'''+str(LargeTickgreen)+'''">'''
													elif str(data.APPROVALSTATUS) == "REJECTED":
														req_status = '''<img title = 'Rejected' src="'''+str(LargeCrossRed)+'''">'''
													elif str(data.APPROVALSTATUS) == "APPROVAL REQUIRED":
														req_status = ''
													elif str(data.APPROVALSTATUS) == "APPROVAL NO LONGER REQUIRED":
														req_status = '''<img title = 'Approval No Longer Required' class = "group_user_green_tick" src="'''+str(GroupUserIcon)+'''">'''
 
													else:
														if ('REJECTED' in steps_status):
															req_status = ""
														else:
															req_status = '''<img title='Approval Required'  src = "'''+str(clock_exe)+'''">'''
													
													if (str(data.APRCHNSTP_APPROVER_ID).startswith("PRO") or str(data.APRCHNSTP_APPROVER_ID).startswith("ROL")):
														Htmlstr += (''' <div class="chainstep_arrow_out">

																	<div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
																		<div class="col-md-3 p-0">
																			<img title="'''+str(data.APPROVAL_RECIPIENT)+'''" class="man_recp" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/approval_user_icon.svg" class="center-block">
																		</div>
																		<div class="col-md-9 p-0">
																			<p class="m-0"><span title="'''+str(data.APPROVAL_RECIPIENT)+'''">'''+str(data.APPROVAL_RECIPIENT)+'''</span>   '''+str(req_status)+'''</p>
																		</div>
																	</div>
																	<div class="col-md-6 chainstep_sub_content p-0">                                                                        
																		<div class="col-md-12 p-0">
																			<p class="m-0"><span title="'''+str(data.RECIPIENT_COMMENTS)+'''">'''+str(data.RECIPIENT_COMMENTS)+'''</span></p>
																		</div>
																	</div>
																	
																	
																</div>
																''')
												if (str(approver_id).startswith("PRO") or str(approver_id).startswith("ROL")):
													Htmlstr += ('''</div>''')
												for data in acaptx_data:
													if (str(data.APRCHNSTP_APPROVER_ID).startswith("USR") or str(data.APRCHNSTP_APPROVER_ID).startswith("USR")):
														
														if str(data.APPROVALSTATUS) == "REQUESTED":
															if (str(User.Id) == str(data.APPROVAL_RECIPIENT_RECORD_ID)):
																if Product.GetGlobal("TreeParentLevel1") != 'Approvals':
																	
																	req_status = '''<a class ='' id="approve_'''+str(data.APPROVAL_TRANSACTION_RECORD_ID)+'''" data-target="#preview_approval" onclick="approve_request(this)" data-toggle="modal"> <img class="iconsize" src="'''+ str(ApprovedIcon)+ '''" alt=""></a><a class ='' id="reject_'''+str(data.APPROVAL_TRANSACTION_RECORD_ID)+'''" data-target="#preview_approval" onclick="reject_request(this)" data-toggle="modal"> <img class="iconsize" src="'''+ str(RejectIcon)+ '''" alt=""></a>'''
																	
																else:
																	req_status = '''<img title='Approval Required' src="'''+str(clock_exe)+'''">'''
															else:
																
																req_status = '''<img title='Approval Required' src="'''+str(clock_exe)+'''">'''
															if ('REJECTED' in steps_status):
																req_status = ""
														elif str(data.APPROVALSTATUS) == "APPROVED":
															req_status = '''<img title = 'Approved' src="'''+str(LargeTickgreen)+'''">'''
														elif str(data.APPROVALSTATUS) == "REJECTED":
															req_status = '''<img title = 'Rejected' src="'''+str(LargeCrossRed)+'''">'''
														elif str(data.APPROVALSTATUS) == "APPROVAL REQUIRED":
															req_status = ''
														elif str(data.APPROVALSTATUS) == "APPROVAL NO LONGER REQUIRED":
															req_status = '''<img title = 'Approval No Longer Required' class = "group_user_green_tick" src="'''+str(GroupUserIcon)+'''">'''

														else:
															if ('REJECTED' in steps_status):
																req_status = ""
															else:
																req_status = '''<img title='Approval Required'  src = "'''+str(clock_exe)+'''">'''
													
														Htmlstr += (''' <div class="chainstep_arrow_out individual_user">

																	<div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
																		<div class="col-md-3 p-0">
																			<img title="'''+str(data.APPROVAL_RECIPIENT)+'''" class="man_recp" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/approval_user_icon.svg" class="center-block">
																		</div>
																		<div class="col-md-9 p-0">
																			<p class="m-0"><span title="'''+str(data.APPROVAL_RECIPIENT)+'''">'''+str(data.APPROVAL_RECIPIENT)+'''</span>   '''+str(req_status)+'''</p>
																		</div>
																	</div>
																	<div class="col-md-6 chainstep_sub_content p-0">                                                                        
																		<div class="col-md-12 p-0">
																			<p class="m-0"><span title="'''+str(data.RECIPIENT_COMMENTS)+'''">'''+str(data.RECIPIENT_COMMENTS)+'''</span></p>
																		</div>
																	</div>
																	
																	
																</div>
																''')
												Htmlstr += ('''</div>''')
												Htmlstr += ('''</div>''')

												# approval_grouping = Sql.GetList("SELECT APRCHNSTP_APPROVER_ID FROM ACAPTX (NOLOCK) WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}' AND APRCHNSTP_ID = '{StepId}'".format(ApprovalRecordId=str(approval_queue_obj.APPROVAL_RECORD_ID) if Product.GetGlobal("TreeParentLevel1") == 'Approvals' else str(GetMaxStep.APPROVAL_RECORD_ID), StepId= str(AllStep.APRCHNSTP_ID)))
												# for group in approval_grouping:
												#     if (str(group.APRCHNSTP_APPROVER_ID).startswith("PRO") or str(group.APRCHNSTP_APPROVER_ID).startswith("ROL")):
												#         Htmlstr += ('''<div class="chainstep_arrow_out_collapse"> <div class="col-md-12 border_rigt_cust chainstep_sub_content p-0">  <a class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapse_'''+str(AllStep.APRCHNSTP_ID)+'''" id="approval-toggle"> <img title="'''+str(apr_chn_stp.APRCHNSTP_APPROVER_ID)+'''" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/group_3_user_icon.svg"> <span title="'''+str(apr_chn_stp.APRCHNSTP_APPROVER_ID)+'''">'''+str(apr_chn_stp.APRCHNSTP_APPROVER_ID)+'''</span> </a> '''+str(dynamic_icon_1)+''' </div> </div>''')
												
												#         Htmlstr += ('''<div id="collapse_'''+str(AllStep.APRCHNSTP_ID)+'''" class="panel-collapse collapse"> ''')

												#         Htmlstr += (''' <div class="chainstep_arrow_out">

												#                     <div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
												#                         <div class="col-md-3 p-0">
												#                             <img title="'''+str(data.APPROVAL_RECIPIENT)+'''" class="man_recp" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/approval_user_icon.svg" class="center-block">
												#                         </div>
												#                         <div class="col-md-9 p-0">
												#                             <p class="m-0"><span title="'''+str(data.APPROVAL_RECIPIENT)+'''">'''+str(data.APPROVAL_RECIPIENT)+'''</span>   '''+str(req_status)+'''</p>
												#                         </div>
												#                     </div>
												#                     <div class="col-md-6 chainstep_sub_content p-0">                                                                        
												#                         <div class="col-md-12 p-0">
												#                             <p class="m-0"><span title="'''+str(data.RECIPIENT_COMMENTS)+'''">'''+str(data.RECIPIENT_COMMENTS)+'''</span></p>
												#                         </div>
												#                     </div>
																	
																	
												#                 </div>
												#                 ''')
												#         Htmlstr += ('''</div>''')
												#         Htmlstr += ('''</div>''')
												#         Htmlstr += ('''</div>''')
												#     else:
												#         Htmlstr += (''' <div class="chainstep_arrow_out">

												#                     <div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
												#                         <div class="col-md-3 p-0">
												#                             <img title="'''+str(data.APPROVAL_RECIPIENT)+'''" class="man_recp" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/approval_user_icon.svg" class="center-block">
												#                         </div>
												#                         <div class="col-md-9 p-0">
												#                             <p class="m-0"><span title="'''+str(data.APPROVAL_RECIPIENT)+'''">'''+str(data.APPROVAL_RECIPIENT)+'''</span>   '''+str(req_status)+'''</p>
												#                         </div>
												#                     </div>
												#                     <div class="col-md-6 chainstep_sub_content p-0">                                                                        
												#                         <div class="col-md-12 p-0">
												#                             <p class="m-0"><span title="'''+str(data.RECIPIENT_COMMENTS)+'''">'''+str(data.RECIPIENT_COMMENTS)+'''</span></p>
												#                         </div>
												#                     </div>
																	
																	
												#                 </div>
												#                 ''')
												#         Htmlstr += ('''</div>''')
												#         Htmlstr += ('''</div>''')

	
				Htmlstr += ('''</div>''')

				


								# Mutedhtml = ('''<div class="chainstep_arrow_out">
								#                 <div class="col-md-12 chainstep_sub_head_out p-0 ">
								#                 <div class="chainstep_sub_head col-md-12 p-0">
								#                     <div class="col-md-6 p-0">
								#                         <p class="m-0">Role :regional bd manager</p>
								#                     </div>
								#                     <div class="col-md-6 p-0">
								#                         <p class="m-0">Role :recipient comments</p>
								#                     </div>
								#                 </div>
								#                 <div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
								#                     <div class="col-md-2 p-0">
								#                         <img src="">
								#                     </div>
								#                     <div class="col-md-10 p-0">
								#                         <p class="m-0">yang tsuo wu</p>
								#                     </div>
								#                 </div>
								#                 <div class="col-md-6 chainstep_sub_content p-0">
								#                     <div class="col-md-2 p-0">
								#                         <img src="">
								#                     </div>
								#                     <div class="col-md-10 p-0">
								#                         <p class="m-0"></p>
								#                     </div>
								#                 </div>
								#                 </div>
								#                 <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/parllel_connector.svg" class="center-block">
											
								#             </div>
								#                                                         <div class="chainstep_arrow_out">
								#                 <div class="col-md-12 chainstep_sub_head_out p-0 ">
								#                 <div class="chainstep_sub_head col-md-12 p-0">
								#                     <div class="col-md-6 p-0">
								#                         <p class="m-0">Role :vp of Marketing</p>
								#                     </div>
								#                     <div class="col-md-6 p-0">
								#                         <p class="m-0">Role :recipient comments</p>
								#                     </div>
								#                 </div>
								#                 <div class="col-md-6 border_rigt_cust chainstep_sub_content p-0">
								#                     <div class="col-md-2 p-0">
								#                         <img src="">
								#             ''')
					# GetMaxStatus = Sql.GetFirst(
					#     """select max(APPROVALSTATUS) as STATUS
					#         from ACAPTX (NOLOCK)
					#         WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}'
					#         AND APRCHNSTP_ID = '{StepId}' AND APRCHN_ID = '{ChainId}' """.format(
					#         ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID),
					#         StepId=str(AllStep.APRCHNSTP_ID),
					#         ChainId=str(GetMaxStep.APRCHN_ID),
					#     )
					# )
					# GetApproverQuery = Sql.GetList(
					#     """select * from ACAPTX (NOLOCK)
					#         WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}'
					#         AND APRCHNSTP_ID = '{StepId}' AND APRCHN_ID = '{ChainId}' """.format(
					#         ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID),
					#         StepId=str(AllStep.APRCHNSTP_ID),
					#         ChainId=str(GetMaxStep.APRCHN_ID),
					#     )
					# )
					# Trace.Write("""select * from ACAPTX (NOLOCK)
					#         WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}'
					#         AND APRCHNSTP_ID = '{StepId}' AND APRCHN_ID = '{ChainId}' """.format(
					#         ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID),
					#         StepId=str(AllStep.APRCHNSTP_ID),
					#         ChainId=str(GetMaxStep.APRCHN_ID),
					#     ))
					# GetApproverCountQuery = Sql.GetFirst(
					#     """select count(*) as cnt from ACAPTX (NOLOCK)
					#         WHERE APPROVAL_RECORD_ID = '{ApprovalRecordId}'
					#         AND APRCHNSTP_ID = '{StepId}' AND APRCHN_ID = '{ChainId}' """.format(
					#         ApprovalRecordId=str(GetMaxStep.APPROVAL_RECORD_ID),
					#         StepId=str(AllStep.APRCHNSTP_ID),
					#         ChainId=str(GetMaxStep.APRCHN_ID),
					#     )
					# )
					# if str(AllStep.REQUIRE_EXPLICIT_APPROVAL) == "True":
					#     AppendImage = "withtick"
					# else:
					#     AppendImage = ""
					# if int(GetApproverCountQuery.cnt) > 4:
					#     HeaderImage = self.ImagePath + "fiveuseralt" + str(AppendImage) + ".svg"
					# elif int(GetApproverCountQuery.cnt) == 4:
					#     HeaderImage = self.ImagePath + "fouruser" + str(AppendImage) + ".svg"
					# elif int(GetApproverCountQuery.cnt) == 3:
					#     HeaderImage = self.ImagePath + "threeuser" + str(AppendImage) + ".svg"
					# elif int(GetApproverCountQuery.cnt) == 2:
					#     Trace.Write("count 222")
					#     HeaderImage = self.ImagePath + "twouser" + str(AppendImage) + ".svg"
					# else:
					#     HeaderImage = self.ImagePath + "approval user icon.svg"
					# if str(GetMaxStatus.STATUS) in ["REQUESTED", "APPROVAL REQUIRED"]:
					#     Trace.Write("REQUESTED APPROVAL REQUIRED")
					#     Cssclass = "whtgraypad3"
					#     StepApproveIcon = clock_exe
					# elif str(GetMaxStatus.STATUS) == "REJECTED":
					#     Trace.Write("REJECTED")
					#     Cssclass = "whtredpad3"
					#     StepApproveIcon = RejectIcon
					# else:
					#     Trace.Write("elseeeeeeeeeeeeeeeeeeeeeeeeeeeee")
					#     Cssclass = "whtgrepad3"
					#     StepApproveIcon = ApprovedIcon
					# # Htmlstr += '<div class="' + str(Cssclass) + ' row row-no-gutters borbot1">'
					# # if str(FromSeg) == "True":
					# #     colOneClass, colTwoClass, fontStyleClass = "col-xs-5", "col-xs-7", "fntsizlin15"
					# # else:
					# #     colOneClass, colTwoClass, fontStyleClass = "col-xs-4", "col-xs-8", "fntsiwtcol"
					# # Htmlstr += '<div class="' + str(colOneClass) + ' marleft3px"><div class="row vert-align">'
					# # Htmlstr += (
					# #     '<div class="col-xs-2"><img class="dishtpadbakmatlt" src="'
					# #     + str(clock_exe)
					# #     + '"></div>'
					# # )
					# # Htmlstr += (
					# #     '<div class="col-xs-8 txt_cnt fnthed clrgray pad10">'
					# #     + str(AllStep.ROLE)
					# #     + " : "
					# #     + str(AllStep.APRCHNSTP_APPROVER_ID)
					# #     + '</div><div class="col-xs-2 txt_cnt padtopbot5">'
					# #     + '<div class="cust_pro_des_para lineht30 '
					# #     + str(fontStyleClass)
					# #     + '">STEP '
					# #     + str(AllStep.APRCHNSTP_ID)
					# #     + "</div></div></div></div><div class='"
					# #     + str(colTwoClass)
					# #     + " txt_cnt fnthed clrgray pad10'>"
					# #     + "<div class='row vert-align'> RECIPIENT COMMENTS </div>"
					# #     + "</div>"
					# # )
					# # Htmlstr += "</div>"

					# if GetApproverQuery:
					#     Trace.Write("GetApproverQuery GetApproverQuery")
					#     for GetApprover in GetApproverQuery:
					#         BackgroundCss = ""
					#         if str(GetApprover.APPROVALSTATUS) == "APPROVED":
					#             UserApproveIcon = ApproveWhiteIcon
					#             BackgroundCss = "greenbg"
					#         elif str(GetApprover.APPROVALSTATUS) == "REJECTED":
					#             UserApproveIcon = RejectWhiteIcon
					#             BackgroundCss = "redbg"
					#         else:
					#             UserApproveIcon = clock_exe
					#         # Htmlstr += '<div class="bgwht borbot1 fntreg row row-no-gutters">'
					#         if (
					#             str(GetApprover.APPROVAL_RECIPIENT_RECORD_ID) == str(User.Id)
					#             and str(FromSeg) != "True"
					#         ):
					#             Trace.Write("APPROVAL_RECIPIENT_RECORD_ID")
					#             readonly = (
					#                 '<a class="clrccc" id="'
					#                 + str(GetApprover.APPROVAL_TRANSACTION_RECORD_ID)
					#                 + '" onclick="ApprovalCommentEdit(this);" '
					#                 + ' data-target="#preview_approval" data-toggle="modal">'
					#                 + '<i class="fa fa-pencil" aria-hidden="true"></i>'
					#                 + "</a>"
					#             )
					#             if str(GetApprover.APPROVALSTATUS) not in ["APPROVED", "REJECTED", "REQUESTED"]:
					#                 Trace.Write("not in approval required--->"+str(GetApprover.APPROVALSTATUS))
					#                 if str(FromSeg) == "True":
					#                     colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
					#                 else:
					#                     colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
					#                 # Htmlstr += (
					#                 #     '<div class="'
					#                 #     + str(colOneClass)
					#                 #     + " borright1px "
					#                 #     + str(BackgroundCss)
					#                 #     + '">'
					#                 #     + '<div class="row vert-align">'
					#                 #     + '<div class="col-xs-2 txt_cnt padtopbot5"><img class="iconsize" src="'
					#                 #     + str(UserIcon)
					#                 #     + '" alt=""></div><div class="col-xs-8 pad10 fntreg">'
					#                 #     + str(GetApprover.APPROVAL_RECIPIENT)
					#                 #     + '</div><div class="col-xs-2 txt_cnt padtopbot5">'
					#                 #     + '<img class="iconsize" src="'
					#                 #     + str(UserApproveIcon)
					#                 #     + '" alt=""></div></div></div>'
					#                 # )
					#             elif (
					#                 str(GetApprover.APPROVALSTATUS) == "REQUESTED"
					#                 and str(GetApprover.ARCHIVED).upper() == "FALSE"
					#             ):  
					#                 Trace.Write(" in REQUESTED--->"+str(GetApprover.APPROVALSTATUS))
					#                 if str(FromSeg) == "True":
					#                     colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
					#                 else:
					#                     colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
					#                 # Htmlstr += (
					#                 #     '<div class="'
					#                 #     + str(colOneClass)
					#                 #     + ' borright1px"><div class="row vert-align">'
					#                 #     + '<div class="col-xs-2 txt_cnt padtopbot5"><img class="iconsize" src="'
					#                 #     + str(UserIcon)
					#                 #     + '" alt=""></div><div class="col-xs-6 pad10 fntreg">'
					#                 #     + str(GetApprover.APPROVAL_RECIPIENT)
					#                 #     + '</div><div class="col-xs-2 text-right padtopbot5"><div>'
					#                 #     + '<a id="approve" data-target="#preview_approval"'
					#                 #     + 'onclick="approve_request()" data-toggle="modal">'
					#                 #     + '<img class="iconsize" src="'
					#                 #     + str(ApprovedIcon)
					#                 #     + '" alt=""></a></div></div>'
					#                 #     + '<div class="col-xs-2 txt_cnt padtopbot5"><div>'
					#                 #     + '<a id="reject" data-target="#preview_approval"'
					#                 #     + 'onclick="reject_request()" data-toggle="modal">'
					#                 #     + '<img class="iconsize" src="'
					#                 #     + str(RejectIcon)
					#                 #     + '" alt=""></a></div></div></div></div>'
					#                 # )
					#             else:
					#                 Trace.Write("approvallllllllllllllllllllllllllllllll")
					#                 if str(FromSeg) == "True":
					#                     colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
					#                 else:
					#                     colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
					#                 # Htmlstr += (
					#                 #     '<div class="'
					#                 #     + str(colOneClass)
					#                 #     + " borright1px "
					#                 #     + str(BackgroundCss)
					#                 #     + '">'
					#                 #     + '<div class="row vert-align">'
					#                 #     + '<div class="col-xs-2 txt_cnt padtopbot5"><img class="iconsize" src="'
					#                 #     + str(UserWhiteIcon)
					#                 #     + '" alt=""></div><div class="col-xs-8 pad10 fntreg clrwht">'
					#                 #     + str(GetApprover.APPROVAL_RECIPIENT)
					#                 #     + '</div><div class="col-xs-2 txt_cnt padtopbot5">'
					#                 #     + '<img class="iconsize" src="'
					#                 #     + str(UserApproveIcon)
					#                 #     + '" alt=""></div></div></div>'
					#                 # )
					#                 # Trace.Write("approvallllllllllllllllllllllllllllllll approvallllllllllllllllllllllllllllllll")
					#         else:
					#             readonly = (
					#                 '<a class="clrccc" id="'
					#                 + str(GetApprover.APPROVAL_TRANSACTION_RECORD_ID)
					#                 + '" onclick="ApprovalCommentView(this);" '
					#                 + ' data-target="#preview_approval" data-toggle="modal">'
					#                 + '<i class="fa fa-eye" aria-hidden="true"></i>'
					#                 + "</a>"
					#             )
					#             if str(GetApprover.APPROVALSTATUS) not in ["APPROVED", "REJECTED"]:
					#                 if str(FromSeg) == "True":
					#                     colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
					#                 else:
					#                     colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
					#                 # Htmlstr += (
					#                 #     '<div class="'
					#                 #     + str(colOneClass)
					#                 #     + ' borright1px"><div class="row vert-align">'
					#                 #     + '<div class="col-xs-2 txt_cnt padtopbot5"><img class="iconsize" src="'
					#                 #     + str(UserIcon)
					#                 #     + '" alt=""></div><div class="col-xs-8 pad10 fntreg">'
					#                 #     + str(GetApprover.APPROVAL_RECIPIENT)
					#                 #     + '</div><div class="col-xs-2 txt_cnt padtopbot5">'
					#                 #     + '<img class="iconsize" src="'
					#                 #     + str(UserApproveIcon)
					#                 #     + '" alt=""></div></div></div>'
					#                 # )
					#             else:
					#                 if str(FromSeg) == "True":
					#                     colOneClass, colTwoClass = "col-xs-5", "col-xs-7"
					#                 else:
					#                     colOneClass, colTwoClass = "col-xs-4", "col-xs-8"
					#                 # Htmlstr += (
					#                 #     '<div class="'
					#                 #     + str(colOneClass)
					#                 #     + " borright1px "
					#                 #     + str(BackgroundCss)
					#                 #     + '">'
					#                 #     + '<div class="row vert-align">'
					#                 #     + '<div class="col-xs-2 txt_cnt padtopbot5"><img class="iconsize" src="'
					#                 #     + str(UserWhiteIcon)
					#                 #     + '" alt=""></div><div class="col-xs-8 pad10 fntreg clrwht">'
					#                 #     + str(GetApprover.APPROVAL_RECIPIENT)
					#                 #     + '</div><div class="col-xs-2 txt_cnt padtopbot5">'
					#                 #     + '<img class="iconsize" src="'
					#                 #     + str(UserApproveIcon)
					#                 #     + '" alt=""></div></div></div>'
					#                 # )
					#         if str(FromSeg) == "True":
					#             colOneClass, colTwoClass, colThreeClass = "col-xs-5", "col-xs-7", "ellipsis_app"
					#         else:
					#             colOneClass, colTwoClass, colThreeClass = "col-xs-4", "col-xs-8", ""
					#         Trace.Write("HtmlstrHtmlstrHtmlstrHtmlstrHtmlstrHtmlstr")    
					#             #         Htmlstr += (
					#             #             '<div class="'
					#             #             + str(colTwoClass)
					#             #             + '"><div class="row vert-align">'
					#             #             + '<div class="pad10 col-xs-11 '
					#             #             + str(colThreeClass)
					#             #             + '">'
					#             #             + str(GetApprover.RECIPIENT_COMMENTS)
					#             #             + '</div><div class="col-xs-1 txtrtpad10">'
					#             #             + str(readonly)
					#             #             + "</div></div></div>"
					#             #         )
					#             #         Htmlstr += "</div>"
					#             # Htmlstr += "</div>"
					# # Htmlstr += "</div>"
				Htmlstr += "</div>"
			else:
				if CurrentTabName == 'Quotes' or CurrentTabName == 'Quote':
					my_approval_queue_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID,OWNER_NAME,QUOTE_STATUS,QTEREV_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id") ,revision_rec_id=  self.quote_revision_record_id))
					
					quote_status = my_approval_queue_obj.QUOTE_STATUS
					if quote_status == 'APPROVED':
						Htmlstr += "<div class='noRecDisp'>This Quote has been self-approved.</div>"
					else:
						Htmlstr += "<div class='noRecDisp'>This quote can be self-approved. Kindly proceed to approve the quote.</div>"
				else:   
					
					Htmlstr += "<div class='noRecDisp'>No Records to Display</div>"
			Trace.Write("Htmlstr"+str(Htmlstr))
			return Htmlstr,data_list
		

		""" except Exception, e:
			self.exceptMessage = (
				"ACSECTACTN : PreviewApprovers : EXCEPTION : UNABLE TO PREVIEW APPROVERS : EXCEPTION E : " + str(e)
			)
			Trace.Write(self.exceptMessage)
			return None """

	# A043S001P01-12838 End
	def getSEGMENT_ID(self):
		"""Get segment id."""
		try:
			sSEGMENT_ID = None
			segmentQuery = Sql.GetFirst(
				"""select PRICEAGREEMENT_ID,AGMREV_ID
					from PASGRV (nolock)
					where PRICEAGREEMENT_REVISION_RECORD_ID = '{}' """.format(
					self.QuoteNumber
				)
			)
			if segmentQuery is not None:
				sSEGMENT_ID = segmentQuery.PRICEAGREEMENT_ID
			return sSEGMENT_ID
		except Exception, e:
			self.exceptMessage = (
				"ACSECTACTN : getSEGMENT_ID : EXCEPTION : UNABLE TO PRICEAGREEMENT_ID : EXCEPTION E : " + str(e)
			)
			Trace.Write(self.exceptMessage)
			return None

	# A043S001P01-12267 start
	# def TrackedFieldValues(self):
	#     """Tracked field values from audit trial table."""
	#     # OBSOLUTED
	#     try:
	#         GetCurrentStrpId = Sql.GetList(
	#             """SELECT ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_ID,OBJECT_NAME,ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL,
	#                 ACAPTF.TRKOBJ_TRACKEDFIELD_RECORD_ID, ACAPTF.TRKOBJECT_NAME,ACAPMA.APPROVAL_RECORD_ID,
	#                 ACAPTX.APRCHN_ID,ACAPTX.APRCHN_RECORD_ID,ACAPTX.APRCHNSTP_ID,ACAPTX.APRCHNSTP_RECORD_ID
	#                 FROM ACAPMA (NOLOCK)
	#                 INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
	#                 INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID
	#                 INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
	#                 INNER JOIN ACAPTF (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID
	#                 WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND APRSTAMAP_APPROVALSTATUS = 'REQUESTED' """.format(
	#                 QuoteNumber=self.QuoteNumber
	#             )
	#         )
	#         for ChainAndStepLoop in GetCurrentStrpId:
	#             getObjSplit = str(ChainAndStepLoop.APPROVAL_ID).split("-")
	#             ObjectName = getObjSplit[0]
	#             TargeobjRelation = Sql.GetFirst(
	#                 """SELECT API_NAME
	#                     FROM SYOBJD (NOLOCK)
	#                     WHERE DATA_TYPE = 'LOOKUP' AND LOOKUP_OBJECT = '{ObjectName}'
	#                     AND OBJECT_NAME = '{ChainObjName}' """.format(
	#                     ObjectName=ObjectName, ChainObjName=str(ChainAndStepLoop.OBJECT_NAME)
	#                 )
	#             )
	#             if str(ObjectName) == "PASGRV":
	#                 SegmentIds = str(ChainAndStepLoop.APRTRXOBJ_RECORD_ID)
	#                 """SegmentIds = str(ChainAndStepLoop.APRTRXOBJ_RECORD_ID).split("-")
	#                 SegId = SegmentIds[0] + "-" + SegmentIds[1]
	#                 RevId = SegmentIds[2] + "-" + SegmentIds[3]"""
	#                 GetRevPrimary = Sql.GetFirst(
	#                     """SELECT PRICEAGREEMENT_REVISION_RECORD_ID
	#                         FROM PASGRV (NOLOCK)
	#                         WHERE AGMREV_ID = '{SegmentIds}' """.format(
	#                         SegmentIds=str(RevId)
	#                     )
	#                 )
	#                 RecordId = str(GetRevPrimary.PRICEAGREEMENT_REVISION_RECORD_ID)
	#             Select_Query = (
	#                 "SELECT CpqTableEntryId FROM "
	#                 + str(ChainAndStepLoop.OBJECT_NAME)
	#                 + " WHERE "
	#                 + str(TargeobjRelation.API_NAME)
	#                 + " = '"
	#                 + str(RecordId)
	#                 + "' "
	#             )
	#             Select_Query_Count = (
	#                 "SELECT count(CpqTableEntryId) AS cnt FROM "
	#                 + str(ChainAndStepLoop.OBJECT_NAME)
	#                 + " WHERE "
	#                 + str(TargeobjRelation.API_NAME)
	#                 + " = '"
	#                 + str(RecordId)
	#                 + "' "
	#             )
	#             GetAllCpqId = Sql.GetList(Select_Query)
	#             GetAllCpqIdCount = Sql.GetList(Select_Query_Count)
	#             ACAPFVLastModify = Sql.GetFirst(
	#                 "SELECT TOP 1000 CpqTableEntryDateModified FROM ACAPFV WHERE APRCHN_RECORD_ID = '"
	#                 + str(ChainAndStepLoop.APRCHN_RECORD_ID)
	#                 + "' AND APRCHNSTP_RECORD_ID = '"
	#                 + str(ChainAndStepLoop.APRCHNSTP_RECORD_ID)
	#                 + "' AND APPROVAL_RECORD_ID = '"
	#                 + str(ChainAndStepLoop.APPROVAL_RECORD_ID)
	#                 + "' ORDER BY CpqTableEntryDateModified DESC"
	#             )
	#             wherecon = ""
	#             if ACAPFVLastModify:
	#                 wherecon = " AND EntryTime >='" + str(ACAPFVLastModify.CpqTableEntryDateModified) + "'  "
	#             CpqTableEntryList = []
	#             for cpqIdLoop in GetAllCpqId:
	#                 CpqTableEntryList.append(str(cpqIdLoop.CpqTableEntryId))
	#             GetTableAndId = Sql.GetList(
	#                 """SELECT EntityId,PreviousValue,NewValue,EntryTime
	#                     from
	#                     CustomTablesActionAuditTrail
	#                     where EntityId like '%"{ObjName}"%'
	#                     AND FieldName = '{FieldLable}'
	#                     AND ActionName <> 'ADD' {wherecon} """.format(
	#                     ObjName=str(ChainAndStepLoop.OBJECT_NAME),
	#                     wherecon=wherecon,
	#                     FieldLable=str(ChainAndStepLoop.TRKOBJ_TRACKEDFIELD_LABEL),
	#                 )
	#             )
	#             if GetTableAndId:
	#                 for getdata in GetTableAndId:
	#                     ksplit = str(getdata.EntityId).split(" ")
	#                     CpQId = str(ksplit[3])
	#                     # Trace.Write(str(CpQId)+" "+str(CpqTableEntryList))
	#                     if CpQId in CpqTableEntryList:
	#                         TrackedValueInsert = """INSERT ACAPFV (APPROVAL_TRACKED_VALUE_RECORD_ID ,APRCHN_ID ,
	#                             APRCHN_RECORD_ID,APRCHNSTP ,APRCHNSTP_RECORD_ID ,APPROVAL_ID ,APPROVAL_RECORD_ID ,
	#                             TRKOBJ_TRACKEDFIELD_LABEL ,TRKOBJ_TRACKEDFIELD_RECORD_ID ,TRKOBJ_TRACKEDFIELD_VALUE ,
	#                             TRKOBJECT_NAME ,ADDUSR_RECORD_ID ,CPQTABLEENTRYADDEDBY ,CPQTABLEENTRYDATEADDED ,
	#                             CpqTableEntryModifiedBy ,CpqTableEntryDateModified)
	#                                 SELECT
	#                                 CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_TRACKED_VALUE_RECORD_ID ,
	#                                 ChainAndStepLoop.APRCHN_ID AS APRCHN_ID ,
	#                                 ChainAndStepLoop.APRCHN_RECORD_ID AS APRCHN_RECORD_ID ,
	#                                 ChainAndStepLoop.APRCHNSTP_ID AS APRCHNSTP ,
	#                                 ChainAndStepLoop.APRCHNSTP_RECORD_ID AS APRCHNSTP_RECORD_ID ,
	#                                 ChainAndStepLoop.APPROVAL_ID AS APPROVAL_ID ,
	#                                 ChainAndStepLoop.APPROVAL_RECORD_ID AS APPROVAL_RECORD_ID ,
	#                                 ChainAndStepLoop.TRKOBJ_TRACKEDFIELD_LABEL AS TRKOBJ_TRACKEDFIELD_LABEL ,
	#                                 ChainAndStepLoop.TRKOBJ_TRACKEDFIELD_RECORD_ID AS TRKOBJ_TRACKEDFIELD_RECORD_ID ,
	#                                 getdata.NewValue AS TRKOBJ_TRACKEDFIELD_VALUE ,
	#                                 ChainAndStepLoop.TRKOBJECT_NAME AS TRKOBJECT_NAME ,
	#                                 '{Get_UserID}' AS ADDUSR_RECORD_ID,
	#                                 '{UserName}' AS CPQTABLEENTRYADDEDBY ,
	#                                 convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED ,
	#                                 '{Get_UserID}' AS CpqTableEntryModifiedBy ,
	#                                 convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified """.format(
	#                             datetime_value=datetime_value, Get_UserID=Get_UserID, UserName=self.UserName
	#                         )
	#                         Trace.Write(TrackedValueInsert)
	#                         a = Sql.RunQuery(TrackedValueInsert)
	#     except Exception, e:
	#         self.exceptMessage = (
	#             "ACSECTACTN : TrackedFieldValues : EXCEPTION : UNABLE TO INSERT TRAKED VALUES : EXCEPTION E : " + str(e)
	#         )
	#         Trace.Write(self.exceptMessage)
	#     return True

	# A043S001P01-12267 End
	def sendmailNotification(self, notifiType, getCpqId=None, stepRecordId=None):
		#try:
		dynamics =""
		bodyname =""
		dearname =""        
		
		if CurrentTabName == 'Quotes':
			quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id = self.quote_revision_record_id))
			quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
			if quote_obj is not None:
				if notifiType == "Request":
					approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA (NOLOCK) INNER JOIN ACAPCH (NOLOCK) ON ACAPMA.APRCHN_ID = ACAPCH.APRCHN_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '{quote_record_id}' AND ACAPCH.APPROVAL_METHOD = 'SERIES STEP APPROVAL'".format(quote_record_id = self.quote_revision_record_id))
					approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
				elif notifiType == "ParallelRequest":
					approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA (NOLOCK) INNER JOIN ACAPCH (NOLOCK) ON ACAPMA.APRCHN_ID = ACAPCH.APRCHN_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '{quote_record_id}' AND ACAPCH.APPROVAL_METHOD = 'PARALLEL STEP APPROVAL'".format(quote_record_id = self.quote_revision_record_id))
					approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID
				else:
					approval_queue_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPMA where APRTRXOBJ_RECORD_ID = '{quote_revision_record_id}'".format(quote_revision_record_id=self.quote_revision_record_id))
					approval_record_id = approval_queue_obj.APPROVAL_RECORD_ID  
		else:
			Quoteid = Sql.GetFirst("Select APRTRXOBJ_RECORD_ID FROM ACAPMA WHERE APPROVAL_RECORD_ID = '"+str(self.QuoteNumber)+"'")
			quote_record_id = Quoteid.APRTRXOBJ_RECORD_ID
			approval_record_id = self.QuoteNumber              
		wherecondition = " "
		if getCpqId is not None:
			ACAPTX_CPQ_ID = str(getCpqId)
		
		actiondict = {
			"Request": "REQUEST_TEMPLATE_RECORD_ID",
			"Recall": "RECALL_TEMPLATE_RECORD_ID",
			"Approve": "APPROVE_TEMPLATE_RECORD_ID",
			"Reject": "REJECT_TEMPLATE_RECORD_ID",
		}
		
		if notifiType != "Approve" and notifiType != "Reject":
			wherecondition = "ACAPTX.APPROVAL_RECORD_ID = '{QuoteNumber}'".format(QuoteNumber=approval_record_id) 
		else:
			wherecondition = "ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '{CPQID}'".format(CPQID=str(ACAPTX_CPQ_ID))

		if notifiType == "Request":
			GetNotificationData = Sql.GetList(
				""" SELECT USERS.EMAIL,USERS.NAME,ACEMTP.SUBJECT,ACEMTP.MESSAGE_BODY,ACEMTP.MESSAGE_BODY_2,
					ACEMTP.MESSAGE_BODY_3,ACEMTP.MESSAGE_BODY_4,ACEMTP.MESSAGE_BODY_5,ACAPMA.APRTRXOBJ_RECORD_ID,
					ACAPMA.APPROVAL_RECORD_ID,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,ACACST.WHERE_CONDITION_01
				from ACAPMA (NOLOCK)
				INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
				AND ACAPMA.APRCHNSTP_RECORD_ID= ACAPTX.APRCHNSTP_RECORD_ID
				INNER JOIN ACEMTP (NOLOCK) ON ACEMTP.EMAIL_TEMPLATE_RECORD_ID = ACAPTX.REQUEST_TEMPLATE_RECORD_ID
				INNER JOIN USERS (NOLOCK) ON ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = USERS.ID
				INNER JOIN ACACST(NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPMA.APRCHNSTP_RECORD_ID
				WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' and APPROVALSTATUS != 'APPROVED' """ .format(
					QuoteNumber=approval_record_id
				)
			)
		if notifiType == "ParallelRequest":
			GetNotificationData = Sql.GetList(
				""" SELECT USERS.EMAIL,USERS.NAME,ACEMTP.SUBJECT,ACEMTP.MESSAGE_BODY,ACEMTP.MESSAGE_BODY_2,
					ACEMTP.MESSAGE_BODY_3,ACEMTP.MESSAGE_BODY_4,ACEMTP.MESSAGE_BODY_5,ACAPMA.APRTRXOBJ_RECORD_ID,
					ACAPMA.APPROVAL_RECORD_ID,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,ACACST.WHERE_CONDITION_01
				from ACAPMA (NOLOCK)
				INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
				INNER JOIN ACEMTP (NOLOCK) ON ACEMTP.EMAIL_TEMPLATE_RECORD_ID = ACAPTX.REQUEST_TEMPLATE_RECORD_ID
				INNER JOIN USERS (NOLOCK) ON ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = USERS.ID
				INNER JOIN ACACST(NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTX.APRCHNSTP_RECORD_ID
				WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' and APPROVALSTATUS != 'APPROVED' """.format(
					QuoteNumber=approval_record_id
				)
			)
		elif notifiType == "Recall":
			Getchintype = Sql.GetFirst(
				"""SELECT APPROVAL_METHOD FROM ACAPCH (NOLOCK) INNER JOIN ACAPMA (NOLOCK)
				ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
				WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' """.format(
					QuoteNumber=approval_record_id
				)
			)
			if str(Getchintype.APPROVAL_METHOD) == "SERIES STEP APPROVAL":
				GetNotificationData = Sql.GetList(
					""" SELECT DISTINCT USERS.EMAIL,USERS.NAME,ACEMTP.SUBJECT,ACEMTP.MESSAGE_BODY,
						ACEMTP.MESSAGE_BODY_2,ACEMTP.MESSAGE_BODY_3,ACEMTP.MESSAGE_BODY_4,
						ACEMTP.MESSAGE_BODY_5,ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_RECORD_ID,
						ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,ACACST.WHERE_CONDITION_01
					from ACAPMA (NOLOCK)
					INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
					INNER JOIN ACACST (NOLOCK) ON ACAPMA.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
					INNER JOIN ACEMTP (NOLOCK) ON ACEMTP.EMAIL_TEMPLATE_RECORD_ID = ACACST.RECALL_TEMPLATE_RECORD_ID
					INNER JOIN USERS (NOLOCK) ON ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = USERS.ID
					WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ARCHIVED <> 'True' """.format(
						QuoteNumber=approval_record_id
					)
				)
			else:
				GetNotificationData = Sql.GetList(
					""" SELECT DISTINCT USERS.EMAIL,USERS.NAME,ACEMTP.SUBJECT,ACEMTP.MESSAGE_BODY,
						ACEMTP.MESSAGE_BODY_2,ACEMTP.MESSAGE_BODY_3,ACEMTP.MESSAGE_BODY_4,
						ACEMTP.MESSAGE_BODY_5,ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_RECORD_ID,
						ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,ACACST.WHERE_CONDITION_01
					from ACAPMA (NOLOCK)
					INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
					AND ACAPMA.APRCHNSTP_RECORD_ID= ACAPTX.APRCHNSTP_RECORD_ID
					INNER JOIN ACACST (NOLOCK) ON ACAPMA.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
					INNER JOIN ACEMTP (NOLOCK) ON ACEMTP.EMAIL_TEMPLATE_RECORD_ID = ACACST.RECALL_TEMPLATE_RECORD_ID
					INNER JOIN USERS (NOLOCK) ON ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = USERS.ID
					WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}'  """.format(
						QuoteNumber=approval_record_id
					)
				)

		elif notifiType == "Approve" or notifiType == "Reject":
			GetNotificationData = Sql.GetList(
				""" SELECT ACAPTX.APPROVAL_RECIPIENT_RECORD_ID,USERS.EMAIL,USERS.NAME,ACEMTP.SUBJECT,ACEMTP.MESSAGE_BODY,
					ACEMTP.MESSAGE_BODY_2,ACEMTP.MESSAGE_BODY_3,ACEMTP.MESSAGE_BODY_4,
					ACEMTP.MESSAGE_BODY_5,ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_RECORD_ID,ACACST.WHERE_CONDITION_01
				from ACAPMA (NOLOCK)
				INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
				INNER JOIN ACEMTP (NOLOCK) ON ACEMTP.EMAIL_TEMPLATE_RECORD_ID = ACAPTX.{templaterecordId}
				INNER JOIN USERS (NOLOCK) ON ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = USERS.ID
				INNER JOIN ACACST(NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPMA.APRCHNSTP_RECORD_ID
				WHERE ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '{userid}' """.format(
					userid=self.UserId,
					QuoteNumber=approval_record_id,
					CPQID=str(ACAPTX_CPQ_ID),
					templaterecordId=str(actiondict.get(notifiType)),
				)
			)
		elif notifiType == "Notification":
			GETTEMPRECID =  Sql.GetFirst("Select EMAIL_TEMPLATE_RECORD_ID from ACEMTP (NOLOCK) WHERE EMAILTEMPLATE_ID ='Notification'")
			#templaterecordId = "FC95AE41-4045-4799-9CD4-17DEB1B3B904"
			GetNotificationData = Sql.GetList(
				"""select DISTINCT 	ACAPMA.APRCHN_ID,ACACSA.USER_RECORD_ID ,USERS.EMAIL,USERS.NAME,ACEMTP.SUBJECT,ACEMTP.MESSAGE_BODY,
					ACEMTP.MESSAGE_BODY_2,ACEMTP.MESSAGE_BODY_3,ACEMTP.MESSAGE_BODY_4,
					ACEMTP.MESSAGE_BODY_5,ACAPMA.APRTRXOBJ_RECORD_ID,ACAPMA.APPROVAL_RECORD_ID,ACACST.WHERE_CONDITION_01 FROM ACAPMA 
					INNER JOIN ACACSA ON ACACSA.APRCHN_ID = ACAPMA.APRCHN_ID AND ACACSA.NOTIFICATION_ONLY = 'True'
					INNER JOIN USERS ON USERS.ID = ACACSA.USER_RECORD_ID   
					JOIN ACEMTP ON EMAIL_TEMPLATE_RECORD_ID = '{tempid}'
					INNER JOIN ACACST(NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPMA.APRCHNSTP_RECORD_ID
					WHERE ACAPMA.APRTRXOBJ_RECORD_ID = '{quote_record_id}' """.format(tempid =str(GETTEMPRECID.EMAIL_TEMPLATE_RECORD_ID),quote_record_id = quote_record_id))
		
		for getnotify in GetNotificationData:
			bodystr = ""
			mailbody = (
				str(getnotify.MESSAGE_BODY)
				+ ""
				+ str(getnotify.MESSAGE_BODY_2)
				+ ""
				+ str(getnotify.MESSAGE_BODY_3)
				+ ""
				+ str(getnotify.MESSAGE_BODY_4)
				+ ""
				+ str(getnotify.MESSAGE_BODY_5)
			)
			bodywithformatsplit = str(mailbody).split("</style>")
			found = re.findall("{(.+?)}", str(bodywithformatsplit[1]))
			final_new_menu = list(dict.fromkeys(found))
			

			column_name = str(final_new_menu).replace("[", "").replace("]", "").replace("'", "")
			
			GetApprovalprocessobj = Sql.GetFirst(
			"""SELECT ACAPCH.APROBJ_LABEL,ACAPCH.APRCHN_DESCRIPTION,ACACST.TSTOBJ_LABEL,ACAPTX.APPROVAL_RECORD_ID,
				ACAPTX.APPROVAL_TRANSACTION_RECORD_ID
				FROM ACAPTX (NOLOCK) INNER JOIN ACAPCH (NOLOCK)
					ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPTX.APRCHN_RECORD_ID INNER JOIN ACACST (NOLOCK)
				ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACST.APRCHN_RECORD_ID
				AND ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
				WHERE {wherecondition} """.format(
				wherecondition=str(wherecondition)
			)
			)
			objectdic = {
				#"approvalObj": str(Quote)
				"approvalObj": str(GetApprovalprocessobj.APROBJ_LABEL),
				"testedObj": str(GetApprovalprocessobj.TSTOBJ_LABEL),
			}
			objlableandobj = {}
			getobjName = {}
			for objloop in objectdic.values():
				getobjquery = Sql.GetFirst(
					"SELECT OBJECT_NAME,RECORD_NAME FROM SYOBJH (NOLOCK) WHERE LABEL = '{}'".format(str(objloop))
				)
				getobjName[str(getobjquery.OBJECT_NAME)] = str(getobjquery.RECORD_NAME)
				objlableandobj[str(objloop)] = str(getobjquery.OBJECT_NAME)
			GetRelationshipt = Sql.GetFirst(
				"""SELECT API_NAME FROM SYOBJD (NOLOCK) 
				WHERE OBJECT_NAME = '{testedObj}' AND LOOKUP_OBJECT = '{approvalObj}' """.format(
					approvalObj=str(objlableandobj.get(str(objectdic.get("approvalObj")))),
					testedObj=str(objlableandobj.get(str(objectdic.get("testedObj")))),
				)
			)
			iskey = Sql.GetFirst(
				"SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME = '{}' AND IS_KEY = 'TRUE' ".format(
					str(objlableandobj.get(objectdic.get("approvalObj")))
				)
			)
			
			
			

			Getplaceholdervalue = Sql.GetFirst(
				"""SELECT {column_name} FROM ACAPMA (NOLOCK) INNER JOIN ACAPTX (NOLOCK)
				ON ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
				INNER JOIN SAOPQT(NOLOCK) ON ACAPMA.APRTRXOBJ_ID = SAOPQT.QUOTE_ID
				INNER JOIN ACAPCH (NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
				INNER JOIN {approvalObj} (NOLOCK) ON ACAPMA.APRTRXOBJ_RECORD_ID = {approvalObj}.{iskeyName}
				LEFT JOIN SAQTSV(NOLOCK) ON ACAPMA.APRTRXOBJ_RECORD_ID = SAQTSV.QTEREV_RECORD_ID 
				INNER JOIN SAQTMT (NOLOCK) ON ACAPMA.APRTRXOBJ_RECORD_ID = SAQTMT.QTEREV_RECORD_ID		
				LEFT JOIN SAQRIT(NOLOCK) ON ACAPMA.APRTRXOBJ_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
				INNER JOIN SAQDLT(NOLOCK) ON ACAPMA.APRTRXOBJ_RECORD_ID = SAQDLT.QTEREV_RECORD_ID
				WHERE {wherecondition} """.format(
					approvalObj=str(objlableandobj.get(objectdic.get("approvalObj"))),
					testedObj=str(objlableandobj.get(objectdic.get("testedObj"))),
					iskeyName=str(iskey.API_NAME),
					approvalObjprimary=str(getobjName.get(objlableandobj.get(objectdic.get("approvalObj")))),
					column_name=str(column_name),
					wherecondition=str(wherecondition),
				)
			)
			getcurrency = Sql.GetFirst("SELECT GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
			getcurrencysymbol = Sql.GetFirst("""SELECT DISPLAY_DECIMAL_PLACES FROM PRCURR (NOLOCK) WHERE CURRENCY_RECORD_ID = '{currencysymbol}' """.format(currencysymbol = getcurrency.GLOBAL_CURRENCY_RECORD_ID))
			for eachkey in final_new_menu:
				values = ""
				eachsplit = eachkey.split(".")
				if str(eachsplit[1]) == "OWNER_NAME":
					getaccountid = Sql.GetFirst("SELECT ACCOUNT_ID,ACCOUNT_NAME FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getaccountid:
						acct_id=str(getaccountid.ACCOUNT_ID)
						acct_name=str(getaccountid.ACCOUNT_NAME)
						values =str(acct_name)+"-"+str(acct_id)
				elif str(eachsplit[1]) == "MEMBER_ID":
					getcontractmanager = Sql.GetFirst("SELECT MEMBER_NAME FROM SAQDLT (NOLOCK) WHERE C4C_PARTNERFUNCTION_ID = 'Sales Employee' and QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getcontractmanager:
						values =str(getcontractmanager.MEMBER_NAME)
				elif str(eachsplit[1]) == "MEMBER_NAME":
					getcontractrole = Sql.GetFirst("SELECT MEMBER_NAME FROM SAQDLT (NOLOCK) WHERE C4C_PARTNERFUNCTION_ID = 'BD' and QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getcontractrole:
						values =str(getcontractrole.MEMBER_NAME)
				elif str(eachsplit[1]) == "CONTRACT_VALID_FROM":
					GETDATE = Sql.GetFirst("SELECT CONVERT(VARCHAR(100),CONTRACT_VALID_FROM, 101) as A FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"'  ")
					if GETDATE:
						values=str(GETDATE.A)
				elif str(eachsplit[1]) == "CONTRACT_VALID_TO" :
					GETDATES = Sql.GetFirst("SELECT CONVERT(VARCHAR(100),CONTRACT_VALID_TO, 101) as B FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"'  ")
					if GETDATES:
						values=str(GETDATES.B)
				elif str(eachsplit[1]) == "QUANTITY":
					GETFPM = Sql.GetFirst("SELECT SUM(QUANTITY) AS QUANTITY FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if GETFPM:
						values=str(GETFPM.QUANTITY)
				elif str(eachsplit[1]) == "NET_PRICE_INGL_CURR":
					getnetprice = Sql.GetFirst("SELECT NET_PRICE_INGL_CURR FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getnetprice.NET_PRICE_INGL_CURR:
						formatting_string = "{0:." + str(getcurrencysymbol.DISPLAY_DECIMAL_PLACES) + "f}"
						value = formatting_string.format(float(getnetprice.NET_PRICE_INGL_CURR))
						values=str(value)+' '+str(getcurrency.GLOBAL_CURRENCY)
				elif str(eachsplit[1]) == "NET_PRICE_INGL_CURR":
					getnetprice = Sql.GetFirst("SELECT NET_PRICE_INGL_CURR FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getnetprice.NET_PRICE_INGL_CURR:
						formatting_string = "{0:." + str(getcurrencysymbol.DISPLAY_DECIMAL_PLACES) + "f}"
						value = formatting_string.format(float(getnetprice.NET_PRICE_INGL_CURR))
						values=str(value)+' '+str(getcurrency.GLOBAL_CURRENCY)
				elif str(eachsplit[1]) == "CREDIT_INGL_CURR":
					getnetprice = Sql.GetFirst("SELECT CREDIT_INGL_CURR FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getnetprice.CREDIT_INGL_CURR:
						formatting_string = "{0:." + str(getcurrencysymbol.DISPLAY_DECIMAL_PLACES) + "f}"
						value = formatting_string.format(float(getnetprice.CREDIT_INGL_CURR))
						values=str(value)+' '+str(getcurrency.GLOBAL_CURRENCY)
				elif str(eachsplit[1]) == "TAX_AMOUNT_INGL_CURR":
					getnetprice = Sql.GetFirst("SELECT TAX_AMOUNT_INGL_CURR FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getnetprice.TAX_AMOUNT_INGL_CURR:
						formatting_string = "{0:." + str(getcurrencysymbol.DISPLAY_DECIMAL_PLACES) + "f}"
						value = formatting_string.format(float(getnetprice.TAX_AMOUNT_INGL_CURR))
						values=str(value)+' '+str(getcurrency.GLOBAL_CURRENCY)
				elif str(eachsplit[1]) == "NET_VALUE_INGL_CURR":
					getnetprice = Sql.GetFirst("SELECT NET_VALUE_INGL_CURR FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
					if getnetprice.NET_VALUE_INGL_CURR:
						formatting_string = "{0:." + str(getcurrencysymbol.DISPLAY_DECIMAL_PLACES) + "f}"
						value = formatting_string.format(float(getnetprice.NET_VALUE_INGL_CURR))
						values=str(value)+' '+str(getcurrency.GLOBAL_CURRENCY)
				else:
					if Getplaceholdervalue:
						values =str(eval("Getplaceholdervalue." + str(eachsplit[1])))
				bodywithformatsplit[1] = bodywithformatsplit[1].replace("{" + eachkey + "}", values)
			
			#emailId = str(getnotify.EMAIL)
			subject = str(GetApprovalprocessobj.APROBJ_LABEL) + " " + str(getnotify.SUBJECT) + " - " + str(GetApprovalprocessobj.APRCHN_DESCRIPTION)
			#bodycontent = re.findall('<td class="productservice">(.+?)</td>', bodywithformatsplit[1])
			servicestr = ""
			getservid = Sql.GetList("SELECT SAQTSV.SERVICE_ID,SAQTSV.SERVICE_DESCRIPTION,SAQTSV.PRODUCT_TYPE,SAQTRV.DOCTYP_ID,SAQTRV.CONTRACT_VALID_FROM,SAQTRV.CONTRACT_VALID_TO FROM SAQTSV (NOLOCK) INNER JOIN SAQTRV ON SAQTSV.QUOTE_RECORD_ID =SAQTRV.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID WHERE SAQTRV.QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND SAQTRV.QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SAQTRV.ACTIVE ='1'")
			if getservid:
				for trloop in getservid:
					validfrom = str(trloop.CONTRACT_VALID_FROM).split(' ')[0]
					validto = str(trloop.CONTRACT_VALID_TO).split(' ')[0]
					servicestr += "<tr class='borders'>"
					servicestr += '<td class="no-border bg-white">' + str(trloop.SERVICE_ID)+ "</td>"
					servicestr += '<td class="no-border bg-white" colspan="2">'+ str(trloop.SERVICE_DESCRIPTION)+"</td>"
					servicestr += '<td class="no-border bg-white" colspan="2">'+ str(trloop.PRODUCT_TYPE)+"</td>"
					servicestr += '<td class="no-border bg-white">'+ str(trloop.DOCTYP_ID)+"</td>"
					servicestr += '<td class="no-border bg-white" colspan="2">'+ str(validfrom)+"</td>"
					servicestr += '<td class="no-border bg-white">'+ str(validto)+"</td>"
					servicestr += "</tr>"
			#bodywithformatsplit = bodywithformatsplit.replace("<tr class ='productservice'></tr>",servicestr)
			bodywithformatsplit[1]=re.sub(r'<tr class="productservice">\s*</tr>',servicestr,bodywithformatsplit[1])
			Trace.Write("mail body 22222222" + str(servicestr))
			Trace.Write("mail body construct" + str(bodywithformatsplit))
			Trace.Write("mail body construct2" + bodywithformatsplit[1])
			C4QUOTE =Sql.GetFirst("SELECT C4C_QUOTE_ID,ADDUSR_RECORD_ID,QTEREV_RECORD_ID FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
			SUBMITTERNAME = Sql.GetFirst("SELECT NAME,EMAIL FROM USERS(NOLOCK) WHERE ID = '"+str(C4QUOTE.ADDUSR_RECORD_ID)+"' ")
			
			if notifiType == "Approve":
				dearname = SUBMITTERNAME.NAME
				dynamics =" approved your request for approval on the"
				bodyname = getnotify.NAME
				emailId = str(SUBMITTERNAME.EMAIL)
			elif notifiType == "Reject":
				dearname = SUBMITTERNAME.NAME
				dynamics =" rejected your request for approval on the"
				bodyname = getnotify.NAME
				emailId = str(SUBMITTERNAME.EMAIL)
			else:
				dearname = getnotify.NAME
				bodyname = SUBMITTERNAME.NAME
				dynamics=" requested your approval for the"
				emailId = str(getnotify.EMAIL)
			splitformailbodyappend = str(bodywithformatsplit[1]).split("</tbody>")
			if mailbody.startswith("<!DOCTYPE html>", 0) == True:
				Trace.Write("ifmessage body")
				mailbdyready = (
					str(bodywithformatsplit[0])
					+ "</style>"
					+ str(splitformailbodyappend[0])
					+ " "
					+ str(bodystr)
					+ "</tbody></table></body></html>"
				)
			else:
				
				mailbdyready = (
					"<!DOCTYPE html><html>Dear "+str(dearname)+" <br><p>"+str(bodyname)+" has"+str(dynamics)+" following quote: </p> <head>"
					+ str(bodywithformatsplit[0])
					+ "</style></head> <body>"
					+ str(splitformailbodyappend[0])
					+ " "
					+ str(bodystr) 
					+ "<tr><td colspan='12'>By Approving the Quote, you are agreeing to the terms and pricing contained within this revision of the Quote. <br> Any subsequent revisions of the quote may require additional approvals. The content of this message is Applied Material Confidential. If you are not the intended recipient and have received this message in error, any use or distribution is prohibited. Please notify us immediately by replying to this email and delete this message from your computer system.</td></tr></tbody></table></body></html>"
				)
			# ApproveLink = """https://sandbox.webcomcpq.com/sso/login.aspx?u=iSbvvR727kdpKBzPhaQlCQG2R2R7BAG7zrBeA09ehWU6IRL8YYeU5IF1kx6EqoTc&d=octanner_dev&ACTION=APPROVEBTN&ApproveDesc=Approved&CurrentTransId={transactionid}&approvalrecid={approvalid}&PriceagreementRevId={priceagreementrevid}""".format(
			#     transactionid=str(getnotify.APPROVAL_TRANSACTION_RECORD_ID),
			#     approvalid=str(getnotify.APPROVAL_RECORD_ID),
			#     priceagreementrevid=str(getnotify.APRTRXOBJ_RECORD_ID),
			# )
			# RejectLink = """https://sandbox.webcomcpq.com/sso/login.aspx?u=iSbvvR727kdpKBzPhaQlCQG2R2R7BAG7zrBeA09ehWU6IRL8YYeU5IF1kx6EqoTc&d=octanner_dev&ACTION=REJECTBTN&ApproveDesc=Rejected&CurrentTransId={transactionid}&approvalrecid={approvalid}&PriceagreementRevId={priceagreementrevid}""".format(
			#     transactionid=str(getnotify.APPROVAL_TRANSACTION_RECORD_ID),
			#     approvalid=str(getnotify.APPROVAL_RECORD_ID),
			#     priceagreementrevid=str(getnotify.APRTRXOBJ_RECORD_ID),
			# )
			#ViewLink = """https://sandbox.webcomcpq.com/sso/login.aspx?u=iSbvvR727kdpKBzPhaQlCQG2R2R7BAG7zrBeA09ehWU6IRL8YYeU5IF1kx6EqoTc&d=octanner_dev&#ACTION=VIEWBTN&CurrentTransId={transactionid}&approvalrecid={approvalid}&PriceagreementRevId={priceagreementrevid}""".format(
			#    transactionid=str(getnotify.APPROVAL_TRANSACTION_RECORD_ID),
			#    approvalid=str(getnotify.APPROVAL_RECORD_ID),
			#    priceagreementrevid=str(getnotify.APRTRXOBJ_RECORD_ID),
			#)
			ApproveLink = """https://my345810-SSO.crm.ondemand.com//sap/public/byd/runtime?bo_ns=http://sap.com/thingTypes&bo=COD_GENERIC&node=Root&operation=OnExtInspect&param.InternalID={c4cid}&param.Type=COD_QUOTE_TT&sapbyd-agent=TAB&OBNRedirect=X""".format(c4cid=str(C4QUOTE.C4C_QUOTE_ID))
			RejectLink = """https://my345810-SSO.crm.ondemand.com//sap/public/byd/runtime?bo_ns=http://sap.com/thingTypes&bo=COD_GENERIC&node=Root&operation=OnExtInspect&param.InternalID={c4cid}&param.Type=COD_QUOTE_TT&sapbyd-agent=TAB&OBNRedirect=X""".format(c4cid=str(C4QUOTE.C4C_QUOTE_ID))
			ViewLink ="""https://my345810-SSO.crm.ondemand.com//sap/public/byd/runtime?bo_ns=http://sap.com/thingTypes&bo=COD_GENERIC&node=Root&operation=OnExtInspect&param.InternalID={c4cid}&param.Type=COD_QUOTE_TT&sapbyd-agent=TAB&OBNRedirect=X""".format(c4cid=str(C4QUOTE.C4C_QUOTE_ID))
			mailbdyready = mailbdyready.replace("ApproveLink", ApproveLink)
			mailbdyready = mailbdyready.replace("RejectLink", RejectLink)
			mailbdyready = mailbdyready.replace("ViewLink", ViewLink)
			# Trace.Write("mail body " + str(mailbdyready))
			# Trace.Write("mail email " + str(emailId))
			# Trace.Write("mail subject " + str(subject))
			Getresponse = self.mailtrigger(str(subject), str(mailbdyready), str(emailId))
		#except Exception, e:
		#    self.exceptMessage = (
		#        "ACSECTACTN : sendmailNotification : EXCEPTION : UNABLE TO SEND EMAIL : EXCEPTION E : " + str(e)
		#    )
		#    Trace.Write(self.exceptMessage)
		return True
	
	def cbcmailtrigger(self):
		revision_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QUOTE_REVISION_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
		if revision_status.REVISION_STATUS=="APPROVED":
			try:
				LOGIN_CRE = Sql.GetFirst("SELECT USER_NAME,PASSWORD FROM SYCONF (NOLOCK) where Domain ='SUPPORT_MAIL'")
				MANAGER_DETAILS=Sql.GetFirst("SELECT EMAIL,MEMBER_NAME,QUOTE_ID FROM SAQDLT WHERE QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' ")
				mailClient = SmtpClient()
				mailClient.Host = "smtp.gmail.com"
				mailClient.Port = 587
				mailClient.EnableSsl = "true"
				mailCred = NetworkCredential()
				mailCred.UserName = str(LOGIN_CRE.USER_NAME)
				mailCred.Password = str(LOGIN_CRE.PASSWORD)
				mailClient.Credentials = mailCred
				toEmail = MailAddress(str(MANAGER_DETAILS.EMAIL))
				fromEmail = MailAddress(str(LOGIN_CRE.USER_NAME))
				msg = MailMessage(fromEmail, toEmail)
				msg.Subject = "Clean Booking Checklist Completion"
				msg.IsBodyHtml = True
				msg.Body = "<!DOCTYPE HTML><html><p>Hi "+str(MANAGER_DETAILS.MEMBER_NAME)+",</p><p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Kindly complete the Clean Booking Checklist of the Quote <b>"+str(MANAGER_DETAILS.QUOTE_ID)+"</b> in order to proceed with the Contract Creation in CRM</p></html>"
				mailClient.Send(msg)
			except Exception as e:
				self.exceptMessage = "ACSECTACTN : mailtrigger : EXCEPTION : UNABLE TO TRIGGER E-EMAIL : EXCEPTION E : " + str(e)
				Trace.Write(self.exceptMessage)
		else:
			Trace.Write('CBC MAIL TRIGGER : QUOTE NOT APPROVED YET')
		return True

	def mailtrigger(self, Subject, mailBody, recepient):
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
			copyEmail1 = MailAddress("surendar.murugachandran@bostonharborconsulting.com")
			msg.CC.Add(copyEmail1)
			#copyEmail2 = MailAddress("wasim.abdul@bostonharborconsulting.com")
			#msg.CC.Add(copyEmail2)
			copyEmail2 = MailAddress("wasim.abdul@bostonharborconsulting.com")
			msg.CC.Add(copyEmail2)
			#copyEmail5 = MailAddress("namrata.sivakumar@bostonharborconsulting.com")
			#msg.CC.Add(copyEmail5)    
			mailClient.Send(msg)
		except Exception, e:
			self.exceptMessage = "ACSECTACTN : mailtrigger : EXCEPTION : UNABLE TO TRIGGER E-EMAIL : EXCEPTION E : " + str(e)
			Trace.Write(self.exceptMessage)
		return True

	def messagebodyvalue(self, objhRecordID):
		Getbodylist = []
		try:
			GetList = Sql.GetList(
				"""SELECT SYOBJD.FIELD_LABEL
					FROM SYOBJH(NOLOCK)
					INNER JOIN SYOBJD(NOLOCK) ON SYOBJD.OBJECT_NAME = SYOBJH.OBJECT_NAME
					WHERE SYOBJH.RECORD_ID = '{objhRecordID}' """.format(
					objhRecordID=str(objhRecordID)
				)
			)
			if GetList:
				for eachval in GetList:
					Getbodylist.append(eachval.FIELD_LABEL)
		except Exception, e:
			self.exceptMessage = (
				"ACSECTACTN : messagebodyvalue : EXCEPTION : ERROR IN MESSAGE BODY GETTING : EXCEPTION E : " + str(e)
			)
			Trace.Write(self.exceptMessage)
		return Getbodylist

	def SaveApproversComments(self, RecipientComment):
		try:
			UpdateApproverComment = """UPDATE ACAPTX SET RECIPIENT_COMMENTS = '{RecipientComment}',
					CpqTableEntryModifiedBy = '{UserId}',
					CpqTableEntryDateModified = '{datetime_value}'
					WHERE APPROVAL_TRANSACTION_RECORD_ID = '{approvalId}' """.format(
				RecipientComment=RecipientComment,
				approvalId=(self.QuoteNumber),
				datetime_value=self.datetime_value,
				UserId=self.UserId,
			)
			a = Sql.RunQuery(UpdateApproverComment)
		except Exception, e:
			self.exceptMessage = (
				"ACSECTACTN : SaveApproversComments : EXCEPTION : ERROR IN RECIPIENT COMMENTS : EXCEPTION E : " + str(e)
			)
			Trace.Write(self.exceptMessage)
		return True

	def PreviewApproversComments(self, ACTION, TransactionId):
		Htmlstr = ""

		if CurrentTabName == 'Quotes':
			quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id = self.quote_revision_record_id ))
			quote_record_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
			revision_record_id = Product.GetGlobal("quote_revision_record_id")
			if quote_obj is not None:
				##multi chain approval
				if str(TransactionId) != 'None': 
					approval_queue_obj = Sql.GetFirst("select TOP 1 ACAPMA.APPROVAL_RECORD_ID,CUR_APRCHNSTP from ACAPMA (NOLOCK) JOIN ACAPTX (NOLOCK) on ACAPTX.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID and ACAPMA.APRCHN_RECORD_ID = ACAPTX.APRCHN_RECORD_ID where APRTRXOBJ_RECORD_ID = '{quote_record_id}' AND ACAPTX.APPROVAL_TRANSACTION_RECORD_ID ='{TransId}' ORDER BY ACAPMA.CpqTableEntryId DESC".format(quote_record_id = revision_record_id,TransId = str(TransactionId)))
				##multi chain approval
				else:
					approval_queue_obj = Sql.GetFirst("select TOP 1 APPROVAL_RECORD_ID,CUR_APRCHNSTP from ACAPMA (NOLOCK) where APRTRXOBJ_RECORD_ID = '{quote_record_id}' ORDER BY CpqTableEntryId DESC".format(quote_record_id = revision_record_id))
				self.QuoteNumber = approval_queue_obj.APPROVAL_RECORD_ID
				Trace.Write("@3134---Approval Record Id--"+str(self.QuoteNumber))
		else:
			try:
				TransactionId = self.QuoteNumber
				transaction_obj = Sql.GetFirst("select APPROVAL_RECORD_ID from ACAPTX where APPROVAL_TRANSACTION_RECORD_ID = '{TransactionId}'".format(TransactionId = TransactionId))
				self.QuoteNumber = transaction_obj.APPROVAL_RECORD_ID
			except:
				Trace.Write("EXCEPT: TransactionId and QuoteNumber")
				TransactionId = ''
				self.QuoteNumber = ''
		   #current_chain_step = approval_queue_obj.CUR_APRCHNSTP
		try:
			Trace.Write("@3146---Approval Trans Record Id--"+str(TransactionId))
			TreeParam = AllParams.get("TreeParam")
			RecipientCommentInfo = "RECIPIENT COMMENT"
			ButtonNeed = "False"
			ApprTrxRecId = "ApproveReject"
			SaveApproverComment = RecipientComment = BtnName = readonly = FromHistory = ""
			if str(TreeParam) == "Approvals":
				FromHistory = "True"
				if TransactionId is None:
					TransactionId = Product.GetGlobal("CurrentApprovalTransaction")
				ApprTrxRecIdQry = Sql.GetFirst(
					"""select ACAPTX.APPROVAL_TRANSACTION_RECORD_ID
						from ACAPMA (nolock)
						inner join ACAPTX (nolock) on ACAPMA.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID
						where APPROVAL_RECIPIENT_RECORD_ID = '{UserId}' and APPROVAL_TRANSACTION_RECORD_ID = '{TransactionId}'
						and ACAPMA.APPROVAL_RECORD_ID = '{QuoteNumber}' AND ARCHIVED = 0""".format(
						QuoteNumber=self.QuoteNumber, UserId=self.UserId,TransactionId=TransactionId
					)
				)
				if ApprTrxRecIdQry:
					ApprTrxRecId = str(ApprTrxRecIdQry.APPROVAL_TRANSACTION_RECORD_ID)
					
					RecipientCommentQuery = Sql.GetFirst(
						"""select RECIPIENT_COMMENTS
							from ACAPTX (nolock)
							where APPROVAL_TRANSACTION_RECORD_ID = '{QuoteNumber}' AND ARCHIVED = 0""".format(
							QuoteNumber=ApprTrxRecId
						)
					)
					if RecipientCommentQuery:
						RecipientComment = str(RecipientCommentQuery.RECIPIENT_COMMENTS)

			if str(ACTION) == "VIEW_COMMENT":
				readonly = "readonly"
			elif str(ACTION) == "EDIT_COMMENT":
				SaveApproverComment = "SaveApproverComment('" + str(self.QuoteNumber) + "')"
				ButtonNeed = "True"
				BtnName = "Save"
			elif str(ACTION) == "SUBMIT_COMMENT":
				SaveApproverComment = "submitfor_approval()"
				RecipientCommentInfo = "REQUESTOR COMMENTS"
				ButtonNeed = "True"
				BtnName = "Submit"
			elif str(ACTION) == "APPROVE_COMMENT":
				SaveApproverComment = "approve_segrev(this, '" + str(FromHistory) + "')"
				RecipientCommentInfo = "RECIPIENT COMMENTS"
				ButtonNeed = "True"
				BtnName = "Approve"
			elif str(ACTION) == "REJECT_COMMENT":
				SaveApproverComment = "reject_segrev(this, '" + str(FromHistory) + "')"
				RecipientCommentInfo = "RECIPIENT COMMENTS"
				ButtonNeed = "True"
				BtnName = "Reject"
			Htmlstr += self.DynamicTextArea(
				RecipientCommentInfo,
				ACTION,
				readonly,
				RecipientComment,
				SaveApproverComment,
				ButtonNeed,
				BtnName,
				ApprTrxRecId,
			)
			Trace.Write("HTML STR---"+str(Htmlstr))
		except Exception, e:
			self.exceptMessage = (
				"ACSECTACTN : PreviewApproversComments : EXCEPTION : ERROR IN APPROVAL COMMENT : EXCEPTION E : " + str(e)
			)
			Trace.Write(self.exceptMessage)
		
		return Htmlstr
	def approvalstatusbar(self,QuoteNumber):
		try:  
			##Showing approve/reject in list grid starts
			
			Trace.Write("QuoteNumber"+str(QuoteNumber)+str(grid_flag))
			if grid_flag == 'True':
				
				get_quote_id = Sql.GetFirst("SELECT ACAPMA.APRTRXOBJ_RECORD_ID FROM ACAPMA (NOLOCK) INNER JOIN ACAPTX (NOLOCK) ON ACAPTX.APPROVAL_RECORD_ID = ACAPMA.APPROVAL_RECORD_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"+str(QuoteNumber)+"' ")
				QuoteNumber = get_quote_id.APRTRXOBJ_RECORD_ID
			##Showing approve/reject in list grid ends
			
			GETstatus=Sql.GetFirst("Select QUOTE_STATUS FROM SAQTMT(NOLOCK) WHERE  MASTER_TABLE_QUOTE_RECORD_ID = '"+str(QuoteNumber)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id) + "'")
			value = str(GETstatus.QUOTE_STATUS)             
			if value =="IN-PROGRESS":
				a=Sql.GetFirst("Select QUOTE_STATUS FROM SAQTMT(NOLOCK) INNER JOIN ACAPMA (NOLOCK) ON ACAPMA.APRTRXOBJ_RECORD_ID = SAQTMT.QTEREV_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '"+str(QuoteNumber)+"' AND SAQTMT.QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
				if a:
					value = "SUBMIT FOR APPROVAL"
				else:
					value = "APPROVALS"
			elif value =="BOOKING SUBMITTED" or value == "CONVERTED TO CONTRACT":
				value = "APPROVED"
			Trace.Write("VALUE---"+str(value))
			return value
		except Exception, e:
			
			self.exceptMessage = (
				"ACSECTACTN : messagebodyvalue : EXCEPTION : ERROR IN approver Quote status bar : EXCEPTION E : " + str(e)
			)
		return ""
	def DynamicTextArea(
		self,
		RecipientCommentInfo,
		ACTION,
		readonly,
		RecipientComment,
		SaveApproverComment,
		ButtonNeed,
		BtnName,
		ApprTrxRecId,
	):
		
		Htmlstr = ""
		try:
			MaxImage = self.ImagePath + "Minimize.svg"
			Htmlstr += """<div class="modulesecbnr brdr marbot0">
					<span id="relatedDelete">COMMENTS</span>
					<button type="button" class="close" data-dismiss="modal">X</button>
					<div class="fullviewdiv flt_rt" style="display: block;">
					<a href="#" class="Clkfull_view"><img class="height18" src="{MaxImage}"></a>
					</div>
				</div>
				<div class="pad10" id="{ACTION}">
					<div id="container" class="g4 pad-10 except_sec">
					<table class="width100" id="bulk_edit">
						<tbody><tr class="fieldRow">
						<td class="preapp_widpostxt" class="labelCol">{RecipientCommentInfo}</td>
						<td lass="dataCol hgt60">
							<div id="massEditFieldDiv" class="inlineEditRequiredDiv removeHorLine ">
							<textarea id="RecipientComment" class="txtArea" {readonly}>{RecipientComment}</textarea>
							</div>
						</td>
						</tr>
					</tbody>
					</table>
					</div>
				</div>""".format(
				RecipientCommentInfo=RecipientCommentInfo,
				ACTION=ACTION,
				readonly=readonly,
				RecipientComment=RecipientComment,
				MaxImage=MaxImage,
			)
			if str(ButtonNeed) == "True":                
				Htmlstr += """<div class="modal-footer">
					<button type="button" id="{ApprTrxRecId}" onclick="{Savefun}" class="flt_rt;" data-dismiss="modal">
					{BtnName}</button>
					<button type="button" class="flt_rt mar_rt6" data-dismiss="modal">Cancel</button>
				</div>""".format(
					Savefun=SaveApproverComment, BtnName=BtnName, ApprTrxRecId=ApprTrxRecId
				)
		except Exception, e:
			self.exceptMessage = (
				"ACSECTACTN : DynamicTextArea : EXCEPTION : ERROR IN DYNAMIC TEXTAREA : EXCEPTION E : " + str(e)
			)
			Trace.Write(self.exceptMessage)
		return Htmlstr

# Getting Param
ACTION = Param.ACTION

try:
	QuoteNumber = Param.QuoteNumber
except:
	QuoteNumber = ""   
if QuoteNumber:
	QuoteNumber = QuoteNumber
else:
	QuoteNumber = ""
TreeParam = Product.GetGlobal("TreeParam")

##Showing approve/reject in list grid starts
try:
	grid_flag = Param.grid_flag
except:
	grid_flag = ""
#Trace.Write("grid_flag"+str(grid_flag))
##Showing approve/reject in list grid ends
Trace.Write("ACTION--->"+str(ACTION))
"""Object Initialization by Factory Method."""
try:
	Trace.Write("QuoteNumber_check "+str(QuoteNumber))
	objDef = eval(violationruleInsert.Factory(ACTION))(QuoteNumber=QuoteNumber)
except Exception, e:
	if ACTION in ["APPROVEBTN", "REJECTBTN","STATUS"]:
		objDef = approvalCenter(QuoteNumber=QuoteNumber)
	else:
		Trace.Write("Class reference is not created" + str(e))
		objDef = ''
if ACTION in ["APPROVE", "REJECT"]:
	AllParams = eval(Param.AllParams)
	ApproveDesc = Param.ApproveDesc
	CurrentTransId = Param.CurrentTransId
	
	ApiResponse = ApiResponseFactory.JsonResponse(
		objDef.ApproveVoilationRule(AllParams, ACTION, ApproveDesc, CurrentTransId)
	)
elif ACTION in ["SUBMIT_FOR_APPROVAL", "RECALL"]:
	Trace.Write("Entered Recall/SubmitforApproval-------")
	try:
		RequestDesc = Param.RequestDesc
	except Exception:
		RequestDesc = ""
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.SubmitForApproval(RequestDesc, ACTION))
# A043S001P01 -  11384  Start
elif ACTION =="STATUS":
	
	valllllll = objDef.approvalstatusbar(QuoteNumber)
	ApiResponse = ApiResponseFactory.JsonResponse(valllllll)
	#ApiResponse = ApiResponseFactory.JsonResponse(objDef.approvalstatusbar(QuoteNumber))
elif ACTION == "RichText":
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.RichTextArea(QuoteNumber))
# A043S001P01 -  11384  End
elif ACTION == "Notifications":
	mailType = Param.MailType
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.CreateMailContent(mailType))
elif ACTION == "PREVIEW_APPROVAL":    
	Trace.Write('In Preview Approval Action')
	AllParams = eval(Param.AllParams)
	try:        
		FromSeg = Param.FromSeg
	except Exception:        
		FromSeg = ""
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.PreviewApprovers(AllParams, FromSeg))
elif ACTION == "GET_SEGMENT_ID":
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.getSEGMENT_ID())
elif ACTION == "TrackedValues":
	Trace.Write("check")
	#ApiResponse = ApiResponseFactory.JsonResponse(objDef.TrackedFieldValues())
elif ACTION == "mailbodyfield":
	objhRecordID = Param.objhRecordID
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.messagebodyvalue(objhRecordID))
elif ACTION in ["VIEW_COMMENT", "EDIT_COMMENT", "SUBMIT_COMMENT", "REJECT_COMMENT", "APPROVE_COMMENT"]:
	AllParams = eval(Param.AllParams)
	try:
		TransactionId = Param.TransactionId
	except Exception:
		TransactionId = None
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.PreviewApproversComments(ACTION, TransactionId))
elif ACTION == "SAVE_COMMENT":
	RecipientComment = Param.RecipientComment
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.SaveApproversComments(RecipientComment))
elif ACTION in ["APPROVEBTN", "REJECTBTN"]:
	AllParams = eval(Param.AllParams)
	ApproveDesc = Param.ApproveDesc
	CurrentTransId = Param.CurrentTransId
	ACTION = ACTION[:-3]
	Result = objDef.ApproveVoilationRule(AllParams, ACTION, ApproveDesc, CurrentTransId)
# A043S001P01-13245 start
elif ACTION in ["BULKAPPROVE", "BULKREJECT"]:
	ApproveDesc = Param.ApproveDesc
	ApiResponse = ApiResponseFactory.JsonResponse(objDef.BulkAction(ACTION, ApproveDesc))
elif ACTION == "CBC_MAIL_TRIGGER":
    Trace.Write('ACSECTACTN: CBC_MAIL_TRIGGER')
    objDef.cbcmailtrigger()
# A043S001P01-13245 end
