"""Used to Drop and Recreate Constraints."""
# =========================================================================================================================================
#   __script_name : SYDRPCONST.PY
#   __script_description : THIS SCRIPT IS USED TO DROP CONSTRAINTS & RECREATE CONSTRAINTS.
#   __primary_author__ : MOHAMED IBRAHIM,DHURGA
#   __create_date : 17-07-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYCNGEGUID as CPQID
#import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import SYERRMSGVL as Message

Sql = SQL()


class DropConstraint:
    """Use to delete constraints."""

    def __init__(self, ObjectName):
        """Use for initialization"""
        self.ObjectName = ObjectName
        self.exceptMessage = ""

    def deleteConstraint(self, Value):
        """Use to delete constraints based on selected constraint type."""
        Output = ""
        Trace.Write('delete constraint from related list----')
        try:
            Trace.Write('try---')
            #constraintType = Value.split(",")[3]
            #objectApiName = Value.split(",")[4]
            #Id = Value.split(",")[1]
            #cpqEntryId = Id.split("-")[1]
            Output = ""
            constraintType = Value.split("#")[0]
            Trace.Write('try-constraintType-----'+str(constraintType))
            objectApiName = Value.split("#")[1]
            Id = Value.split("#")[2]
            cpqEntryId = ""
            Output = ""

            # DROP FOREIGN KEY
            if constraintType == "FOREIGN KEY":
                query_result = Sql.GetList(
                    "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME, "
                    + "FK.CONSTRAINT_NAME FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME=CON.OBJECT_APINAME AND FK.COLUMN_NAME= "
                    + " CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%FK_%' WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND REFOBJECT_APINAME = '"
                    + str(self.ObjectName)
                    + "' AND REFOBJECTFIELD_APINAME='"
                    + str(objectApiName)
                    + "' "
                )
                for loop in query_result:
                    query = "ALTER TABLE " + loop.TABLE_NAME + " DROP CONSTRAINT " + loop.CONSTRAINT_NAME + " "
                    queryStatement = Sql.RunQuery(query)

                # DROP FOREIGN KEY
                query_result = Sql.GetList(
                    "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME, "
                    + "FK.CONSTRAINT_NAME FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME=CON.OBJECT_APINAME AND FK.COLUMN_NAME = "
                    + " CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%FK_%' WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND OBJECT_APINAME ='"
                    + str(self.ObjectName)
                    + "'  AND OBJECTFIELD_APINAME ='"
                    + str(objectApiName)
                    + "' "
                )

                for loop in query_result:
                    query = "ALTER TABLE " + loop.TABLE_NAME + " DROP CONSTRAINT " + loop.CONSTRAINT_NAME + ""
                    queryStatement = Sql.RunQuery(query)
                delete_query_string = """DELETE FROM SYOBJC WHERE OBJECT_APINAME = '{objectname}' and OBJECTFIELD_APINAME = '{apiname_column}'""".format(
                    objectname=str(self.ObjectName),apiname_column = str(objectApiName)
                )
                Sql.RunQuery(delete_query_string)
                #self.deleteRecord(cpqEntryId)
                Output = "True"

            elif constraintType == "UNIQUE":
                # DROP UNIQUE KEY
                #Trace
                FK_CONSTRAINT = Sql.GetList(
                    "SELECT Result=COUNT(1) FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE SCHCON ON SCHCON.TABLE_NAME = CON.OBJECT_APINAME AND "
                    + " SCHCON.COLUMN_NAME = CON.OBJECTFIELD_APINAME AND SCHCON.CONSTRAINT_NAME LIKE '%FK_%'  WHERE CON.REFOBJECT_APINAME='"
                    + str(self.ObjectName)
                    + "' AND CON.REFOBJECTFIELD_APINAME = '"
                    + str(objectApiName)
                    + "'"
                )
                if FK_CONSTRAINT is not None:
                    for fkey in FK_CONSTRAINT:
                        result = fkey.Result
                        if result == 0:
                            query_result = Sql.GetList(
                                "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME, "
                                + " FK.CONSTRAINT_NAME FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME=CON.OBJECT_APINAME AND FK.COLUMN_NAME = "
                                + " CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%UQ_%' WHERE CONSTRAINT_TYPE='UNIQUE' AND OBJECT_APINAME ='"
                                + str(self.ObjectName)
                                + "'  AND OBJECTFIELD_APINAME ='"
                                + str(objectApiName)
                                + "' "
                            )

                            for loop in query_result:
                                query = "ALTER TABLE " + loop.TABLE_NAME + " DROP CONSTRAINT " + loop.CONSTRAINT_NAME + " "
                                queryStatement = Sql.RunQuery(query)
                            delete_query_string = """DELETE FROM SYOBJC WHERE OBJECT_APINAME = '{objectname}' and OBJECTFIELD_APINAME = '{apiname_column}'""".format(
                                objectname=str(self.ObjectName),apiname_column = str(objectApiName)
                            )
                            Sql.RunQuery(delete_query_string)
                            #self.deleteRecord(cpqEntryId)
                            Output = "True"
                            
                        else:
                            ErrorMsg = Message.GetErrorMessage(
                                "BE3705B4-B532-4D9E-9790-17742318DC7B", "OBJECT_APINAME", self.ObjectName, "ERROR"
                            )
                            Output = ErrorMsg

            elif constraintType == "NOT NULL":
                # DROP NOT NULL
                query_result = Sql.GetList(
                    "SELECT OBJECT_APINAME, OBJECTFIELD_APINAME FROM SYOBJC(NOLOCK) WHERE CONSTRAINT_TYPE = 'NOT NULL' AND OBJECT_APINAME = '"
                    + str(self.ObjectName)
                    + "' "
                    + " AND OBJECTFIELD_APINAME ='"
                    + str(objectApiName)
                    + "' "
                )

                for loop in query_result:
                    FK_CONSTRAINT = Sql.GetFirst(
                        "SELECT Result=COUNT(1) FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE SCHCON ON SCHCON.TABLE_NAME = CON.OBJECT_APINAME AND "
                        + " SCHCON.COLUMN_NAME = CON.OBJECTFIELD_APINAME AND CON.CONSTRAINT_NAME LIKE '%FK_%'  WHERE CON.REFOBJECT_APINAME='"
                        + str(self.ObjectName)
                        + "' AND CON.REFOBJECTFIELD_APINAME = '"
                        + str(objectApiName)
                        + "'"
                    )
                    if FK_CONSTRAINT is not None:
                        foreignKey = FK_CONSTRAINT.Result
                        if foreignKey == 0:
                            UQ_CONSTRAINT = Sql.GetFirst(
                                "SELECT result=COUNT(1) FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE WHERE FK.CONSTRAINT_NAME LIKE '%UQ_%' AND COLUMN_NAME = '"
                                + loop.COLUMN_NAME
                                + "' AND TABLE_NAME= '"
                                + loop.TABLE_NAME
                                + "' "
                            )
                            if UQ_CONSTRAINT is not None:
                                uniqueKey = UQ_CONSTRAINT.Result
                                if uniqueKey == 0:
                                    query = (
                                        "ALTER TABLE "
                                        + loop.OBJECT_APINAME
                                        + " ALTER COLUMN "
                                        + loop.OBJECTFIELD_APINAME
                                        + " NVARCHAR(250) NULL"
                                    )
                                    queryStatement = Sql.RunQuery(query)
                                    #self.deleteRecord(cpqEntryId)
                                    delete_query_string = """DELETE FROM SYOBJC WHERE OBJECT_APINAME = '{objectname}' and OBJECTFIELD_APINAME = '{apiname_column}'""".format(
                                        objectname=str(self.ObjectName),apiname_column = str(objectApiName)
                                    )
                                    Sql.RunQuery(delete_query_string)
                                    Output = "True"

                        else:
                            ErrorMsg = Message.GetErrorMessage(
                                "BE3705B4-B532-4D9E-9790-17742318DC7B", "OBJECT_APINAME", self.ObjectName, "ERROR"
                            )
                            Output = ErrorMsg
           
        except Exception as e:
            self.exceptMessage = "SYDRPCONST : DropConstraint : EXCEPTION : UNABLE TO DROP CONSTRAINT: " + str(e)
           
        return Output

    def deleteRecord(self, cpqEntryId):
        """ Delete record from SYOBJC table"""
        try:
            delete_query_string = """DELETE FROM SYOBJC WHERE CpqTableEntryId = '{cpqEntryId}' """.format(
                cpqEntryId=cpqEntryId
            )
            
            Sql.RunQuery(delete_query_string)
        except:
            Log.Info("Error in {} - delete".format("SYOBJC"))

    def bulkDeleteConstraint(self):
        """Use to delete all the constraints of an object."""
        try:
            query_result = Sql.GetList(
                "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME, "
                + "REFERENCECOLUMN=REFOBJECTFIELD_APINAME,FK.CONSTRAINT_NAME FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON "
                + "FK.TABLE_NAME = CON.OBJECT_APINAME AND FK.COLUMN_NAME=CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%FK_%' "
                + "WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND REFOBJECT_APINAME ='"
                + str(self.ObjectName)
                + "' "
            )
            for loop in query_result:
                DROP_FKCONSTRAINT = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE " + loop.TABLE_NAME + " DROP CONSTRAINT " + loop.CONSTRAINT_NAME + "  '"
                )

            query_result = Sql.GetList(
                "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME,"
                + "FK.CONSTRAINT_NAME FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME = CON.OBJECT_APINAME AND "
                + "FK.COLUMN_NAME=CON.OBJECTFIELD_APINAME AND FK.CONSTRAINT_NAME LIKE '%FK_%' WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND OBJECT_APINAME ='"
                + str(ObjectName)
                + "' "
            )
            for loop in query_result:
                DROP_FKCONSTRAINT = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE " + loop.TABLE_NAME + " DROP CONSTRAINT " + loop.CONSTRAINT_NAME + "  '"
                )

            query_result = Sql.GetList(
                "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME,FK.CONSTRAINT_NAME FROM SYOBJC CON INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE FK ON FK.TABLE_NAME = CON.OBJECT_APINAME AND FK.COLUMN_NAME=CON.OBJECTFIELD_APINAME AND "
                + "FK.CONSTRAINT_NAME LIKE '%UQ_%' WHERE CONSTRAINT_TYPE='UNIQUE' AND OBJECT_APINAME ='"
                + str(self.ObjectName)
                + "' "
            )
            for loop in query_result:
                DROP_FKCONSTRAINT = Sql.GetFirst(
                    "sp_executesql @T=N'ALTER TABLE " + loop.TABLE_NAME + " DROP CONSTRAINT " + loop.CONSTRAINT_NAME + "  '"
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
            delete_query_string = """DELETE FROM SYOBJC WHERE OBJECT_APINAME = '{objectname}' """.format(
                objectname=self.ObjectName
            )
            Sql.RunQuery(delete_query_string)
        except Exception as e:
            self.exceptMessage = (
                "SYDRPCONST : bulkDeleteConstraint : EXCEPTION : UNABLE TO DROP ALL CONSTRAINTS OF THE OBJECT: " + str(e)
            )
            Trace.Write(self.exceptMessage)

        return True

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
                #drop constraints --UNIQUE--start
                DROP_CONSTRAINT = Sql.GetList(
                    "SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE WHERE CONSTRAINT_NAME LIKE '%UQ_%' AND COLUMN_NAME = '"
                    + loop.OBJECTFIELD_APINAME
                    + "' AND TABLE_NAME= '"
                    + loop.OBJECT_APINAME
                    + "' "
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
                #drop constraints --UNIQUE-- end
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
                "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME FROM SYOBJC WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND OBJECT_APINAME = '"
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
                "SELECT TABLE_NAME=OBJECT_APINAME,COLUMN_NAME=OBJECTFIELD_APINAME,REFERENCETABLE=REFOBJECT_APINAME,REFERENCECOLUMN=REFOBJECTFIELD_APINAME FROM SYOBJC WHERE CONSTRAINT_TYPE='FOREIGN KEY' AND REFOBJECT_APINAME='"
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

        except Exception as e:
            self.exceptMessage = "SYDRPCONST : recreateConstraint : EXCEPTION : UNABLE TO CREATE CONSTRAINTS: " + str(e)
            Trace.Write(self.exceptMessage)
        return True


RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00517").GetValue()
# ObjectName = Param.Grid_Id
ObjectName = RecAttValue
constraint = DropConstraint(ObjectName)


Action = Param.Action
if Action == "DELETE":
    Value = Param.Values
    ApiResponse = ApiResponseFactory.JsonResponse(constraint.deleteConstraint(Value))

if Action == "BULK_DELETE":
    ApiResponse = ApiResponseFactory.JsonResponse(constraint.bulkDeleteConstraint())

if Action == "RECREATE":
    ApiResponse = ApiResponseFactory.JsonResponse(constraint.recreateConstraint())
