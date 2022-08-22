# =========================================================================================================================================
#   __script_name : SYPVSAVALL.PY
#   __script_description :  THIS SCRIPT IS USED TO SAVE DATA WHEN IN CREATE AND EDIT MODE IN A PIVOT TABLE.
#   __primary_author__ : SENTHIL NATHAN
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
Sql = SQL()

LABLE = list(Param.LABLE)
VALUE = list(Param.VALUE)
TABLEID = (Param.TABLEID).strip()
KEYS = list(Param.KEYS)
COL_VAL = list(Param.COL_VAL)
keys_col = zip(KEYS, COL_VAL)
Set_type = str(Product.Attributes.GetByName("QSTN_SYSEFL_MA_00077").GetValue())
MaterialContainer = Product.GetContainerByName("CTR_MATERIALS_PIVOT_TABLE")
Recodrid = ""
Recodrid = VALUE[0]
oper = VALUE[0]
sap_number = ""
result = ""
next_id = ""
row = dict(zip(LABLE, VALUE))
keys_col = zip(KEYS, COL_VAL)


if Recodrid == "":
	if TABLEID == "SYSEFL-MA-00382":
		# Log.Info('row TABLEID---- '+str(dict(row)))
		next_id = Sql.GetFirst("SELECT CONVERT(VARCHAR(4000),NEWID()) AS RECORD_ID")

		if next_id is not None and next_id != "":
			new_val = str(next_id.RECORD_ID)
			# Log.Info('The new record_id is here----MASMAV '+str(new_val))
			# Log.Info('The new SAP_PART_NUMBER is here---MASMAV '+str(row.get('SAP_PART_NUMBER')))
			row1 = {}
			data = {}
			if (
				str(row.get("SAP_PART_NUMBER")) is not None
				and str(row.get("SAP_PART_NUMBER")) != ""
			):
				if not keys_col:
					new_val = str(Guid.NewGuid()).upper()

					row1["VALUE_CODE"] = ""
					row1["ATTRIBUTE_NAME"] = ""
					row1["ATTRIBUTE_TYPE"] = ""
					row1["ATTVAL_RECORD_ID"] = ""
					row1["SETMATATTVAL_RECORD_ID"] = str(new_val)
					row1["SAP_PART_NUMBER"] = str(row.get("SAP_PART_NUMBER"))
					row1["SET_NAME"] = str(row.get("SET_NAME"))
					row1["SET_RECORD_ID"] = str(row.get("SET_RECORD_ID"))
					row1["SETATT_RECORD_ID"] = str(row.get("SETATT_RECORD_ID"))
					row1["SETMAT_RECORD_ID"] = str(row.get("SETMAT_RECORD_ID"))
					row1["SET_TYPE"] = str(row.get("SET_TYPE"))
					row1["SAP_DESCRIPTION"] = row.get("SAP_DESCRIPTION")

					if str(row1):
						Table.TableActions.Create("MASMAV", row1)
				else:
					for rows, val in zip(KEYS, COL_VAL):
						if str(val) == "None":
							val = ""

						if str(val) != "":
							val_cd = Sql.GetFirst(
								"SELECT ATTRIBUTEVALUE_RECORD_ID,ATTRIBUTE_RECORD_ID,ATTRIBUTE_NAME FROM MAATVL (NOLOCK) where ATTRIBUTE_NAME = '{}' and ATTVAL_VALCODE='{}' ".format(
									rows, val
								)
							)

							if val_cd is None:
								new_valmatvl = str(Guid.NewGuid()).upper()

								val_insert = Sql.GetFirst(
									"SELECT ATTRIBUTE_NAME,ATTRIBUTE_RECORD_ID,ATTRIBUTE_TYPE FROM MASTAT (NOLOCK) where ATTRIBUTE_NAME = '{}' ".format(
										rows
									)
								)
								data["ATTRIBUTEVALUE_RECORD_ID"] = str(new_valmatvl)
								data["ATTRIBUTE_RECORD_ID"] = str(
									val_insert.ATTRIBUTE_RECORD_ID
								)
								data["ATTRIBUTE_NAME"] = str(val_insert.ATTRIBUTE_NAME)
								data["ATTVAL_DISPLAYVAL"] = str(val)
								#7936 strat
								data["VALUE_CODE"] = str(val_insert.ATTRIBUTE_NAME)+'_'+str(val)
								#7936 end
								data["ATTRIBUTE_TYPE"] = str(val_insert.ATTRIBUTE_TYPE)
								if str(row1):
									#7936 start
									query = Sql.GetFirst("select top 1 ATTVAL_VALCODE from MAATVL where ATTVAL_VALCODE = '"+str(data["VALUE_CODE"])+"'")
									if query is None and query == '':
										Table.TableActions.Create("MAATVL", data)
									#7936 End
									new_val = str(Guid.NewGuid()).upper()
									row1["VALUE_CODE"] = str(val)
									row1["ATTRIBUTE_NAME"] = str(
										val_insert.ATTRIBUTE_NAME
									)
									row1["ATTVAL_RECORD_ID"] = str(new_valmatvl)
									row1["ATTRIBUTE_TYPE"] = str(
										val_insert.ATTRIBUTE_TYPE
									)
									row1["SETMATATTVAL_RECORD_ID"] = str(new_val)
									row1["SAP_PART_NUMBER"] = str(
										row.get("SAP_PART_NUMBER")
									)
									row1["SET_NAME"] = str(row.get("SET_NAME"))
									row1["SET_RECORD_ID"] = str(
										row.get("SET_RECORD_ID")
									)
									row1["SETATT_RECORD_ID"] = str(
										row.get("SETATT_RECORD_ID")
									)
									row1["SETMAT_RECORD_ID"] = str(
										row.get("SETMAT_RECORD_ID")
									)
									row1["SET_TYPE"] = str(row.get("SET_TYPE"))
									row1["SAP_DESCRIPTION"] = row.get("SAP_DESCRIPTION")
									if str(row1):
										Table.TableActions.Create("MASMAV", row1)

							else:
								new_valmatvl = str(Guid.NewGuid()).upper()
								new_val = str(Guid.NewGuid()).upper()
								row1["VALUE_CODE"] = str(val)
								row1["ATTRIBUTE_NAME"] = str(val_cd.ATTRIBUTE_NAME)
								row1["ATTVAL_RECORD_ID"] = str(new_valmatvl)
								row1["ATTRIBUTE_TYPE"] = str(val_cd.ATTRIBUTE_TYPE)
								row1["SETMATATTVAL_RECORD_ID"] = str(new_val)
								row1["SAP_PART_NUMBER"] = str(
									row.get("SAP_PART_NUMBER")
								)
								row1["SET_NAME"] = str(row.get("SET_NAME"))
								row1["SET_RECORD_ID"] = str(row.get("SET_RECORD_ID"))
								row1["SETATT_RECORD_ID"] = str(
									row.get("SETATT_RECORD_ID")
								)
								row1["SETMAT_RECORD_ID"] = str(
									row.get("SETMAT_RECORD_ID")
								)
								row1["SET_TYPE"] = str(row.get("SET_TYPE"))
								row1["SAP_DESCRIPTION"] = row.get("SAP_DESCRIPTION")
								if str(row1):
									Table.TableActions.Create("MASMAV", row1)

						if str(val) == "":
							new_val = str(Guid.NewGuid()).upper()
							val_insert = Sql.GetFirst(
								"SELECT ATTRIBUTEVALUE_RECORD_ID,ATTRIBUTE_RECORD_ID,ATTRIBUTE_NAME FROM MAATVL (NOLOCK) where ATTRIBUTE_NAME = '{}' ".format(
									rows
								)
							)
							row1["VALUE_CODE"] = ""

							if val_insert is None:
								row1["ATTRIBUTE_NAME"] = str(rows)
								#row1["ATTRIBUTE_TYPE"] = ""
								row1["ATTVAL_RECORD_ID"] = ""
							else:
								row1["ATTRIBUTE_NAME"] = str(val_insert.ATTRIBUTE_NAME)
								#row1["ATTRIBUTE_TYPE"] = str(val_insert.ATTRIBUTE_TYPE)
								row1["ATTVAL_RECORD_ID"] = ""

							row1["SETMATATTVAL_RECORD_ID"] = str(new_val)
							row1["SAP_PART_NUMBER"] = str(row.get("SAP_PART_NUMBER"))
							row1["SET_NAME"] = str(row.get("SET_NAME"))
							row1["SET_RECORD_ID"] = str(row.get("SET_RECORD_ID"))
							row1["SETATT_RECORD_ID"] = str(row.get("SETATT_RECORD_ID"))
							row1["SETMAT_RECORD_ID"] = str(row.get("SETMAT_RECORD_ID"))
							row1["SET_TYPE"] = str(row.get("SET_TYPE"))
							row1["SAP_DESCRIPTION"] = row.get("SAP_DESCRIPTION")
							if str(row1):
								Table.TableActions.Create("MASMAV", row1)

		# To update SET_TYPE in MASMAV Custom Table
		SET_NAME = str(row.get("SET_NAME"))
		if Set_type != "":
			SetType_MASMAV = Sql.GetList(
				"SELECT SET_TYPE FROM MASMAV (NOLOCK) where SET_NAME = '{}'".format(
					SET_NAME
				)
			)
			if SetType_MASMAV is not None:
				result = {}
				tableInfoData = Sql.GetTable("MASMAV")
				for settype in SetType_MASMAV:
					result["SET_TYPE"] = Set_type
					tableInfoData.AddRow(result)
					Sql.Upsert(tableInfoData)

				# To update MAVARM Custom Table
				# row2={}
				# ParMtrl_PartNumber = Product.Attributes.GetByName('QSTN_SYSEFL_MA_00387').GetValue()
				# Material_ID = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION FROM MAMTRL  (NOLOCK) WHERE SAP_PART_NUMBER ='{}'".format(str(row.get('SAP_PART_NUMBER'))))
				# next_id = Sql.GetFirst("SELECT NEWID() AS RECORD_ID")
				# #Log.Info('next_idnext_idnext_idnext_id---MAVARM '+str(next_id.RECORD_ID))
				# if next_id is not None and next_id != '':
				# new_val = str(next_id.RECORD_ID)
				# Trace.Write('new_val '+str(new_val))
				# if str(row.get('SAP_PART_NUMBER')) is not None and str(row.get('SAP_PART_NUMBER')) !="" :
				# row2['SET_MATERIAL_RECORD_ID'] = str(new_val)
				# row2['MATERIAL_RECORD_ID'] = str(Material_ID.MATERIAL_RECORD_ID)
				# row2['SAP_DESCRIPTION'] = str(Material_ID.SAP_DESCRIPTION)
				# row2['SAP_PART_NUMBER'] = str(row.get('SAP_PART_NUMBER'))
				# row2['SET_TYPE'] = str(row.get('SET_TYPE'))
				# row2['SETMAT_NAME'] = str(row.get('SET_NAME'))
				# row2['SET_RECORD_ID'] = str(row.get('SET_RECORD_ID'))
				# row2['SETPAR_MATERIAL_SAP_PART_NUMBER'] = str(ParMtrl_PartNumber)
				# Trace.Write('the new row value is here for MAVARM---- '+str(dict(row2)))
				Table.TableActions.Create("MAVARM", row2)

	else:
		MAMAATRecord = Sql.GetFirst(
			"SELECT B.ATTRIBUTE_RECORD_ID,B.SAP_PART_NUMBER,A.VALUE_CODE FROM MAMAAT B (NOLOCK) inner join MAMAAV A WITH (NOLOCK) ON A.ATTRIBUTE_RECORD_ID = B.ATTRIBUTE_RECORD_ID  where B.ATTRIBUTE_RECORD_ID='"
			+ str(row.get("ATTRIBUTE_RECORD_ID"))
			+ "' and A.SAP_PART_NUMBER = '"
			+ str(row.get("SAP_PART_NUMBER"))
			+ "' AND upper(A.VALUE_CODE)='"
			+ str(row.get("VALUE_CODE")).upper()
			+ "'"
		)
		# Trace.Write(
		# 	"SELECT B.ATTRIBUTE_RECORD_ID,B.SAP_PART_NUMBER,A.VALUE_CODE FROM MAMAAT B (NOLOCK) inner join MAMAAV A WITH (NOLOCK) ON A.ATTRIBUTE_RECORD_ID = B.ATTRIBUTE_RECORD_ID  where B.ATTRIBUTE_RECORD_ID='"
		# 	+ str(row.get("ATTRIBUTE_RECORD_ID"))
		# 	+ "' and A.SAP_PART_NUMBER = '"
		# 	+ str(row.get("SAP_PART_NUMBER"))
		# 	+ "' AND upper(A.VALUE_CODE)='"
		# 	+ str(row.get("VALUE_CODE")).upper()
		# 	+ "'"
		# )

		if MAMAATRecord is None:
			next_id = Sql.GetFirst(
				"SELECT CONVERT(VARCHAR(4000),NEWID()) AS RECORD_ID"
			)
			if next_id is not None and next_id != "":
				new_val = str(next_id.RECORD_ID)
				# Trace.Write(
				# 	str(new_val)
				# 	+ "The new record_id is here "
				# 	+ str(row.get("MATERIAL_RECORD_ID"))
				# )
				row1 = {}
				row1["MATERIAL_ATTRIBUTE_RECORD_ID"] = str(new_val)
				row1["MATERIAL_RECORD_ID"] = str(row.get("MATERIAL_RECORD_ID"))
				row1["SAP_PART_NUMBER"] = str(row.get("SAP_PART_NUMBER"))
				row1["ATTRIBUTE_RECORD_ID"] = str(row.get("ATTRIBUTE_RECORD_ID"))
				row1["ATTRIBUTE_NAME"] = str(row.get("ATTRIBUTE_NAME"))
				#row1["ATTRIBUTE_TYPE"] = str(row.get("ATTRIBUTE_TYPE"))
				#row1["MATATT_ID"] = (
				#	str(row.get("SAP_PART_NUMBER"))
				#	+ "-"
				#	+ str(row.get("ATTRIBUTE_NAME"))
				#)
				# Trace.Write(
				# 	"SELECT ATTVAL_VALCODE,ATTRIBUTE_NAME,ATTRIBUTE_RECORD_ID,ATTRIBUTEVALUE_RECORD_ID FROM MAATVL WHERE ATTVAL_VALCODE = '"
				# 	+ str(row.get("VALUE_CODE"))
				# 	+ "' AND ATTRIBUTE_NAME ='"
				# 	+ str(row.get("ATTRIBUTE_NAME"))
				# 	+ "' AND ATTRIBUTE_RECORD_ID='"
				# 	+ str(row.get("ATTRIBUTE_RECORD_ID"))
				# 	+ "'"
				# )
				maatvl_obj = Sql.GetFirst(
					"SELECT ATTVAL_VALCODE,ATTRIBUTE_NAME,ATTRIBUTE_RECORD_ID,ATTRIBUTEVALUE_RECORD_ID FROM MAATVL (NOLOCK) WHERE ATTVAL_VALCODE ='"
					+ str(row.get("VALUE_CODE"))
					+ "' AND ATTRIBUTE_NAME ='"
					+ str(row.get("ATTRIBUTE_NAME"))
					+ "' AND ATTRIBUTE_RECORD_ID='"
					+ str(row.get("ATTRIBUTE_RECORD_ID"))
					+ "' "
				)
				if maatvl_obj is None:
					maatvl_next_id1 = Sql.GetFirst(
						"SELECT CONVERT(VARCHAR(4000),NEWID()) AS RECORD_ID"
					)
					attr_data_type = ""
					attr_obj = Sql.GetFirst(
						"SELECT ATTVAL_DATA_TYPE,ATTRIBUTE_RECORD_ID FROM MAATTR (NOLOCK) WHERE ATTRIBUTE_RECORD_ID='"
						+ str(row.get("ATTRIBUTE_RECORD_ID"))
						+ "' "
					)
					if attr_obj is not None:
						attr_data_type = str(attr_obj.ATTVAL_DATA_TYPE)
					if maatvl_next_id1 is not None:
						new_val12 = str(maatvl_next_id1.RECORD_ID)
						rows = {}
						rows["RANK"] = ""
						rows["ATTRIBUTEVALUE_RECORD_ID"] = str(new_val12)
						#7936 start
						#rows["VALUE_CODE"] = str(row.get("VALUE_CODE"))
						#7936 End
						rows["ATTRIBUTE_NAME"] = str(row.get("ATTRIBUTE_NAME"))
						rows["ATTRIBUTE_RECORD_ID"] = str(
							row.get("ATTRIBUTE_RECORD_ID")
						)
						rows["ATTRIBUTE_TYPE"] = str(row.get("ATTRIBUTE_TYPE"))
						#7936 start - ATTRIBUTE VALUE CODE SAVE START
						if str(row.get("ATTRIBUTE_DISPLAYVAL")) == "":
							rows["ATTVAL_DISPLAYVAL"] = "None"
							rows["VALUE_CODE"] = str(row.get("ATTRIBUTE_NAME")) + '_'+ str(rows["ATTVAL_DISPLAYVAL"])
						else:
							rows["ATTVAL_DISPLAYVAL"] = str(
								row.get("ATTRIBUTE_DISPLAYVAL")
							)
							rows["VALUE_CODE"] = str(row.get("ATTRIBUTE_NAME")) + '_'+ str(row.get("ATTRIBUTE_DISPLAYVAL"))
							#7936 END - ATTRIBUTE VALUE CODE SAVE END
						
						if (
							str(attr_data_type).title().strip() == "String"
							or str(attr_data_type).title().strip() == "Text"
						):
							#7936 start - ATTRIBUTE VALUE CODE SAVE START
							query = Sql.GetFirst("select top 1 ATTVAL_VALCODE from MAATVL where ATTVAL_VALCODE = '"+str(rows["VALUE_CODE"])+"'")
							if query is None and query == '':
								Table.TableActions.Create("MAATVL", rows)
							#7936 END - ATTRIBUTE VALUE CODE SAVE END
				
				next_id1 = Sql.GetFirst(
					"SELECT CONVERT(VARCHAR(4000),NEWID()) AS RECORD_ID"
				)
				new_val1 = str(next_id1.RECORD_ID)
				"""next_id1 = Sql.GetFirst("select top 1 MATATTVAL_RECORD_ID as RECORD_ID from MAMAAV(nolock) order by CpqTableEntryId desc")
				if next_id1 is not None:
					nex_val1 = str(next_id1.RECORD_ID).split('-')
					nex_val1=nex_val1[1]
				if nex_val1 != '' and nex_val1 is not None:
					next_val=str(eval("next_id1.RECORD_ID")).split('-')
					next_val=nex_val1[1]
					next_val2=int(next_val)+1
					new_val1='MAMAAV-'+str(next_val2).rjust(5, '0')
				else:
					next_val1='300000'
					next_val2=int(next_val1)+1
					new_val1='MAMAAV-'+str(next_val2).rjust(5, '0')"""
				
				value_rec_id = ""
				value_rec_obj = Sql.GetFirst(
					"SELECT ATTRIBUTEVALUE_RECORD_ID FROM MAATVL (NOLOCK) where ATTRIBUTE_NAME = '"
					+ str(row.get("ATTRIBUTE_NAME"))
					+ "' and ATTVAL_VALDISPLAY = '"
					+ str(row.get("ATTVAL_DISPLAYVAL"))
					+ "' "
				)
				if value_rec_obj is not None:
					value_rec_id = str(value_rec_obj.ATTRIBUTEVALUE_RECORD_ID)
					
				row["MATATTVAL_RECORD_ID"] = str(new_val1)
				# row['MATATTVAL_ID']=str(row.get('SAP_PART_NUMBER'))+str(row.get('ATTRIBUTE_NAME'))+str(row.get('VALUE_CODE'))
				row["ATTVAL_RECORD_ID"] = str(value_rec_id)
				row["VALUE_CODE"] = str(row.get("VALUE_CODE"))
				row["SAP_PART_NUMBER"] = str(row.get("SAP_PART_NUMBER"))
				row["ATTRIBUTE_NAME"] = str(row.get("ATTRIBUTE_NAME"))
				row["ATTRIBUTE_RECORD_ID"] = str(row.get("ATTRIBUTE_RECORD_ID"))
				row["ATTRIBUTE_TYPE"] = str(row.get("ATTRIBUTE_TYPE"))
				row["MATATT_RECORD_ID"] = str(row1.get("MATERIAL_ATTRIBUTE_RECORD_ID"))
				if str(row.get("ATTVAL_DISPLAYVAL")) == "":
					row["ATTVAL_DISPLAYVAL"] = "None"
				else:
					row["ATTVAL_DISPLAYVAL"] = str(row.get("ATTVAL_DISPLAYVAL"))
				if str(row.get("ATTRIBUTE_TYPE")) != "":
					Table.TableActions.Create("MAMAAV", row)
					Table.TableActions.Create("MAMAAT", row1)
					if MaterialContainer is not None:
						row2 = {}
						row2 = MaterialContainer.AddNewRow(False)
						row2["ATTRIBUTE_NAME"] = str(row.get("ATTRIBUTE_NAME"))
						row2["Values"] = str(row.get("ATTRIBUTE_DISPLAYVAL"))
						row2["ATTRIBUTE_TYPE"] = str(row.get("ATTRIBUTE_TYPE"))
						row2["Attribute_recordid"] = str(row.get("ATTRIBUTE_RECORD_ID"))
Log.Info("LABLE[3]--------------------" + str(LABLE[3]))
valueSAP = []
valueSAP.insert(1, sap_number)
ApiResponse = ApiResponseFactory.JsonResponse(valueSAP)