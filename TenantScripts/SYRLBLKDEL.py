# =========================================================================================================================================
#   __script_name : SYRLBLKDEL.PY
#   __script_description :  THIS SCRIPT IS USED FOR BULK DELETING RECORDS.
#   __primary_author__ : JOE EBENEZER,WASIM ABDUL
#   __create_date :
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()


Id = []
Trace.Write("Id--------" + str(list(Id)))
Trace.Write("selected id------" + str(Id))
table_id = Param.table_id
checkedrows = Param.checkedrows
selectall = Param.selectall
# INC08632845 - Start - A
subtab = Param.SubtabName
# INC08632845 - End - M
TreeParam = Product.GetGlobal("TreeParam")
Trace.Write(checkedrows)
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
    #Trace.Write("TreeParentParam"+str(TreeParentParam))    
    #Trace.Write("TreeSuperParentParam"+str(TreeSuperParentParam))
    #Trace.Write("TreeTopSuperParentParam"+str(TreeTopSuperParentParam))

    #INC08737172 Start - M
    Qstr = ""      
    if subtab == "New Parts":
        Qstr = " AND NEW_PART = 'True'"
    elif subtab == "Inclusions":
        Qstr = " AND NEW_PART = 'False' AND INCLUDED = 1"
    elif subtab == "Exclusions":
        Qstr = " AND NEW_PART = 'False' AND INCLUDED = 0"
    #INC08737172 End - M
        
    if selectall == "yes":       
        GetParts = Sql.GetList("SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND PAR_SERVICE_ID = '{}' AND GREENBOOK = '{}'{}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeParentParam,TreeParam,Qstr))
        parts = []
        for x in GetParts:
            parts.append(x.PART_NUMBER)
        
        Sql.RunQuery("DELETE FROM SAQRSP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND PAR_SERVICE_ID = '{}' AND GREENBOOK = '{}'{}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeParentParam,TreeParam,Qstr))      
 
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

        #INC08737172 Start - A
        Sql.RunQuery("DELETE FROM SAQRSP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND PAR_SERVICE_ID = '{}' AND SERVICE_ID = 'Z0101' AND GREENBOOK = '{}' AND PART_NUMBER IN {} {}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeParentParam,TreeParam, tuple(parts), Qstr))
        #INC08737172 End - A
#elif table_id == "SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578":

elif 'SYOBJR_98882' in table_id:
    TreeParam = Product.GetGlobal("TreeParam")
    TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
    TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
    if selectall == "yes":
        Sql.RunQuery("DELETE FROM SAQSCN WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = 'Z0123' AND GREENBOOK = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeParentParam))

    elif selectall == "no":
        checkedrows = checkedrows.split(",")
        checkedrows = tuple(checkedrows)
        rows = []
        parts = []
        Trace.Write("checkedrows_chk_j "+str(checkedrows))
        for x in checkedrows:
            rows.append(x.split("-")[1])
        Sql.RunQuery("DELETE FROM SAQSCN WHERE CpqTableEntryId IN {}".format(tuple(rows)))

elif 'SYOBJR_00005' in table_id:
    if selectall == "yes":
        Sql.RunQuery("DELETE FROM SAQSPT WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),TreeParam))
    elif selectall == "no":
        checkedrows = tuple(checkedrows.split(","))
        Trace.Write("values"+str(checkedrows))

        rows = []
        for x in checkedrows:
            rows.append(x.split("-")[1])
        Sql.RunQuery("DELETE FROM SAQSPT WHERE CpqTableEntryId IN {}".format(tuple(rows)))
# INC08632845 - Start - A
elif 'SYOBJR_00033' in table_id:
    rows = []
    fieldName = 'SND_EQUIPMENT_ID'
    Trace.Write("checkedrows ==> "+str(checkedrows))
    if "," in checkedrows:
        checkedrows = tuple(checkedrows.split(","))
        for x in checkedrows:            
            rows.append(x)
        ids = tuple(rows)
    else:
        ids = "(" + checkedrows + ")"
        rows.append(checkedrows)

    Trace.Write("checkedrows after ==> "+str(checkedrows))
    getFabLocId = Sql.GetFirst("SELECT SNDFBL_ID FROM SAQASE WHERE QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_RECORD_ID = '{qtRecId}' AND {field} = '{fabId}'".format(qtRevRecId = Quote.GetGlobal("quote_revision_record_id"), qtRecId = Quote.GetGlobal("contract_quote_record_id"), field = fieldName, fabId = rows[0]))
    Trace.Write('first value -- ' + str(getFabLocId.SNDFBL_ID))
    if selectall == "yes":
        Sql.RunQuery("DELETE FROM SAQASE WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SNDFBL_ID = {}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"), getFabLocId.SNDFBL_ID))
    elif selectall == "no":
        Sql.RunQuery("DELETE FROM SAQASE WHERE QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_RECORD_ID = '{qtRecId}' AND {field} IN {rowIds} AND SNDFBL_ID = {fabId}".format(qtRevRecId = Quote.GetGlobal("quote_revision_record_id"), qtRecId = Quote.GetGlobal("contract_quote_record_id"), field = fieldName, rowIds = ids, fabId = getFabLocId.SNDFBL_ID))
        
elif ('SYOBJR_00038' in table_id or 'SYOBJR_00040' in table_id) and subtab == 'Receiving Equipment':
    rows = []
    fieldName = 'EQUIPMENT_ID'
    Trace.Write("RE checkedrows ==> "+str(checkedrows))
    if "," in checkedrows:
        checkedrows = tuple(checkedrows.split(","))
        for x in checkedrows:            
            rows.append(x)
        ids = tuple(rows)
    else:
        ids = "(" + checkedrows + ")"
        rows.append(checkedrows)

    Trace.Write("RE checkedrows after ==> "+str(checkedrows))
    getFabLocId = Sql.GetFirst("SELECT FABLOCATION_ID FROM SAQFEQ WHERE QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_RECORD_ID = '{qtRecId}' AND {field} = '{fabId}'".format(qtRevRecId = Quote.GetGlobal("quote_revision_record_id"), qtRecId = Quote.GetGlobal("contract_quote_record_id"), field = fieldName, fabId = rows[0]))
    Trace.Write('RE first value -- ' + str(getFabLocId.FABLOCATION_ID))
    if selectall == "yes":
        Sql.RunQuery("DELETE FROM SAQFEQ WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = {}".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"), getFabLocId.FABLOCATION_ID))
    elif selectall == "no":
        Sql.RunQuery("DELETE FROM SAQFEQ WHERE QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_RECORD_ID = '{qtRecId}' AND {field} IN {rowIds} AND FABLOCATION_ID = {fabId}".format(qtRevRecId = Quote.GetGlobal("quote_revision_record_id"), qtRecId = Quote.GetGlobal("contract_quote_record_id"), field = fieldName, rowIds = ids, fabId = getFabLocId.FABLOCATION_ID))
# INC08632845 - End - A

#CR BULK DELETE fab level Starts
elif table_id in ('fab_equipment_deletion', 'fab_greenbook_equipment_deletion') and subtab == 'Equipment':
    qtRevRecId = Quote.GetGlobal("quote_revision_record_id")
    qtRecId = Quote.GetGlobal("contract_quote_record_id")
    rows = []
    greenbook_whr_cond = ""
    fab_loc_id = str(TreeParam)
    record_ids = []
    #fab Green book level deletion in 2.1
    #if table_id == 'fab_greenbook_equipment_deletion':
    #    greenbook_whr_cond = " AND SAQFEQ.GREENBOOK  = '" + str(TreeParam) + "'"
    #    fab_loc_id = Product.GetGlobal("TreeParentLevel0")
    master_object_name = "SAQFEQ"
    if "," in checkedrows:
        checkedrows = tuple(checkedrows.split(","))
        for x in checkedrows:            
            rows.append(x)
        ids = tuple(rows)
        Trace.Write(""+str(ids))
        record_ids = [CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in ids]
        equipment_key_ids = tuple(record_ids)
        #SAQGPA
        saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND B.QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqgpa_del)
        #SAQGPM
        saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId)
        Sql.RunQuery(saqgpm_del)
        #SAQRGG
        saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId)
        Sql.RunQuery(saqrgg_del)
        #SAQGPE
        saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId)
        Sql.RunQuery(saqgpe_del)        
        #SAQSAP
        saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND B.QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids =equipment_key_ids)
        Sql.RunQuery(saqsap_del)
        #SAQSKP
        saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND B.QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqskp_del)
        #SAQSKP2
        saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND ISNULL(QTEGBKPME_RECORD_ID,'') != '' AND QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqskp_del_2)
        #SAQSAE
        saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND B.QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqsae_del)
        #SAQSCE
        saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND B.QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqsae_del)
        #SAQSCA
        saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqsca_del)
        #SAQSCO
        saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqsco_del)
        #SAQSGB
        get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId))
        for delete in get_saqsgb:
            Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND GREENBOOK = '{greenbook}'".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,greenbook =str(delete.GREENBOOK))
            Sql.RunQuery(Saqsgb_del)
        #SAQSGE
        get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId))
        for delete in get_saqsge:
            Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,greenbook =str(delete.QTESRVGBK_RECORD_ID))
            Sql.RunQuery(Saqsge_del)
        #SAQFEA
        Saqfea_del = "DELETE FROM SAQFEA WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTEREVFEQ_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(Saqfea_del)
        #SAQFEQ
        Saqfea_del = "DELETE FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID IN {equipment_key_ids}".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(Saqfea_del)
        #SAQFGB
        get_saqfgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQFGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND FABLOCATION_ID ='{fab_loc_id}' )".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,fab_loc_id = fab_loc_id))
        for delete in get_saqfgb:
            Saqfgb_del = "DELETE FROM SAQFGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK = '{greenbook}'".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,fab_loc_id = fab_loc_id,greenbook =str(delete.GREENBOOK))
            Sql.RunQuery(Saqfgb_del)
    else:
        info = "LN 245 - multiple items are not sent to the request. Fab or Fab -> Greenbook level deletions are not performed"
        Log.Info(info)
        Trace.Write("info => " + str(info))
#CR BULK DELETE -fab level Ends
#CR BULK DELETE -service level Starts
elif table_id in ('po_equipment_deletion', 'po_greenbook_equipment_deletion') and subtab == 'Equipment':
    qtRevRecId = Quote.GetGlobal("quote_revision_record_id")
    qtRecId = Quote.GetGlobal("contract_quote_record_id")
    rows = []
    greenbook_whr_cond = ""
    service_id = str(TreeParam)
    if table_id == 'po_greenbook_equipment_deletion':
        greenbook_whr_cond = " AND GREENBOOK = '" + str(TreeParam) + "'"
        service_id = str(Product.GetGlobal("TreeParentLevel0"))
    record_ids = []
    master_object_name = "SAQSCO"
    # This delete functionality only for multiple equipments
    Trace.Write("checkedrows"+str(checkedrows))
    if "," in checkedrows:
        checkedrows = tuple(checkedrows.split(","))
        for x in checkedrows:            
            rows.append(x)
        ids = tuple(rows)
        record_ids = [CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in ids]
        key_ids = tuple(record_ids)
        equip_rec_ids = Sql.GetList("SELECT QTEREVFEQ_RECORD_ID,EQUIPMENT_ID FROM SAQSCO(NOLOCK) WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID IN {key_ids} AND SERVICE_ID = '{service_id}'".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,key_ids =key_ids,service_id = service_id))
        #equipment_key_ids = tuple(equip_rec_id.QTEREV_RECORD_ID for equip_rec_id in equip_rec_ids)
        equipment_key_ids = "','".join([equip_rec_id.QTEREVFEQ_RECORD_ID for equip_rec_id in equip_rec_ids])
        equipment_ids = "','".join([equip_rec_id.EQUIPMENT_ID for equip_rec_id in equip_rec_ids])
        #SAQGPA
        saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}') AND B.QTESRVCOB_RECORD_ID IN {key_ids} ".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids,service_id = service_id,key_ids = key_ids)
        Sql.RunQuery(saqgpa_del)
        #SAQGPM
        saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,service_id = service_id)
        Sql.RunQuery(saqgpm_del)
        #SAQRGG
        saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' )".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,service_id = service_id)
        Sql.RunQuery(saqrgg_del)
        #SAQGPE
        saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,service_id = service_id)
        Sql.RunQuery(saqgpe_del)
        #SAQSAP
        saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids =equipment_key_ids,service_id = service_id)
        Sql.RunQuery(saqsap_del)
        #SAQSKP
        saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids,service_id = service_id)
        Sql.RunQuery(saqskp_del)
        #SAQSKP2
        saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTEREVFEQ_RECORD_ID in ('{equipment_key_ids}') AND ISNULL(QTEGBKPME_RECORD_ID,'') != '' AND SERVICE_ID = '{service_id}' ".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,service_id = service_id,equipment_key_ids = equipment_key_ids)
        Sql.RunQuery(saqskp_del_2)
        #SAQSAE
        saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids,service_id = service_id)
        Sql.RunQuery(saqsae_del)
        #SAQSCE
        saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{qtRecId}' AND A.QTEREV_RECORD_ID = '{qtRevRecId}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids,service_id= service_id)
        Sql.RunQuery(saqsae_del)
        #SAQSCA
        saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids,service_id = service_id)
        Sql.RunQuery(saqsca_del)
        #SAQSCO
        saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,equipment_key_ids = equipment_key_ids,service_id=service_id)
        Sql.RunQuery(saqsco_del)
        #SAQSGB
        get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,service_id = service_id))
        for delete in get_saqsgb:
            Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,greenbook =str(delete.GREENBOOK),service_id = service_id)
            Sql.RunQuery(Saqsgb_del)
        #SAQSGE
        get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND SERVICE_ID = '{service_id}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,service_id = service_id))
        for delete in get_saqsge:
            Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,greenbook =str(delete.QTESRVGBK_RECORD_ID))
            Sql.RunQuery(Saqsge_del)
        #addon delete implemented for only normal tools
        #SAQSCE
        saqsce_del = "DELETE FROM SAQSCE WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND PAR_SERVICE_ID = '{service_id}' AND EQUIPMENT_ID IN ('{equipment_ids}')".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,key = equipment_ids,service_id = service_id)
        Sql.RunQuery(saqsce_del)
        #SAQSCO
        saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND PAR_SERVICE_ID = '{service_id}' AND EQUIPMENT_ID IN ('{equipment_ids}') ".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,key = key,service_id=service_id)
        Sql.RunQuery(saqsco_del)
        #SAQSCN
        Saqscn_del = "DELETE FROM SAQSCN WHERE QUOTE_RECORD_ID = '{qtRecId}' AND QTEREV_RECORD_ID = '{qtRevRecId}' AND PAR_SERVICE_ID = '{service_id}' AND EQUIPMENT_ID IN ('{equipment_ids}') ".format(qtRevRecId = qtRevRecId,qtRecId = qtRecId,key =key,service_id = service_id)
        Sql.RunQuery(Saqscn_del)        
    else:
        info = "LN 288 - multiple items are not sent to the request. PO or PO -> Greenbook level deletions are not performed"
        Log.Info(info)
        Trace.Write("info => " + str(info))
#CR BULK DELETE -service level ends
