from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()


Product_name = Product.Name
for tab in Product.Tabs:
    tab_name = tab.Name
    if tab.IsSelected == True:
        CurrentTabName = (tab.Name).strip()
        sql_obj = Sql.GetFirst(
            "select RECORD_ID,TAB_NAME from SYTABS where SAPCPQ_ALTTAB_NAME = '"
            + str(CurrentTabName)
            + "' and RTRIM(LTRIM(APP_LABEL))='"
            + str(Product_name)
            + "' order by DISPLAY_ORDER"
        )
        if sql_obj is not None:
            str1 = str(sql_obj.TAB_NAME).strip()
            Trace.Write("str1" + str(str1))

            SYSECT_OBJNAME = Sql.GetFirst(
                "select SYSECT.RECORD_ID,SYSECT.PRIMARY_OBJECT_NAME FROM SYSECT NOLOCK) INNER JOIN SYPAGE (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_NAME ='"
                + str(str1)
                + "' and SYPAGE.TAB_RECORD_ID ='"
                + str(sql_obj.RECORD_ID).strip()
                + "'"
            )

            if SYSECT_OBJNAME is not None:

                TABLE_NAME = str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME).strip()

                REC_ID_OBJ = Sql.GetFirst(
                    "Select RECORD_NAME from SYOBJH where RTRIM(LTRIM(OBJECT_NAME))='" + str(TABLE_NAME).strip() + "'"
                )

                if REC_ID_OBJ is not None:

                    QUE_OBJ = Sql.GetFirst(
                        "Select RECORD_ID from SYSEFL where API_NAME='"
                        + str(REC_ID_OBJ.RECORD_NAME).strip()
                        + "' and API_NAME='"
                        + str(TABLE_NAME).strip()
                        + "'  "
                    )

                    if QUE_OBJ is not None:
                        RECORDID = str(QUE_OBJ.RECORD_ID).replace("-", "_").replace(" ", "")
                        ATTRIBUTENAME = (RECORDID).upper()
                        RECORD_ID = "QSTN_" + str(ATTRIBUTENAME).strip()

                        RecId = str(REC_ID_OBJ.RECORD_NAME).strip()

                        if Product.Attributes.GetByName(str(RECORD_ID)) is not None:
                            Rec_Id_Value = Product.Attributes.GetByName(str(RECORD_ID)).GetValue() or ""

                            if Rec_Id_Value != "":
                                ScriptExecutor.ExecuteGlobal(
                                    "SYALLTABOP",
                                    {"Primary_Data": Rec_Id_Value, "TabNAME": str1, "ACTION": "CLONE", "RELATED": ""},
                                )