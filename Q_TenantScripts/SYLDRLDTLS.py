# =========================================================================================================================================
#   __script_name : SYLDRLDTLS.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE RELATED LIST DETAILS IN THE SEGMENT AND MATERIAL APPS WHEN USERS CLICK ON THE LEFTHANDSIDE TREE NODE.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import unicodedata
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()


class SYLDRLDTLS:
	def MaterialTree(
		self, MODE, RECORD_ID, ObjectName, TreeParam, NEWVAL, LOOKUPOBJ, LOOKUPAPI, SECTION_EDIT, Flag, TreeSuperParentParam,
	):
		try:
			current_prod = Product.Name
		except:
			current_prod = ""

		sec_str = ""
		Chkctry = ""
		canedit = ""
		text = ""
		ERP_MAMAAT_CHECK = Gold_value = Silver_value = current_obj_value_float = onchange_txt = Mandatory = ""

		action_visible_str = ""
		# A043S001P01-9760 - End
		# CURRENCY_SYMBOL = Sql.GetFirst("SELECT CURRENCY_RECORD_ID FROM PRCURR(NOLOCK) WHERE CURRENCY = 'USD'")
		# CURRENCY_SYMBOL_VALUE = CURRENCY_SYMBOL.CURRENCY_RECORD_ID
		date_field = []
		Count_val = 0
		if Flag == 1:
			if ObjectName in str(RECORD_ID):
				RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
		primary_value = RECORD_ID
		CurrentTab = TestProduct.CurrentTab
		auto_field = ""
		sNotInCondition = sNodeTxt = ""
		nodeCount = 3

		if MODE == "EDIT":

			RECORD_ID = primary_value

		elif MODE == "EDIT_CLEAR":
			MODE = "EDIT"

		elif MODE == "CANCEL":

			RECORD_ID = primary_value
			MODE = "VIEW"
		TableName = primary_value.split("-")
		LOOKUPOBJ = LOOKUPOBJ.replace("table_", "")
		objh_obj = Sql.GetFirst("SELECT * FROM SYOBJH WITH (NOLOCK) WHERE OBJECT_NAME='" + str(ObjectName) + "' ")
		objr_obj = (
			Sql.GetFirst(
				"SELECT top 1000 MR.* FROM SYOBJR MR WHERE MR.PARENT_LOOKUP_REC_ID ='"
				+ str(PARENT_LOOKUP_REC_ID)
				+ "' and MR.OBJ_REC_ID='"
				+ str(objh_obj.RECORD_ID)
				+ "'"
			)
			if objh_obj is not None
			else ""
		)
		Sqq_obj = Sql.GetList(
			"SELECT top 1000 API_NAME, DATA_TYPE, LOOKUP_OBJECT, PERMISSION, REQUIRED, LOOKUP_API_NAME, FIELD_LABEL,SOURCE_DATA FROM SYOBJD WITH (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' ORDER BY abs(DISPLAY_ORDER)"
		)
		lookup_val = [val.LOOKUP_API_NAME for val in Sqq_obj]
		lookup_list = {ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}
		lookup_list1 = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Sqq_obj}
		new_value_dict = {}
		api_name = ""

		for tab in Product.Tabs:
			if tab.IsSelected == True:
				if tab.Name == "Country":
					Chkctry = "true"
		if NEWVAL != "":
			if str(LOOKUPOBJ) == "CLEAR SELECTION":
				attrval_obj = Sql.GetFirst(
					"select SYOBJD.API_NAME,SYOBJD.OBJECT_NAME,SYSEFL.API_NAME,SYSEFL.API_NAME from SYOBJD(NOLOCK)  inner join SYSEFL(NOLOCK)  on SYOBJD.API_NAME = SYSEFL.API_NAME and SYOBJD.OBJECT_NAME = SYSEFL.API_NAME inner join SYSECT(NOLOCK) on SYSECT.PRIMARY_OBJECT_NAME = SYSEFL.API_NAME and SYSECT.SECTION_NAME = SYSEFL.SECTION_NAME  and SYSECT.RECORD_ID = '"
					+ str(SECTION_EDIT)
					+ "' and OBJECT_NAME='"
					+ str(ObjectName)
					+ "' AND LOOKUP_OBJECT='"
					+ str(NEWVAL)
					+ "' "
				)
				
				api_name = attrval_obj.API_NAME.strip()
				TABLE_OBJS = Sql.GetList(
					"select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM SYOBJD WITH (NOLOCK) where OBJECT_NAME ='"
					+ str(ObjectName)
					+ "' and FORMULA_LOGIC like '%"
					+ str(api_name)
					+ "%'"
				)
				if TABLE_OBJS is not None:
					for TABLE_OBJ in TABLE_OBJS:
						if TABLE_OBJ.DATA_TYPE != "":
							DATA_TYPE = str(TABLE_OBJ.DATA_TYPE)

							if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
								new_value_dict[str(TABLE_OBJ.API_NAME)] = ""
								new_value_dict[str(api_name)] = ""
			else:
				try:
					lookupval = str(LOOKUPOBJ).split("_")[1]
				except:
					lookupval = str(LOOKUPOBJ)
				attrval_obj = Sql.GetFirst(
					"SELECT API_NAME FROM SYOBJD WITH (NOLOCK) WHERE OBJECT_NAME='"
					+ str(ObjectName)
					+ "' AND LOOKUP_OBJECT='"
					+ str(lookupval)
					+ "' and  LOOKUP_API_NAME='"
					+ str(LOOKUPAPI)
					+ "'"
				)
				api_name = attrval_obj.API_NAME.strip()
				NEWVAL = NEWVAL.split("|")
				result = ScriptExecutor.ExecuteGlobal(
					"SYPARCEFMA", {"Object": ObjectName, "API_Name": api_name, "API_Value": NEWVAL[0]},
				)
				new_value_dict = {API_Names["API_NAME"]: API_Names["FORMULA_RESULT"] for API_Names in result}
				lookup_ObjName = ""
				if len(lookupval) == 1:
					lookup_ObjName = lookupval[0]
				else:
					lookup_ObjName = lookupval[1]
				segment_rec_id = Product.GetGlobal("segment_rec_id")

		sec_str += '<div class="col-md-12" id="alert_msg"  style="display: none;"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio10" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert_notifcatio10" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"   ><label ><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error"> <span></span></label></div></div></div>'

		if objr_obj is not None and len(objr_obj) > 0:
			canedit = str(objr_obj.CAN_EDIT)

		editclick = "mtrlEDIT(this)"
		cancelclick = "mtrlCancel()"
		saveclick = "mtrlSAVE()"
		lookup_popup = "mtrlTree_lookup_popup(this)"
		if str(SECTION_EDIT) == "" and str(MODE) == "EDIT":
			section_edit_obj = Sql.GetFirst(
				"SELECT top 1000 SYSECT.* FROM SYSECT WITH (NOLOCK) INNER JOIN SYSEFL (NOLOCK) ON SYSECT.RECORD_ID = SYSEFL.SECTION_RECORD_ID INNER JOIN SYOBJD (NOLOCK) ON SYSEFL.API_NAME = SYOBJD.OBJECT_NAME AND SYSEFL.API_NAME = SYOBJD.API_NAME WHERE SYSECT.PRIMARY_OBJECT_NAME='"
				+ str(ObjectName)
				+ "' AND SYSECT.SAPCPQ_ATTRIBUTE_NAME not in ('SYSECT-SE-00035','SYSECT-MA-00396','SYSECT-MA-00465','SYSECT-MA-00466') and SYSECT.SAPCPQ_ATTRIBUTE_NAME like '%"
				+ str(crnt_prd_val)
				+ "%' AND SYOBJD.PERMISSION <> 'READ ONLY' ORDER BY abs(SYSECT.DISPLAY_ORDER)"
			)
			if section_edit_obj is not None:
				SECTION_EDIT = str(section_edit_obj.SAPCPQ_ATTRIBUTE_NAME)
				api_name = SECTION_EDIT
		get_user_id = Session["USERID"]
		if str(TreeParentParam) == "Translations":
			QStr1 = (
				"SELECT top 1000 SYSECT.* FROM SYSECT WITH (NOLOCK) WHERE SYSECT.PRIMARY_OBJECT_NAME='"
				+ str(ObjectName)
				+ "'  AND SAPCPQ_ATTRIBUTE_NAME not in ('SYSECT-MA-00413','SYSECT-MA-00414','SYSECT-MA-00415') and SYSECT.SAPCPQ_ATTRIBUTE_NAME like '%"
				+ str(crnt_prd_val)
				+ "%' ORDER BY abs(SYSECT.DISPLAY_ORDER)"
			)

		QStr1 = (
			"SELECT top 1000 SYSECT.* FROM SYSECT WITH (NOLOCK)   WHERE SYSECT.PRIMARY_OBJECT_NAME='"
			+ str(ObjectName)
			+ "'   AND SYSECT.SAPCPQ_ATTRIBUTE_NAME not in ('SYSECT-SE-00035','SYSECT-MA-00396','SYSECT-MA-00497') and SYSECT.SAPCPQ_ATTRIBUTE_NAME like '%"
			+ str(crnt_prd_val)
			+ "%' ORDER BY abs(SYSECT.DISPLAY_ORDER)"
		)
		Trace.Write("else part")

		canedit = "TRUE"
		Trace.Write("QStr1-->" + str(QStr1))
		section_obj = Sql.GetList(QStr1)
		for sec in section_obj:
			sec_rec_id = str(sec.SAPCPQ_ATTRIBUTE_NAME)
			b = "sec_" + str(sec_rec_id)
			a = "g4 " + str(sec_rec_id)
			#Trace.Write("sec_rec_id1---------->" + str(sec_rec_id))
			#Trace.Write("sec_rec_id2---------->" + str(b))
			#Trace.Write("sec_rec_id3---------->" + str(a))
			editable_permission = "FALSE"
			if SECTION_EDIT != "":
				if str(sec.SAPCPQ_ATTRIBUTE_NAME) != str(SECTION_EDIT):
					MODE = "SEC_VIEW"
				else:
					MODE = "EDIT"

			QuStr = (
				"SELECT TOP 1000 A.SOURCE_DATA, A.FIELD_LABEL, A.RECORD_ID, A.API_NAME, A.DATA_TYPE, A.PERMISSION, A.FORMULA_DATA_TYPE, A.LOOKUP_API_NAME, A.LOOKUP_OBJECT,A.REQUIRED,A.DECIMALS FROM SYOBJD A WITH (NOLOCK) "
				+ " JOIN SYSEFL Q WITH (NOLOCK) ON A.API_NAME = Q.API_FIELD_NAME  WHERE Q.API_NAME = '"
				+ str(ObjectName)
				+ "' AND Q.SECTION_RECORD_ID = '"
				+ str(sec.RECORD_ID)
				+ "' AND A.OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
				+ sNotInCondition
				+ " ORDER BY ABS(Q.DISPLAY_ORDER)"
			)
			
			data_obj = Sql.GetList(QuStr)

			API_NAMES = ",".join(str(data.API_NAME) for data in data_obj if data.DATA_TYPE != "DATE")
			for data in data_obj:
				if data.PERMISSION != "READ ONLY":
					editable_permission = "TRUE"
				if data.DATA_TYPE == "DATE" or str(data.API_NAME) == "EXCHANGE_RATE_DATE":
					if text == "":
						text = "CONVERT(VARCHAR(10)," + str(data.API_NAME) + ",101) AS " + str(data.API_NAME)
					else:
						text = text + "," + "CONVERT(VARCHAR(10)," + str(data.API_NAME) + ",101) AS " + str(data.API_NAME)
					API_NAMES = API_NAMES + "," + ",".join(str(data) for data in text.split(","))
			sec_str += '<div id="container" class="wdth100 ' + str(a) + '"  >'

			Trace.Write(
				"""
										SELECT
											SYSECT.*
										FROM
											SYSECT (NOLOCK)

											WHERE
											SYSECT.SAPCPQ_ATTRIBUTE_NAME='{Section_Rec_Id}'
											ORDER BY SYSECT.DISPLAY_ORDER
											""".format(
					Section_Rec_Id=sec.RECORD_ID
				)
			)
			action_visible_obj = Sql.GetFirst(
				"""
										SELECT top 1
											SYPRSN.*,SYSECT.DISPLAY_ORDER
										FROM
											SYPRSN (NOLOCK) JOIN SYSECT ON SYSECT.RECORD_ID = SYPRSN.SECTION_RECORD_ID
										JOIN
											USERS_PERMISSIONS (NOLOCK) ON USERS_PERMISSIONS.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID
										WHERE
											SYPRSN.SECTION_RECORD_ID='{Section_Rec_Id}' AND
											USERS_PERMISSIONS.USER_ID='{User_Record_Id}' AND
											SYPRSN.EDITABLE = 0
											ORDER BY
											SYSECT.DISPLAY_ORDER
											""".format(
					Section_Rec_Id=sec.RECORD_ID, User_Record_Id=get_user_id
				)
			)

			'''action_visible_obj = Sql.GetFirst("""
										SELECT
											SYSECT.*
										FROM
											SYSECT (NOLOCK)

										WHERE
											SYSECT.RECORD_ID='{Section_Rec_Id}'
											ORDER BY SYSECT.DISPLAY_ORDER
										""".format(Section_Rec_Id=sec.RECORD_ID))'''
			if action_visible_obj is not None:
				if str(action_visible_obj.SECTION_RECORD_ID):
					action_visible_str = str(action_visible_obj.SECTION_RECORD_ID)
			

			if editable_permission == "TRUE":
				sec_str += (
					'<div onclick="dyn_main_sec_collapse_arrow(this)"class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down collapsed" data-toggle="collapse" data-target=".'
					+ str(b)
					+ '"><label class="onlytext"><div>'
				)
				sec_not_list = [
					"SYSECT-MA-00019",
					"SYSECT-MA-00407",
					"SYSECT-MA-00023",
					"SYSECT-MA-00410",
					"SYSECT-MA-00416",
					"SYSECT-MA-00417",
					"SYSECT-MA-00418",
					"SYSECT-MA-00419",
					"SYSECT-CA-00106",
					"SYSECT-CA-00012",
					"SYSECT-CA-00013",
					"SYSECT-CA-00014",
					"SYSECT-MA-00460",
					"SYSECT-MA-00461",
					"SYSECT-MA-00429",
					"SYSECT-MA-00497",
				]  
				if action_visible_str:
					sec_not_list.append(action_visible_str)
				
				if (MODE == "SEC_VIEW" or MODE == "VIEW") and str(sec.SAPCPQ_ATTRIBUTE_NAME) not in sec_not_list:

					sec_str += (
						'<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
						+ str(sec.SAPCPQ_ATTRIBUTE_NAME)
						+ '" class="dropdown-item" href="#" onclick="'
						+ str(editclick)
						+ '">EDIT</a></li></ul></div></div>'
					)
				sec_str += str(sec.SECTION_NAME) + "</div></label> </div>"
			else:

				sec_str += (
					'<div onclick="dyn_main_sec_collapse_arrow(this)"  class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down collapsed" data-toggle="collapse" data-target="#'
					+ str(b)
					+ '"><label class="onlytext"><div>'
					+ str(sec.SECTION_NAME)
					+ "</div></label></div>"
				)

			sec_str += '<div id="' + str(b) + '" class="collapse in ' + str(b) + '"><table  class="ma_width_marg">'
			sec_str += auto_field
			query_value = Sql.GetFirst(
				"SELECT * FROM SYOBJD WITH (NOLOCK) WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			autoNumber = query_value.API_NAME
			try:
				script = (
					"SELECT * FROM " + str(ObjectName) + " (NOLOCK) WHERE " + str(autoNumber) + " = '" + str(RECORD_ID) + "'"
				)
				Custom_obj = Sql.GetFirst(script)
			except:
				script = (
					"SELECT * FROM " + str(ObjectName) + " (NOLOCK) WHERE " + str(autoNumber) + " = '" + str(RECORD_ID) + "'"
				)
				Custom_obj = Sql.GetFirst(script)

			if data_obj is not None:
				for val in data_obj:
					readonly = "readonly"
					disable = "disabled"
					current_obj_api_name = val.API_NAME.strip()
					current_obj_field_lable = val.FIELD_LABEL.strip()
					readonly_val = val.PERMISSION.strip()
					data_type = val.DATA_TYPE.strip()
					Deciaml_Value = val.DECIMALS
					formula_data_type = ""
					if str(val.FORMULA_DATA_TYPE) != "" and len(str(val.FORMULA_DATA_TYPE)) > 0:
						formula_data_type = val.FORMULA_DATA_TYPE
					else:
						formula_data_type = ""
					erp_source = str(val.SOURCE_DATA)
					current_obj_value = ""
					header_obj_value = ""
					datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
					ids = ""
					add_style = ""
					idval = ""
					edit_warn_icon = ""
					formula_permission = ""
					formula_obj_permission = ""
					left_float = ""
					id_val = ""
					id_api = ""
					priceclass_val = ""
					keypressval = ""
					current_obj_value12 = ""
					ERP_MAMAAT_CHECK = ""
					datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"
					Trace.Write("LAST current object value" + str(current_obj_api_name))
					if Custom_obj is not None:
						Trace.Write(
							"str(current_obj_api_name) 11111111111----- >"
							+ str(current_obj_api_name)
							+ " ------- >str(current_obj_value)00"
							+ str(current_obj_value)
						)
						current_obj_value = eval(
							str("Custom_obj." + str(current_obj_api_name).encode("ascii", "ignore")).strip()
						)

						try:
							current_obj_value = str(current_obj_value)

						except UnicodeEncodeError:
							current_obj_value = current_obj_value

						except:
							Trace.Write("Error")
					if str(current_obj_api_name).upper() == "CPQTABLEENTRYMODIFIEDBY":
						
						if current_obj_value != "":
							current_obj_value = Sql.GetFirst(
								"select USERNAME from users where id = " + str(current_obj_value)
							).USERNAME
					if action_visible_str:
						# edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					elif (
						readonly_val.upper() != "READ ONLY"
						and data_type != "AUTO NUMBER"
						and erp_source != "ERP"
						and canedit.upper() == "TRUE"
					):
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					elif readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER":
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					else:
						edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'

					"""## Hide the Price adjustment currency exchange rate from PASPAL object only code starts..
					if (str(current_obj_api_name) == "PRCADJCUR_EXCHANGE_RATE_DATE") and str(ObjectName) == "PASPAL" and Custom_obj is not None:
						add_style = "display:none"
					## Hide the Price adjustment currency exchange rate from PASPAL object only code end.."""
					if len(current_obj_value) > 0:
						current_obj_value = current_obj_value

					else:
						current_obj_value = ""

					if current_obj_api_name in lookup_val:
						for key, value in lookup_list.items():
							if key == current_obj_api_name:
								ids = value.strip()
					if current_obj_api_name in lookup_val:
						formula_obj_permission = "true"
						for key, value in lookup_list1.items():
							if key == current_obj_api_name:
								formula_permission_qry = Sql.GetFirst(
									"SELECT * FROM SYOBJD WITH (NOLOCK) WHERE API_NAME = '"
									+ str(value)
									+ "' and OBJECT_NAME = '"
									+ str(ObjectName)
									+ "' "
								)
								formula_permission = str(formula_permission_qry.PERMISSION).strip()
				   
					if readonly_val == "READ ONLY":
						if (
							formula_obj_permission == "true"
							and formula_permission != "READ ONLY"
							and canedit.upper() == "TRUE"
						):
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							if str(current_obj_api_name) == "AGMREV_ID" or "PRICEAGREEMENT_ID" or "STP_ACCOUNT_ID":
								edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							if MODE == "EDIT":
								readonly = ""
								disable = ""

								if (str(current_obj_api_name) == "COUNTRY") and str(ObjectName) == "PAACSP":
									edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
								readonly = "readonly"
								disable = "disabled"
						else:
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							readonly = "readonly"
							disable = "disabled"
					elif MODE == "EDIT":
						# str(ERP_MAMAAT_CHECK).upper() == 'TRUE'
						if canedit.upper() == "TRUE":
							if erp_source != "ERP":
								edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
								# jira 8180 start
								if str(current_obj_api_name) == "AGMREV_ID":
									edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
								# Trace.Write("612")
								# jira 8180 end
								readonly = ""
								disable = ""
							else:
								edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
								readonly = "readonly"
								disable = "disabled"
						else:
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							readonly = "readonly"
							disable = "disabled"
						if (
							str(ERP_MAMAAT_CHECK).upper() == "TRUE"
							and str(current_obj_api_name) == "ATTRIBUTE_NAME"
							and str(ObjectName) == "MAMAAT"
						):
							readonly = "readonly"
							disable = "disabled"
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'


					if data_type == "LOOKUP":
						add_style = "display: none;"

					displaynoneList = [
						"SAP_DESCRIPTION",
						"MATERIAL_NAME",
						"ACCOUNT_ID",
						"PRICEAGREEMENT_ID",
						"PRICEAGREEMENT_NAME",
						"AGMREV_ID" "ACCOUNT_NAME",
						"STP_ACCOUNT_ID",
					]
					if current_obj_api_name in displaynoneList and str(TreeSuperParentParam) != "Revisions":  ###6110 ends...
						add_style = "display: none;"
					#### SEGMENT REVISION MIGRATION CODE ENDS...
					if current_obj_api_name == "MODMTH_RECORD_ID" and str(NEWVAL) != "":
						current_obj_value = str(NEWVAL[0])
						

					Trace.Write(
						"DISPLAY_CURRENCY_METHOD------------>"
						+ str(current_obj_value12)
						+ "str(current_obj_value)"
						+ (current_obj_value)
					)

					imagefunction = "imagePopupFunction('" + current_obj_value + "')"
					segment_rec_id = Product.GetGlobal("segment_rec_id")
					
					#### SEGMENT REVISION MIGRATION CODE START...
					valuestr = Sql.GetFirst(
						"SELECT GIFTCARD_LPBS_RECORD_ID,MERCHANDISE_LPBS_ID,OTHER_LPBS_RECORD_ID FROM PASGRV WITH (NOLOCK) WHERE PRICEAGREEMENT_RECORD_ID='"
						+ str(segment_rec_id)
						+ "'"
					)
					if valuestr is not None:
						if str(valuestr.GIFTCARD_LPBS_RECORD_ID) is not None:
							gift = str(valuestr.GIFTCARD_LPBS_RECORD_ID)
							val1 = gift.split("-")
							test = val1[0]
							valuestrGift = Sql.GetFirst(
								"SELECT PRICEMODEL_ID FROM PRPRMD WITH (NOLOCK)WHERE INC_BURDEN_IN_SEGMENT_PRICE='True' and PRICEMODEL_ID = '"
								+ str(test)
								+ "'"
							)
							# 9622 START
							if valuestrGift is not None and str(current_obj_api_name) == "DEF_GIFTC_BURDEN_FACTOR":
								add_style = ""
							else:
								if str(current_obj_api_name) == "DEF_GIFTC_BURDEN_FACTOR":
									add_style = ""
							# 9622 END
						if str(valuestr.MERCHANDISE_LPBS_ID) is not None:
							merchant = str(valuestr.MERCHANDISE_LPBS_ID)
							val1 = merchant.split("_")
							merchant_val = val1[0]
							valuestrmercahnt = Sql.GetFirst(
								"SELECT PRICEMODEL_ID FROM PRPRMD WITH (NOLOCK) WHERE INC_BURDEN_IN_SEGMENT_PRICE='True' and PRICEMODEL_ID = '"
								+ str(merchant_val)
								+ "'"
							)
							if valuestrmercahnt is not None and str(current_obj_api_name) == "DEF_MERCH_BURDEN_FACTOR":
								add_style = ""
							else:
								if str(current_obj_api_name) == "DEF_MERCH_BURDEN_FACTOR":
									add_style = ""
						if str(valuestr.OTHER_LPBS_RECORD_ID) is not None:
							other_pb = str(valuestr.OTHER_LPBS_RECORD_ID)
							val1 = other_pb.split("-")
							other_pb_val = val1[0]
							valuestrpb = Sql.GetFirst(
								"SELECT PRICEMODEL_ID FROM PRPRMD WITH (NOLOCK) WHERE INC_BURDEN_IN_SEGMENT_PRICE='True' and PRICEMODEL_ID = '"
								+ str(other_pb_val)
								+ "'"
							)
							if valuestrpb is not None and str(current_obj_api_name) == "DEF_OTHER_BURDEN_FACTOR":
								add_style = ""
							else:
								if str(current_obj_api_name) == "DEF_OTHER_BURDEN_FACTOR":
									add_style = ""
					noneList = ["AGMREV_ID", "ACCOUNT_NAME"]
					if str(ObjectName) == "PASACS" and (str(current_obj_api_name)) in noneList:
						add_style = "display: none;"
					if str(current_obj_api_name) in [
						"POINTS_CURRENCY_EXC_RATE",
						"POINTS_CURRENCY_EXC_RATE_DATE",
						"POINTS_CURRENCY",
						"CURRENCY_TO_POINT_VALUE",
						"CURRENCY_TO_POINT_FACTOR",
						"HIDE_POINTS_INCATALOG",
					]:
						if str(current_obj_value12).upper() == "CURRENCY":
							add_style = "display:none"
							current_obj_value = ""
						else:
							add_style = ""
					"""if str(current_obj_api_name) in ("DISPLAY_CURRENCY")
						if str(current_obj_value12).upper() == "POINTS":
							add_style = "display:none"
							current_obj_value = "" """
					sec_str += (
						'<tr class="iconhvr brdbt" id="'
						+ str(current_obj_api_name)
						+ '" style="  '
						+ str(add_style)
						+ '"><td class="width350"><label class="pad5mrgbt0">'
						+ str(current_obj_field_lable)
						+ '</label></abbr></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="'
						+ str(current_obj_field_lable)
						+ '" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i>'
					)
					if val.REQUIRED == "True" or val.REQUIRED == "1":
						sec_str += ""
						sec_str += '<span class="req-field mrg3fltltmt7"  >*</span>'
						sec_str += "</a>" + str(Mandatory) + "</td>"
					# Trace.Write(
					#     "current_obj_api_name"
					#     + str(current_obj_api_name)
					#     + "data_type"
					#     + str(data_type)
					#     + "formula_data_type"
					#     + str(formula_data_type)
					# )
					if data_type == "AUTO NUMBER":
						if current_obj_value == "":
							if RECORD_ID.startswith(ObjectName):
								current_obj_value = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
						current_obj_value = CPQID.KeyCPQId.GetCPQId(str(ObjectName), str(current_obj_value))

						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" disabled></td>'
						)
						auto_field = (
							'<tr style="display: none;" class="iconhvr brdbt" style=" '
							+ str(add_style)
							+ '"><td class="width350"><label class="pad5mrgbt0">'
							+ str(current_obj_field_lable)
							+ '</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="'
							+ str(current_obj_field_lable)
							+ '" class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i><td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" disabled></td><tr>'
						)

					elif data_type == "LONG TEXT AREA":
						if str(ObjectName) == "CAMAIM" and str(current_obj_api_name) == "IMAGE_URL":
							sec_str += (
								'<td><a  onclick="'
								+ imagefunction
								+ '" class="form-control related_popup_css hgt100wth100" id="'
								+ str(current_obj_api_name)
								+ '" data-target="#image_view_popup" data-toggle="modal" ><img src="'
								+ current_obj_value
								+ '" height="100" width="100" ></a></td>'
							)
						else:
							sec_str += (
								'<td><textarea class="form-control related_popup_css txtArea" id="'
								+ str(current_obj_api_name)
								+ '" rows="1" cols="100" '
								+ disable
								+ ">"
								+ current_obj_value
								+ "</textarea></td>"
							)

					elif data_type == "LOOKUP":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" ></td>'
						)
					elif data_type == "FORMULA" and MODE == "EDIT" and formula_data_type != "CHECKBOX":
						Log.Info(str(lookup_val) + "354--------formaula" + str(current_obj_value))
						if current_obj_api_name in lookup_val and str(readonly) != "readonly":
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="text" value="'
								+ current_obj_value
								+ '" class="form-control lookupBg related_popup_css fltlt"  readonly>'
							)
							# jira 8180 start
							#Trace.Write("current_obj_api_name" + str(current_obj_api_name))
							if str(current_obj_api_name) != "AGMREV_ID":
								sec_str += (
									'<input class="popup fltlt" id="'
									+ str(ids)
									+ '" onclick="'
									+ str(lookup_popup)
									+ '"   type="image" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif"></td>'
								)
							# jira 8180 end
						else:
							if str(formula_data_type) == "TEXT" and str(readonly) != "readonly":
								sec_str += (
									'<td><input id="'
									+ str(current_obj_api_name)
									+ '" type="text" value="'
									+ current_obj_value
									+ '" class="form-control related_popup_css fltlt" style=" '
									+ str(left_float)
									+ ' ">'
									+ str(edit_warn_icon)
									+ "</td>"
								)
							else:
								if str(current_obj_api_name) == "PRICEMODEL_ID" and ObjectName == "PRPBMA":
									sec_str += (
										'<td><input id="'
										+ str(current_obj_api_name)
										+ '_VALUE" type="text" value="'
										+ current_obj_value
										+ '" class="form-control related_popup_css fltlt" style=" '
										+ str(left_float)
										+ ' " disabled>'
										+ str(edit_warn_icon)
										+ "</td>"
									)
								else:
									sec_str += (
										'<td><input id="'
										+ str(current_obj_api_name)
										+ '" type="text" value="'
										+ current_obj_value
										+ '" class="form-control related_popup_css fltlt" style=" '
										+ str(left_float)
										+ ' " disabled>'
										+ str(edit_warn_icon)
										+ "</td>"
									)
					elif data_type == "CHECKBOX":
						if current_obj_api_name == "INC_INTERNATL_CHARGE_INFREIGHT":
							current_obj_value = "1"
						if str(current_obj_value).upper() == "TRUE" or current_obj_value == "1":
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="'
								+ str(data_type)
								+ '" value="'
								+ current_obj_value
								+ '" class="custom" '
								+ disable
								+ ' checked><span class="lbl"></span></td>'
							)
						else:
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="'
								+ str(data_type)
								+ '" value="False" class="custom" '
								+ disable
								+ '><span class="lbl"></span></td>'
							)
					elif data_type == "FORMULA" and formula_data_type == "CHECKBOX":
						if str(current_obj_value).upper() == "TRUE" or current_obj_value == "1":
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="CHECKBOX" value="'
								+ current_obj_value
								+ '" class="custom" '
								+ disable
								+ ' checked><span class="lbl"></span></td>'
							)
						else:
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="CHECKBOX" value="False" class="custom" '
								+ disable
								+ '><span class="lbl"></span></td>'
							)

					elif data_type == "PICKLIST":
						if ObjectName == "MAMAFC":
							if MODE == "EDIT":
								select_drop_css = "height: 28px;"
							else:
								select_drop_css = "border: 0;height: 28px;"
							if str(current_obj_api_name) == "COUNTRIES":
								Sql_Countries = Sql.GetList(
									"select COUNTRY_NAME FROM SACTRY WITH (NOLOCK) where COUNTRY_NAME != ''"
								)
								Check_Country = 0
								Countries_List = []
								for cont in Sql_Countries:
									Check_Country = 1
									Countries_List.append(cont.COUNTRY_NAME)
								if len(Countries_List) != 0:
									Countries_List.insert(0, "ALL COUNTRIES")
								sec_str += (
									'<td class="posrelclr555" onclick="showCheckboxes()"><select id="select_id" value="'
									+ current_obj_value
									+ '" type="text" class="form-control related_popup_css fltltfnt13"   '
									+ disable
									+ ' > "add" </select><input id="'
									+ str(current_obj_api_name)
									+ '" style="'
									+ select_drop_css
									+ ' background-color: #fff;" class="inp_val" type="text" disabled />'
								)
								sec_str += '<div id="checkboxes" class="chxcust16"  style="display: none; ">'
								Selected_Countries = Sql.GetFirst(
									"select INC_COUNTRY_TEMPLATES,COUNTRIES FROM MAMAFC WITH (NOLOCK) where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID = '"
									+ str(RECORD_ID)
									+ "'"
								)
								Sel_Coun_qry = Sql.GetList(
									"select COUNTRIES FROM MAMAFC WITH (NOLOCK) where MATERIAL_RECORD_ID = '"
									+ str(mat_rec_id)
									+ "' and COUNTRY_RECORD_ID = '"
									+ str(coun_rec_id)
									+ "'"
								)
								Sel_Coun_list = [ins.COUNTRIES for ins in Sel_Coun_qry]
								Selected_Countries_List = []
								if len(str(Selected_Countries.COUNTRIES)) > 0:
									Selected_Countries_List = (Selected_Countries.COUNTRIES).split(",")
								Selected_Countries_List = Selected_Countries_List + Sel_Coun_list
								if "ALL COUNTRIES" not in Selected_Countries_List:
									for req in Countries_List:
										if str(req).upper() in Selected_Countries_List:
											sec_str += (
												'<label><input checked = "checked" type="checkbox" onchange="labelDropdown(this)" class="'
												+ str(req).upper()
												+ '" />'
												+ str(req).upper()
												+ "</label>"
											)
										else:
											sec_str += (
												'<label><input  type="checkbox" onchange="labelDropdown(this)" class="'
												+ str(req).upper()
												+ '" />'
												+ str(req).upper()
												+ "</label>"
											)
								else:
									for req in Countries_List:
										sec_str += (
											'<label><input  checked = "checked" type="checkbox" onchange="labelDropdown(this)" class="'
											+ str(req).upper()
											+ '" />'
											+ str(req).upper()
											+ "</label>"
										)
								sec_str += "</div></td>"
							elif str(current_obj_api_name) == "INC_COUNTRY_TEMPLATES":
								sec_str += (
									'<td onclick="Default_Checkboxes()"><select id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ current_obj_value
									+ '" type="text" class="form-control related_popup_css fltltfnt13"   '
									+ disable
									+ " >"
								)
								Selected_Countries = Sql.GetFirst(
									"select INC_COUNTRY_TEMPLATES,COUNTRIES FROM MAMAFC WITH (NOLOCK) where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID = '"
									+ str(RECORD_ID)
									+ "'"
								)
								sec_str += "<option></option>"
								sec_str += "</select></td>"
						else:
							sec_str += "<td>"
							if str(current_obj_api_name) == "DISPLAY_CURRENCY_METHOD":
								sec_str += (
									'<select id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ current_obj_value
									+ '" type="text" onchange="Currency12()" class="form-control pop_up_brd_rad related_popup_css fltltfnt13"    '
									+ disable
									+ " >"
								)
							#### SEGMENT REVISION MIGRATION CODE START...
							elif str(TreeParam) == "Price Model" and CurrentTab == "Price Agreement":
								if str(current_obj_api_name) == "USE_SYSTEM_GOLD_BASE":
									onchange_txt = "GoldMetal()"
								elif str(current_obj_api_name) == "HOLD_CUSTOM_GOLD_BASE":
									onchange_txt = "holdgoldvalue()"
								elif str(current_obj_api_name) == "USE_SYSTEM_SILVER_BASE":
									onchange_txt = "SilverMetal()"
								elif str(current_obj_api_name) == "HOLD_CUSTOM_SILVER_BASE":
									onchange_txt = "holdsilvervalue()"
								elif (
									str(current_obj_api_name) == "MERCHANDISE_MARKET_TYPE"
									or str(current_obj_api_name) == "MERCHANDISE_MODEL_TYPE"
								):
									onchange_txt = "MerchandiseClear()"
								elif (
									str(current_obj_api_name) == "GIFTCARD_MARKET_TYPE"
									or str(current_obj_api_name) == "GIFTCARD_MODEL_TYPE"
								):
									onchange_txt = "GiftCardClear()"
								elif str(current_obj_api_name) == "OTHER_MARKET_TYPE or OTHER_MODEL_TYPE":
									onchange_txt = "OtherProductClear()"
								sec_str += (
									'<select id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ current_obj_value
									+ '" type="text" onchange="'
									+ str(onchange_txt)
									+ '" class="form-control pop_up_brd_rad related_popup_css fltltfnt13"  '
									+ disable
									+ " >"
								)
							else:
								sec_str += (
									'<select id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ current_obj_value
									+ '" type="text" class="form-control pop_up_brd_rad related_popup_css fltltfnt13" '
									+ disable
									+ " >"
								)
							#### SEGMENT REVISION MIGRATION CODE ENDS...
							Sql_Quality_Tier = Sql.GetFirst(
								"select PICKLIST_VALUES FROM SYOBJD WITH (NOLOCK) where OBJECT_NAME='"
								+ str(ObjectName)
								+ "' and DATA_TYPE='PICKLIST' and API_NAME = '"
								+ str(current_obj_api_name)
								+ "' "
							)

							if (
								str(Sql_Quality_Tier.PICKLIST_VALUES).strip() is not None
								and str(Sql_Quality_Tier.PICKLIST_VALUES).strip() != ""
							):
								Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
								for req1 in Tier_List:
									if current_obj_value == req1:
										sec_str += "<option selected>" + str(req1) + "</option>"
									else:
										sec_str += "<option>" + str(req1) + "</option>"
							else:
								sec_str += "<option selected>" + str(current_obj_value) + "</option>"
							sec_str += "</select></td>"
					elif data_type == "DATE" and MODE == "EDIT":
						date_field.append(current_obj_api_name)
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" value="'
							+ current_obj_value
							+ '" type="text"  onclick="'
							+ str(datepicker)
							+ '" onchange="'
							+ str(datepicker_onchange)
							+ '" class="form-control datePickerField wth157fltltbrdbt"   '
							+ disable
							+ " ></td>"
						)
					elif data_type == "NUMBER" and str(current_obj_api_name) not in (
						"DEF_COMM_CONCESSION_FACTOR",
						"COMM_CONCESSION_FACTOR",
						"MERCHANDISE_INVOICE_MERCH_PRIADJ",
						"GIFTCARD_INVOICE_PRIADJ",
						"OTHER_INVOICE_PRIADJ",
						"DEF_MERCH_BURDEN_FACTOR",
						"DEF_GIFTC_BURDEN_FACTOR",
						"DEF_OTHER_BURDEN_FACTOR",
						"MERCHANDISE_BURDEN_FACTOR",
						"GIFTCARD_BURDEN_FACTOR",
						"OTHER_BURDEN_FACTOR",
					):
						# A043S001P01-9752 - End
						# A043S001P01-9760 - Start
						""" if str(current_obj_api_name) == 'SYSTEM_GOLD_BASE':
							#current_obj_value = str(currecy_Symbol_qry.SYMBOL) + ' ' +str(SYSTEM_GOLD_BASE_VALUE.SYSTEMBASE_VALUE)
							current_obj_value = str(currecy_Symbol_qry.SYMBOL) + ' ' +"{:.3f}".format(SYSTEM_GOLD_BASE_VALUE.SYSTEMBASE_VALUE)
						elif str(current_obj_api_name) == 'SYSTEM_SILVER_BASE':
							#current_obj_value = str(SYSTEM_SILVER_BASE_VALUE.SYSTEMBASE_VALUE)
							current_obj_value = "{:.3f}".format(SYSTEM_SILVER_BASE_VALUE.SYSTEMBASE_VALUE) """
						# A043S001P01-9760 - End
						txtonchange = ""
						if str(current_obj_api_name) in (
							"POINTRANGE_ADJUSTMENT_FACTOR",
							"MIN_START_POINTS",
							"MAX_START_POINT",
						):
							txtonchange = "pointcal()"
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="number" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" onchange="'
							+ txtonchange
							+ '"'
							+ disable
							+ "></td>"
						)
					#### SEGMENT REVISION MIGRATION CODE ENDS...
					elif data_type == "FORMULA" and formula_data_type == "NUMBER":
						# A043S001P01-9760 - Start
						""" if str(current_obj_api_name) == 'SPOT_GOLD_PRICE_CALC':
							current_obj_value = str(MARKET_GPA_UNITS_VALUE)
							Trace.Write("formulanumber")
						if str(current_obj_api_name) == 'SPOT_SILVER_PRICE_CALC':
							current_obj_value = str(MARKET_SPA_UNITS_VALUE)
							Trace.Write("formulnumberformulanumer") """
						# A043S001P01-9760 - End
						"""if str(current_obj_api_name) in ["SPOT_GOLD_PRICE_CALC","CUSTOM_GPA_UNITS","ADJ_TOMKT_GPAUNITS"]:
							Trace.Write("current_obj_api_namecurrent_obj_api_namecurrent_obj_api_namecurrent_obj_api_name------------>"+str(current_obj_api_name))
							Trace.Write("current_obj_valuegold------------>"+str(current_obj_value))
							Trace.Write("aaaaaaaaamode------->"+str(MODE))
							if(current_obj_value is not None and current_obj_value != ""):
								current_obj_value_float = float(current_obj_value)
								current_obj_value_round = round(current_obj_value_float)
								current_obj_value = str(current_obj_value_round)
								Trace.Write("cccccccccccccccccc"+str(current_obj_value_round))
								#current_obj_value_int = int(current_obj_value_round)
								#Trace.Write("ccccccccccccccccccint"+str(current_obj_value_int))
								#current_obj_value = str(current_obj_value_int)
								Trace.Write("customobjvalueeeeeeee"+str(current_obj_value))
						if str(current_obj_api_name) in ["SPOT_SILVER_PRICE_CALC","CUSTOM_SPA_UNITS","ADJ_TOMKT_SPAUNITS"]:
							if(current_obj_value is not None and current_obj_value != ""):
								current_obj_value_float = float(current_obj_value)
								current_obj_value_round = round(current_obj_value_float,0)
								current_obj_value_int = int(current_obj_value_round)
								current_obj_value = str(current_obj_value_int)
								Trace.Write("current_obj_valuesilver------------>"+str(current_obj_value))"""
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="number" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ "></td>"
						)
						# start---7797
					elif data_type == "TEXT":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ "></td>"
						)
					elif data_type == "FORMULA" and formula_data_type == "TEXT":
						# 9738 start
						if Custom_obj and str(current_obj_api_name) == "SALESORG_NAME" and str(ObjectName) == "PAACSO":
							var = str(Custom_obj.SALESORG_ID)
							SOR_ID = Sql.GetFirst("select SALESORG_NAME from SASORG where SALESORG_ID = '" + str(var) + "'")
							if SOR_ID is not None and str(SOR_ID) != "":
								current_obj_value = str(SOR_ID.SALESORG_NAME)
							else:
								current_obj_value = ""
						# 9738 end
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ "></td>"
						)
						# end---7797
					elif str(formula_data_type) == "DATE" and str(current_obj_api_name) == "POINTS_CURRENCY_EXC_RATE_DATE":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ "></td>"
						)
					elif data_type == "CURRENCY":
						curr_symbol = ""
						decimal_val = 3
						cur_api_name = Sql.GetFirst(
							"select CURRENCY_INDEX from SYOBJD WITH (NOLOCK) where API_NAME = '"
							+ str(current_obj_api_name)
							+ "' and OBJECT_NAME = '"
							+ str(ObjectName)
							+ "' and DATA_TYPE = 'CURRENCY' "
						)
						
						if str(cur_api_name) is not None:
							curr_symbol_obj = Sql.GetFirst(
								"select SYMBOL,DECIMAL_PLACES,CURRENCY from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select "
								+ str(cur_api_name.CURRENCY_INDEX)
								+ " from "
								+ str(ObjectName)
								+ " where "
								+ str(autoNumber)
								+ " = '"
								+ str(RECORD_ID)
								+ "' ) "
							)
							if curr_symbol_obj is not None:
								if curr_symbol_obj != "":
									curr_symbol = curr_symbol_obj.CURRENCY

									decimal_val = curr_symbol_obj.DECIMAL_PLACES
							if current_obj_value != "" and decimal_val != "":
								formatting_string = "{0:." + str(decimal_val) + "f}"
								current_obj_value = formatting_string.format(float(current_obj_value))
						curr_span_open = ""
						curr_span_close = ""
						if current_obj_value is not None:
							if current_obj_value != "":
								curr_span_open = "<span style='display: flex;align-items: center;'>" + str(curr_symbol)
								curr_span_close = "</span>"
								# current_obj_value = curr_symbol + "" + current_obj_value
								current_obj_value = current_obj_value + " " + curr_symbol
						"""sec_str += (
							'<td>'+curr_span_open+'<input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ ">"+curr_span_close+"</td>"
						)"""
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ "></td>"
						)
					elif str(formula_data_type) == "PERCENT" or data_type == "PERCENT":
						nCom_Con_Fact = None
						if str(current_obj_api_name) == "DEF_COMM_CONCESSION_FACTOR":

							nCom_Con_Fact = Sql.GetFirst(
								"SELECT STP.COMM_CONCESSION_FACTOR AS CCF FROM SAACNT AS STP INNER JOIN PASGMT AS SGM ON SGM.STP_ACCOUNT_ID = STP.ACCOUNT_ID WHERE SGM.PRICEAGREEMENT_RECORD_ID ='"
								+ str(segment_rec_id)
								+ "'"
							)
							
							if nCom_Con_Fact is not None:
								current_obj_value = str(nCom_Con_Fact.CCF)

						if current_obj_value == "" and current_obj_api_name == "COMM_CONCESSION_FACTOR":
							nCom_Con_Fact = Sql.GetFirst(
								"SELECT STP.COMM_CONCESSION_FACTOR AS CCF FROM SAACNT AS STP INNER JOIN PASGMT AS SGM ON SGM.STP_ACCOUNT_ID = STP.ACCOUNT_ID WHERE SGM.PRICEAGREEMENT_RECORD_ID ='"
								+ str(segment_rec_id)
								+ "'"
							)
							
							if nCom_Con_Fact is not None:
								current_obj_value = str(nCom_Con_Fact.CCF)

						if current_obj_value:

							my_format = "{:." + str(Deciaml_Value) + "f}"
							current_obj_value = str(my_format.format(round(float(current_obj_value), int(Deciaml_Value))))

						symbol = " %"
						data_type = "text"
						if (
							MODE == "EDIT"
							or current_obj_value == ""
							or current_obj_value == "0.000"
							or current_obj_value is None
						):
							symbol = ""
							data_type = "number"
							if current_obj_value == "0.000":
								current_obj_value = ""
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ data_type
							+ '" value="'
							+ current_obj_value
							+ symbol
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)

					elif data_type == "NUMBER" or data_type == "CURRENCY":
						if current_obj_value:
							my_format = "{:." + str(Deciaml_Value) + "f}"
							current_obj_value = str(my_format.format(round(float(current_obj_value), int(Deciaml_Value))))
						symbol = " "
						data_type = "text"
						if MODE == "EDIT" or current_obj_value == "":
							symbol = ""
							data_type = "number"
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ data_type
							+ '" value="'
							+ current_obj_value
							+ symbol
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)

					elif (
						data_type == "PERCENT"
						or str(formula_data_type) == "PERCENT"
						and ObjectName == "PASGRV"
						and current_obj_api_name
						in ("MERCHANDISE_INVOICE_MERCH_PRIADJ", "GIFTCARD_INVOICE_PRIADJ", "OTHER_INVOICE_PRIADJ")
					):
						symbol = " %"
						data_type = "text"
						if MODE == "EDIT" or current_obj_value == "":
							symbol = ""
							data_type = "number"
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ data_type
							+ '" value="'
							+ current_obj_value
							+ symbol
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)
					elif (
						data_type == "PERCENT"
						or str(formula_data_type) == "PERCENT"
						and ObjectName == "PASACS"
						and current_obj_api_name
						in (
							"DEF_MERCH_BURDEN_FACTOR",
							"DEF_GIFTC_BURDEN_FACTOR",
							"DEF_OTHER_BURDEN_FACTOR",
							"MERCHANDISE_BURDEN_FACTOR",
							"GIFTCARD_BURDEN_FACTOR",
							"OTHER_BURDEN_FACTOR",
						)
					):
						symbol = " %"
						data_type = "text"
						if MODE == "EDIT" or current_obj_value == "":
							symbol = ""
							data_type = "number"
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ data_type
							+ '" value="'
							+ current_obj_value
							+ symbol
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)
					elif (
						str(current_obj_api_name) == "DEF_COMM_CONCESSION_FACTOR"
						or str(current_obj_api_name) == "COMM_CONCESSION_FACTOR"
					):
						DataType = "text"
						ValPercentage = "  %"
						nCom_Con_Fact = None
						if str(current_obj_api_name) == "DEF_COMM_CONCESSION_FACTOR":
							nCom_Con_Fact = Sql.GetFirst(
								"SELECT STP.COMM_CONCESSION_FACTOR AS CCF FROM SAACNT AS STP INNER JOIN PASGMT AS SGM ON SGM.STP_ACCOUNT_ID = STP.ACCOUNT_ID WHERE SGM.PRICEAGREEMENT_RECORD_ID ='"
								+ str(segment_rec_id)
								+ "'"
							)
							if nCom_Con_Fact is not None:
								current_obj_value = str(nCom_Con_Fact.CCF)

						if current_obj_value == "" and current_obj_api_name == "COMM_CONCESSION_FACTOR":
							nCom_Con_Fact = Sql.GetFirst(
								"SELECT STP.COMM_CONCESSION_FACTOR AS CCF FROM SAACNT AS STP INNER JOIN PASGMT AS SGM ON SGM.STP_ACCOUNT_ID = STP.ACCOUNT_ID WHERE SGM.PRICEAGREEMENT_RECORD_ID ='"
								+ str(segment_rec_id)
								+ "'"
							)
							if nCom_Con_Fact is not None:
								current_obj_value = str(nCom_Con_Fact.CCF)

						if MODE == "EDIT" and current_obj_api_name == "COMM_CONCESSION_FACTOR":
							readonly = disable = add_style = ""
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						if MODE == "EDIT":
							DataType = "number"
							ValPercentage = ""
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ DataType
							+ '" value="'
							+ current_obj_value
							+ ValPercentage
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)
					#### SEGMENT REVISION MIGRATION CODE ENDS...
					else:
						if str(current_obj_api_name) == "PRICEMODEL_ID" and ObjectName == "PRPBMA":
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '_VALUE" type="text" value="'
								+ current_obj_value
								+ '" class="form-control related_popup_css" style="'
								+ str(left_float)
								+ ' " '
								+ disable
								+ ">"
								+ str(edit_warn_icon)
								+ "</td>"
							)
						elif str(current_obj_api_name) == "SET_NAME" and ObjectName == "MASETS":
							Trace.Write(
								"IN SET_NAME : ObjectName : "
								+ str(ObjectName)
								+ " current_obj_value : "
								+ str(current_obj_value)
							)
							set_tab_name = "Sets"
							sec_str += (
								'<td><a id="'
								+ str(RECORD_ID)
								+ "|"
								+ str(set_tab_name)
								+ '" onclick="Move_to_parent_obj(this)" >'
								+ current_obj_value
								+ "</a></td>"
							)
						elif str(current_obj_api_name) == "SETMAT_NAME" and ObjectName == "MAVARM":
							Trace.Write(
								"IN SETMAT_NAME : ObjectName : "
								+ str(ObjectName)
								+ " current_obj_value : "
								+ str(current_obj_value)
							)
							set_tab_name = "Sets"
							set_record_id = Sql.GetFirst(
								"SELECT SET_RECORD_ID FROM MAVARM WHERE SET_MATERIAL_RECORD_ID ='" + str(RECORD_ID) + "'"
							)
							sec_str += (
								'<td><a id="'
								+ str(set_record_id.SET_RECORD_ID)
								+ "|"
								+ str(set_tab_name)
								+ '" onclick="Move_to_parent_obj(this)" >'
								+ current_obj_value
								+ "</a></td>"
							)
						else:
							if current_obj_value != "":
								if str(current_obj_api_name).upper() == "CPQTABLEENTRYMODIFIEDBY" and ObjectName != "PASATG":
									if str(current_obj_value) != "":
										current_obj_value = SqlHelper.GetFirst(
											"select USERNAME from users where USERNAME = " + str(current_obj_value) + ""
										).USERNAME
										# current_obj_value1 = str(current_obj_value1)
								sec_str += (
									'<td><input id="'
									+ str(current_obj_api_name)
									+ '" type="text" value="'
									+ current_obj_value
									+ '" class="form-control related_popup_css" style="'
									+ str(left_float)
									+ ' " '
									+ disable
									+ ">"
									+ str(edit_warn_icon)
									+ "</td>"
								)
							else:
								sec_str += (
									'<td><input id="'
									+ str(current_obj_api_name)
									+ '" type="text" value="'
									+ current_obj_value
									+ '" class="form-control related_popup_css" style="'
									+ str(left_float)
									+ ' " '
									+ disable
									+ ">"
									+ str(edit_warn_icon)
									+ "</td>"
								)  # 9707 end
					Trace.Write(
						"pick1" + str(edit_pencil_icon) + "   --- current_obj_api_name is >" + str(current_obj_api_name)
					)
					sec_str += (
						'<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick">'
						+ str(edit_pencil_icon)
						+ "</a></div></td>"
					)
					sec_str += "</tr>"
			sec_str += "</table></div>"
			sec_str += "</div>"


		returnList = []
		returnList = eval(Product.GetGlobal("MtrlTreeList"))
		self.recur_func(returnList, RECORD_ID)
		ret_value = str(Product.GetGlobal("MtrlTreeListNodeId"))
		Trace.Write("new_value_dict------------> " + str(dict(new_value_dict)))
	   #Trace.Write(sec_str)
		# 9709 start
		Trace.Write("Count" + str(Count_val))
		return sec_str, date_field, new_value_dict, api_name, ret_value, Count_val
		# 9709 end

	def recur_func(self, test, key):
		for d_data in test:
			if "nodes" in d_data.keys():
				if d_data.get("id") == key:
					Trace.Write(d_data)
					Product.SetGlobal("MtrlTreeListNodeId", str(d_data.get("nodeId")))
				else:
					self.recur_func(d_data.get("nodes"), key)
			else:
				if d_data.get("id"):
					if d_data.get("id") == key:
						Trace.Write(d_data)
						Product.SetGlobal("MtrlTreeListNodeId", str(d_data.get("nodeId")))
		return "true"

	def tree_node_func(self, Tnodes, key, obj):
		for d_data in Tnodes:
			if "nodes" in d_data.keys():
				if d_data.get("id") == key and d_data.get("obj") == obj:
					Trace.Write(d_data)
					Product.SetGlobal("MtrlTreeListNodeId", str(d_data.get("nodeId")))
				else:
					self.tree_node_func(d_data.get("nodes"), key, obj)
					Trace.Write(d_data)
			else:
				if d_data.get("id") and d_data.get("obj"):
					if d_data.get("id") == key and d_data.get("obj") == obj:
						Trace.Write(d_data)
						Product.SetGlobal("MtrlTreeListNodeId", str(d_data.get("nodeId")))
		return "true"

	def tree_node_text_func(self, Tnodes, key, obj, nodeCount):
		for d_data in Tnodes:
			if "nodes" in d_data.keys():
				if d_data.get("text") == str(key) and d_data.get("obj") == obj and d_data.get("parnt") == "Catalog Products":
					Trace.Write(d_data)
					Nnodeid = int(d_data.get("nodeId")) + nodeCount
					Product.SetGlobal("MtrlTreeListNodeId", str(Nnodeid))
					break
				else:
					self.tree_node_text_func(d_data.get("nodes"), key, obj, nodeCount)
					Trace.Write(d_data)
			else:
				if d_data.get("text") and d_data.get("obj"):
					if (
						d_data.get("text") == str(key)
						and d_data.get("obj") == obj
						and d_data.get("parnt") == "Catalog Products"
					):
						Trace.Write(d_data)
						Nnodeid = int(d_data.get("nodeId")) + nodeCount
						Product.SetGlobal("MtrlTreeListNodeId", str(Nnodeid))
						break
		return "true"


ObjSYLDRLDTLS = SYLDRLDTLS()
RECORD_ID = Param.RECORD_ID
Trace.Write(RECORD_ID)

try:
	TreeParam = Param.TreeParam
	TreeParentParam = Param.TreeParentParam
	TreeSuperParentParam = Param.TreeSuperParentParam
	TopSuperParentParam = Param.TopSuperParentParam
	GrandTopSuperParentParam = ""
	GrandGrandTopSuperParentParam = ""
	GrandGrandGrandTopSuperParentParam = ""
except:
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	GrandTopSuperParentParam = Product.GetGlobal("TreeParentLevel3")
	GrandGrandTopSuperParentParam = Product.GetGlobal("TreeParentLevel4")
	GrandGrandGrandTopSuperParentParam = Product.GetGlobal("TreeParentLevel5")
NEWVAL = Param.NEWVAL
LOOKUPOBJ = Param.LOOKUPOBJ
LOOKUPAPI = Param.LOOKUPAPI
MODE = Param.MODE
TableId = Param.TableId
SECTION_EDIT = ""

if MODE == "EDIT":
	SECTION_EDIT = Param.SECTION_EDIT
try:
	Flag = Param.Flag
except:
	Flag = 0
ObjectName = ""
try:
	CTRY = Param.CTRY
except:
	CTRY = ""
Trace.Write(TreeParentParam)

if (
	TableId is not None and TableId != "" and str(TreeParentParam) != "Unpublished" and str(TreeParentParam) != "Published"
):  ###6110 ends...
	
	objr_obj = Sql.GetFirst("select * FROM SYOBJR WITH (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME = '" + str(TableId) + "' ")
	#### SEGMENT REVISION MIGRATION CODE ENDS...
	objr_obj_id = str(objr_obj.OBJ_REC_ID) if objr_obj is not None else ""
	if objr_obj_id is not None:
		objh_obj = Sql.GetFirst("select * FROM SYOBJH WITH (NOLOCK) where RECORD_ID = '" + str(objr_obj_id) + "' ")
		ObjectName = str(objh_obj.OBJECT_NAME) if objh_obj is not None else ""


ApiResponse = ApiResponseFactory.JsonResponse(
	ObjSYLDRLDTLS.MaterialTree(
		MODE, RECORD_ID, ObjectName, TreeParam, NEWVAL, LOOKUPOBJ, LOOKUPAPI, SECTION_EDIT, Flag, TreeSuperParentParam,
	)
)