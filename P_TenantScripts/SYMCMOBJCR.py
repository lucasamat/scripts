# =========================================================================================================================================
#   __script_name : SYMCMOBJCR.PY
#   __script_description : THIS SCRIPT IS USED TO DEPLOY/CREATE A NEW CUSTOM TABLE IN CPQ.To RENAME CUSTO TABLE.TO RENAME API NAME IN CUSTOM TABLE
#   __primary_author__ : BAJI BABA,MOHAMED IBRAHIM,DHURGA GOPALAKRISHNAN
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
from SYDATABASE import SQL
import SYERRMSGVL as Message

Sql = SQL()

# A043S001P01-13332 Start
def Module_Table_Operation(Obj_RecId):
    SYQSCO_OBJNAME = Sql.GetList("select *  FROM SYOBJH (nolock) where OBJECT_NAME = '" + str(Obj_RecId) + "'")
    if SYQSCO_OBJNAME is not None:
        for SYQSCO_Details in SYQSCO_OBJNAME:
            ObjName = str(SYQSCO_Details.OBJECT_NAME).strip()
            # Trace.Write("ObjName--->"+str(ObjName));
            tableInfo = Sql.GetTable(str(ObjName))
            SYOBJD_RECORDS = Sql.GetList(
                "Select top 1000 API_NAME,REQUIRED,DATA_TYPE,LENGTH,DECIMALS,LOOKUP_OBJECT,PICKLIST_VALUES,FORMULA_DATA_TYPE FROM SYOBJD (nolock) where OBJECT_NAME='"
                + str(ObjName)
                + "' order by abs(DISPLAY_ORDER)"
            )
            if SYOBJD_RECORDS is not None:
                for SYOBJD_Details in SYOBJD_RECORDS:
                    ColumnName = str(SYOBJD_Details.API_NAME).strip()
                    if ColumnName.upper() in ("CPQTABLEENTRYMODIFIEDBY", "CPQTABLEENTRYDATEMODIFIED",):
                        continue
                    if str(SYOBJD_Details.DATA_TYPE) == "CHECKBOX" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "CHECKBOX":
                        dataType = "BIT"
                        length = 0
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "TEXT"
                        or str(SYOBJD_Details.DATA_TYPE) == "LONG TEXT AREA"
                        or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "TEXT"
                        or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "LONG TEXT AREA"
                    ):

                        dataType = "NVARCHAR"
                        try:
                            length = int(SYOBJD_Details.LENGTH)
                        except:
                            length = 255
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "NUMBER" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "NUMBER"
                    ) and str(SYOBJD_Details.DECIMALS) == "0":
                        dataType = "DECIMAL"
                        length = 0
                        # decimal = int(row['DECIMALS'])
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "NUMBER" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "NUMBER"
                    ) and str(SYOBJD_Details.DECIMALS) != "0":
                        dataType = "DECIMAL"
                        length = int(SYOBJD_Details.DECIMALS)
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "PERCENT" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "PERCENT"
                    ) and str(SYOBJD_Details.DECIMALS) == "0":
                        dataType = "DECIMAL"
                        length = 0
                        # decimal = int(row['DECIMALS'])
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "PERCENT" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "PERCENT"
                    ) and str(SYOBJD_Details.DECIMALS) != "0":
                        dataType = "DECIMAL"
                        length = int(SYOBJD_Details.DECIMALS)
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "CURRENCY" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "CURRENCY"
                    ) and str(SYOBJD_Details.DECIMALS) == "0":
                        dataType = "DECIMAL"
                        length = 0
                        # decimal = int(row['DECIMALS'])
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "CURRENCY" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "CURRENCY"
                    ) and str(SYOBJD_Details.DECIMALS) != "0":
                        dataType = "DECIMAL"
                        # Trace.Write(
                        #    " SYOBJD_Details.DECIMALS" + str( SYOBJD_Details.DECIMALS)
                        # )
                        # Trace.Write(
                        #    " SYOBJD_Details.API_NAME" + str( SYOBJD_Details.API_NAME)
                        # )
                        length = int(SYOBJD_Details.DECIMALS)
                    elif str(SYOBJD_Details.DATA_TYPE) == "DATE" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "DATE":
                        dataType = "DATE"
                        length = 0
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "DATE/TIME" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "DATE/TIME"
                    ):
                        dataType = "DATETIME"
                        length = 0
                    elif str(SYOBJD_Details.DATA_TYPE) == "PICKLIST" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "PICKLIST":
                        dataType = "NVARCHAR"
                        length = 500
                    elif (
                        str(SYOBJD_Details.DATA_TYPE) == "PICKLIST (MULTI-SELECT)"
                        or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "PICKLIST (MULTI-SELECT)"
                    ):
                        dataType = "NVARCHAR"
                        length = 4000
                    elif str(SYOBJD_Details.DATA_TYPE) == "IMAGE" or str(SYOBJD_Details.FORMULA_DATA_TYPE) == "IMAGE":
                        dataType = "NVARCHAR"
                        length = 0
                    elif str(SYOBJD_Details.DATA_TYPE) == "LOOKUP":
                        dataType = "NVARCHAR"
                        length = 250
                    elif str(SYOBJD_Details.DATA_TYPE) == "AUTO NUMBER":
                        dataType = "NVARCHAR"
                        length = 250
                    elif str(SYOBJD_Details.DATA_TYPE) == "FORMULA":
                        dataType = "NVARCHAR"
                        length = 250
                    else:
                        dataType = "NVARCHAR"
                        length = 250

                    tableInfo.AddColumn(str(ColumnName), dataType, length, True)

                tableInfo.HiddenTable = False

                SqlHelper.CreateTable(tableInfo)


# LOGIN_CREDENTIALS=Record=Sql.GetFirst("SELECT Username,Password,Domain FROM SYCONF")
# if LOGIN_CREDENTIALS is not None:
# Login_Username = str(LOGIN_CREDENTIALS.Username)
# Login_Password = str(LOGIN_CREDENTIALS.Password)
# Login_Domain = str(LOGIN_CREDENTIALS.Domain)

# username = str(Login_Username)+"#"+str(Login_Domain)
# password = str(Login_Password)
# Action = "ADDORUPDATE"
OBJD_result = SqlHelper.GetList(
    "SELECT Result=COUNT(1)  FROM SYOBJD (NOLOCK) OBJD WHERE (OBJD.REV_API_NAME <>'' OR OBJD.REV_DATA_TYPE<>'' OR OBJD.REV_LENGTH > 0 OR OBJD.REV_DECIMALS <>'' )"
)

OBJH_result = SqlHelper.GetList("SELECT Result=COUNT(1)  FROM SYOBJH (NOLOCK) OBJH WHERE (OBJH.REV_API_NAME <>'')")


class AlterObject:
    """Use to rename object name, api name, data type, data length"""

    
    def __init__(self, ObjectName):
        """Use for initialization"""
        self.ObjectName = ObjectName
        self.exceptMessage = ""

    def bulkDeleteConstraint(self):
        """Use to delete all the constraints of an object."""
        try:
            query_result = Sql.GetList(
                "SELECT OBJECT_APINAME,FK.CONSTRAINT_NAME FROM SYOBJC CON "
                + "INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON "
                + "FK.TABLE_NAME = CON.OBJECT_APINAME AND FK.COLUMN_NAME=CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%FK_%' "
                + "WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND REFOBJECT_APINAME ='"
                + str(self.ObjectName)
                + "' "
            )
            for loop in query_result:
                DROP_FKCONSTRAINT = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.OBJECT_APINAME
                    + " DROP CONSTRAINT "
                    + loop.CONSTRAINT_NAME
                    + "  '"
                )

            query_result = Sql.GetList(
                "SELECT OBJECT_APINAME,FK.CONSTRAINT_NAME FROM SYOBJC CON "
                + "INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME = CON.OBJECT_APINAME AND "
                + "FK.COLUMN_NAME=CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%FK_%' WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND OBJECT_APINAME ='"
                + str(ObjectName)
                + "' "
            )
            for loop in query_result:
                DROP_FKCONSTRAINT = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.OBJECT_APINAME
                    + " DROP CONSTRAINT "
                    + loop.CONSTRAINT_NAME
                    + "  '"
                )

            query_result = Sql.GetList(
                "SELECT OBJECT_APINAME,FK.CONSTRAINT_NAME FROM SYOBJC CON "
                + "INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME = CON.OBJECT_APINAME AND FK.COLUMN_NAME=CON.OBJECTFIELD_APINAME AND "
                + "FK.CONSTRAINT_NAME LIKE '%UQ_%' WHERE CONSTRAINT_TYPE='UNIQUE' AND OBJECT_APINAME ='"
                + str(self.ObjectName)
                + "' "
            )
            for loop in query_result:
                DROP_FKCONSTRAINT = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.OBJECT_APINAME
                    + " DROP CONSTRAINT "
                    + loop.CONSTRAINT_NAME
                    + "  '"
                )

            query_result = Sql.GetList(
                "SELECT OBJECT_APINAME,OBJECTFIELD_APINAME FROM SYOBJC(NOLOCK) WHERE CONSTRAINT_TYPE='NOT NULL' AND OBJECT_APINAME = '"
                + str(self.ObjectName)
                + "'"
            )
            for loop in query_result:
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.OBJECT_APINAME
                    + " ALTER COLUMN "
                    + loop.OBJECTFIELD_APINAME
                    + " NVARCHAR(250) NULL'"
                )
            result_update = " UPDATE SYOBJH SET HAS_CONSTRAINTS = 0 WHERE OBJECT_NAME='" + str(self.ObjectName) + "'"
            query_result = Sql.RunQuery(str(result_update))

        except Exception, e:
            self.exceptMessage = (
                "SYDRPCONST : bulkDeleteConstraint : EXCEPTION : UNABLE TO DROP ALL CONSTRAINTS OF THE OBJECT: " + str(e)
            )

        return True

    # SCRIPT TO RENAME OBJECT'S API NAME , DATA TYPE & DATA LENGTH
    def AlterObjectAPI(self):
        """Use to rename Object API"""
        try:

            query_result = Sql.GetList(
                "SELECT OBJECT_NAME,API_NAME,REV_API_NAME,REV_DATA_TYPE,REV_LENGTH=CAST(REV_LENGTH AS INT),DataType=COL.data_type, "
                + "Length=CAST(COL.character_maximum_length AS INT),REV_DECIMALS=CAST(REV_DECIMALS AS INT),TAB.TABLE_ID,SCH.IS_NULLABLE,OBJD.CpqTableEntryId FROM SYOBJD OBJD "
                + "INNER JOIN INFORMATION_SCHEMA.COLUMNS COL ON COL.column_name = OBJD.API_NAME AND COL.table_name = OBJD.OBJECT_NAME "
                + "INNER JOIN XLS_TABLES TAB ON TAB.TABLE_NAME = OBJD.OBJECT_NAME "
                + "INNER JOIN [INFORMATION_SCHEMA].[COLUMNS] SCH ON SCH.TABLE_NAME = OBJD.OBJECT_NAME AND SCH.COLUMN_NAME=COL.column_name "
                + "WHERE OBJD.OBJECT_NAME ='"
                + str(self.ObjectName)
                + "' AND (OBJD.REV_API_NAME <>'' OR OBJD.REV_DATA_TYPE<>'' OR OBJD.REV_LENGTH > 0 OR OBJD.REV_DECIMALS <>'' ) "
            )
            for loop in query_result:
                # ALTER API NAME
                if len(loop.REV_API_NAME) > 0:
                    columnrename_CPQ = (
                        "EXEC sp_RENAME '"
                        + loop.OBJECT_NAME
                        + "."
                        + loop.API_NAME
                        + "' , '"
                        + loop.REV_API_NAME
                        + "', 'COLUMN'"
                    )
                    columnrename_CPQ = columnrename_CPQ.replace("'", "''")
                    rename_CPQ = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(columnrename_CPQ) + "'")

                    columnrename_XLS = (
                        "UPDATE COL SET COL.COLUMN_NAME = '"
                        + loop.REV_API_NAME
                        + "' FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                        + str(loop.TABLE_ID)
                        + " AND COL.COLUMN_NAME='"
                        + loop.API_NAME
                        + "';"
                    )
                    columnrename_XLS = columnrename_XLS.replace("'", "''")
                    rename_XLS = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(columnrename_XLS) + "'")

                    columnrename_OBJD = (
                        "UPDATE objd SET objd.API_NAME = '"
                        + loop.REV_API_NAME
                        + "' FROM SYOBJD objd WHERE objd.OBJECT_NAME='"
                        + str(loop.OBJECT_NAME)
                        + "' AND objd.API_NAME='"
                        + loop.API_NAME
                        + "'; UPDATE SYSEFL SET API_FIELD_NAME ='"
                        + loop.REV_API_NAME
                        + "'  WHERE API_NAME = '"
                        + loop.OBJECT_NAME
                        + "' AND API_FIELD_NAME ='"
                        + loop.API_NAME
                        + "';"
                    )
                    columnrename_OBJD = columnrename_OBJD.replace("'", "''")
                    rename_XLS = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(columnrename_OBJD) + "'")

                else:
                    loop.REV_API_NAME = loop.API_NAME

                # ALTER API DATA TYPE LENGTH
                if loop.REV_DATA_TYPE.upper() == loop.DataType.upper():
                    if loop.REV_LENGTH > 0:  # CONVERSION OF NVARCHAR & DECIMAL DATA LENGTH
                        if loop.DataType.upper() == "DECIMAL":
                            alterdecimallen_CPQ = (
                                "ALTER TABLE "
                                + loop.OBJECT_NAME
                                + " ALTER COLUMN "
                                + loop.REV_API_NAME
                                + " "
                                + (loop.REV_DATA_TYPE).upper()
                                + " ("
                                + str(loop.REV_LENGTH)
                                + ","
                                + str(loop.REV_DECIMALS)
                                + ") "
                            )
                            _alterdecimallen_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdecimallen_CPQ) + "'"
                            )

                            alterdecimallen_XLS = (
                                "UPDATE COL SET COL.SIZE = "
                                + str(loop.REV_DECIMALS)
                                + " FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                                + str(loop.TABLE_ID)
                                + " AND COL.COLUMN_NAME='"
                                + loop.REV_API_NAME
                                + "';"
                            )
                            alterdecimallen_XLS = alterdecimallen_XLS.replace("'", "''")
                            _alterdecimallen_XLS = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdecimallen_XLS) + "'"
                            )
                        else:
                            updatedatatypelen_CPQ = (
                                "ALTER TABLE "
                                + loop.OBJECT_NAME
                                + " ALTER COLUMN "
                                + loop.REV_API_NAME
                                + " "
                                + str(loop.REV_DATA_TYPE).upper()
                                # + " ("
                                # + str(loop.REV_LENGTH)
                                # + ")"
                            )
                            datatypelenupdate_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(updatedatatypelen_CPQ) + "'"
                            )

                            updatedatatypelen_XLS = (
                                "UPDATE COL SET COL.SIZE = "
                                + str(loop.REV_LENGTH)
                                + " FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                                + str(loop.TABLE_ID)
                                + " AND COL.COLUMN_NAME='"
                                + loop.REV_API_NAME
                                + "';"
                            )
                            updatedatatypelen_XLS = updatedatatypelen_XLS.replace("'", "''")
                            datatypeupdatelen_XLS = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(updatedatatypelen_XLS) + "'"
                            )
                # ALTER API DATA TYPE & LENGTH
                elif loop.REV_DATA_TYPE.upper() != loop.DataType.upper():
                    if loop.REV_LENGTH > 0:  # CONVERSION OF DATA TYPE & LENGTH (DECIMAL & NVARCHAR)
                        if loop.REV_DATA_TYPE.upper() == "DECIMAL":
                            decimalconversion_CPQ = (
                                "UPDATE "
                                + loop.OBJECT_NAME
                                + " SET "
                                + loop.REV_API_NAME
                                + " = CAST("
                                + loop.REV_API_NAME
                                + " AS DECIMAL("
                                + str(loop.REV_LENGTH)
                                + ","
                                + str(loop.REV_DECIMALS)
                                + ")) WHERE "
                                + loop.REV_API_NAME
                                + " <> ''"
                            )
                            _decimalconversion_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(decimalconversion_CPQ) + "'"
                            )

                            alterdecimallen_CPQ = (
                                "ALTER TABLE "
                                + loop.OBJECT_NAME
                                + " ALTER COLUMN "
                                + loop.REV_API_NAME
                                + " "
                                + loop.REV_DATA_TYPE.upper()
                                + " ("
                                + str(loop.REV_LENGTH)
                                + ","
                                + str(loop.REV_DECIMALS)
                                + ") "
                            )
                            _alterdecimallen_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdecimallen_CPQ) + "'"
                            )

                            alterdecimallen_XLS = (
                                "UPDATE COL SET COL.DB_TYPE = '"
                                + loop.REV_DATA_TYPE.upper()
                                + "', COL.SIZE = "
                                + str(loop.REV_DECIMALS)
                                + " FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                                + str(loop.TABLE_ID)
                                + " AND COL.COLUMN_NAME='"
                                + loop.REV_API_NAME
                                + "';"
                            )
                            alterdecimallen_XLS = alterdecimallen_XLS.replace("'", "''")
                            _alterdecimallen_XLS = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdecimallen_XLS) + "'"
                            )

                        else:
                            alternvarchar_CPQ = (
                                "ALTER TABLE "
                                + loop.OBJECT_NAME
                                + " ALTER COLUMN "
                                + loop.REV_API_NAME
                                + " "
                                + str(loop.REV_DATA_TYPE).upper()
                                # + " ("
                                # + str(loop.REV_LENGTH)
                                # + ")"
                            )
                            _alternvarchar_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alternvarchar_CPQ) + "'"
                            )

                            alternvarchar_XLS = (
                                "UPDATE COL SET COL.DB_TYPE = '"
                                + loop.REV_DATA_TYPE.upper()
                                + +"', COL.SIZE = "
                                + str(loop.REV_LENGTH)
                                + " FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                                + str(loop.TABLE_ID)
                                + " AND COL.COLUMN_NAME='"
                                + loop.REV_API_NAME
                                + "';"
                            )
                            alternvarchar_XLS = alternvarchar_XLS.replace("'", "''")
                            _alternvarchar_XLS = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alternvarchar_XLS) + "'"
                            )
                    # CONVERSION OF DATA TYPE & LENGTH (INT,DATETIME,DATE,BIT)
                    else:
                        if loop.REV_DATA_TYPE.upper() == "INT":
                            altertablevalue_CPQ = (
                                "UPDATE "
                                + loop.OBJECT_NAME
                                + " SET "
                                + loop.REV_API_NAME
                                + " = CAST(ROUND("
                                + loop.REV_API_NAME
                                + ",0) AS "
                                + loop.REV_DATA_TYPE.upper()
                                + ") WHERE "
                                + loop.REV_API_NAME
                                + " IS NOT NULL "
                            )
                            #Trace.Write("sp_executesql @statement = N'" + str(altertablevalue_CPQ) + "'")
                            _altertablevalue_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(altertablevalue_CPQ) + "'"
                            )

                            alterdatatype_CPQ = (
                                "ALTER TABLE "
                                + loop.OBJECT_NAME
                                + " ALTER COLUMN "
                                + loop.REV_API_NAME
                                + " "
                                + loop.REV_DATA_TYPE.upper()
                                + ";"
                            )
                            _alterdatatype_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdatatype_CPQ) + "'"
                            )

                            alterdatatype_XLS = (
                                "UPDATE COL SET COL.DB_TYPE = '"
                                + str(loop.REV_DATA_TYPE.upper())
                                + "' FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                                + str(loop.TABLE_ID)
                                + " AND COL.COLUMN_NAME='"
                                + loop.REV_API_NAME
                                + "';"
                            )
                            alterdatatype_XLS = alterdatatype_XLS.replace("'", "''")
                            _alterdatatype_XLS = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdatatype_XLS) + "'"
                            )

                        else:
                            altertablevalue_CPQ = (
                                "UPDATE "
                                + loop.OBJECT_NAME
                                + " SET "
                                + loop.REV_API_NAME
                                + " = CAST("
                                + loop.REV_API_NAME
                                + " AS "
                                + loop.REV_DATA_TYPE.upper()
                                + ") WHERE "
                                + loop.REV_API_NAME
                                + " IS NOT NULL "
                            )
                            _altertablevalue_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(altertablevalue_CPQ) + "'"
                            )

                            alterdatatype_CPQ = (
                                "ALTER TABLE "
                                + loop.OBJECT_NAME
                                + " ALTER COLUMN "
                                + loop.REV_API_NAME
                                + " "
                                + loop.REV_DATA_TYPE.upper()
                                + ";"
                            )
                            _alterdatatype_CPQ = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdatatype_CPQ) + "'"
                            )

                            alterdatatype_XLS = (
                                "UPDATE COL SET COL.DB_TYPE = '"
                                + str(loop.REV_DATA_TYPE.upper())
                                + "' FROM XLS_TABLE_COLUMN COL WHERE COL.TABLE_ID="
                                + str(loop.TABLE_ID)
                                + " AND COL.COLUMN_NAME='"
                                + loop.REV_API_NAME
                                + "';"
                            )
                            alterdatatype_XLS = alterdatatype_XLS.replace("'", "''")
                            _alterdatatype_XLS = SqlHelper.GetFirst(
                                "sp_executesql @statement = N'" + str(alterdatatype_XLS) + "'"
                            )

                OBJC_update = (
                    "UPDATE OBJC SET OBJC.OBJECTFIELD_APINAME=CASE WHEN REV_API_NAME<>'' THEN REV_API_NAME ELSE OBJC.OBJECTFIELD_APINAME END FROM SYOBJC OBJC WHERE OBJECT_APINAME='"
                    + str(loop.OBJECT_NAME)
                    + "' AND OBJECTFIELD_APINAME=' "
                    + loop.API_NAME
                    + "'"
                )
                OBJC_result = Sql.RunQuery(str(OBJC_update))

                _OBJC_update = (
                    "UPDATE OBJC SET OBJC.REFOBJECTFIELD_APINAME=CASE WHEN REV_API_NAME<>'' THEN REV_API_NAME ELSE OBJC.REFOBJECTFIELD_APINAME END FROM SYOBJC OBJC WHERE REFOBJECT_APINAME='"
                    + str(loop.OBJECT_NAME)
                    + "' AND REFOBJECTFIELD_APINAME=' "
                    + loop.API_NAME
                    + "'"
                )
                _OBJC_result = Sql.RunQuery(str(_OBJC_update))

                OBJD_update = (
                    "UPDATE OBJD SET OBJD.API_NAME=CASE WHEN REV_API_NAME<>'' THEN REV_API_NAME ELSE OBJD.API_NAME END,OBJD.LENGTH = CASE WHEN REV_LENGTH>0 THEN REV_LENGTH ELSE OBJD.LENGTH END,OBJD.DECIMALS = CASE WHEN REV_DECIMALS<>'' THEN REV_DECIMALS ELSE OBJD.DECIMALS END, OBJD.REV_API_NAME=NULL,OBJD.REV_LENGTH = NULL,OBJD.REV_DECIMALS=NULL,OBJD.REV_DATA_TYPE=NULL FROM SYOBJD OBJD WHERE CpqTableEntryId="
                    + str(loop.CpqTableEntryId)
                    + " "
                )
                OBJD_result = Sql.RunQuery(str(OBJD_update))

        except Exception, e:
            self.exceptMessage = "SYALTEROBJECT : AlterObjectAPI : EXCEPTION : ERROR IN SCRIPT: " + str(e)

        return True

    # SCRIPT TO RENAME OBJECT
    def AlterObject(self):
        """Use to rename Object"""
        try:

            query_result = Sql.GetList(
                "SELECT OBJECT_NAME,REV_API_NAME,OBJH.CpqTableEntryId FROM SYOBJH (NOLOCK) OBJH "
                + "WHERE OBJH.OBJECT_NAME ='"
                + str(self.ObjectName)
                + "' AND OBJH.REV_API_NAME <>'' "
            )
            for loop in query_result:
                if len(loop.REV_API_NAME) > 0:
                    tablerename_CPQ = "EXEC sp_rename '" + loop.OBJECT_NAME + "','" + loop.REV_API_NAME + "' "
                    tablerename_CPQ = tablerename_CPQ.replace("'", "''")
                    rename_CPQ = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(tablerename_CPQ) + "'")

                    tablerename_XLS = (
                        "UPDATE XLS_TABLES set table_name ='"
                        + loop.REV_API_NAME
                        + "' WHERE TABLE_NAME='"
                        + str(loop.OBJECT_NAME)
                        + "';"
                    )
                    tablerename_XLS = tablerename_XLS.replace("'", "''")
                    rename_XLS = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(tablerename_XLS) + "'")

                OBJC_update = (
                    "UPDATE OBJC SET OBJC.OBJECT_APINAME=CASE WHEN REV_API_NAME<>'' THEN REV_API_NAME ELSE OBJC.OBJECT_APINAME END FROM SYOBJC OBJC WHERE OBJECT_APINAME='"
                    + str(loop.OBJECT_NAME)
                    + "' "
                )
                OBJC_result = Sql.RunQuery(str(OBJC_update))

                _OBJC_update = (
                    "UPDATE OBJC SET OBJC.REFOBJECT_APINAME=CASE WHEN REV_API_NAME<>'' THEN REV_API_NAME ELSE OBJC.REFOBJECT_APINAME END FROM SYOBJC OBJC WHERE REFOBJECT_APINAME='"
                    + str(loop.OBJECT_NAME)
                    + "' "
                )
                _OBJC_result = Sql.RunQuery(str(_OBJC_update))

                OBJH_update = (
                    "UPDATE OBJH SET OBJH.OBJECT_NAME=CASE WHEN REV_API_NAME<>'' THEN REV_API_NAME ELSE OBJH.OBJECT_NAME END, OBJH.REV_API_NAME=NULL FROM OBJH OBJD WHERE CpqTableEntryId="
                    + str(loop.CpqTableEntryId)
                    + " "
                )
                OBJH_result = Sql.RunQuery(str(OBJH_update))

        except Exception, e:
            self.exceptMessage = "SYALTEROBJECT : AlterObjectAPI : EXCEPTION : ERROR IN SCRIPT: " + str(e)

        return True

    # RECREATE CONSTRAINTS
    def recreateConstraint(self):
        """Use to recreate all the constraints for an object."""
        try:
            # CREATE NOT NULL Constraint
            query_result = Sql.GetList(
                "SELECT OBJECT_APINAME, OBJECTFIELD_APINAME FROM SYOBJC(NOLOCK) CON INNER JOIN [INFORMATION_SCHEMA].[COLUMNS] SCHCON ON SCHCON.TABLE_NAME = CON.OBJECT_APINAME AND SCHCON.COLUMN_NAME = CON.OBJECTFIELD_APINAME AND SCHCON.IS_NULLABLE='YES' WHERE CONSTRAINT_TYPE ='NOT NULL' AND OBJECT_APINAME='"
                + str(self.ObjectName)
                + "'  "
            )
            for loop in query_result:
                DROP_CONSTRAINT = Sql.GetList(
                    "SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE WHERE CONSTRAINT_NAME LIKE '%UQ_%' AND COLUMN_NAME = '"
                    + loop.OBJECTFIELD_APINAME
                    + "' AND TABLE_NAME= '"
                    + loop.OBJECT_APINAME
                    + "' "
                )

                DROP_INDEX = Sql.GetList(
                    "SELECT C.NAME AS INDEX_N  FROM sys.index_columns A JOIN SYS.COLUMNS B ON A.COLUMN_ID = B.COLUMN_ID AND A.OBJECT_ID = B.OBJECT_ID JOIN SYS.INDEXES C ON A.INDEX_ID = C.INDEX_ID AND A.OBJECT_ID = C.OBJECT_ID WHERE OBJECT_NAME(A.OBJECT_ID)='"
                    + loop.OBJECT_APINAME
                    + "' AND B.NAME = '"
                    + loop.OBJECTFIELD_APINAME
                    + "'  "
                )

                if len(DROP_CONSTRAINT) > 0:
                    for ins in DROP_CONSTRAINT:
                        CONSTRAINT = Sql.GetFirst(
                            "sp_executesql @T=N'ALTER TABLE "
                            + loop.OBJECT_APINAME
                            + " DROP CONSTRAINT "
                            + str(ins.CONSTRAINT_NAME)
                            + "  '"
                        )

                if len(DROP_INDEX) > 0:
                    for inse in DROP_INDEX:
                        INDEX = Sql.GetFirst(
                            "sp_executesql @T=N'DROP INDEX " + str(inse.INDEX_N) + " ON " + loop.OBJECT_APINAME + " '"
                        )
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.OBJECT_APINAME
                    + " ALTER COLUMN "
                    + loop.OBJECTFIELD_APINAME
                    + " NVARCHAR(250) NOT NULL'"
                )

                for abc in DROP_INDEX:
                    INDEX1 = Sql.GetFirst(
                        "sp_executesql @T=N'CREATE INDEX "
                        + str(abc.INDEX_N)
                        + " ON "
                        + loop.OBJECT_APINAME
                        + "("
                        + loop.OBJECTFIELD_APINAME
                        + ") '"
                    )

            # CREATE UNIQUE Constraint
            query_result = Sql.GetList(
                "SELECT OBJECT_APINAME, OBJECTFIELD_APINAME FROM SYOBJC(NOLOCK) WHERE CONSTRAINT_TYPE='UNIQUE' AND OBJECT_APINAME='"
                + str(self.ObjectName)
                + "'"
            )
            for loop in query_result:
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.OBJECT_APINAME
                    + " ADD CONSTRAINT UQ_"
                    + loop.OBJECT_APINAME
                    + "_"
                    + loop.OBJECTFIELD_APINAME
                    + " UNIQUE("
                    + loop.OBJECTFIELD_APINAME
                    + ")'  "
                )

            # CREATE FOREIGN KEY Constraint
            query_result = Sql.GetList(
                "SELECT TABLE_NAME = OBJECT_APINAME, COLUMN_NAME = OBJECTFIELD_APINAME, REFERENCETABLE = REFOBJECT_APINAME, REFERENCECOLUMN = REFOBJECTFIELD_APINAME FROM SYOBJC WHERE CONSTRAINT_TYPE = 'FOREIGN KEY' AND OBJECT_APINAME = '"
                + str(self.ObjectName)
                + "'   "
            )

            for loop in query_result:
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.TABLE_NAME
                    + " ADD CONSTRAINT FK_"
                    + loop.TABLE_NAME
                    + "_"
                    + loop.COLUMN_NAME
                    + " FOREIGN KEY ("
                    + loop.COLUMN_NAME
                    + ") REFERENCES "
                    + loop.REFERENCETABLE
                    + " ("
                    + loop.REFERENCECOLUMN
                    + ")' "
                )

            # CREATE FOREIGN KEY Reference
            query_result = Sql.GetList(
                "SELECT TABLE_NAME = OBJECT_APINAME, COLUMN_NAME=OBJECTFIELD_APINAME, REFERENCETABLE=REFOBJECT_APINAME, REFERENCECOLUMN = REFOBJECTFIELD_APINAME FROM SYOBJC WHERE CONSTRAINT_TYPE = 'FOREIGN KEY' AND REFOBJECT_APINAME = '"
                + str(self.ObjectName)
                + "' "
            )

            for loop in query_result:
                result = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE "
                    + loop.TABLE_NAME
                    + " ADD CONSTRAINT FK_"
                    + loop.TABLE_NAME
                    + "_"
                    + loop.COLUMN_NAME
                    + " FOREIGN KEY ("
                    + loop.COLUMN_NAME
                    + ") REFERENCES "
                    + loop.REFERENCETABLE
                    + " ("
                    + loop.REFERENCECOLUMN
                    + ")' "
                )

            result_update = "UPDATE SYOBJH SET HAS_CONSTRAINTS = 1 WHERE OBJECT_NAME='" + str(self.ObjectName) + "'"
            query_result = Sql.RunQuery(str(result_update))

        except Exception, e:
            self.exceptMessage = "SYDRPCONST : recreateConstraint : EXCEPTION : UNABLE TO CREATE CONSTRAINTS: " + str(e)
        return True


# ObjectName = Param.ObjectName
# constraint = AlterObject(ObjectName)


Obj_RecId = Param.Primary_Data or ""
objChangestatus = Param.objChangestatus or ""
ObjectName = Param.Primary_Data or ""
constraint = AlterObject(ObjectName)
if str(objChangestatus).upper() == "NEW":
    Module_Table_Operation(Obj_RecId)
    Scrpcount = Sql.GetFirst("select * FROM SYOBJH (NOLOCK) where OBJECT_NAME ='" + str(Obj_RecId) + "'")
    if Scrpcount is not None:
        row = {"OBJECT_NAME": Obj_RecId, "OBJECT_STATUS": "DEPLOYED"}
        Table.TableActions.Update("SYOBJH", "OBJECT_NAME", row)
else:
    constraint.AlterObject()
    constraint.AlterObjectAPI()

# A043S001P01-13332 end
# Product.GetContainerByName("MM_OBJ_CTR_OBJ_INFO").Clear()
# Product.GetContainerByName("MM_OBJ_CTR_OBJ_INFO").LoadFromDatabase("SELECT top 1000 * FROM SYOBJH ORDER BY RECORD_ID", "")