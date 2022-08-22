# =========================================================================================================================================
#   __script_name : SYALLTABOP.PY
#   __script_description : THIS SCRIPT IS USED TO REDIRECT A PAGE FROM THE LIST GRID TO VIEW, EDIT, CLONE PAGE
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
import Webcom.Configurator.Scripting.Test.TestProduct
Trace = Trace  # pylint: disable=E0602
Webcom = Webcom  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
AttributeAccess = AttributeAccess  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
Param = Param  # pylint: disable=E0602
# pylint: disable = no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import datetime
from datetime import datetime

Sql = SQL()
get_user_id = User.Id


def set_global_values(key, value):
    Product.SetGlobal(key, value)


def get_value_from_obj(record_obj, column):
    return getattr(record_obj, column, "")


def load_attr_with_anchor_tag(record_obj, column_name, get_record_val, app_attr_name, anchor_tag_value):
    record_val = ""
    
    parent_rec_id = get_value_from_obj(record_obj, column_name)
    if column_name == 'SOURCE_CONTRACT_ID':
        
        contract_obj = Sql.GetFirst("SELECT CONTRACT_RECORD_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_ID = '{}'".format(parent_rec_id))
        if contract_obj:
            parent_rec_id = contract_obj.CONTRACT_RECORD_ID
    elif column_name == 'APRTRXOBJ_ID':
        quote_obj = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(parent_rec_id,quote_revision_record_id))
        if quote_obj:
            parent_rec_id = quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
            
    if get_record_val is not None and parent_rec_id:
        anchor_tag_id_value = parent_rec_id + anchor_tag_value
        
        if column_name == 'APRTRXOBJ_ID':
            record_val = "<a href='/Configurator.aspx?pid=273' id='{Id}' onclick='Move_to_parent_obj(this)' class='curptr''>{Value}</a>".format(
            Id=anchor_tag_id_value, Value=str(get_record_val)
        )
        else:
            
            record_val = "<a id='{Id}' onclick='Move_to_parent_obj(this)' class='curptr''>{Value}</a>".format(
                Id=anchor_tag_id_value, Value=str(get_record_val)
            )
    Trace.Write("====================> app_attr_name "+str(app_attr_name))
    Trace.Write("====================> record_val "+str(record_val))
    Product.Attributes.GetByName(app_attr_name).AssignValue(record_val)
    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly


def process_clone(details_and_qstns_obj, record_obj, record_id, tab_name, product_name, table_name):
    for detail_and_qstn_obj in details_and_qstns_obj:
        if detail_and_qstn_obj is not None:
            qstn_rec_id = (str(detail_and_qstn_obj.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")).upper()
            qstn_custom_object_field = str(detail_and_qstn_obj.API_FIELD_NAME)

            ####QUESTION ATTRIBUTES
            data_type = str(detail_and_qstn_obj.DATA_TYPE)
            app_attr_name = (
                "QSTN_{}_LONG".format(qstn_rec_id) if data_type == "LONG TEXT AREA" else "QSTN_{}".format(qstn_rec_id)
            )

            if Product.Attributes.GetByName(app_attr_name) is not None:
                if detail_and_qstn_obj.API_FIELD_NAME == "" or detail_and_qstn_obj.API_FIELD_NAME is None:
                    Product.Attributes.GetByName(app_attr_name).AssignValue("")
                    Product.Attributes.GetByName(app_attr_name).Access = 0
                    continue

                get_record_val = get_value_from_obj(record_obj, str(detail_and_qstn_obj.API_FIELD_NAME))
                if data_type == "AUTO NUMBER":
                    if Product.Attributes.GetByName(app_attr_name).DisplayType != "HiddenCalculatedNoMatching":
                        attr_value = Product.Attributes.GetByName(app_attr_name).GetValue()
                        Product.Attributes.GetByName(app_attr_name).HintFormula = record_id
                        Product.Attributes.GetByName(app_attr_name).DisplayType = "HiddenCalculatedNoMatching"
                        Product.Attributes.GetByName(app_attr_name).AssignValue(str(attr_value))

                elif data_type == "PICKLIST":
                    try:
                        # A043S001P01-9167 start
                        if qstn_custom_object_field.upper() == "DECIMAL_PLACES":
                            Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(str(get_record_val))
                        else:
                            Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(get_record_val)
                        Product.Attributes.GetByName(app_attr_name).Access = 0
                        Trace.Write("app_attr_name--> " + str(app_attr_name) + " get_record_val--> " + str(get_record_val))
                    except:
                        Trace.Write("Error: PickList --> Can't get the attribute or assign value")
                        # A043S001P01-9167 end
                elif data_type == "CHECKBOX":
                    if str(get_record_val).upper() == "TRUE" or str(get_record_val) == "1":
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValue("1")
                        Product.Attributes.GetByName(app_attr_name).Access = 0
                    else:
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValue("0")
                        Product.Attributes.GetByName(app_attr_name).Access = 0

                elif data_type == "LOOKUP":
                    Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly

                elif data_type == "FORMULA":
                    Product.Attributes.GetByName(app_attr_name).AssignValue("")
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly

                    app_lookup_attr_name = "QSTN_LKP_{}".format(qstn_rec_id)
                    try:
                        lookup_detail_obj = Sql.GetFirst(
                            """
                                                    SELECT 
                                                        API_NAME AS API_FIELD_NAME 
                                                    FROM 
                                                        SYOBJD (NOLOCK) 
                                                    WHERE 
                                                        LTRIM(RTRIM(DATA_TYPE))='LOOKUP' AND 
                                                        LTRIM(RTRIM(OBJECT_NAME))='{Obj_Name}' AND
                                                        LTRIM(RTRIM(LOOKUP_API_NAME))='{LOOKUP_API_NAME}'
                                                """.format(
                                Obj_Name=table_name, LOOKUP_API_NAME=str(detail_and_qstn_obj.API_FIELD_NAME).strip(),
                            )
                        )

                        if lookup_detail_obj is not None:
                            custom_obj_val = get_value_from_obj(record_obj, str(lookup_detail_obj.API_FIELD_NAME))

                            # Segment Clone - STP Account Editable - Start
                            if Product.Attributes.GetByName(app_lookup_attr_name):
                                Product.Attributes.GetByName(app_lookup_attr_name).Allowed = True
                            # Segment Clone - STP Account Editable - End
                            if Product.Attributes.GetByName(app_lookup_attr_name) is not None and custom_obj_val:
                                Product.Attributes.GetByName(app_lookup_attr_name).HintFormula = custom_obj_val
                            elif Product.Attributes.GetByName(app_lookup_attr_name) is not None:
                                Product.Attributes.GetByName(app_lookup_attr_name).HintFormula = ""
                    except:
                        Trace.Write("EXCEPTION : ERROR")
                else:
                    try:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(get_record_val)
                        Product.Attributes.GetByName(app_attr_name).Access = 0
                    except:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                        Product.Attributes.GetByName(app_attr_name).Access = 0


def process_view(details_and_qstns_obj, record_obj, record_id, tab_name, product_name, table_name):
    formula_data_type = ""
    get_record_val_qry = ""
    for detail_and_qstn_obj in details_and_qstns_obj:
        qstn_custom_object_field = str(detail_and_qstn_obj.API_FIELD_NAME)
        # Trace.Write(
        #     "<<<<<<<<<<"
        #     + str(qstn_custom_object_field)
        #     + ">>>>>>>>>>>>>>>>>>>>>"
        #     + str(detail_and_qstn_obj.SAPCPQ_ATTRIBUTE_NAME)
        # )
        qstn_rec_id = (str(detail_and_qstn_obj.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")).upper()
        data_type = str(detail_and_qstn_obj.DATA_TYPE)
        Decimal_Value = str(detail_and_qstn_obj.DECIMALS)
        if data_type == "LONG TEXT AREA" or data_type == "RICH TEXT AREA":
            app_attr_name = "QSTN_{}_LONG".format(qstn_rec_id)
        else:
            app_attr_name = "QSTN_{}".format(qstn_rec_id)
        if detail_and_qstn_obj.FIELD_LABEL in ["Added Date", "Added By", "Last Modified By", "Last Modified Date"]:
            if Product.Attributes.GetByName(app_attr_name) is not None:
                Product.Attributes.GetByName(app_attr_name).Allowed = True
                
        elif detail_and_qstn_obj.FIELD_LABEL in ["Archived", "Owned By", "Owned Date"]:
            if Product.Attributes.GetByName(app_attr_name) is not None:
                Product.Attributes.GetByName(app_attr_name).Allowed = True
        
        if detail_and_qstn_obj.FIELD_LABEL in [
            "Sales Office ID",
            "Sales Org Currency",
            "Distribution Channel ID",
            "Division ID",
            "Segment ID",
            "Reason for Rejection",            
            "Predecessor Contract ID",
            "Predecessor Contract Name",
            "Parent Quote ID",
            "Parent Quote Name",
            "Employee ID",
            "Net Value",
            "Opportunity ID",
            "Opportunity Name",
            "Pricing Procedure ID",
            "Pricing Procedure Name",
            "Price List ID",
            "Price List Name",            
            "Address 2",
            "Owner ID",
            "Owner Name",
            "Number Of Days",
            "Archived",
            "Owned By",
            "Owned Date",
            "Incoterms Location",
            "Segment Record ID",
            
        ]:
            Trace.Write("che==="+str(detail_and_qstn_obj.FIELD_LABEL)+"attr"+str(app_attr_name))
            if Product.Attributes.GetByName(str(app_attr_name)):
                #Trace.Write("chejjj"+str(app_attr_name))
                Product.Attributes.GetByName(str(app_attr_name)).Allowed = False
                
        Trace.Write("app_attr_name-->" + str(app_attr_name))
        if Product.Attributes.GetByName(app_attr_name) is not None:
            if detail_and_qstn_obj.API_FIELD_NAME == "" or detail_and_qstn_obj.API_FIELD_NAME is None:
                Product.Attributes.GetByName(app_attr_name).AssignValue("")
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                continue
            Product.ResetAttr(str(app_attr_name))
            
            get_record_val = get_value_from_obj(record_obj, str(detail_and_qstn_obj.API_FIELD_NAME))
            Trace.Write('get_record_val@@@'+str(get_record_val))
            if qstn_custom_object_field.upper() == "CPQTABLEENTRYMODIFIEDBY":
                if str(get_record_val) != "" and get_record_val is not None:
                    Trace.Write('get_record_val####'+str(get_record_val))
                    try:
                        get_record_val_qry = Sql.GetFirst(
                            "select USERNAME from users (nolock) where id = ' " + str(get_record_val) + " ' "
                        )
                        
                    except:
                        get_record_val_qry = ""
                    if str(get_record_val_qry) != "" and str(get_record_val_qry) is not None:
                        get_record_val = get_record_val_qry.USERNAME
                        

            formula_data_type = str(detail_and_qstn_obj.FORMULA_DATA_TYPE)
            if data_type == "AUTO NUMBER":
                
                Product.Attributes.GetByName(app_attr_name).Allowed = True
                Product.Attributes.GetByName(app_attr_name).DisplayType = "FreeInputNoMatching"
                Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                Trace.Write("AUTONUMBER-----" + str(Product.Attributes.GetByName(app_attr_name).GetValue()))

            elif data_type == "PICKLIST":
                
                try:
                    
                    Trace.Write("app_attr_name++" + str(app_attr_name))
                    Trace.Write("get_record_val" + str(get_record_val))
                    if app_attr_name == "QSTN_SYSEFL_SY_00773":
                        Trace.Write("app_attr_name---218------" + str(app_attr_name))
                    if app_attr_name == "QSTN_SYSEFL_QT_01155":
                        Trace.Write("app_attr_name-90 DAYS" + str(app_attr_name))
                        cncl = Product.Attributes.GetByName('QSTN_SYSEFL_QT_01155').SelectDisplayValues("90 DAYS")
                        Trace.Write("cancel"+str(cncl))
                        # QUE = Sql.GetTable("SAQTMT")
                        # row = {}
                        # row['CANCELLATION_PERIOD'] = '90 DAYS'
                        # QUE.AddRow(row)
                        # Sql.Upsert(QUE)                        
                        Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly    
                    if qstn_custom_object_field.upper() == "DECIMAL_PLACES":

                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(str(get_record_val))
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(str(get_record_val))
                    elif qstn_custom_object_field.upper() == "CONTRACT_STATUS":
                        
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(str(get_record_val))
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(str(get_record_val))
                    else:
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(get_record_val)
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(get_record_val)
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                except:
                    Trace.Write("Error: PickList --> Can't get the attribute or assign value")
            elif data_type == "CHECKBOX" or formula_data_type == "CHECKBOX":
                # Trace.Write(str(app_attr_name) + " Error: PickList -->" + str(data_type))
                # Trace.Write("Error: PickList1 -->" + str(get_record_val))
                if str(get_record_val).upper() == "TRUE" or str(get_record_val) == "1":
                    Trace.Write(str(app_attr_name) + " Error: PickList33 -->" + str(data_type))
                    Product.Attributes.GetByName(app_attr_name).SelectDisplayValue("1")
                    #   Product.Attributes.GetByName(app_attr_name).Access = 1
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                elif str(get_record_val) == "False" or str(get_record_val) == "0":
                    Product.Attributes.GetByName(app_attr_name).SelectDisplayValue("0")
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                    # Product.Attributes.GetByName(app_attr_name).Access = 0
                elif str(get_record_val)=="":
                    Trace.Write('Empty get_rec_val')
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                    
                    
            elif data_type == "NUMBER" or data_type == "CURRENCY":
                # Trace.Write("Error444444: PickList1 -->" + str(get_record_val))
                # Trace.Write("Error444444: PickList1 -->" + str(app_attr_name))
                # Trace.Write("Error444444: PickList1 -->" + str(Decimal_Value))
                if data_type == "CURRENCY":
                    Sym = "$"
                else:
                    Sym = ""
                if get_record_val is not None and str(get_record_val).strip() != "" and str(get_record_val).strip() != "0":
                    
                    if str(qstn_rec_id) == "SYSEFL_TQ_00895":
                        data_type = "number"
                    #Trace.Write("Error444444: PickList12 -->" + str(Decimal_Value))
                    my_format = "{:." + str(Decimal_Value) + "f}"
                    
                    get_record_val = Sym + str(my_format.format(round(float(get_record_val), int(Decimal_Value))))
                    
                    Product.Attributes.GetByName(app_attr_name).AssignValue((get_record_val))
                #Trace.Write("check1111122223Decimal_Value" + str(Product.Attributes.GetByName(app_attr_name).GetValue()))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly

            elif formula_data_type == "PERCENT" or data_type == "PERCENT":
                #Trace.Write("258 get_record_val" + str(get_record_val))
                if get_record_val:
                    my_format = "{:." + str(Decimal_Value) + "f}"
                    get_record_val = str(my_format.format(round(float(get_record_val), int(Decimal_Value))))
                    Product.Attributes.GetByName(app_attr_name).AssignValue((get_record_val))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                

            elif data_type == "FORMULA" and formula_data_type != "CHECKBOX":
                if tab_name == "Quotes" and detail_and_qstn_obj.API_FIELD_NAME == "SOURCE_CONTRACT_ID":
                    
                    load_attr_with_anchor_tag(record_obj, "SOURCE_CONTRACT_ID", get_record_val, app_attr_name, "|Contracts")
                elif (tab_name == "My Approval Queue" and detail_and_qstn_obj.API_FIELD_NAME == "APRTRXOBJ_ID") or (tab_name == "Team Approval Queue" and detail_and_qstn_obj.API_FIELD_NAME == "APRTRXOBJ_ID"):
                    load_attr_with_anchor_tag(record_obj, "APRTRXOBJ_ID", get_record_val, app_attr_name, "|Quotes")
                else:
                    if detail_and_qstn_obj.API_FIELD_NAME == "EXCHANGE_RATE_DATE" and get_record_val != "":
                        get_record_val = str(get_record_val).split(" ")[0]
                    try:
                        Trace.Write(">>>>>>>>>>>>" + str(app_attr_name))
                        Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                    except:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(get_record_val)

                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                    app_lookup_attr_name = "QSTN_LKP_{}".format(qstn_rec_id)
                    Trace.Write("app_lookup_attr_name----------> " + str(app_lookup_attr_name))
                    try:
                        lookup_detail_obj = Sql.GetFirst(
                            """
                                                SELECT 
                                                    API_NAME
                                                FROM 
                                                    SYOBJD (NOLOCK) 
                                                WHERE 
                                                    LTRIM(RTRIM(DATA_TYPE))='LOOKUP' AND 
                                                    LTRIM(RTRIM(OBJECT_NAME))='{Obj_Name}' AND
                                                    LTRIM(RTRIM(LOOKUP_API_NAME))='{LOOKUP_API_NAME}'
                                            """.format(
                                Obj_Name=table_name, LOOKUP_API_NAME=str(detail_and_qstn_obj.API_FIELD_NAME).strip(),
                            )
                        )

                        if lookup_detail_obj is not None:
                            if Product.Attributes.GetByName(app_lookup_attr_name):
                                Product.Attributes.GetByName(app_lookup_attr_name).Allowed = False
                            custom_obj_val = get_value_from_obj(record_obj, str(lookup_detail_obj.API_FIELD_NAME))
                            if Product.Attributes.GetByName(app_lookup_attr_name) is not None and custom_obj_val:
                                Product.Attributes.GetByName(app_lookup_attr_name).HintFormula = custom_obj_val
                            elif Product.Attributes.GetByName(app_lookup_attr_name) is not None:
                                Product.Attributes.GetByName(app_lookup_attr_name).HintFormula = ""
                    except:
                        Trace.Write("ERROR")
            elif data_type == "LOOKUP":
                Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
            elif data_type == "DATE/TIME":
                try:
                    get_record_val=datetime.strptime(str(get_record_val), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')
                    Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                except:
                    Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
            else:
                if str(app_attr_name) == "QSTN_SYSEFL_AC_00067_LONG":
                    GetMsgBoyVal = Sql.GetFirst(
                        " select * FROM ACEMTP(NOLOCK) WHERE EMAIL_TEMPLATE_RECORD_ID = '" + str(record_id) + "' "
                    )
                    if GetMsgBoyVal is not None:
                        get_record_val = (
                            str(GetMsgBoyVal.MESSAGE_BODY)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_2)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_3)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_4)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_5)
                        )
                    Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                else:    
                    try:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                        Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                    except:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(get_record_val)
                        Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
    


def process_edit(details_and_qstns_obj, record_obj, record_id, tab_name, product_name, table_name):
    get_record_val_qry = ""
    Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = ""
    for detail_and_qstn_obj in details_and_qstns_obj:
        qstn_rec_id = (str(detail_and_qstn_obj.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")).upper()
        qstn_custom_object_field = str(detail_and_qstn_obj.API_FIELD_NAME)
        #Trace.Write("RES_CHK" + str(qstn_custom_object_field))
        data_type = str(detail_and_qstn_obj.DATA_TYPE)
        if data_type == "LONG TEXT AREA" or data_type == "RICH TEXT AREA":
            
            app_attr_name = "QSTN_{}_LONG".format(qstn_rec_id)
            if str(detail_and_qstn_obj.EDITABLE_ONINSERT).upper() == "TRUE":
                #Trace.Write("-------69---------"+str(app_attr_name))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.Editable
        else:
            app_attr_name = "QSTN_{}".format(qstn_rec_id)
        #Trace.Write("315-app_attr_name--> " + str(app_attr_name))
        if detail_and_qstn_obj.FIELD_LABEL in [
            "Sales Office ID",
            "Sales Org Currency",
            "Distribution Channel ID",
            "Division ID",
            "Segment ID",
            "Reason for Rejection",
            "Predecessor Contract ID",
            "Predecessor Contract Name",
            "Parent Quote ID",
            "Parent Quote Name",
            "Employee ID",
            "Net Value",
            "Opportunity ID",
            "Opportunity Name",
            #"Pricing Procedure ID",
            #"Pricing Procedure Name",
            "Price List ID",
            "Price List Name",            
            "Address 2",            
        ]:
            if Product.Attributes.GetByName(app_attr_name) is not None:
                Product.Attributes.GetByName(app_attr_name).Allowed = False
                
        if Product.Attributes.GetByName(app_attr_name) is not None:
            #Trace.Write("318 inside if" + str(detail_and_qstn_obj.API_FIELD_NAME))
            if detail_and_qstn_obj.API_FIELD_NAME == "" or detail_and_qstn_obj.API_FIELD_NAME is None:
                Product.Attributes.GetByName(app_attr_name).AssignValue("")
                if detail_and_qstn_obj.PERMISSION != "READ ONLY" and detail_and_qstn_obj.SOURCE_DATA != "ERP":
                    Product.Attributes.GetByName(app_attr_name).Access = 0
                else:
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                continue

            get_record_val = get_value_from_obj(record_obj, str(detail_and_qstn_obj.API_FIELD_NAME))
            if qstn_custom_object_field.upper() == "CPQTABLEENTRYMODIFIEDBY":
                if str(get_record_val) != "" and get_record_val is not None:
                    try:
                        get_record_val_qry = Sql.GetFirst(
                            "select USERNAME from users (nolock) where id = ' " + str(get_record_val) + " ' "
                        )
                        
                    except:
                        get_record_val_qry = ""
                    if str(get_record_val_qry) != "" and str(get_record_val_qry) is not None:
                        get_record_val = get_record_val_qry.USERNAME
                        
            formula_data_type = str(detail_and_qstn_obj.FORMULA_DATA_TYPE)

            if data_type == "AUTO NUMBER":
                Product.Attributes.GetByName(app_attr_name).Allowed = True
                Product.Attributes.GetByName(app_attr_name).DisplayType = "FreeInputNoMatching"
                Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly

            elif data_type == "PICKLIST":
                try:
                    if qstn_custom_object_field.upper() == "DECIMAL_PLACES":
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(str(get_record_val))
                    else:
                        Product.Attributes.GetByName(app_attr_name).SelectDisplayValues(get_record_val)
                    if detail_and_qstn_obj.PERMISSION != "READ ONLY" and detail_and_qstn_obj.SOURCE_DATA != "ERP":
                        Product.Attributes.GetByName(app_attr_name).Access = 0
                    else:
                        Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                except:
                    Trace.Write("Error: PickList --> Can't get the attribute or assign value")
            elif data_type == "CHECKBOX" or formula_data_type == "CHECKBOX":
                sap_part_no = ""
                maspmc_list_obj = Sql.GetList(
                    "SELECT ITMCATGRP_ID,SAP_PART_NUMBER,SORPLTMATFULLCTY_RECORD_ID FROM MASPMC  with (nolock) WHERE SAP_PART_NUMBER='{}'".format(
                        sap_part_no
                    )
                )
                if maspmc_list_obj is not None:
                    bans_chk = 0
                    for maspmc_obj in maspmc_list_obj:
                        if str(maspmc_obj.ITMCATGRP_ID) == "BANS":
                            bans_chk = 1
                            break
                    if bans_chk == 1:
                        Product.Attributes.GetByName("QSTN_SYSEFL_MA_00367").SelectValue("0")
                        Product.Attributes.GetByName("QSTN_SYSEFL_MA_00367").Access = AttributeAccess.Editable
                    else:
                        Product.Attributes.GetByName("QSTN_SYSEFL_MA_00367").SelectValue("1")
                        Product.Attributes.GetByName("QSTN_SYSEFL_MA_00367").Access = AttributeAccess.Editable

            elif data_type == "LOOKUP":
                Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                if detail_and_qstn_obj.PERMISSION != "READ ONLY" and detail_and_qstn_obj.SOURCE_DATA != "ERP":
                    Product.Attributes.GetByName(app_attr_name).Access = 0
                else:
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly

            elif data_type == "FORMULA" and formula_data_type != "CHECKBOX":
                Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                app_lookup_attr_name = "QSTN_LKP_{}".format(qstn_rec_id)

                lookup_detail_obj = Sql.GetFirst(
                    """
                                                SELECT 
                                                    API_NAME 
                                                FROM 
                                                    SYOBJD (NOLOCK) 
                                                WHERE 
                                                    LTRIM(RTRIM(DATA_TYPE))='LOOKUP' AND 
                                                    LTRIM(RTRIM(OBJECT_NAME))='{Obj_Name}' AND
                                                    LTRIM(RTRIM(LOOKUP_API_NAME))='{LOOKUP_API_NAME}'
                                            """.format(
                        Obj_Name=table_name, LOOKUP_API_NAME=str(detail_and_qstn_obj.API_FIELD_NAME).strip()
                    )
                )

                if lookup_detail_obj is not None:
                    custom_obj_val = get_value_from_obj(record_obj, str(lookup_detail_obj.API_NAME))
                    if Product.Attributes.GetByName(app_lookup_attr_name) is not None and custom_obj_val:
                        Product.Attributes.GetByName(app_lookup_attr_name).HintFormula = custom_obj_val
                    elif Product.Attributes.GetByName(app_lookup_attr_name) is not None:
                        Product.Attributes.GetByName(app_lookup_attr_name).HintFormula = ""

                if detail_and_qstn_obj.PERMISSION != "READ ONLY" and detail_and_qstn_obj.SOURCE_DATA != "ERP":
                    if Product.Attributes.GetByName(app_attr_name):
                        Product.Attributes.GetByName(app_attr_name).Access = 0
                    if Product.Attributes.GetByName(app_lookup_attr_name):
                        Product.Attributes.GetByName(app_lookup_attr_name).Access = 0
                elif detail_and_qstn_obj.PERMISSION == "READ ONLY" or detail_and_qstn_obj.SOURCE_DATA == "ERP":
                    if Product.Attributes.GetByName(app_attr_name):
                        Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                    if Product.Attributes.GetByName(app_lookup_attr_name):
                        Product.Attributes.GetByName(app_lookup_attr_name).Access = AttributeAccess.ReadOnly
            else:
                
                if str(app_attr_name) == "QSTN_SYSEFL_AC_00067_LONG":
                    GetMsgBoyVal = Sql.GetFirst(
                        " select * FROM ACEMTP(NOLOCK) WHERE EMAIL_TEMPLATE_RECORD_ID = '" + str(record_id) + "' "
                    )
                    if GetMsgBoyVal is not None:
                        get_record_val = (
                            str(GetMsgBoyVal.MESSAGE_BODY)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_2)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_3)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_4)
                            + ""
                            + str(GetMsgBoyVal.MESSAGE_BODY_5)
                        )
                    Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                    Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.Editable
                else:                    
                    try:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(str(get_record_val))
                        if detail_and_qstn_obj.PERMISSION != "READ ONLY" and detail_and_qstn_obj.SOURCE_DATA != "ERP":
                            
                            Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.Editable
                            
                        else:
                            
                            Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly
                    except:
                        Product.Attributes.GetByName(app_attr_name).AssignValue(get_record_val)
                        if (
                            detail_and_qstn_obj.PERMISSION != "READ ONLY"
                            and detail_and_qstn_obj.SOURCE_DATA != "ERP"
                            and app_attr_name != "QSTN_SYSEFL_PB_01436"
                        ):
                            
                            Product.Attributes.GetByName(app_attr_name).Access = 0
                        else:
                            Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.ReadOnly


def do_process(record_id, tab_name, action, product_name):
    def get_record_obj(obj_name):
        Trace.Write(obj_name)
        
        header_obj = Sql.GetFirst(
            """
                                    SELECT 
                                        RECORD_ID, RECORD_NAME 
                                    FROM 
                                        SYOBJH (NOLOCK) 
                                    WHERE 
                                        OBJECT_NAME='{Obj_Name}'
                                """.format(
                Obj_Name=str(obj_name).strip()
            )
        )

        if header_obj is not None:
            record_obj = Sql.GetFirst(
                """
                                        SELECT 
                                            *
                                        FROM 
                                            {Table_Name} (NOLOCK) 
                                        WHERE
                                            {Record_Id_Column} = '{Record_Id_Value}'
                                    """.format(
                    Table_Name=str(obj_name).strip(), Record_Id_Column=str(header_obj.RECORD_NAME), Record_Id_Value=record_id
                )
            )
            
            if record_obj is not None:
                Trace.Write("ffffffff" + str(record_obj))
                return record_obj

        return None
    #A055S000P01-3428-restrict section level permissions-start
    '''sections_obj = Sql.GetList(
        """
                            SELECT 
                                SYTABS.RECORD_ID as TAB_RECORD_ID, SYTABS.SAPCPQ_ALTTAB_NAME, SYSECT.RECORD_ID, SYSECT.SECTION_NAME, SYSECT.PRIMARY_OBJECT_NAME 
                            FROM 
                                SYTABS (NOLOCK) 
                            JOIN 
                                SYPAGE (NOLOCK) ON SYPAGE.TAB_RECORD_ID = SYTABS.RECORD_ID AND SYPAGE.TAB_NAME = SYTABS.TAB_LABEL   
                            JOIN
                                SYSECT (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID AND SYSECT.PAGE_NAME = SYPAGE.PAGE_NAME
                            WHERE 
                                LTRIM(RTRIM(SYTABS.TAB_LABEL)) = '{TAB_NAME}' AND 
                                LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND
                                ISNULL(SYSECT.SECTION_NAME,'') != '' AND
                                ISNULL(SYSECT.PRIMARY_OBJECT_NAME,'') != ''  
                            """.format(
            TAB_NAME=tab_name, APP_LABEL=product_name, get_user_id=get_user_id
        )
    )'''
    
    
    sections_obj = Sql.GetList(
        """
                            SELECT 
                                SYTABS.RECORD_ID as TAB_RECORD_ID, SYTABS.SAPCPQ_ALTTAB_NAME, SYSECT.RECORD_ID, SYSECT.SECTION_NAME, SYSECT.PRIMARY_OBJECT_NAME 
                            FROM 
                                SYTABS (NOLOCK) 
                            JOIN 
                                SYPAGE (NOLOCK) ON SYPAGE.TAB_RECORD_ID = SYTABS.RECORD_ID AND SYPAGE.TAB_NAME = SYTABS.TAB_LABEL   
                            JOIN
                                SYSECT (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID AND SYSECT.PAGE_NAME = SYPAGE.PAGE_NAME   
                            JOIN 
                                SYPRSN (NOLOCk) ON  SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID  
                            JOIN 
                                USERS_PERMISSIONS UP (NOLOCK) ON UP.Permission_id = SYPRSN.PROFILE_RECORD_ID      
                            WHERE 
                                LTRIM(RTRIM(SYTABS.TAB_LABEL)) = '{TAB_NAME}' AND 
                                LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND
                                ISNULL(SYSECT.SECTION_NAME,'') != '' AND Up.user_id = '{get_user_id}' AND
                                SYPRSN.VISIBLE = 1 AND
                                ISNULL(SYSECT.PRIMARY_OBJECT_NAME,'') != ''  
                            """.format(
            TAB_NAME=tab_name, APP_LABEL=product_name, get_user_id=get_user_id
        )
    )
    #A055S000P01-3428-restrict section level permissions-end
    '''sections_obj = Sql.GetList("""
                            SELECT 
                                SYTABS.RECORD_ID as TAB_RECORD_ID, SYTABS.SAPCPQ_ALTTAB_NAME, SYSECT.RECORD_ID, SYSECT.SECTION_NAME, SYSECT.PRIMARY_OBJECT_NAME 
                            FROM 
                                SYTABS (NOLOCK) 
                            JOIN
                                SYSECT (NOLOCK) ON SYSECT.TAB_RECORD_ID = SYTABS.RECORD_ID AND SYSECT.TAB_NAME = SYTABS.TAB_LABEL                          
                            WHERE 
                                LTRIM(RTRIM(SYTABS.TAB_NAME)) = '{Tab_Text}' AND 
                                LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND
                                ISNULL(SYSECT.SECTION_NAME,'') != '' AND
                                ISNULL(SYSECT.PRIMARY_OBJECT_NAME,'') != ''  
                            """.format(Tab_Text=tab_name, APP_LABEL=product_name))'''

    if sections_obj is not None:
        
        Trace.Write("sections_obj" + str(sections_obj))
        for index, section_obj in enumerate(sections_obj):
            if index == 0:
                TestProduct.ChangeTab(str(section_obj.SAPCPQ_ALTTAB_NAME).strip())
                Trace.Write("TestProduct" + str(TestProduct))
                try:
                    Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue(action.upper())
                except:
                    pass
            table_name = section_obj.PRIMARY_OBJECT_NAME
            Trace.Write("table_name--->"+str(table_name))
            record_obj = get_record_obj(section_obj.PRIMARY_OBJECT_NAME)
            
            if record_obj is not None:
                
                details_and_qstns_obj = Sql.GetList(
                    """
                                                    SELECT TOP 1000 
                                                        SYSEFL.RECORD_ID,SYSEFL.SAPCPQ_ATTRIBUTE_NAME, SYSEFL.FIELD_LABEL, SYSEFL.API_FIELD_NAME, 
                                                        SYSEFL.API_NAME, SYSEFL.SECTION_NAME,  SYOBJD.DATA_TYPE,
                                                        SYOBJD.EDITABLE_ONINSERT, SYOBJD.CURRENCY_INDEX, SYOBJD.FORMULA_DATA_TYPE,  SYOBJD.PERMISSION, 
                                                        SYOBJD.SOURCE_DATA, SYOBJD.DECIMALS
                                                    FROM 
                                                        SYSEFL (NOLOCK) 
                                                    INNER JOIN 
                                                        SYOBJD (NOLOCK) ON  SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME 
                                                                            AND  SYOBJD.OBJECT_NAME = SYSEFL.API_NAME 
                                                    WHERE
                                                        RTRIM(LTRIM(SYSEFL.API_NAME)) ='{Custom_Object_Name}' AND
                                                        RTRIM(LTRIM(SYSEFL.SECTION_NAME))='{Section_Text}' AND
                                                        RTRIM(LTRIM(SYSEFL.SECTION_RECORD_ID))='{Section_Record_Id}'
                                                    ORDER BY SYSEFL.DISPLAY_ORDER                                                   
                                                    """.format(
                        Custom_Object_Name=str(section_obj.PRIMARY_OBJECT_NAME).strip(),
                        Section_Text=str(section_obj.SECTION_NAME).strip(),
                        Section_Record_Id=str(section_obj.RECORD_ID).strip(),
                    )
                )
                # Trace.Write(
                #     "SELECT TOP 1000 SYSEFL.RECORD_ID,SYSEFL.SAPCPQ_ATTRIBUTE_NAME, SYSEFL.FIELD_LABEL, SYSEFL.API_FIELD_NAME, SYSEFL.API_NAME, SYSEFL.SECTION_NAME,  SYOBJD.DATA_TYPE, SYOBJD.EDITABLE_ONINSERT,SYOBJD.CURRENCY_INDEX, SYOBJD.FORMULA_DATA_TYPE,  SYOBJD.PERMISSION, SYOBJD.SOURCE_DATA, SYOBJD.DECIMALS FROM SYSEFL (NOLOCK) INNER JOIN SYOBJD (NOLOCK) ON  SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME AND  SYOBJD.OBJECT_NAME = SYSEFL.API_NAME WHERE RTRIM(LTRIM(SYSEFL.API_NAME)) ='{Custom_Object_Name}' AND RTRIM(LTRIM(SYSEFL.SECTION_NAME))='{Section_Text}' AND RTRIM(LTRIM(SYSEFL.SECTION_RECORD_ID))='{Section_Record_Id}' ORDER BY SYSEFL.DISPLAY_ORDER ".format(
                #         Custom_Object_Name=str(section_obj.PRIMARY_OBJECT_NAME).strip(),
                #         Section_Text=str(section_obj.SECTION_NAME).strip(),
                #         Section_Record_Id=str(section_obj.RECORD_ID).strip(),
                #     )
                # )

                if details_and_qstns_obj is not None:
                    
                    if action == "CLONE":
                        process_clone(details_and_qstns_obj, record_obj, record_id, tab_name, product_name, table_name)
                    elif action == "EDIT":
                        process_edit(details_and_qstns_obj, record_obj, record_id, tab_name, product_name, table_name)
                    elif action == "VIEW":
                        process_view(details_and_qstns_obj, record_obj, record_id, tab_name, product_name, table_name)
    return True


record_id = str(Param.Primary_Data).strip()
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ""
Trace.Write("record_name-------------" + str(record_id))
tab_name = str(Param.TabNAME).strip()
Trace.Write("tab_name-------------" + str(tab_name))
action = str(Param.ACTION).strip()
Trace.Write('Action--------'+str(action))
try:
    product_name = Product.Name 
except:
    product_name="SALES"

# A043S001P01-11419-Dhurga Start
if hasattr(Param, "Primary_Data_rec"):
    try:
        Primary_Data_rec = Param.Primary_Data_rec
        
        Product.SetGlobal("Primary_Data_rec", str(Primary_Data_rec))
    except UnicodeEncodeError:
        
        Product.SetGlobal("Primary_Data_rec", Primary_Data_rec)
    except:
        Trace.Write("Error")

else:
    Primary_Data_rec = ""


# A043S001P01-11419-Dhurga End

Product.SetGlobal("Pricemodel", "")

if tab_name != "":
    try:
        CurrentTab = TestProduct.CurrentTab
    except:
        CurrentTab = "Quotes"
    Trace.Write("TestProduct.CurrentTab "+str(CurrentTab))
    if (CurrentTab == "Quotes" or CurrentTab == "SALES") and record_id != "":
        Product.SetGlobal("contract_quote_record_id", record_id)
    elif (CurrentTab == "Contracts" or CurrentTab == "SALES") and record_id != "":
        Product.SetGlobal("contract_record_id", record_id)
        #Trace.Write("COntract_TESTZ"+str(Product.GetGlobal("contract_record_id")))
    elif (CurrentTab == "Team Approvals Queue" or CurrentTab == "Team Approvals Queues"):
        Product.SetGlobal("team_approval_record_id", record_id)
    if tab_name == "Quotes" and product_name == "APPROVAL CENTER":
        product_name = "SALES"
    do_process(record_id, tab_name, action, product_name)
    ScriptExecutor.ExecuteGlobal("SYLDRLADBN")
    ScriptExecutor.ExecuteGlobal("SYGETVRCTX")
    ScriptExecutor.ExecuteGlobal("SYRLEXEEND")