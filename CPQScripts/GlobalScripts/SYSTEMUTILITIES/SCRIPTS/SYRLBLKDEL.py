# =========================================================================================================================================
#   __script_name : SYRLBLKDEL.PY
#   __script_description :  THIS SCRIPT IS USED FOR BULK DELETING RECORDS.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
import SYCNGEGUID as CPQID

# import PRCTPRFPBE
from SYDATABASE import SQL

Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
CurrentTab = TestProduct.CurrentTab
Trace.Write("CurrentTab-------->" + str(CurrentTab))
Id = Param.SELECTEDROW
Trace.Write("Id--------" + str(list(Id)))
Trace.Write("selected id------" + str(Id))
table_id = Param.table_id
Trace.Write("table_id--- " + str(table_id))
Table_ID = table_id
Table_ID = "-".join(Table_ID.split("_")[-5:]).strip()
Trace.Write("Table_IDssss---------------------" + str(Table_ID))
Value = 0
Objd_ColumnName = ""
Objd_ColumnName_val = ""
value1_re = ""
data_val = ""
ID_val = ""
del_dict = {}
for ID in list(Id):
    

    # Trace.Write('ObjectName----DELTE'+str(ObjectName))
    ObjectName = ID.split("-")[0]
    # Trace.Write("ObjectName-----"+str(ObjectName))
    ##CHANGES GUID TO TABLEID + CPQEntryID BY MALAR
    ###CODE STARTS
    ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(ID))
    
    ###CODE ENDS

    if Value == 0:
        # Trace.Write("table_id--------------------------------------->"+str(table_id))
        if str(table_id) == "ADDNEW__SYOBJR_90004_MMOBJ_00122":
            # Trace.Write("table_id inside if--------------------------------------->"+str(table_id))
            query = Sql.GetFirst(
                "select RECORD_ID,OBJECT_NAME,RECORD_NAME from SYOBJH (NOLOCK) where RECORD_ID ='"
                + str(Table_ID)
                + "' and DATA_TYPE = 'AUTO NUMBER'"
            )
            ObjectName = str(query.OBJECT_NAME)
            # Trace.Write('ObjectName-------'+str(ObjectName)+'idddddd'+str(ID))


        # Trace.Write("table_id inside else--------------------------------------->"+str(Table_ID))
        query = Sql.GetFirst(
            "select RECORD_ID,OBJECT_NAME,RECORD_NAME from SYOBJH (NOLOCK) where RECORD_ID ='"
            + str(Table_ID)
            + "' and DATA_TYPE = 'AUTO NUMBER'"
        )
        ObjectName = str(query.OBJECT_NAME)
        # Trace.Write('62222222222222222222222222222222222222'+str(ObjectName))

        Objd_Recors = Sql.GetFirst(
            "select API_NAME from  SYOBJD (NOLOCK) where DATA_TYPE = 'AUTO NUMBER' and OBJECT_NAME = '"
            + str(ObjectName)
            + "'"
        )
        if Objd_Recors is not None:
            Objd_ColumnName = ""
            # Trace.Write('Objd_Recors-----------------> '+str(Objd_Recors.API_NAME))
            Objd_ColumnName = str(Objd_Recors.API_NAME).strip()

            Value = 1


    if len(str(ObjectName)) > 0 and len(str(Objd_ColumnName)) > 0 and len(str(ID)) > 0:
        Trace.Write("ObjectName-------------102-------------------------->" + str(ObjectName))
        Trace.Write("Objd_ColumnName------------103--------------------------->" + str(Objd_ColumnName))
        Trace.Write("ID--------------------------104------------->" + str(ID))

 

   

       

