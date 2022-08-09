# =========================================================================================================================================
#   __script_name : SYEDITREPO.PY
#   __script_description : THIS SCRIPT IS USED TO DO VALIDATION WHEN NAVIGATING FROM VIEW MODE TO EDIT MODE IN RELATED LISTS
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product_name = Product.Name


def check_table_Value():
    Flag_Val = "False"
    Auto_Val = ""
    for tab in Product.Tabs:
        tab_name = tab.Name

        if tab.IsSelected == True:
            CurrentTabName = (tab.Name).strip()
            sql_obj = Sql.GetFirst(
                "select RECORD_ID,TAB_LABEL from SYTABS where SAPCPQ_ALTTAB_NAME = '"
                + str(CurrentTabName)
                + "' and RTRIM(LTRIM(APP_LABEL))='"
                + str(Product_name)
                + "' order by DISPLAY_ORDER"
            )
            if sql_obj is not None:
                str1 = (sql_obj.TAB_LABEL).strip()
                SYSECT_OBJNAME = Sql.GetList(
                    "select SYSECT.RECORD_ID,PRIMARY_OBJECT_NAME FROM SYSECT INNER JOIN SYPAGE (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where RTRIM(LTRIM(SYPAGE.TAB_NAME)) ='"
                    + str(str1)
                    + "' and SYPAGE.TAB_RECORD_ID ='"
                    + str(sql_obj.RECORD_ID).strip()
                    + "'"
                )

                if SYSECT_OBJNAME is not None:
                    ##TO GET THE SECTION INFORMATION
                    for secobj in SYSECT_OBJNAME:

                        TABLE_NAME = str(secobj.PRIMARY_OBJECT_NAME).strip()

                        REC_ID_OBJ = Sql.GetFirst(
                            "Select RECORD_ID,RECORD_NAME from SYOBJH where RTRIM(LTRIM(OBJECT_NAME))='"
                            + str(TABLE_NAME).strip()
                            + "'"
                        )

                        if REC_ID_OBJ is not None:
                            SYOBJH_OBJ = REC_ID_OBJ.RECORD_ID
                            QUE_OBJ = Sql.GetFirst(
                                "Select RECORD_ID from SYSEFL where API_NAME='"
                                + str(REC_ID_OBJ.RECORD_NAME).strip()
                                + "' and API_NAME='"
                                + str(TABLE_NAME).strip()
                                + "' and SECTION_RECORD_ID='"
                                + str(secobj.RECORD_ID)
                                + "' "
                            )
                            ###TO GET THE QUESTION INFORMATION
                            if QUE_OBJ is not None:
                                RECORDID = str(QUE_OBJ.RECORD_ID).replace("-", "_").replace(" ", "")
                                ATTRIBUTENAME = (RECORDID).upper()
                                RECORD_ID = "QSTN_" + str(ATTRIBUTENAME).strip()
                                RecId = str(REC_ID_OBJ.RECORD_NAME).strip()
                                CurrentTabName = TestProduct.CurrentTab
                                if Product.Tabs.GetByName(str(TestProduct.CurrentTab)) is not None:
                                    Tab_Name = Product.Tabs.GetByName(str(TestProduct.CurrentTab)).Attributes
                                    for attr in Tab_Name:
                                        if str(attr.Name) == RECORD_ID:
                                            Auto_Val = Product.Attributes.GetByName(str(RECORD_ID)).GetValue()
                                    if Auto_Val != "":
                                        Tab_OBJ = Sql.GetFirst(
                                            "Select * from "
                                            + str(TABLE_NAME)
                                            + " where "
                                            + str(RecId)
                                            + "='"
                                            + str(Auto_Val)
                                            + "'"
                                        )
                                        
                                        for attr in Tab_Name:
                                            if str(attr.Name).startswith("QSTN_SYSEFL_"):
                                                QSTN_REC = (attr.Name[5:]).strip().replace("_", "-").replace(" ", "")
                                                if Tab_OBJ is not None:
                                                    Que_OBJ = Sql.GetFirst(
                                                        "Select API_NAME from SYSEFL where LTRIM(RTRIM(RECORD_ID))='"
                                                        + str(QSTN_REC).strip()
                                                        + "'"
                                                    )
                                                    if Que_OBJ is not None:
                                                        Attr_Val = str(Que_OBJ.API_NAME)
                                                        Tab_Val = eval(str("Tab_OBJ." + str(Attr_Val)))

                                                        if Tab_Val == "TRUE" or Tab_Val == "True":
                                                            Tab_Val = 1
                                                        if Tab_Val == "FALSE" or Tab_Val == "False":
                                                            Tab_Val = 0

                                                        curr_Val = Product.Attributes.GetByName(str(attr.Name)).GetValue()

                                                        if str(Tab_Val) != str(curr_Val):
                                                            Flag_Val = "True"
                                                            if Flag_Val == "True":
                                                                break
    return Flag_Val


ApiResponse = ApiResponseFactory.JsonResponse(check_table_Value())