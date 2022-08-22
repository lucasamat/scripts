# =========================================================================================================================================
#   __script_name : SYATABSAVE.PY
#   __script_description : THIS SCRIPT IS USED TO SAVE THE RECORDS FROM THE TABLIST ADD NEW.
#   __primary_author__ :AYYAPPAN SUBRAMANIYAN
#   __create_date :
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import datetime
import re
from SYDATABASE import SQL

Sql = SQL()
UserId = str(User.Id)
UserName = str(User.Name)

REC_NO = RecId = ""
Field_Labels = []
row = {}

Product_name = Product.Name
flag = "True"
for tab in Product.Tabs:
	tab_name = tab.Name    
	if tab.IsSelected == True:
		CurrentTabName = tab_name.strip()
		
		tab_obj = Sql.GetFirst(
			"select RECORD_ID,TAB_LABEL from SYTABS (nolock) where SAPCPQ_ALTTAB_NAME = '"
			+ str(CurrentTabName)
			+ "' and RTRIM(LTRIM(APP_LABEL))='"
			+ str(Product_name)
			+ "'"
		)
		if tab_obj:
			tab_label = tab_obj.TAB_LABEL            
			SYSECT_OBJNAME = Sql.GetList(
					"select SYSECT.RECORD_ID,SYSECT.PRIMARY_OBJECT_NAME FROM SYSECT (nolock) INNER JOIN SYPAGE ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID ='"
					+ str(tab_obj.RECORD_ID).strip()
					+ "' "
			)
			if SYSECT_OBJNAME is not None:
				##TO GET THE SECTION INFORMATION
				for secobj in SYSECT_OBJNAME:
					TABLE_NAME = str(secobj.PRIMARY_OBJECT_NAME).strip()
					REC_ID_OBJ = Sql.GetFirst(
						"Select RECORD_ID,RECORD_NAME from SYOBJH (nolock) where RTRIM(LTRIM(OBJECT_NAME))='"
						+ TABLE_NAME
						+ "'"
					)
					if REC_ID_OBJ:
						SYOBJH_OBJ = REC_ID_OBJ.RECORD_ID
						QUE_OBJ = Sql.GetFirst(
							"Select RECORD_ID,SAPCPQ_ATTRIBUTE_NAME from SYSEFL (nolock) where API_FIELD_NAME='"
							+ str(REC_ID_OBJ.RECORD_NAME).strip()
							+ "' and API_NAME='"
							+ TABLE_NAME
							+ "' and SECTION_RECORD_ID='"
							+ str(secobj.RECORD_ID)
							+ "' "
						)
						###TO GET THE QUESTION INFORMATION
						if QUE_OBJ:
							RECORDID = str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
							ATTRIBUTENAME = RECORDID.upper()
							RECORD_ID = "QSTN_" + ATTRIBUTENAME.strip()
							RecId = str(REC_ID_OBJ.RECORD_NAME).strip()                            
							Rec_Id_Value = ""
							####ACTION OF TABS                                                       
							if Product.Attributes.GetByName(RECORD_ID) is not None:
								Rec_Id_Value = Product.Attributes.GetByName(RECORD_ID).GetValue()
								
							#####add SAVE ACTION
							if Rec_Id_Value == "":
								details_obj = Sql.GetList(
									"SELECT OBJECT_NAME as TABLE_NAME ,API_NAME, DATA_TYPE,FORMULA_LOGIC,LOOKUP_API_NAME FROM  SYOBJD (nolock) where RTRIM(LTRIM(OBJECT_NAME)) ='"
									+ TABLE_NAME
									+ "' and LTRIM(RTRIM(PARENT_OBJECT_RECORD_ID))='"
									+ str(SYOBJH_OBJ).strip()
									+ "' "
								)
								
								if details_obj is not None:
									for detail_obj in details_obj:
										
										section_obj = Sql.GetList(
											"select SE.RECORD_ID  FROM SYSECT (nolock)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID where RTRIM(LTRIM(PG.TAB_NAME)) ='"
											+ str(tab_label)
											+ "' and PG.TAB_RECORD_ID ='"
											+ str(tab_obj.RECORD_ID).strip()
											+ "'"
										)
										if section_obj:
											for SECT in section_obj:
												SYSEFL_OBJNAME12 = Sql.GetList(
													"SELECT RECORD_ID,FIELD_LABEL, API_NAME,API_FIELD_NAME,SECTION_NAME,FLDDEF_VARIABLE_RECORD_ID,FLDDEF_VARIABLE_NAME,SAPCPQ_ATTRIBUTE_NAME FROM SYSEFL (nolock) where LTRIM(RTRIM(API_NAME)) ='{}' and LTRIM(RTRIM(API_FIELD_NAME))='{}' and LTRIM(RTRIM(SECTION_RECORD_ID))='{}'".format(str(detail_obj.TABLE_NAME).strip(), detail_obj.API_NAME, SECT.RECORD_ID)
												)
												if SYSEFL_OBJNAME12 is not None and len(SYSEFL_OBJNAME12) > 0:
													for SYSEFL_OBJNAME in SYSEFL_OBJNAME12:                                                        
														MM_MOD_CUS_OBJ = (SYSEFL_OBJNAME.API_FIELD_NAME).strip()
														SECTIONQSTNRECORDID = (
															str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
															.replace("-", "_")
															.replace(" ", "")
														)                                                        
														SECQSTNATTRIBUTENAME = SECTIONQSTNRECORDID.upper()                                                    
														if str(detail_obj.DATA_TYPE) == "LONG TEXT AREA":
															MM_MOD_ATTR_NAME = "QSTN_" + SECQSTNATTRIBUTENAME + "_LONG"
														else:
															MM_MOD_ATTR_NAME = "QSTN_" + SECQSTNATTRIBUTENAME  
														if detail_obj.DATA_TYPE == "AUTO NUMBER":
															REC_NO = str(Guid.NewGuid()).upper()
															row[RecId] = str(REC_NO)
														elif detail_obj.DATA_TYPE not in ("LOOKUP","FORMULA","PICKLIST","CHECKBOX"):
															if (
																Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																is not None
																and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
															):
																Attr_qstn1 = ""
																Attr_qstn2 = ""
																ATTR_Value = ""
																if str(MM_MOD_CUS_OBJ) == "ATTRIBUTE_NAME":
																	row[MM_MOD_CUS_OBJ] = Attr_qstn1
																if str(MM_MOD_CUS_OBJ) == "ATTRIBUTE_DESCRIPTION":
																	row[MM_MOD_CUS_OBJ] = Attr_qstn2
																else:
																	if MM_MOD_ATTR_NAME == "QSTN_SYSEFL_AC_00067_LONG":
																		msgbody = str(
																			Product.GetGlobal("RichTextVaslue").encode(
																				"ASCII", "ignore"
																			)
																		)                                                                        
																		if len(msgbody) <= 8000:
																			ATTR_Value = str(msgbody)
																			row["MESSAGE_BODY_2"] = ""
																			row["MESSAGE_BODY_3"] = ""
																			row["MESSAGE_BODY_4"] = ""
																			row["MESSAGE_BODY_5"] = ""
																		elif len(msgbody) < 16000:
																			msgsplit = str(msgbody).split("@!#$@!")
																			ATTR_Value = str(msgsplit[0][0:8000])
																			row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:])
																			row["MESSAGE_BODY_3"] = ""
																			row["MESSAGE_BODY_4"] = ""
																			row["MESSAGE_BODY_5"] = ""
																		elif len(msgbody) < 24000:
																			msgsplit = str(msgbody).split("@!#@!")
																			ATTR_Value = str(msgsplit[0][0:8000])
																			row["MESSAGE_BODY_2"] = str(
																				msgsplit[0][8000:16000]
																			)
																			row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:])
																			row["MESSAGE_BODY_4"] = ""
																			row["MESSAGE_BODY_5"] = ""
																		elif len(msgbody) < 32000:
																			msgsplit = str(msgbody).split("@!#@!")
																			ATTR_Value = str(msgsplit[0][0:8000])
																			row["MESSAGE_BODY_2"] = str(
																				msgsplit[0][8000:16000]
																			)
																			row["MESSAGE_BODY_3"] = str(
																				msgsplit[0][16000:24000]
																			)
																			row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:])
																			row["MESSAGE_BODY_5"] = ""
																		elif len(msgbody) < 40000:
																			msgsplit = str(msgbody).split("@!#@!")
																			ATTR_Value = str(msgsplit[0][0:8000])
																			row["MESSAGE_BODY_2"] = str(
																				msgsplit[0][8000:16000]
																			)
																			row["MESSAGE_BODY_3"] = str(
																				msgsplit[0][16000:24000]
																			)
																			row["MESSAGE_BODY_4"] = str(
																				msgsplit[0][24000:32000]
																			)
																			row["MESSAGE_BODY_5"] = str(msgsplit[0][32000:])
																	else:
																		ATTR_Value = (
																			Product.Attributes.GetByName(
																				str(MM_MOD_ATTR_NAME)
																			).GetValue()
																			or ""
																		)
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)                                                                
															elif (
																Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																is not None
																and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
															):
																FLDDEF_VARIABLE_RECORD_ID = (
																	SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
																)
																CTX_Logic = Sql.GetFirst(
																	"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
																	+ str(FLDDEF_VARIABLE_RECORD_ID)
																	+ "' "
																)
																if CTX_Logic:
																	result = ScriptExecutor.ExecuteGlobal(
																		"SYPARVRLLG",
																		{
																			"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
																			"Obj_Name": TABLE_NAME,
																		},
																	)
																if result != "":
																	ATTR_Value = str(result)
																	row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
																else:
																	row[MM_MOD_CUS_OBJ] = ""
														elif (detail_obj.DATA_TYPE).strip() == "PICKLIST (MULTI-SELECT)":                                                         
															attr_val = Product.GetGlobal("ATTR_VAL")                                                        
															if attr_val == "":
																attr_val = "MATERIAL ATTRIBUTE"
															
															row[MM_MOD_CUS_OBJ] = attr_val
															
														elif (detail_obj.DATA_TYPE).strip() == "PICKLIST":                                                            
															ATTR_Value = Product.Attributes.GetByName(
																str(MM_MOD_ATTR_NAME)
															).GetValue()
															try:
																row[MM_MOD_CUS_OBJ] = ATTR_Value
															except:
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
														elif detail_obj.DATA_TYPE == "CHECKBOX":
															if (
																Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																is not None
																and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
															):
																ATTR_Value = Product.Attributes.GetByName(
																	str(MM_MOD_ATTR_NAME)
																).GetValue()
																if ATTR_Value == "1":
																	ATTR_Value = "True"
																else:
																	ATTR_Value = "False"
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
																'''if str(MM_MOD_CUS_OBJ) == "ALLOW_EX_RT_UPD_SEG_PBK_ENTRY":
																	row[MM_MOD_CUS_OBJ] = "True"'''
															elif (
																Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																is not None
																and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
															):
																FLDDEF_VARIABLE_RECORD_ID = (
																	SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
																)
																CTX_Logic = Sql.GetFirst(
																	"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
																	+ str(FLDDEF_VARIABLE_RECORD_ID)
																	+ "' "
																)
																result = ScriptExecutor.ExecuteGlobal(
																	"SYPARVRLLG",
																	{
																		"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
																		"Obj_Name": TABLE_NAME,
																	},
																)
																if result != "":
																	ATTR_Value = str(result)
																	if ATTR_Value == "1":
																		ATTR_Value = "True"
																	else:
																		ATTR_Value = "False"
																	row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
															elif (
																Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																is not None
																and str(SYSEFL_OBJNAME.FLDEDT_VARIABLE_RECORD_ID) != ""
															):
																FLDEDT_VARIABLE_RECORD_ID = (
																	SYSEFL_OBJNAME.FLDEDT_VARIABLE_RECORD_ID
																)
																CTX_Logic = Sql.GetFirst(
																	"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
																	+ str(FLDEDT_VARIABLE_RECORD_ID)
																	+ "' "
																)
																result = ScriptExecutor.ExecuteGlobal(
																	"SYPARVRLLG",
																	{
																		"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
																		"Obj_Name": TABLE_NAME,
																	},
																)
																if result != "":
																	ATTR_Value = str(result)
																	row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

														elif detail_obj.DATA_TYPE == "FORMULA":
															if (
																detail_obj.FORMULA_LOGIC != ""
																and "select" in str(detail_obj.FORMULA_LOGIC).lower()
															):
																if TABLE_NAME != "PRPRCL":
																	SECTIONQSTNRECORDID = (
																		str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
																		.replace("-", "_")
																		.replace(" ", "")
																	)
																	SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
																	MM_MOD_ATTR_NAME = "QSTN_LKP_" + str(
																		SECQSTNATTRIBUTENAME
																	)                                                                    
																	if (
																		Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																		is not None
																	):
																		API_Value = str(
																			Product.Attributes.GetByName(
																				str(MM_MOD_ATTR_NAME)
																			).HintFormula
																		)
																		API_obj = Sql.GetFirst(
																			"select API_NAME from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
																			+ str(MM_MOD_CUS_OBJ)
																			+ "'and OBJECT_NAME='"
																			+ TABLE_NAME
																			+ "' "
																		) 
																		if API_obj is not None:                                                                    
																			API_Name = str(API_obj.API_NAME).strip()
																			if str(API_Value).upper() == "LOOKUP":
																				OM_ACNT_REC_ID = Product.GetGlobal(
																					"OM_ACNT_REC_ID"
																				)
																				if OM_ACNT_REC_ID != "":
																					API_Value = OM_ACNT_REC_ID
																				else:
																					API_Value = ""
																			row[API_Name] = str(API_Value)
																			result = ScriptExecutor.ExecuteGlobal(
																				"SYPARCEFMA",
																				{
																					"Object": TABLE_NAME,
																					"API_Name": API_Name,
																					"API_Value": API_Value,
																				},
																			)
																			for API_Names in result:
																				API_NAME = str(API_Names["API_NAME"]).strip()
																				RESULT = API_Names["FORMULA_RESULT"]
																				row[API_NAME] = RESULT
																elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
																	ATTR_Value = Product.Attributes.GetByName(
																		str(MM_MOD_ATTR_NAME)
																	).GetValue()
																	row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
																else:
																	row[MM_MOD_CUS_OBJ] = ""
															elif (
																detail_obj.FORMULA_LOGIC != ""
																and "select" not in str(detail_obj.FORMULA_LOGIC).lower()
															):
																ATTR_Value = str(detail_obj.FORMULA_LOGIC).strip()
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
															elif detail_obj.FORMULA_LOGIC == "":
																if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
																	ATTR_Value = Product.Attributes.GetByName(
																		str(MM_MOD_ATTR_NAME)
																	).GetValue()
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
															else:
																row[MM_MOD_CUS_OBJ] = ""
									
									if TABLE_NAME == "ACAPCH":
										row["APRCHN_ID"] = row['APRCHN_ID'].upper()
										datetime_value = datetime.datetime.now()
										Get_UserID = User.Id
										UserName = User.Name
										ApprovalchainId = row["APRCHN_ID"]
										ApprovalchainRecId = row["APPROVAL_CHAIN_RECORD_ID"]
										ApprovalObject = row["APROBJ_LABEL"]
										ApprovalObjectRecId = row["APROBJ_RECORD_ID"]
										StatusLlist = [
											"REQUESTED",
											"APPROVED",
											"REJECTED",
											"APPROVAL REQUIRED",
											"RECALLED",
											"ASSIGNED",
											"RESOLVED",
											"EXCLUDED",
										]
										for status in StatusLlist:
											InsertStatus = """INSERT ACACSS (APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID, APRCHN_ID, APPROVALSTATUS, EXCLUDED_STATUS, APROBJ_LABEL, APROBJ_STATUSFIELD_LABEL, APROBJ_STATUSFIELD_VAL, APROBJ_STATUSFIELD_RECORD_ID, APROBJ_RECORD_ID, APRCHN_RECORD_ID,ADDUSR_RECORD_ID ,CPQTABLEENTRYADDEDBY ,CPQTABLEENTRYDATEADDED , CpqTableEntryModifiedBy ,CpqTableEntryDateModified)SELECT CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID ,'{ApprovalchainId}' AS APRCHN_ID,'{status}' AS APPROVALSTATUS,'False' AS EXCLUDED_STATUS,'{ApprovalObject}' AS APROBJ_LABEL,'' AS APROBJ_STATUSFIELD_LABEL,'' AS APROBJ_STATUSFIELD_VAL,'' AS APROBJ_STATUSFIELD_RECORD_ID,'{ApprovalObjectRecId}' AS APROBJ_RECORD_ID,'{ApprovalchainRecId}' AS APRCHN_RECORD_ID,'{Get_UserID}' AS ADDUSR_RECORD_ID, '{UserName}' AS CPQTABLEENTRYADDEDBY , convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED , '{Get_UserID}' AS CpqTableEntryModifiedBy, convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified""".format(
												datetime_value=datetime_value,
												Get_UserID=Get_UserID,
												UserName=UserName,
												ApprovalchainId=ApprovalchainId,
												ApprovalchainRecId=ApprovalchainRecId,
												status=status,
												ApprovalObject=ApprovalObject,
												ApprovalObjectRecId=ApprovalObjectRecId,
											)
											a = Sql.RunQuery(InsertStatus)
									elif TABLE_NAME == "SYVABL":
										row["VARIABLE_NAME"] = row["VARIABLE_NAME"].upper()     
									Required_obj = Sql.GetList(
										"select top 1000 API_NAME,FIELD_LABEL,DISPLAY_ORDER,REQUIRED from  SYOBJD (nolock) where LTRIM(RTRIM(OBJECT_NAME)) ='"
										+ TABLE_NAME
										+ "'and LTRIM(RTRIM(UPPER(REQUIRED)))='1' ORDER BY DISPLAY_ORDER "
									)
									if Required_obj:
										for x in Required_obj:
											sectalert = x.FIELD_LABEL
											Trace.Write("row----"+str(row))
											if x.API_NAME in row.keys():
												
												API_NAME_val = row[x.API_NAME]                                                
												if str(API_NAME_val) == "" or API_NAME_val.upper() == "NONE":
													Trace.Write("False111===")                                                    
													flag = "False"
													break
												else:
													Trace.Write("False===")                                                    
													flag = "True"

										for req_add_new in Required_obj:
											if req_add_new.API_NAME in row.keys():
												API_NAME_val = row[req_add_new.API_NAME]                                                
												if str(API_NAME_val) == "" or API_NAME_val.upper() == "NONE":
													Field_Labels.append(req_add_new.FIELD_LABEL)
													Trace.Write('Field_Labels==='+str(Field_Labels))
										iskey = Sql.GetFirst(
											"select API_NAME from  SYOBJD (nolock) where OBJECT_NAME ='"
											+ TABLE_NAME
											+ "' and IS_KEY='True' "
										)
										   
										if TABLE_NAME == "ACAPCH" and len(row['APRCHN_ID']) < 8:
											flag = 'False'
										Trace.Write("99999888"+str(flag)) 
										if iskey is not None and flag == "True": 
											Trace.Write("99999")                                           
											col_name = (iskey.API_NAME).strip()                                                                                                                                    
											unique_val = row[col_name]                                                                                       
											if unique_val is not None and unique_val != "":
												is_key_table = Sql.GetFirst(
													"select "
													+ col_name
													+ " from "
													+ TABLE_NAME
													+ " (nolock)  where "
													+ col_name
													+ " ='"
													+ str(unique_val)
													+ "' "
												)
												if is_key_table is None:
													if (
														"CPQTABLEENTRYMODIFIEDBY" in row.keys()
														and "CPQTABLEENTRYDATEMODIFIED" in row.keys()
													):
														row.pop("CPQTABLEENTRYMODIFIEDBY")
														row.pop("CPQTABLEENTRYDATEMODIFIED")                                                        
													
													if str(CurrentTabName) == "Profile":
														prfid = Product.Attributes.GetByName(
															"QSTN_SYSEFL_SY_00128"
														).GetValue()
														prfname = Product.Attributes.GetByName(
															"QSTN_SYSEFL_SY_00129"
														).GetValue()
														existprofilecheck = SqlHelper.GetList(
															"Select * from cpq_permissions where SYSTEM_ID ='"
															+ str(prfid)
															+ "'"
														)                                                        
														#nativeProfileSave(row)
														ScriptExecutor.ExecuteGlobal(
																				"SYAPROFILES",
																				{
																					"row": row,
																					"nativeProfileSave":"Yes"
																				},
																			)
														query = Sql.GetList(
															"SELECT APP_LABEL,APP_ID,APP_DESCRIPTION FROM SYAPPS"
														)
														tableInfo = Sql.GetTable("SYPRAP")
														prfid = Product.Attributes.GetByName(
															"QSTN_SYSEFL_SY_00128"
														).GetValue()
														per_id = Product.GetGlobal("Profile_ID_val")
														prfname = Product.Attributes.GetByName(
															"QSTN_SYSEFL_SY_00129"
														).GetValue()
														prfname = prfid
														prfdesc = Product.Attributes.GetByName(
															"QSTN_SYSEFL_SY_00130_LONG"
														).GetValue()
														if query is not None:
															row = {}
															for val in query:

																new_val = str(Guid.NewGuid()).upper()
																row["APP_ID"] = val.APP_LABEL
																row["APP_RECORD_ID"] = val.APP_ID
																
																if row["APP_ID"] == "MATERIALS":
																	row["DEFAULT"] = "True"
																else:
																	row["DEFAULT"] = "False"
																
																row["PROFILE_RECORD_ID"] = per_id
																row["PROFILE_ID"] = prfname
																
																if row["APP_ID"] in [
																	"MATERIALS",
																	"SALES",
																	"SYSTEM ADMIN",
																]:
																	row["VISIBLE"] = True
																else:
																	row["VISIBLE"] = False
																
																row["PROFILE_APP_RECORD_ID"] = new_val
																tableInfo.AddRow(row)
																
															Sql.Upsert(tableInfo)
															# to save in SYPRAP End
															
															QueryStatementTB = """INSERT INTO SYPRTB ( APP_ID,APP_RECORD_ID,TAB_ID,TAB_RECORD_ID,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_TAB_RECORD_ID,VISIBLE, CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy,CPQTABLEENTRYDATEADDED,CpqTableEntryDateModified) SELECT SYTABS.APP_LABEL, SYTABS.APP_RECORD_ID,SYTABS.TAB_LABEL,SYTABS.RECORD_ID,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),'True','{}','{}',convert(VARCHAR(10), '{}', 101),convert(VARCHAR(10), '{}', 101) FROM SYTABS""".format(
																per_id, prfname,UserName,UserId,datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
															)
															Sql.RunQuery(QueryStatementTB)
															
															QueryStatementSN = """INSERT INTO SYPRSN (SECTION_RECORD_ID,SECTION_ID,TAB_ID,TAB_RECORD_ID,PROFILE_RECORD_ID,PROFILE_ID,VISIBLE,PROFILE_SECTION_RECORD_ID,OBJECT_NAME,OBJECT_RECORD_ID,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy) SELECT SYSECT.RECORD_ID, SYSECT.SECTION_NAME,SYPAGE.TAB_NAME,SYPAGE.TAB_RECORD_ID,'{}','{}','True', CONVERT(VARCHAR(4000),NEWID()),SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID,'{}','{}'  FROM SYSECT INNER JOIN SYPAGE(NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID""".format(
																per_id, prfname,UserName,UserId
															)
															Sql.RunQuery(QueryStatementSN)
															
															QueryStatementAC = """INSERT INTO SYPRAC ( ACTION_RECORD_ID, TAB_RECORD_ID, TAB_NAME, ACTION_TEXT, SECTION_RECORD_ID, SECTION_NAME,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_ACTION_RECORD_ID,VISIBLE,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy) SELECT SYPSAC.RECORD_ID, SYPSAC.TAB_RECORD_ID,SYPSAC.TAB_NAME,SYPSAC.ACTION_NAME,SYPSAC.SECTION_RECORD_ID,SYPSAC.SECTION_NAME,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),'True','{}','{}' FROM SYPSAC""".format(
																per_id, prfname,UserName,UserId
															)
															Sql.RunQuery(QueryStatementAC)
															
														   
															QueryStatementQS = """INSERT INTO SYPRSF (SECTIONFIELD_RECORD_ID,SECTION_FIELD_ID,SECTION_RECORD_ID,SECTION_NAME,OBJECT_RECORD_ID,OBJECT_NAME,OBJECTFIELD_API_NAME,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_SECTIONFIELD_RECORD_ID,VISIBLE,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy)SELECT QS.RECORD_ID, QS.FIELD_LABEL,QS.SECTION_RECORD_ID,QS.SECTION_NAME,SC.RECORD_ID,QS.API_NAME,QS.API_NAME,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),1,'{}','{}'  FROM SYSEFL QS inner join SYOBJH SC on  SC.OBJECT_NAME = QS.API_NAME """.format(
																per_id, prfname,UserName,UserId
															)
															Sql.RunQuery(QueryStatementQS)

															QueryStatementOD = """INSERT INTO SYPROD (OBJECTFIELD_RECORD_ID,OBJECT_FIELD_ID,OBJECT_RECORD_ID,OBJECT_NAME,OBJECTFIELD_LABEL,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_OBJECTFIELD_RECORD_ID,VISIBLE,EDITABLE,DEFAULT_EDIT_ACCESS)SELECT SD.RECORD_ID, SD.FIELD_LABEL,SD.PARENT_OBJECT_RECORD_ID,SD.OBJECT_NAME,SD.API_NAME,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),1,1,1 FROM SYOBJD SD  """.format(
																per_id, prfname
															)
															Sql.RunQuery(QueryStatementOD)

															QueryStatementOH = """INSERT INTO SYPROH (OBJECT_RECORD_ID,OBJECT_NAME,CAN_ADD,CAN_EDIT,CAN_DELETE,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_OBJECT_RECORD_ID,VISIBLE)SELECT SH.RECORD_ID, SH.OBJECT_NAME,JS.CAN_ADD,JS.CAN_EDIT,JS.CAN_DELETE,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),1 FROM SYOBJH SH INNER JOIN SYOBJS JS ON JS.CONTAINER_NAME = SH.OBJECT_NAME  """.format(
																per_id, prfname
															)
															Sql.RunQuery(QueryStatementOH)

																									   
													else:
														Trace.Write('123456')
														##CPQ Attribute name starts                                                        
														if ("SAPCPQ_ATTRIBUTE_NAME" in row) and TABLE_NAME == "SYTABS":
															if (str(row["APP_ID"]) != ""):
																APP_ID = TABLE_NAME+"-"+str(row["APP_ID"])+"-"
																cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYTABS (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
																x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
																length = len(x[len(x)-1])
																row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
														elif ("SAPCPQ_ATTRIBUTE_NAME" in row) and TABLE_NAME == "SYOBJH":
															cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYOBJH (NOLOCK)")
															x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
															length = len(x[len(x)-1])
															row["SAPCPQ_ATTRIBUTE_NAME"] = "SYOBJ-"+ str(int(x[len(x)-1])+1).zfill(length)
														##CPQ Attribute name ends
														tableInfo = Sql.GetTable(TABLE_NAME)                                                        
														tableInfo.AddRow(row)
														Sql.Upsert(tableInfo)
														
														
													Product.Attributes.GetByName(str(RECORD_ID)).Allowed = True
													Product.Attributes.GetByName(str(RECORD_ID)).AssignValue(str(REC_NO))
													try:
														result = ScriptExecutor.ExecuteGlobal(
															"SYPARCEFMA",
															{
																"Object": TABLE_NAME,
																"API_Name": str(RecId),
																"API_Value": str(REC_NO),
															},
														)
														new_value_dict = {
															API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
															for API_Names in result
															if API_Names["FORMULA_RESULT"] != ""
														}
														if new_value_dict is not None:
															row = {RecId: str(REC_NO)}
															row.update(new_value_dict)
															Table.TableActions.Update(TABLE_NAME, RecId, row)

													except:
														Trace.Write("NOT SELF REFERENCE RECORD")
													if str(SYOBJH_OBJ):
														if str(REC_ID_OBJ.RECORD_NAME) != "permission_id":
															RecId = str(REC_ID_OBJ.RECORD_NAME).strip()
															AutoFieldId = row.get("RecId")
															# Dont Delete the line
															# violationruleInsert.InsertAction(str(SYOBJH_OBJ),str(AutoFieldId),str(TABLE_NAME))
															ScriptExecutor.ExecuteGlobal(
																"SYALLTABOP",
																{
																	"Primary_Data": str(REC_NO),
																	"TabNAME": str(tab_label),
																	"ACTION": "VIEW",
																	"RELATED": "",
																},
															)

														else:
															per_id = Product.GetGlobal("Profile_ID_val")
															ScriptExecutor.ExecuteGlobal(
																"SYALLTABOP",
																{
																	"Primary_Data": str(per_id),
																	"TabNAME": str(tab_label),
																	"ACTION": "VIEW",
																	"RELATED": "",
																},
															)
													

												else:
													if TABLE_NAME == "cpq_permissions"  and Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													):
														Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True                                                
														Product.Attributes.GetByName(
															"SEC_N_TAB_PAGE_ALERT"
														).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert11" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert11" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : This "PROFILE" Already exists </label></div></div></div>'
																  
													elif Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT"):
														Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
														Trace.Write("TABLE_NAME_CHK_J "+str(TABLE_NAME))
														if TABLE_NAME == "ACAPCH":
															Product.Attributes.GetByName(
																"SEC_N_TAB_PAGE_ALERT"
															).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert11" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert11" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : This "Approval Chain Id" Already exists </label></div></div></div>'
														else:
															Product.Attributes.GetByName(
																"SEC_N_TAB_PAGE_ALERT"
															).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert11" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert11" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : This "Role Id & Name" Already exists </label></div></div></div>'
																						  
											else:                                                
												if (
													Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
													and flag == "True"
												):
													Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
													Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert12" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert12" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : You will not be able to save your data until all required fields are populated </label></div></div></div>'

												   
										else:   
											Trace.Write("888")                                         
											col_name = (iskey.API_NAME).strip()
											if (
												Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
												and flag == "False"
											):  
												Trace.Write("88877")                                              
												Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
												Trace.Write("88866")

												# Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = """<div class='col-md-12' id='PageAlert' style='display':'block'; ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : '{}' is a required field </label></div></div></div>""".format(sectalert)
												sectalert = ", ".join(Field_Labels)
												# product = Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula
												#Trace.Write("prod999==="+str(product))
																							   
												if len(Field_Labels) > 1:
													Trace.Write('Field_Labels======')                                                    
													Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													).HintFormula = "<div class='col-md-12' id='PageAlert' style='display':'block';  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' are required fields </label></div></div></div>".format(
														sectalert
													)                                                    
												
												if Product.Attributes.GetByName("QSTN_SYSEFL_AC_00006"):
													ApprovalMethod =  Product.Attributes.GetByName("QSTN_SYSEFL_AC_00006")
													if ApprovalMethod == "":
														Product.Attributes.GetByName(
															"SEC_N_TAB_PAGE_ALERT"
														).HintFormula = "<div class='col-md-12' id='PageAlert' style='display':'block';  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : Please select an Approval Method from the list for Approval Chain</label></div></div></div>".format(
															sectalert
														)    
												if len(Field_Labels) <= 1:
													Trace.Write('Field_Labels2222======'+str(sectalert))                                                     
													if sectalert:  
														Product.Attributes.GetByName(
															"SEC_N_TAB_PAGE_ALERT"
														).HintFormula = "<div class='col-md-12' id='PageAlert' style='display':'block';  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' is a required field</label></div></div></div>".format(
															sectalert
														)      
													else:
														Product.Attributes.GetByName(
															"SEC_N_TAB_PAGE_ALERT"
														).HintFormula = "<div class='col-md-12' id='PageAlert' style='display':'block';  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : Approval Chain Id should be 8 Characters</label></div></div></div>"
											elif (
												Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
												and flag == "null"
											):
												Trace.Write("flag999===")
												Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
												sectalert = ", ".join(Field_Labels)                                                

												if len(Field_Labels) > 1:
													Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' are required fields </label></div></div></div>".format(
														sectalert
													)
												elif "Approval Chain ID" in str(Field_Labels):
													Trace.Write("Comming inside length check")

												else:
													Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' is a required field</label></div></div></div>".format(
														sectalert
													)

										# A043S001P01-10904 - End
							#####EDIT SAVE ACTION
							else:
								row[RecId] = str(Rec_Id_Value)
								details_obj = Sql.GetList(
									"SELECT OBJECT_NAME,API_NAME, DATA_TYPE,FORMULA_LOGIC, LOOKUP_API_NAME FROM  SYOBJD (nolock) where LTRIM(RTRIM(OBJECT_NAME)) ='"
									+ TABLE_NAME
									+ "' and LTRIM(RTRIM(PARENT_OBJECT_RECORD_ID))='"
									+ str(SYOBJH_OBJ).strip()
									+ "' "
								)
								if details_obj is not None:
									for detail_obj in details_obj:
										SECT_OBJNAME = Sql.GetList(
											"select SYSECT.RECORD_ID  FROM SYSECT (nolock) INNER JOIN SYPAGE ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where RTRIM(LTRIM(TAB_NAME)) ='"
											+ str(tab_label)
											+ "' and SYPAGE.TAB_RECORD_ID ='"
											+ str(tab_obj.RECORD_ID).strip()
											+ "'"
										)
										if SECT_OBJNAME is not None:
											for SECT in SECT_OBJNAME:
												SYSEFL_OBJNAME = Sql.GetFirst(
													"SELECT RECORD_ID,FIELD_LABEL,SAPCPQ_ATTRIBUTE_NAME,API_FIELD_NAME, API_NAME,SECTION_NAME,FLDDEF_VARIABLE_RECORD_ID,FLDDEF_VARIABLE_NAME FROM SYSEFL (nolock) where API_NAME ='"
													+ str(detail_obj.OBJECT_NAME).strip()
													+ "' and API_FIELD_NAME='"
													+ str(detail_obj.API_NAME).strip()
													+ "' and  SECTION_RECORD_ID='"
													+ str(SECT.RECORD_ID)
													+ "'"
												)
												if SYSEFL_OBJNAME is not None and str(SYSEFL_OBJNAME.API_NAME) != "":
													MM_MOD_CUS_OBJ = (SYSEFL_OBJNAME.API_FIELD_NAME).strip()
													SECTIONQSTNRECORDID = (
														str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
														.replace("-", "_")
														.replace(" ", "")
													)
													SECQSTNATTRIBUTENAME = SECTIONQSTNRECORDID.upper()
													# A043S001P01-11384 Start
													if str(detail_obj.DATA_TYPE) == "LONG TEXT AREA":
														MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME) + "_LONG"
													else:
														MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
													# A043S001P01-11384 End
													if detail_obj.DATA_TYPE not in ("LOOKUP","AUTO NUMBER","FORMULA","PICKLIST","CHECKBOX","CURRENCY"
													):
														if (
															Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
															and SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID == ""
														):      
															if MM_MOD_ATTR_NAME == "QSTN_SYSEFL_AC_00067_LONG":
																msgbody = str(
																	Product.GetGlobal("RichTextVaslue").encode(
																		"ASCII", "ignore"
																	)
																)
																if len(msgbody) <= 8000:
																	ATTR_Value = str(msgbody)
																	row["MESSAGE_BODY_2"] = ""
																	row["MESSAGE_BODY_3"] = ""
																	row["MESSAGE_BODY_4"] = ""
																	row["MESSAGE_BODY_5"] = ""
																elif len(msgbody) < 16000:
																	msgsplit = str(msgbody).split("@!#$@!")
																	ATTR_Value = str(msgsplit[0][0:8000])
																	row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:])
																	row["MESSAGE_BODY_3"] = ""
																	row["MESSAGE_BODY_4"] = ""
																	row["MESSAGE_BODY_5"] = ""
																elif len(msgbody) < 24000:
																	msgsplit = str(msgbody).split("@!#@!")
																	ATTR_Value = str(msgsplit[0][0:8000])
																	row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
																	row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:])
																	row["MESSAGE_BODY_4"] = ""
																	row["MESSAGE_BODY_5"] = ""
																elif len(msgbody) < 32000:
																	msgsplit = str(msgbody).split("@!#@!")
																	ATTR_Value = str(msgsplit[0][0:8000])
																	row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
																	row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:24000])
																	row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:])
																	row["MESSAGE_BODY_4"] = ""
																	row["MESSAGE_BODY_5"] = ""
																elif len(msgbody) < 40000:
																	msgsplit = str(msgbody).split("@!#@!")
																	ATTR_Value = str(msgsplit[0][0:8000])
																	row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
																	row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:24000])
																	row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:32000])
																	row["MESSAGE_BODY_5"] = str(msgsplit[0][32000:])
															else:        
																ATTR_Value = (
																	Product.Attributes.GetByName(
																		str(MM_MOD_ATTR_NAME)
																	).GetValue()
																	or ""
																)  
															try:
																row[MM_MOD_CUS_OBJ] = ATTR_Value
															except Exception:
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
														elif (
															Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
															and SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID != ""
														):
															FLDDEF_VARIABLE_RECORD_ID = str(
																SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
															).strip()
															CTX_Logic = Sql.GetFirst(
																"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
																+ str(FLDDEF_VARIABLE_RECORD_ID)
																+ "' "
															)
															result = ScriptExecutor.ExecuteGlobal(
																"SYPARVRLLG",
																{
																	"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
																	"Obj_Name": TABLE_NAME,
																},
															)
															if result != "":
																ATTR_Value = str(result)
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
													elif detail_obj.DATA_TYPE == "PICKLIST (MULTI-SELECT)":
														attr_val = Product.GetGlobal("ATTR_VAL")
														row[MM_MOD_CUS_OBJ] = attr_val
													elif detail_obj.DATA_TYPE == "PICKLIST":               
														sec_attr = []
														Calc_fctr_array = {}
														if str(SECQSTNATTRIBUTENAME) not in sec_attr:
															ATTR_Value = Product.Attributes.GetByName(
																str(MM_MOD_ATTR_NAME)
															).GetValue()
															try:
																row[MM_MOD_CUS_OBJ] = ATTR_Value
															except Exception:
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
														if str(SECQSTNATTRIBUTENAME) in sec_attr:
															row[MM_MOD_CUS_OBJ] = str(
																dict(Calc_fctr_array).get(SECQSTNATTRIBUTENAME)
															)
													elif detail_obj.DATA_TYPE == "CURRENCY":
														if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
															ATTR_Value = Product.Attributes.GetByName(
																str(MM_MOD_ATTR_NAME)
															).GetValue()
															t = ATTR_Value.split(" ")
															if len(t) > 1:
																ATTR_Value = ATTR_Value[2:]
															try:
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
															except Exception:
																row[MM_MOD_CUS_OBJ] = ATTR_Value
													elif detail_obj.DATA_TYPE == "CHECKBOX":
														if (
															Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
															and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
														):
															ATTR_Value = Product.Attributes.GetByName(
																str(MM_MOD_ATTR_NAME)
															).GetValue()
															if ATTR_Value == "1":
																ATTR_Value = "True"
															else:
																ATTR_Value = "False"                                                            
															row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

														elif (
															Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
															and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
														):

															FLDDEF_VARIABLE_RECORD_ID = (
																SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
															)

															CTX_Logic = Sql.GetFirst(
																"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
																+ str(FLDDEF_VARIABLE_RECORD_ID)
																+ "' "
															)
															result = ""
															if CTX_Logic:
																result = ScriptExecutor.ExecuteGlobal(
																	"SYPARVRLLG",
																	{
																		"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
																		"Obj_Name": TABLE_NAME,
																	},
																)
															if result != "":
																ATTR_Value = str(result)
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

													elif (
														detail_obj.DATA_TYPE == "FORMULA"
														and str(MM_MOD_CUS_OBJ) != "EMPLOYEE_STATUS"
													):
														OBJD_OBJ = Sql.GetFirst(
															"select PERMISSION from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
															+ str(MM_MOD_CUS_OBJ)
															+ "' and OBJECT_NAME ='"
															+ str(TABLE_NAME).strip()
															+ "' "
														)
														if OBJD_OBJ is not None and OBJD_OBJ.PERMISSION != "READ ONLY":
															if (
																detail_obj.FORMULA_LOGIC != ""
																and "select" in str(detail_obj.FORMULA_LOGIC).lower()
															):
																SECTIONQSTNRECORDID = (
																	str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
																	.replace("-", "_")
																	.replace(" ", "")
																)
																SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
																MM_MOD_ATTR_NAME = "QSTN_LKP_" + str(SECQSTNATTRIBUTENAME)
																if (
																	Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
																	is not None
																):                                                                    
																	API_Value = str(
																		Product.Attributes.GetByName(
																			str(MM_MOD_ATTR_NAME)
																		).HintFormula
																	)
																	API_obj = Sql.GetFirst(
																		"select API_NAME,DATA_TYPE from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
																		+ str(MM_MOD_CUS_OBJ)
																		+ "' and OBJECT_NAME ='"
																		+ TABLE_NAME
																		+ "' "
																	)
																	if API_obj is not None:
																		API_Name = str(API_obj.API_NAME).strip()
																		if str(API_Value).upper() == "LOOKUP":
																			API_Value = ""
																		row[API_Name] = str(API_Value)
																		if "DATE" in str(API_obj.DATA_TYPE):
																			API_Name = CONVERT(VARCHAR(10), API_Name, 101,)

																		result = ScriptExecutor.ExecuteGlobal(
																			"SYPARCEFMA",
																			{
																				"Object": TABLE_NAME,
																				"API_Name": str(API_Name),
																				"API_Value": API_Value,
																			},
																		)

																		for API_Names in result:
																			API_NAME = str(API_Names["API_NAME"]).strip()
																			RESULT = str(API_Names["FORMULA_RESULT"])
																			row[API_NAME] = str(RESULT)

																			
															elif (
																detail_obj.FORMULA_LOGIC != ""
																and "select" not in str(detail_obj.FORMULA_LOGIC).lower()
															):
																ATTR_Value = str(detail_obj.FORMULA_LOGIC).strip()
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
															elif detail_obj.FORMULA_LOGIC == "":
																ATTR_Value = Product.Attributes.GetByName(
																	str(MM_MOD_ATTR_NAME)
																).GetValue()
																row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
														else:
															ATTR_Value = Product.Attributes.GetByName(
																str(MM_MOD_ATTR_NAME)
															).GetValue()
															row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

													else:                                                      
														ATTR_Value = Product.Attributes.GetByName(
															str(MM_MOD_ATTR_NAME)
														).GetValue()
														row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
														
									if "CPQTABLEENTRYMODIFIEDBY" in row.keys() and "CPQTABLEENTRYDATEMODIFIED" in row.keys():
										row.pop("CPQTABLEENTRYMODIFIEDBY")
										row.pop("CPQTABLEENTRYDATEMODIFIED")

									is_key = Sql.GetFirst(
										"select API_NAME from  SYOBJD where OBJECT_NAME ='"
										+ TABLE_NAME
										+ "'and IS_KEY='True' "
									)
									if is_key:
										col_name = (is_key.API_NAME).strip()
										if str(tab_name) not in ("Tab","Page","Object","Variable","Script","Email Template","Role","Currency"):
											row[col_name] = str(col_name)
										unique_val = row[col_name]

										if (
												unique_val is not None
												and unique_val != ""
												or Product.Attributes.GetByName("QSTN_SYSEFL_MA_00387") != ""
												and not None
											):

												REC_OBJ = Sql.GetFirst(
													"select RECORD_NAME from SYOBJH where OBJECT_NAME ='"
													+ TABLE_NAME
													+ "' "
												)

												Required_obj1 = Sql.GetList(
													"select API_NAME,REQUIRED,FIELD_LABEL from  SYOBJD where LTRIM(RTRIM(OBJECT_NAME)) ='"
													+ TABLE_NAME
													+ "'and REQUIRED='TRUE' "
												)

												if Required_obj1 :
													for x in Required_obj1:
														API_NAME_val = row[x.API_NAME]                                                        
														if API_NAME_val == "":
															flag = "False"
															break
														else:
															flag = "True"

													for req_fields in Required_obj1:
														API_NAME_val = row[req_fields.API_NAME]
														if API_NAME_val == "":
															Field_Labels.append(req_fields.FIELD_LABEL)

												if REC_OBJ is not None:
													Auto_Col = (REC_OBJ.RECORD_NAME).strip()

													REC_VAL = row[Auto_Col]                                                    
													if REC_VAL != "":                                                        
														is_key_table = Sql.GetFirst(
															"select "
															+ col_name
															+ " from "
															+ TABLE_NAME
															+ "  where "
															+ col_name
															+ " ='"
															+ str(unique_val)
															+ "' and "
															+ Auto_Col
															+ "!='"
															+ str(REC_VAL)
															+ "'"
														)
														if is_key_table and flag == "False":
															if (
																Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT")
																is not None
															):   
																Trace.Write('iskey_requ---')                                                            
																sectalert = ", ".join(Field_Labels)
																Product.Attributes.GetByName(
																	"SEC_N_TAB_PAGE_ALERT"
																).Allowed = True
																if len(Field_Labels) > 1:
																	Product.Attributes.GetByName(
																		"SEC_N_TAB_PAGE_ALERT"
																	).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{0}' are required fields </label></div></div></div>".format(
																		sectalert
																	)

																else:
																	if str(sectalert) != "":
																		Product.Attributes.GetByName(
																			"SEC_N_TAB_PAGE_ALERT"
																		).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert17" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert17" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" is a required field </label></div></div></div>'.format(
																			sectalert
																		)
																	else:
																		Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed =False
																		Table.TableActions.Update(TABLE_NAME, RecId, row)
																		
														elif is_key_table is None:                                                       
															Product.Attributes.GetByName(
																"SEC_N_TAB_PAGE_ALERT"
															).Allowed = False
															if TABLE_NAME == "cpq_permissions":
																#nativeProfileUpdate(row)
																ScriptExecutor.ExecuteGlobal(
																				"SYAPROFILES",
																				{
																					"row": row,
																					"nativeProfileUpdate":"Yes"
																				},
																			)
															else:                                                                
																Table.TableActions.Update(
																	TABLE_NAME, RecId, row,
																)                                                       
															try:
																result = ScriptExecutor.ExecuteGlobal(
																	"SYPARCEFMA",
																	{
																		"Object": TABLE_NAME,
																		"API_Name": str(RecId),
																		"API_Value": Rec_Id_Value,
																	},
																)

																new_value_dict = {
																	API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
																	for API_Names in result
																	if API_Names["FORMULA_RESULT"] != ""
																}

																if new_value_dict is not None:
																	row = {RecId: str(Rec_Id_Value)}
																	row.update(new_value_dict)                                                                    
																	Table.TableActions.Update(
																		TABLE_NAME, RecId, row,
																	)                                                                    
															except Exception:
																Trace.Write("NOT SELF REFERENCE RECORD")                               
															
															ScriptExecutor.ExecuteGlobal(
																"SYALLTABOP",
																{
																	"Primary_Data": Rec_Id_Value,
																	"TabNAME": tab_label,
																	"ACTION": "VIEW",
																	"RELATED": "",
																},
															)
															
															if (
																Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT")
																is not None
																and flag != "False"
															):
																Product.Attributes.GetByName(
																	"SEC_N_TAB_PAGE_ALERT"
																).Allowed = False
																Product.Attributes.GetByName(
																	"SEC_N_TAB_PAGE_ALERT"
																).HintFormula = ""

														else:
															sectalert = ", ".join(Field_Labels)
															if (
																Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT")
																is not None
															):
															   
																if len(Field_Labels) > 1:
																	Product.Attributes.GetByName(
																		"SEC_N_TAB_PAGE_ALERT"
																	).Allowed = True
																	Product.Attributes.GetByName(
																		"SEC_N_TAB_PAGE_ALERT"
																	).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert18" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert18" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" are required fields </label></div></div></div>'.format(
																		sectalert
																	)
																else:
																	result = ScriptExecutor.ExecuteGlobal(
																		"SYPARCEFMA",
																		{
																			"Object": TABLE_NAME,
																			"API_Name": str(RecId),
																			"API_Value": Rec_Id_Value,
																		},
																	)
																	
																	Table.TableActions.Update(
																		TABLE_NAME, RecId, row,
																	)
																	   
																	ScriptExecutor.ExecuteGlobal(
																		"SYALLTABOP",
																		{
																			"Primary_Data": Rec_Id_Value,
																			"TabNAME": tab_label,
																			"ACTION": "VIEW",
																			"RELATED": "",
																		},
																	)
																	
																	if Field_Labels:
																		Product.Attributes.GetByName(
																			"SEC_N_TAB_PAGE_ALERT"
																		).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert18" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert18" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" are required fields </label></div></div></div>'.format(
																			sectalert
																	)
										else:
											if Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None:
												Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
												sectalert = ", ".join(Field_Labels)
												if len(Field_Labels) > 1:
													Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert19" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert19" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" are required fields </label></div></div></div>'.format(
														sectalert
													)
												else:
													Product.Attributes.GetByName(
														"SEC_N_TAB_PAGE_ALERT"
													).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert19" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert19" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error"> ERROR :"{0}" is a required field  </label></div></div></div>'.format(
														sectalert
													)