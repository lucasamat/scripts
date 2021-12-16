# =========================================================================================================================================
#   __script_name : SYRLBLKDEL.PY
#   __script_description :  THIS SCRIPT IS USED FOR BULK DELETING RECORDS.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID

# import PRCTPRFPBE
from SYDATABASE import SQL

Sql = SQL()


Id = []
Trace.Write("Id--------" + str(list(Id)))
Trace.Write("selected id------" + str(Id))
table_id = Param.table_id
checkedrows = Param.checkedrows
selectall = Param.selectall
Trace.Write("checkedrows------" + str(checkedrows))
Trace.Write("selectall------" + str(selectall))
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
#if table_id == "ADDNEW__SYOBJR_00029_SYOBJ_1177034":
if 'SYOBJR_00029' in table_id:
    TreeParam = Product.GetGlobal("TreeParam")
    TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
    TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
    if selectall == "yes":
        Sql.RunQuery("DELETE FROM SAQRSP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeSuperParentParam,TreeParam))

        GetParts = Sql.GetList("SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeSuperParentParam,TreeParam))
        parts = []
        for x in GetParts:
            parts.append(x.PART_NUMBER)
        
        Sql.RunQuery("DELETE FROM SAQRIP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = 'Z0101' AND PART_NUMBER IN {}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),tuple(parts)))
    elif selectall == "no":
        checkedrows = checkedrows.split(",")
        checkedrows = tuple(checkedrows)
        rows = []
        parts = []
        for x in checkedrows:
            rows.append(x.split("-")[1])
            getPart = Sql.GetFirst("SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE CpqTableEntryId = {}".format(x.split("-")[1]))
            part = str(getPart.PART_NUMBER)
            parts.append(part)
        Sql.RunQuery("DELETE FROM SAQRSP WHERE CpqTableEntryId IN {}".format(tuple(rows)))
        Sql.RunQuery("DELETE FROM SAQRIP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = 'Z0101' AND PART_NUMBER IN {}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),tuple(parts)))
#elif table_id == "SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578":
elif 'SYOBJR_00005' in table_id:
    if selectall == "yes":
        Sql.RunQuery("DELETE FROM SAQSPT WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeParam))
    elif selectall == "no":
        checkedrows = tuple(checkedrows.split(","))
        rows = []
        for x in checkedrows:
            rows.append(x.split("-")[1])
        Sql.RunQuery("DELETE FROM SAQSPT WHERE CpqTableEntryId IN {}".format(tuple(rows)))
        
 

   

       

