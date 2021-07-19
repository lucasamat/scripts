# =========================================================================================================================================
#   __script_name : SYMCMOBJCL.PY
#   __script_description : THIS SCRIPT IS USED TO CANCEL THE CHANGES IN EDIT IN OBJECTS IN SYSTEM ADMIN APP
#   __primary_author__ : BAJI BABA
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL

Sql = SQL()

RecordId = Product.Attributes.GetByName("MM_OBJ_REC_ID").GetValue()
Product.Attributes.GetByName("MM_OBJ_ACTION").AssignValue(str("VIEW"))

Product.Attributes.GetByName("MM_OBJ_BTN_BTL").Allowed = True
Product.Attributes.GetByName("MM_OBJ_BTN_EDIT").Allowed = True
Product.Attributes.GetByName("MM_OBJ_BTN_DELETE").Allowed = True
Product.Attributes.GetByName("MM_OBJ_BTN_SAVE").Allowed = False
Product.Attributes.GetByName("MM_OBJ_BTN_CANCEL").Allowed = False
Product.Attributes.GetByName("MM_OBJ_FI_BTN_ADDFIELD").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_BTN_SAVE").Allowed = False
Product.Attributes.GetByName("MM_OBJ_FI_BTN_CANCEL").Allowed = False
Product.Attributes.GetByName("MM_OBJ_TAB_BANNER").HintFormula = "OBJECT INFORMATION : VIEW"
CompObj = Sql.GetList("SELECT * FROM SYOBJH WHERE RECORD_ID='" + str(RecordId) + "'")
for data in CompObj:
    Product.Attributes.GetByName("MM_OBJ_REC_ID").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_REC_ID").AssignValue(str(data.RECORD_ID))
    Product.Attributes.GetByName("MM_OBJ_REC_ID").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_LABEL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_LABEL").AssignValue(str(data.LABEL))
    Product.Attributes.GetByName("MM_OBJ_LABEL").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_PL_LABEL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL").AssignValue(str(data.PLURAL_LABEL))
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_TBL_NAME").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME").AssignValue(str(data.OBJECT_NAME))
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_DESC").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_DESC").AssignValue(str(data.OBJ_DESC))
    Product.Attributes.GetByName("MM_OBJ_DESC").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_REC_NAME").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_REC_NAME").AssignValue(str(data.RECORD_NAME))
    Product.Attributes.GetByName("MM_OBJ_REC_NAME").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").AssignValue(str(data.DATA_TYPE))
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").AssignValue(str(data.DIS_FORMAT))
    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_API_NAME").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_API_NAME").AssignValue(str(data.API_NAME))
    Product.Attributes.GetByName("MM_OBJ_API_NAME").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJ_KEY_FIELD_LABEL").AssignValue(str(data.FIELD_LABEL))
    Product.Attributes.GetByName("MM_OBJ_KEY_FIELD_LABEL").Access = AttributeAccess.ReadOnly

    MM_OBJECT_STATUS = Product.Attributes.GetByName("MM_OBJECT_STATUS").GetValue() or ""
    if str(MM_OBJECT_STATUS) == "DEPLOYED":
        Product.Attributes.GetByName("MM_OBJ_BTN_REFRESH").Allowed = False
    else:
        Product.Attributes.GetByName("MM_OBJ_BTN_REFRESH").Allowed = True

    # For Related List Information
    RecordNo = Product.Attributes.GetByName("MM_OBJ_REC_ID").GetValue()
    if RecordNo != "":
        SQL_Quaryobj = Sql.GetList("SELECT * FROM SYSECT WHERE PRIMARY_OBJECT_RECORD_ID LIKE '%" + str(RecordNo) + "%'")
        Flag = 0
        for dat in SQL_Quaryobj:
            Flag = 1

        if Flag == 1:
            Product.Attributes.GetByName("MM_OBJ_SEC_REL_LIST").Allowed = True
            Product.Attributes.GetByName("MM_OBJ_SUBSEC_SEC_REL_LIST").Allowed = True
            Product.Attributes.GetByName("MM_OBJ_CTR_SEC_REL_LST").Allowed = True

            Cont = Product.GetContainerByName("MM_OBJ_CTR_SEC_REL_LST")
            Cont.Rows.Clear()
            for data_obj in SQL_Quaryobj:
                row = Cont.AddNewRow(False)
                # Log.Info("section container added")
                row.SetColumnValue("RECORD_ID", str(data_obj.RECORD_ID))
                row.SetColumnValue("SECTION_NAME", str(data_obj.SECTION_NAME))
                row.SetColumnValue("ATTRIBUTE_NAME", str(data_obj.ATTRIBUTE_NAME))
                row.SetColumnValue("PRIMARY_OBJECT_NAME", str(data_obj.PRIMARY_OBJECT_NAME))

    # For FIELDS AND RELATIONSHIPS container
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").Clear()
    con = Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA")

    SQLobj = Sql.GetList(
        "SELECT top 1000 * FROM  SYOBJD WHERE OBJECT_NAME ='" + str(data.OBJECT_NAME) + "' and  DATA_TYPE != 'AUTO NUMBER'"
    )
    if SQLobj is not None:
        for obj in SQLobj:
            row = con.AddNewRow()
            row["RECORD_ID"] = str(obj.RECORD_ID)
            row["FIELD_LABEL"] = str(obj.FIELD_LABEL)
            row["API_NAME"] = str(obj.API_NAME)
            row["REQUIRED"] = str(obj.REQUIRED)
            row["DATA_TYPE"] = str(obj.DATA_TYPE)
            row["LENGTH"] = str(obj.LENGTH)
            row["DECIMALS"] = str(obj.DECIMALS)
            row["PICKLIST_VALUES"] = str(obj.PICKLIST_VALUES)
            row["PERMISSIONS"] = str(obj.PERMISSION)
            row["DESCRIPTION"] = str(obj.DESCRIPTION)
            row["LOOKUP_OBJECTECT"] = str(obj.LOOKUP_OBJECT)
            row["FORMULA_LOGIC"] = str(obj.FORMULA_LOGIC)
            row["IS_KEY"] = str(obj.IS_KEY)

    Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Access = AttributeAccess.ReadOnly
    # Product.Attributes.GetByName('MM_OBJ_FI_BTN_ADDFIELD').Allowed = False

    # For Hideing error msg
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_KEY_FIELD_LABEL_ERR").Allowed = False

    # For container row hiding:
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanDeleteRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanEditRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanCopyRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanAddNewRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanReorderRows = True

    if Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").Rows.Count == 0:
        Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = False
        Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = False
    else:
        Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = True
        Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False

    # FIELDS AND RELATIONSHIPS container VISIBLITY IN VIEW MODE
    Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanDeleteRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanEditRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanCopyRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanAddNewRows = True
    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").CanReorderRows = True
    Product.GetContainerByName("MM_OBJ_CTR_SEARCH_LIST").CanReorderRows = False
