# =========================================================================================================================================
#   __script_name : SYALMODLDL.PY
#   __script_description : THIS SCRIPT IS USED TO DELETE A RECORD WHEN THE USER CLICKS ON THE DELETE BUTTON.
#   __primary_author__ : JOE EBENEZER
#   __create_date : 26/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
import SYTABACTIN as Table

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product_name = Product.Name
import SYCNGEGUID as CPQID

##variable declaration
current_tab = ""
Related_Tab = ""
recno = ""
TableName = ""
#TreeParam = Product.GetGlobal("TreeParentLevel0")

status_flag = "FALSE"


def del_record():
    status_flag = "FALSE"
    if TestProduct != "":
        current_tab = str(TestProduct.CurrentTab)
        sql_obj = Sql.GetFirst(
            "select RECORD_ID,TAB_LABEL from SYTABS where SAPCPQ_ALTTAB_NAME = '"
            + str(current_tab)
            + "' and RTRIM(LTRIM(APP_LABEL))='"
            + str(Product_name)
            + "' order by DISPLAY_ORDER "
        )
        if sql_obj is not None:
            Related_Tab = str(sql_obj.TAB_LABEL).strip()
            SYSECT_OBJNAME = Sql.GetList(
                "select RECORD_ID,SECTION_NAME,PRIMARY_OBJECT_NAME FROM SYSECT (NOLOCK) JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID=SYSECT.RECORD_ID  AND SYSECT.PAGE_NAME = SYPAGE.PAGE_NAME  where SYSECT.PAGE_NAME = '"
                + str(sql_obj.TAB_LABEL).strip()
                + "' and SYPAGE.TAB_RECORD_ID = '"
                + str(sql_obj.RECORD_ID)
                + "' "
            )
            
            if SYSECT_OBJNAME is not None:
                for SYSECT_Details in SYSECT_OBJNAME:
                    if SYSECT_Details.SECTION_NAME != "" and SYSECT_Details.PRIMARY_OBJECT_NAME != "":
                        TableName = str(SYSECT_Details.PRIMARY_OBJECT_NAME)
                        
                        SYOBJH_OBJNAME = Sql.GetFirst(
                            "select RECORD_NAME from SYOBJH where RTRIM(LTRIM(OBJECT_NAME)) = '"
                            + str(SYSECT_Details.PRIMARY_OBJECT_NAME).strip()
                            + "' "
                        )
                        if SYOBJH_OBJNAME is not None:
                            SYSEFL_OBJNAME = Sql.GetFirst(
                                "select RECORD_ID FROM SYSEFL where RTRIM(LTRIM(API_NAME)) ='"
                                + str(SYSECT_Details.PRIMARY_OBJECT_NAME).strip()
                                + "' and LTRIM(RTRIM(SECTION_NAME))='"
                                + str(SYSECT_Details.SECTION_NAME)
                                + "' and SECTION_RECORD_ID='"
                                + str(SYSECT_Details.RECORD_ID).strip()
                                + "' and LTRIM(RTRIM(API_NAME))='"
                                + str(SYOBJH_OBJNAME.RECORD_NAME).strip()
                                + "' "
                            )
                            
                            if SYSEFL_OBJNAME is not None:
                                SECTIONQSTNRECORDID = str(SYSEFL_OBJNAME.RECORD_ID).replace("-", "_").replace(" ", "")

                                SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
                                MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
                                
                                if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
                                    ID = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
                                   
                                    ##CHANGES GUID TO TABLEID + CPQEntryID BY MALAR
                                    ###CODE STARTS
                                    # ID = CPQID.KeyCPQId.GetKEYId(str(TableName),str(ID))
                                    
                                    ###CODE ENDS

    
    if len(ID) > 0:
        idval = ""
        flag = 0
        tableInfo = Sql.GetTable(TableName)
        
        ColumnName = Sql.GetFirst(
            "select API_NAME from  SYOBJD where OBJECT_NAME ='" + str(TableName) + "' and DATA_TYPE ='AUTO NUMBER'"
        )
        sqlobjs = Sql.GetList(
            "select OBJECT_NAME,API_NAME from  SYOBJD where LOOKUP_OBJECT ='" + str(TableName) + "' and DATA_TYPE ='LOOKUP'"
        )
        flag = ""
        if sqlobjs is not None:
            for sqlobj in sqlobjs:
                sqlobj1 = Sql.GetFirst(
                    "select "
                    + str(sqlobj.API_NAME)
                    + " from "
                    + str(sqlobj.OBJECT_NAME)
                    + " where "
                    + str(sqlobj.API_NAME)
                    + " ='"
                    + str(ID)
                    + "'"
                )
                
                ####to delete the record
                if sqlobj1 is None:
                    flag = 0
                    status_flag = "FALSE"
                else:
                    status_flag = "TRUE"
                    flag = 1
                    break

            if flag == 0:
                GetQuery = Sql.GetList(
                    "select CpqTableEntryId from "
                    + str(TableName)
                    + " where "
                    + str(ColumnName.API_NAME)
                    + "='"
                    + str(ID)
                    + "'"
                )
                if GetQuery is not None:
                    for tablerow in GetQuery:
                        tableInfo.AddRow(tablerow)
                        Sql.Delete(tableInfo)
                        TestProduct.ChangeTab(Related_Tab)
                        


            ###to reload the container
            Container = ""
            Con_Col_Name = "RECORD_ID"
            for tab in Product.Tabs:
                if tab.IsSelected == True:
                    currenttab = tab.Name
                    sql_obj = Sql.GetList(
                        "SELECT PRIMARY_OBJECT_RECORD_ID,PRIMARY_OBJECT_NAME FROM SYSECT WHERE SYSECT (NOLOCK) ON SYSECT.RECORD_ID = SYPAGE.RECORD_ID AND SYSECT.PAGE_NAME = SYPAGE.PAGE_NAME SYPAGE.TAB_NAME='"
                        + str(currenttab)
                        + "' "
                    )
                    if sql_obj is not None:
                        for sql in sql_obj:
                            data_obj = Sql.GetList(
                                "SELECT CONTAINER_NAME FROM SYOBJS WHERE NAME='Tab list' AND OBJ_REC_ID = '"
                                + str(sql.PRIMARY_OBJECT_RECORD_ID)
                                + "'"
                            )
                            if data_obj is not None:
                                for data in data_obj:
                                    Container = "LIST_" + str(data.CONTAINER_NAME).strip()
            
    return str(status_flag)


ApiResponse = ApiResponseFactory.JsonResponse(del_record())