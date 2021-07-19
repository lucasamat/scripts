# =========================================================================================================================================
#   __script_name : SYMCMOBJED.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT A CUSTOM TABLE CONFIGURATION IN SYSTEM ADMIN
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
ids = Param.Primary_Data
Cont = Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA")
Product.Attributes.GetByName("MM_OBJ_FI_BTN_SAVE").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_BTN_CANCEL").Allowed = True
if Cont.Rows.Count > 0:
    for row in Cont.Rows:
        if row["RECORD_ID"] == str(ids):

            Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").Allowed = True
            data_type = row["DATA_TYPE"]
            Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").SelectDisplayValue(str(data_type))

            Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL").Allowed = True
            filed_label = row["FIELD_LABEL"]
            Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL").AssignValue(str(filed_label))

            
            Product.Attributes.GetByName("MM_OBJ_FI_SHORT_LBL").Allowed = True
            field_short_label = row["FIELD_SHORT_LABEL"]
            Product.Attributes.GetByName("MM_OBJ_FI_SHORT_LBL").AssignValue(str(field_short_label))
            

            Product.Attributes.GetByName("MM_OBJ_FI_API_NAME").Allowed = True
            api_name = row["API_NAME"]
            Product.Attributes.GetByName("MM_OBJ_FI_API_NAME").AssignValue(str(api_name))

            Product.Attributes.GetByName("MM_OBJ_FI_REQ").Allowed = True
            req = row["REQUIRED"]
            if str(req) == "TRUE":
                Product.Attributes.GetByName("MM_OBJ_FI_REQ").SelectDisplayValue("1")
            else:
                Product.Attributes.GetByName("MM_OBJ_FI_REQ").SelectDisplayValue("0")

            Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = True
            req_IsKey = row["IS_KEY"]
            if str(req_IsKey) == "TRUE":
                Product.Attributes.GetByName("MM_OBJ_FI_KEY").SelectDisplayValue("1")
            else:
                Product.Attributes.GetByName("MM_OBJ_FI_KEY").SelectDisplayValue("0")

            Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").Allowed = True
            fi_permissions = row["PERMISSIONS"]
            Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").SelectDisplayValue(str(fi_permissions))

            Product.Attributes.GetByName("MM_OBJ_FI_DESC").Allowed = True
            description = row["DESCRIPTION"]
            Product.Attributes.GetByName("MM_OBJ_FI_DESC").AssignValue(str(description))

            Product.Attributes.GetByName("MM_OBJ_FI_RECNO").Allowed = True
            Cont_Rec_no = row["RECORD_ID"]
            Product.Attributes.GetByName("MM_OBJ_FI_RECNO").AssignValue(str(Cont_Rec_no))

            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False
            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False

            if (
                str(data_type) == ""
                or str(data_type) == "DATE"
                or str(data_type) == "DATE/TIME"
                or str(data_type) == "CHECKBOX"
            ):

                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
                

                if str(data_type) == "CHECKBOX":
                    Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = False

            elif str(data_type) == "LOOKUP":

                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = True
                look_up_obj = row["LOOKUP_OBJECTECT"]
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").AssignValue(str(look_up_obj))
                Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = True
                Rel_List_Name = row["RELATED_LIST_NAME"]
                Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").AssignValue(str(Rel_List_Name))

                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = True
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = True
                Rel_List_LOOKUP_API_NAME = row["LOOKUP_API_NAME"]
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").AssignValue(str(Rel_List_LOOKUP_API_NAME))

                Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = True
                Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = True

            elif str(data_type) == "TEXT":

                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = True
                lenth = row["LENGTH"]
                Product.Attributes.GetByName("MM_OBJ_FI_LEN").AssignValue(str(lenth))
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False

            elif str(data_type) == "NUMBER" or str(data_type) == "CURRENCY":

                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = True
                lenth = row["LENGTH"]
                Product.Attributes.GetByName("MM_OBJ_FI_LEN").AssignValue(str(lenth))
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = True
                decmal = row["DECIMALS"]
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").AssignValue(str(decmal))
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False

            elif str(data_type) == "PICKLIST" or str(data_type) == "PICKLIST (MULTI-SELECT)":

                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = True
                piclist_val = row["PICKLIST_VALUES"]
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").AssignValue(str(piclist_val))
                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
                
            elif str(data_type) == "FORMULA":

                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = True
                Formula_Logic = row["FORMULA_LOGIC"]
                Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").AssignValue(str(Formula_Logic))
                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
                
                Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = False

            else:

                Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False

                Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False

                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_LOGIC").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_LOGIC_ERR").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
                Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
