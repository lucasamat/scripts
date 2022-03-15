"""THIS SCRIPT IS USED TO LOAD THE BANNER, ICON, CPQID CONVERT, REQ FIELD SYMBOL, CURRENCY SYMBOL."""
# =========================================================================================================================================
#   __script_name : SYCONUPDAL.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE BANNER, ICON, CPQID CONVERT, REQ FIELD SYMBOL, CURRENCY SYMBOL
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQ
from datetime import *
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
Sql = SQL()
Param = Param

get_user_id = User.Id
class ConfigUpdateScript:
	"""Configure Update Script."""

	def __init__(self):
		"""Initilize the variable."""
		self.get_user_id = Session["USERID"]
		try:
			TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
			self.product_name = Product.Name
			self.current_tab_name = str(TestProduct.CurrentTab)
		except:
			TestProduct = ""
			self.product_name = "Sales"
			self.current_tab_name = "Quote"
		if Param.CurrentTab == "Quotes":
			self.current_tab_name = "Quote"
		elif Param.CurrentTab == "App":
			self.current_tab_name = "App"
		elif Param.CurrentTab == "Tab":
			self.current_tab_name = "Tab"
		elif Param.CurrentTab == "Page":
			self.current_tab_name = "Page"			
		elif Param.CurrentTab == "Object":
			self.current_tab_name = "Object"
		elif Param.CurrentTab == "Script":
			self.current_tab_name = "Script"
		elif Param.CurrentTab == "Profile":
			self.current_tab_name = "Profile"
		elif Param.CurrentTab == "Role":
			self.current_tab_name = "Role"
		elif Param.CurrentTab == "Currency":
			self.current_tab_name = "Currency"
		elif Param.CurrentTab == "Message":
			self.current_tab_name = "Message"
		elif Param.CurrentTab == "Error Log":
			self.current_tab_name = "Error Log"	
		elif Param.CurrentTab == "Variable":
			self.current_tab_name = "Variable"	
		elif Param.CurrentTab == "My Approval Queue":
			self.current_tab_name = "My Approval Queue"
		elif Param.CurrentTab == "Team Approval Queue":
			self.current_tab_name = "Team Approval Queue"
		else:
			self.current_tab_name = Param.CurrentTab
		Trace.Write("Current_Tab_CHK_J "+str(Param.CurrentTab))
	def get_obj_name(self):
		"""TO DO."""
		CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
		obj_name = ""
		return obj_name

	def build_query(self, column, obj_name, where_string):
		"""TO DO."""
		##A055S000P01-9370 ,A055S000P01-4191 code starts...
		if obj_name == "SAQTMT":
			column = "SAQTRV.TRANSACTION_TYPE,SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID,SAQTRV.QUOTE_ID,SAQTRV.QTEREV_ID,SAQTMT.ACCOUNT_ID,SAQTMT.ACCOUNT_NAME,SAQTRV.CONTRACT_VALID_FROM,SAQTRV.CONTRACT_VALID_TO,SAQTRV.REVISION_STATUS,SAQTRV.SALESORG_ID,SAQTMT.OWNER_NAME,SAQTMT.POES,SAQTMT.LOW,SAQTMT.EXPIRED"
			query_string = """
					SELECT {Column_Name}
					FROM {Table_Name} (NOLOCK)
					INNER JOIN SAQTRV ON  SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID AND SAQTRV.ACTIVE = 1
					WHERE {Where_String}
					""".format(
				Column_Name=column, Table_Name=obj_name, Where_String=where_string
			)
		else:
			query_string = """
					SELECT {Column_Name}
					FROM {Table_Name} (NOLOCK)
					WHERE {Where_String}
					""".format(
				Column_Name=column, Table_Name=obj_name, Where_String=where_string
			)
		##A055S000P01-9370, A055S000P01-4191  code ends..
		return query_string

	def get_value_from_obj(self, record_obj, column):
		"""TO DO."""
		return getattr(record_obj, column, "")

	def get_factor_symbol(self, obj_name):
		"""TO DO."""
		factor_fields_list = []
		factor_fields_obj = Sql.GetList(
			"SELECT FORMAT,FIELD_LABEL FROM  SYOBJD (NOLOCK) WHERE (FORMAT <> '' or FORMAT IS NOT NULL) AND "
			+ " OBJECT_NAME = '{}'".format(obj_name)
		)
		if factor_fields_obj is not None:
			for factor_field_obj in factor_fields_obj:
				if factor_field_obj.FORMAT:
					# <* TABLE ( SELECT DATA_TYPE FROM PRCAFC WHERE PRICEFACTOR_NAME='CONCESSION FACTOR' ) *>
					symbol = "%" if Product.ParseString(factor_field_obj.FORMAT) == "PERCENT" else ""
					if symbol:
						factor_fields_list.append(factor_field_obj.FIELD_LABEL + "|" + symbol)
		return factor_fields_list

	def get_currency_and_decimal_details(self, record_id):
		"""TO DO."""
		decimal_list = []
		currency_symbol_list = []
		factor_fields_list = []
		objh_record_obj = Sql.GetFirst(
			"""
				SELECT
					SYOBJH.OBJECT_NAME
				FROM
					SYTABS (NOLOCK)
				INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.TAB_NAME = SYTABS.TAB_LABEL
				INNER JOIN SYSECT (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID
				INNER JOIN SYOBJS (NOLOCK) ON SYOBJS.OBJ_REC_ID = SYSECT.PRIMARY_OBJECT_RECORD_ID
				INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.RECORD_ID = SYOBJS.OBJ_REC_ID
				WHERE
					SYOBJS.NAME='Tab list' AND
					SYSECT.SECTION_NAME = 'BASIC INFORMATION' AND
					SYTABS.SAPCPQ_ALTTAB_NAME = '{}' """.format(
				self.current_tab_name
			)
		)
		if objh_record_obj is not None:
			current_obj_name = self.get_obj_name()
			if not current_obj_name:
				current_obj_name = str(objh_record_obj.OBJECT_NAME)
				objd_records_obj = Sql.GetList(
					"""
						SELECT
							CURRENCY_INDEX,FIELD_LABEL
						FROM
							SYOBJD (NOLOCK)
						WHERE
							(DATA_TYPE='CURRENCY' or FORMULA_DATA_TYPE='CURRENCY') AND ISNULL(CURRENCY_INDEX,'') != ''
							AND OBJECT_NAME = '{}'
						""".format(
						current_obj_name
					)
				)
				factor_fields_list = self.get_factor_symbol(current_obj_name)
		return currency_symbol_list, decimal_list, factor_fields_list

	def banner_content(self, record_id):
		"""TO DO."""
		field_lables, field_values = "", ""
		record_obj = Sql.GetFirst(
			"""
				SELECT
					REPLACE(REPLACE(SYOBJS.COLUMNS,'[',''),']','') as COLUMNS, SYSECT.PRIMARY_OBJECT_RECORD_ID
				FROM
					SYTABS (NOLOCK)
				INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.TAB_NAME = SYTABS.TAB_LABEL
				INNER JOIN SYSECT (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID
				INNER JOIN SYOBJS (NOLOCK) ON SYOBJS.OBJ_REC_ID = SYSECT.PRIMARY_OBJECT_RECORD_ID
				WHERE
					SYOBJS.NAME='Header list' AND
					SYTABS.SAPCPQ_ALTTAB_NAME = '{}' """.format(
				self.current_tab_name
			)
		)
		if record_obj is not None:
			columns = (record_obj.COLUMNS).replace("'", "").replace(" ", "").split(",")
			table_name = ""
			##A055S000P01-9370 ,A055S000P01-4191 code starts..
			
			if self.current_tab_name == "Quote":
				objd_records_obj = Sql.GetList(
					"""
						SELECT TOP 10
							DISPLAY_ORDER,FIELD_LABEL, OBJECT_NAME
						FROM
							SYOBJD (NOLOCK)
						WHERE API_NAME IN %s AND OBJECT_NAME IN ('SAQTMT','SAQTRV')  ORDER BY abs(DISPLAY_ORDER) """
					% (tuple(columns),)
				)
			else:
				objd_records_obj = Sql.GetList(
					"""
						SELECT TOP 10
							DISPLAY_ORDER,FIELD_LABEL, OBJECT_NAME
						FROM
							SYOBJD (NOLOCK)
						WHERE API_NAME IN %s AND PARENT_OBJECT_RECORD_ID ='%s'  ORDER BY abs(DISPLAY_ORDER) """
					% (tuple(columns), record_obj.PRIMARY_OBJECT_RECORD_ID)
				)
			##A055S000P01-9370 , A055S000P01-4191 code ends..
			# Trace.Write(
			# 	""" SELECT TOP 10 DISPLAY_ORDER,FIELD_LABEL, OBJECT_NAME FROM SYOBJD (NOLOCK) WHERE API_NAME IN %s
			# 		AND PARENT_OBJECT_RECORD_ID ='%s'  ORDER BY abs(DISPLAY_ORDER) """
			# 	% (tuple(columns), record_obj.PRIMARY_OBJECT_RECORD_ID)
			# )
			if objd_records_obj is not None:
				labels = []
				for index, objd_record in enumerate(objd_records_obj):
					if index == 0:
						table_name = objd_record.OBJECT_NAME
					# if str(objd_record.FIELD_LABEL) == "Approval Object ID" and table_name == "ACAPMA":
					# 	Getdynamiclable = Sql.GetFirst(
					# 		"""SELECT SYOBJH.RECORD_NAME,SYOBJH.OBJECT_NAME FROM SYOBJH(NOLOCK)
					# 		INNER JOIN {table_name}(NOLOCK) ON {table_name}.APROBJ_LABEL = SYOBJH.LABEL
					# 		WHERE {key_column} = '{record_id}' """.format(
					# 			record_id=str(record_id), table_name=str(table_name), key_column=str(columns[0])
					# 		)
					# 	)
					# 	dynamicLable = Sql.GetFirst(
					# 		"""SELECT FIELD_LABEL  FROM SYOBJD
					# 			WHERE OBJECT_NAME = '{objname}' AND IS_KEY = 'TRUE' """.format(
					# 			objname=str(Getdynamiclable.OBJECT_NAME)
					# 		)
					# 	)
					# 	labels.append(dynamicLable.FIELD_LABEL)
					# else:
					labels.append(objd_record.FIELD_LABEL)
				##A055S000P01-9370 , A055S000P01-4191 code starts...
				if self.current_tab_name == "Quote":
					field_lables = "Key,Quote ID,Active Revision ID,Account ID,Account Name,Contract Valid From,Contract Valid To,Revision status,Sales Org ID,Quote owner,Transaction Type,POES,LOW,Expired"
				else:
					field_lables = ",".join(labels)
				##A055S000P01-9370, A055S000P01-4191 code ends..
			#Trace.Write("selftab"+str(self.current_tab_name))
			"""if str(self.current_tab_name.upper()) == "QUOTE": 
				key_column = "MASTER_TABLE_QUOTE_RECORD_ID"
			else:
				key_column = columns[0]"""
			key_column = columns[0]
			if table_name == 'CTCNRT' and (self.product_name != "SYSTEM ADMIN" and self.product_name != "APPROVAL CENTER"):
				record_id = Quote.GetGlobal("contract_record_id")
			##A055S000P01-9370 , A055S000P01-4191 code starts..
			if table_name == 'SAQTMT':
				getQuote = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT WHERE QUOTE_ID ='{}'".format(Quote.CompositeNumber))
				record_id = getQuote.MASTER_TABLE_QUOTE_RECORD_ID
				key_column = "SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID"
			##A055S000P01-9370, A055S000P01-4191  code ends..
			Trace.Write("columns_chk_j "+str(columns))
			if key_column and record_id:
				query_string = self.build_query(
					column=",".join(columns),
					obj_name=table_name,
					where_string="{Column} = '{Value}'".format(Column=key_column, Value=record_id),

				)
				# if table_name == "ACAPCH":
				# 	quer = Sql.GetFirst(query_string)
				# 	Trace.Write("querrr"+str(query_string))
				# 	field_values = [quer.APPROVAL_CHAIN_RECORD_ID]
				# 	if field_values == "FALSE":
				# 		field_values = "INACTIVE"
				# 	else:
				# 		field_values == "TRUE"
				# 		field_values = "ACTIVE"					
				# else:	
				field_values = Sql.GetFirst(query_string)
				# vallist = [field_values.APPROVAL_CHAIN_RECORD_ID, field_values.APPROVAL_METHOD, field_values.APRCHN_ID, field_values.APRCHN_NAME, field_values.APRCHN_STATUS]
				# if table_name == "ACAPCH":
				# 	Trace.Write("999"+str(vallist[4]))
				# 	if vallist[4] == True:					
				# 		vallist[4] = 'ACTIVE'
				Trace.Write(" field_lables "+str(field_lables)+"field_values "+str(field_values))
		return field_lables, field_values

	def get_attributes_permission_details(self):
		"""TO DO."""
		result = []
		if str(self.current_tab_name.upper()) != "":
			get_object_name = """
				SELECT
					SYOBJS.CONTAINER_NAME, SYOBJS.CAN_EDIT, SYTABS.RECORD_ID FROM SYTABS INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.TAB_RECORD_ID = SYTABS.RECORD_ID INNER JOIN SYSECT(NOLOCK) ON
					SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID INNER JOIN SYOBJS (NOLOCK) ON SYOBJS.OBJ_REC_ID =
					SYSECT.PRIMARY_OBJECT_RECORD_ID
				WHERE
					SYOBJS.NAME = 'Tab list' AND
					SYSECT.SECTION_NAME = 'BASIC INFORMATION' AND

					SYTABS.SAPCPQ_ALTTAB_NAME = '{0}' """.format(
				self.current_tab_name
			)
		object_name = Sql.GetFirst(get_object_name)
		if object_name is not None:
			tab_record_id = str(object_name.RECORD_ID)
			#A055S000P01-3428 start-section level access
			get_section_edit_access = """
				SELECT
					DISTINCT SYSECT.RECORD_ID,SP.EDITABLE FROM SYSECT (NOLOCK)
					INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID
					INNER JOIN SYTABS (NOLOCK) ON SYTABS.RECORD_ID = SYPAGE.TAB_RECORD_ID  INNER JOIN SYPRSN SP ON
					SP.SECTION_RECORD_ID = SYSECT.RECORD_ID INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID =
					SP.PROFILE_RECORD_ID
				WHERE
					SP.VISIBLE = 1 AND
					SYSECT.PRIMARY_OBJECT_NAME = '{0}' AND
					SYPAGE.TAB_RECORD_ID = '{1}' AND UP.USER_ID = '{2}'""".format(
				object_name.CONTAINER_NAME, tab_record_id, str(User.Id)
			)
			#A055S000P01-3428 -section level access-end
			'''get_section_edit_access = """
				SELECT
					DISTINCT SYSECT.RECORD_ID FROM SYSECT (NOLOCK)
					INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID
					INNER JOIN SYTABS (NOLOCK) ON SYTABS.RECORD_ID = SYPAGE.TAB_RECORD_ID
				WHERE
					SYSECT.PRIMARY_OBJECT_NAME = '{0}' AND
					SYPAGE.TAB_RECORD_ID = '{1}' """.format(
			object_name.CONTAINER_NAME, tab_record_id)'''
			
			#Trace.Write("get_section_edit_access : " + get_section_edit_access)
			section_edit_access_list = Sql.GetList(get_section_edit_access)
			if section_edit_access_list is not None:
				for section_edit_access in section_edit_access_list:
					#section_write_access = section_edit_access.EDITABLE
					'''objd_records_obj_query = """
						SELECT
							DISTINCT SYOBJD.OBJECT_NAME, SYOBJD.FIELD_LABEL, SYOBJD.PERMISSION
							FROM SYOBJD (NOLOCK)
							INNER JOIN SYSECT (NOLOCK) ON SYSECT.PRIMARY_OBJECT_NAME = SYOBJD.OBJECT_NAME
							INNER JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID
							AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME

						WHERE

							SYSECT.RECORD_ID = '{0}' AND
							SYSEFL.SECTION_RECORD_ID = '{0}'
							""".format(
						section_edit_access.RECORD_ID
					)'''
					objd_records_obj_query = """
							SELECT
								DISTINCT SYOBJD.OBJECT_NAME, SYOBJD.FIELD_LABEL,case when SYOBJD.EDITABLE_ONINSERT ='TRUE' then 'EDITABLE' Else 'READ ONLY' end AS PERMISSION,SYPRSF.EDITABLE
								FROM SYOBJD (NOLOCK)
								INNER JOIN SYSECT (NOLOCK) ON SYSECT.PRIMARY_OBJECT_NAME = SYOBJD.OBJECT_NAME
								INNER JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID
								INNER JOIN SYPRSF (NOLOCK) ON SYPRSF.SECTIONFIELD_RECORD_ID = SYSEFL.RECORD_ID
								INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID
								AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME

							WHERE

								SYSECT.RECORD_ID = '{0}' AND UP.USER_ID ='{1}' AND
								SYSEFL.SECTION_RECORD_ID = '{0}'
								""".format(
							section_edit_access.RECORD_ID, str(User.Id)
						)
					objd_records_obj = Sql.GetList(objd_records_obj_query)
					if objd_records_obj is not None:
						for objd_record in objd_records_obj:
							#if section_write_access == 1 and str(object_name.CAN_EDIT).upper != "FALSE":
							if str(object_name.CAN_EDIT).upper != "FALSE":
								access = str(objd_record.PERMISSION).upper()
							elif str(objd_record.OBJECT_NAME) == "cpq_permissions" and str(objd_record.FIELD_LABEL) in ['Profile ID','Profile Name']:
								access = str(objd_record.PERMISSION).upper()
							else:
								access = "READ ONLY"
							result.append(objd_record.OBJECT_NAME + "|" + objd_record.FIELD_LABEL + "|" + access)
							# Trace.Write(
							# 	"ACCESS : " + (objd_record.OBJECT_NAME + "|" + objd_record.FIELD_LABEL + "|" + access)
							# )
		return result

	def get_required_fields(self):
		"""TO DO."""
		fields_list = []
		objd_records_obj = Sql.GetList(
			"""
				SELECT
					SYOBJD.FIELD_LABEL
				FROM
					SYTABS (NOLOCK)
				INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.TAB_NAME = SYTABS.TAB_LABEL
				INNER JOIN SYSECT (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID
				INNER JOIN  SYOBJD (NOLOCK) ON  SYOBJD.OBJECT_NAME = SYSECT.PRIMARY_OBJECT_NAME
				WHERE SYTABS.SAPCPQ_ALTTAB_NAME = '{}' AND SYSECT.SECTION_NAME = 'BASIC INFORMATION' AND
				SYOBJD.REQUIRED = 'TRUE'
				""".format(
				self.current_tab_name
			)
		)
		if objd_records_obj is not None:
			fields_list = [objd_record.FIELD_LABEL for objd_record in objd_records_obj]

		return fields_list

	def get_cpqid(self):
		"""TO DO."""
		attr_name = ""
		cpq_record_id = ""
		if self.current_tab_name != "APP":
			qstn_obj = Sql.GetFirst(
				"""
					SELECT
						SYOBJH.OBJECT_NAME, SYSEFL.RECORD_ID, SYSEFL.FIELD_LABEL,SYSEFL.SAPCPQ_ATTRIBUTE_NAME
					FROM
						SYAPPS (NOLOCK)
					JOIN
						SYTABS (NOLOCK) ON SYTABS.APP_LABEL = SYAPPS.APP_LABEL
					JOIN
						SYPAGE (NOLOCK) ON SYPAGE.TAB_RECORD_ID = SYTABS.RECORD_ID
					JOIN
						SYSECT (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID
					JOIN
						SYOBJH (NOLOCK) ON SYOBJH.OBJECT_NAME = SYSECT.PRIMARY_OBJECT_NAME
					JOIN
						SYSEFL (NOLOCK) ON SYSEFL.API_NAME = SYOBJH.OBJECT_NAME AND SYSEFL.SECTION_RECORD_ID =
						SYSECT.RECORD_ID
					WHERE
						SYAPPS.APP_LABEL LIKE '%{}%' AND SYTABS.SAPCPQ_ALTTAB_NAME = '{}' AND SYSECT.SECTION_NAME =
						'BASIC INFORMATION'
						AND SYSEFL.FIELD_LABEL = 'Key'
					""".format(
					self.product_name, self.current_tab_name
				)
			)
			if qstn_obj is not None:
				if self.current_tab_name != "APP" and self.current_tab_name!= 'Quote'and self.current_tab_name!= 'Contract' :
					qstn_record_id = str(qstn_obj.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
					attr_name = "QSTN_{}".format(qstn_record_id)
					#Trace.Write("---attr_name----" + attr_name + "--------" + str(qstn_obj.OBJECT_NAME))
					if Product.Attributes.GetByName(attr_name):
						key_value = Product.Attributes.GetByName(attr_name).GetValue()
						#cpq_record_id = str(key_value)
						if str(qstn_obj.OBJECT_NAME) != "cpq_permissions":
							cpq_record_id = CPQ.KeyCPQId.GetCPQId(str(qstn_obj.OBJECT_NAME), str(key_value))
						else:
							cpq_record_id = str(key_value)
					else:
						key_value = ""
						cpq_record_id = ""
				elif self.current_tab_name == 'Quote' or self.current_tab_name == 'Contract':
					getQuote = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT WHERE QUOTE_ID = '{}'".format(Quote.CompositeNumber))

					key_value = getQuote.MASTER_TABLE_QUOTE_RECORD_ID
					#cpq_record_id = str(key_value)
					if str(qstn_obj.OBJECT_NAME) != "cpq_permissions":
						cpq_record_id = CPQ.KeyCPQId.GetCPQId(str(qstn_obj.OBJECT_NAME), str(key_value))
					else:
						cpq_record_id = str(key_value)
					
		return attr_name, cpq_record_id

	def restrict_section_level_edit(self):
		"""TO DO."""
		action_visible_obj = ""
		res=""
		mmtab_obj = Sql.GetFirst(
			"""
				SELECT
					RECORD_ID
				FROM
					SYTABS (NOLOCK)
				WHERE
					LTRIM(RTRIM(SYTABS.SAPCPQ_ALTTAB_NAME)) = '{Tab_Text}' AND
					LTRIM(RTRIM(SYTABS.APP_LABEL)) = '{APP_LABEL}'
				""".format(
				Tab_Text=self.current_tab_name, APP_LABEL=self.product_name
			)
		)
		if mmtab_obj is not None:
			#section based restrictions
			SYSECTs_obj = Sql.GetList(
				"""
					SELECT
						SYSECT.RECORD_ID
					FROM
						SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID
						JOIN SYPRSN (NOLOCK) SP  ON SP.SECTION_RECORD_ID =
							SYSECT.RECORD_ID JOIN
							USERS_PERMISSIONS UP on Up.Permission_id = SP.PROFILE_RECORD_ID
					WHERE
						LTRIM(RTRIM(SYPAGE.TAB_RECORD_ID)) = '{Tab_Rec_Id}' and SP.VISIBLE = 1 AND Up.USER_ID = '{get_user_id}' 
					""".format(
					Tab_Rec_Id=mmtab_obj.RECORD_ID,get_user_id = get_user_id
				)
			)
			if SYSECTs_obj is not None:
				section_id_list = ""
				
				Trace.Write("Price")
				section_ids = [SYSECT.RECORD_ID for SYSECT in SYSECTs_obj]
				if len(section_ids) == 1:
					section_id_list = "('" + str(section_ids[0]) + "')"
				else:
					section_id_list = tuple(section_ids)
				#return [SYSECT.RECORD_ID for SYSECT in SYSECTs_obj]
				action_visible_obj = Sql.GetList(
					"""
						SELECT
							SYSECT.*
						FROM
							SYSECT (NOLOCK) JOIN SYPRSN (NOLOCK) SP  ON SP.SECTION_RECORD_ID =
							SYSECT.RECORD_ID
						JOIN
							USERS_PERMISSIONS UP on Up.Permission_id = SP.PROFILE_RECORD_ID
						WHERE
							SP.EDITABLE = 0 AND Up.USER_ID = '%s' AND
							SYSECT.RECORD_ID IN %s
						"""
					% (get_user_id, section_id_list)
				)
				'''action_visible_obj = Sql.GetList(
					"""
						SELECT
							*
						FROM
							SYPSAC (NOLOCK)
						WHERE SECTION_RECORD_ID IN %s
						"""
					% (section_id_list,)
				)'''
				
				#if action_visible_obj is not None:
					#for record in action_visible_obj:
				Trace.Write('At 453')
				res=[record.RECORD_ID for record in action_visible_obj]
				Trace.Write('##res--->'+str(res))
		return res
		#return []

	#This Function validate recall button is required or not for quote specific.
	def recall_button_validate(self):
		try:
			getRevision = Sql.GetFirst("SELECT QUOTE_REVISION_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(Quote.CompositeNumber))
			quote_revision_record_id = getRevision.QUOTE_REVISION_RECORD_ID
			getQuote = Sql.GetFirst("SELECT COUNT(SAQTMT.OWNER_NAME) AS CNT FROM SAQTMT (NOLOCK) JOIN SAQTRV (NOLOCK) ON SAQTMT.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID WHERE SAQTRV.QUOTE_REVISION_RECORD_ID='{}' AND SAQTMT.OWNER_NAME='{}' AND SAQTRV.REVISION_STATUS='{}'".format(quote_revision_record_id,User.Name,'APR-REJECTED'))
			return getQuote.CNT
		except:
			pass
	
	def ConfiguratorCall(self, keyData_val):
		"""TO DO."""
		try:
			getval = Product.GetGlobal("ApprovalMasterRecId")
		except:
			getval = ""
		Trace.Write('At line 464')
		BannerContent = self.banner_content(keyData_val)
		Trace.Write('At line 466')
		EditLockIcon = self.get_attributes_permission_details()
		Trace.Write('At line 468')
		CpqIdConvertion = self.get_cpqid()
		Trace.Write('At line 470')
		RequiredFieldSymbol = self.get_required_fields()
		Trace.Write('At line 472')
		CurrencySymbol = self.get_currency_and_decimal_details(keyData_val)
		Trace.Write('At line 474')
		restrict_section_edit = self.restrict_section_level_edit()
		Trace.Write('At line 476')
		# This function call only add recall button if Quote Owner & User are same.
		recall_button_flag = self.recall_button_validate()

		return BannerContent, EditLockIcon, CpqIdConvertion, RequiredFieldSymbol, CurrencySymbol,restrict_section_edit, recall_button_flag

configobj = ConfigUpdateScript()

if hasattr(Param, "keyData_val"):
	keyData_val = Param.keyData_val
	# Changes for sales app primary banner load - start
	if not keyData_val:
		try:
			quote_obj = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID,QTEREV_RECORD_ID FROM SAQTMT(NOLOCK) WHERE QUOTE_ID ='{}'".format(Quote.CompositeNumber))
			if quote_obj:
				keyData_val = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
				quote_revision_record_id = quote_obj.QTEREV_RECORD_ID
		except Exception:
			pass
	# Changes for sales app primary banner load - End
	ApiResponse = ApiResponseFactory.JsonResponse(configobj.ConfiguratorCall(keyData_val))

