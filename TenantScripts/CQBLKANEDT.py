# =========================================================================================================================================
#   __script_name : CQBLKANEDT.PY
#   __script_description : THIS SCRIPT IS USED FOR ANNUALIZED BULK UPDATE FUNCTIONALITY
#   __primary_author__ : VIKNESH DURAISAMY, MARK THOMSON
#   __create_date :02-09-2022
# ==========================================================================================================================================
from SYDATABASE import SQL
import System.Net
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
productAttributesGetByName = lambda productAttribute: Product.Attributes.GetByName(productAttribute) or ""
class AnnualizedItemsQuery:
    def __init__(self):
        try:
            self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        except:
            self.contract_quote_record_id = ''	
        try:
            self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        except:
            self.quote_revision_record_id = ''
        try:
            self.current_prod = Product.Name
        except:
            self.current_prod = "Sales"
        try:
            if PARAM.SORT_COLUMN.upper() != 'NONE':
                self.sort_column = Param.SORT_COLUMN
            else:
                self.sort_column = " LINE "
            if Param.SORT_ORDER.upper() != 'NONE':
                self.sort_order = Param.SORT_ORDER
            else:
                self.sort_order = " ASC "
        except:
            self.sort_column = " LINE "
            self.sort_order = " ASC "
        self.RECORD_ID = RECORD_ID
    def get_columns(self):
        table_columns = Sql.GetFirst("SELECT OBJ_REC_ID,COLUMNS,COLUMN_REC_ID,SAPCPQ_ATTRIBUTE_NAME,PARENT_LOOKUP_REC_ID FROM SYOBJR (nolock) WHERE SAPCPQ_ATTRIBUTE_NAME = '{}' ".format(self.RECORD_ID))
        return table_columns
    def load_query_grid(self):
        RelatedDrop_str = ""
        table_header = ""
        Test = PerPage = Page_start = Page_End = PageInform = ""
        if str(PerPage) == "" and str(PageInform) == "":
            Page_start = 1
            Page_End = PerPage = 10
            PageInform = "1___10___10"
        else:
            Page_start = int(PageInform.split("___")[0])
            Page_End = int(PageInform.split("___")[1])
            PerPage = PerPage
        table_columns = self.get_columns()
        input_type = "data-filter-control='select'"
        action_name = "ACTIONS"
        PARENT_LOOKUP_REC_ID = table_columns.PARENT_LOOKUP_REC_ID
        columnList = eval(table_columns.COLUMNS)
        Obj_Name = table_columns.OBJ_REC_ID
        table_id = table_columns.SAPCPQ_ATTRIBUTE_NAME.replace("-", "_") + "_" + str(Obj_Name).replace("-", "_") + "QI"
        table_ids = "#"+table_id
        for col in columnList:
            column_titles = Sql.GetFirst("select FIELD_SHORT_LABEL,FIELD_LABEL from SYOBJD (nolock) where API_NAME = '{col}' and OBJECT_NAME = 'SAQICO'".format(col = col))
            table_header += ("""<th data-field="{column_name}"  data-sortable="true" {input_type} data-title-tooltip="{label}"><div>{title}</div></th>""".format(column_name = col,title = str(column_titles.FIELD_SHORT_LABEL).upper() if column_titles.FIELD_SHORT_LABEL is not None else str(column_titles.FIELD_LABEL).upper(),label=str(column_titles.FIELD_LABEL),input_type = input_type))
        QuryCount_str = Sql.GetFirst("select count(*) as cnt from SAQICO (nolock) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') ")
        count = str(QuryCount_str.cnt) + " Record Found" if QuryCount_str.cnt == 1 else str(QuryCount_str.cnt) + " Records Found"
        table_content = """
            <table id="{table_id}" data-pagination="false" data-filter-control="true"  data-maintain-selected="true" data-locale = "en-US">
                <thead>
                    <tr id='getbannername' >
                        <th data-field="{action_name}" >
                            <div class="action_col">{action_name}</div>
                            <button class="searched_button" id="Act_{table_id}" onclick = "searchQueryGrid()">Search</button>
                        </th>
                        {table_header}
                    </tr>
                </thead>
                <tbody onclick="Table_Onclick_Scroll(this)">
                    <tr class = 'noRecDisp'>
                        <td colspan = '12' class = 'txtltimp'>{count}</td>
                    </tr>
                </tbody>
            </table>
        """.format(count = count,table_id = table_id,table_header = table_header,action_name = action_name)
        table_content = table_content.format(table_header)
        table_data = []
        filter_level_list = []
        cv_list = []
        dropdowndiv = ""
        selectalldiv = ""
        domain_name = str(Sql.getDomainDetails())
        status = {
                'ACQUIRED':'<img title="Acquired" src="/mt/'+str(domain_name)+'/Additionalfiles/Green_Tick.svg">',
                'CFG-ON HOLD TKM':'<img title="ON-HOLD-TKM" src="/mt/'+str(Sql.getDomainDetails())+'/Additionalfiles/icons/on_hold_tkm.svg">',
                'OFFLINE PRICING':'<img title="OFFLINE PRICING" src="/mt/'+str(domain_name)+'/Additionalfiles/manual_pricing.svg">', 
                'PRR-ON HOLD PRICING':'<img title="PRR-ON HOLD PRICING" src="/mt/'+str(domain_name)+'/Additionalfiles/pricing_on_hold.svg">'
            }
        COLUMNS = table_columns.COLUMNS.replace('[','').replace(']','').replace("'",'')
        get_data = Sql.GetList("select TOP 10 "+str(COLUMNS)+" from SAQICO (nolock) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') ORDER BY LINE ASC")
        for record in get_data:
            row = {}
            for column in COLUMNS.split(','):
                value = eval('record.'+str(column))
                if column == "STATUS":
                    row[column] = status.get(value)
                else:
                    row[column] = str(value)
            row['ACTIONS'] = ''
            table_data.append(row)
        QueryCount = QuryCount_str.cnt
        Page_start = 0 if int(QueryCount)==0 else str(Page_start)
        if QueryCount < int(Page_End):
            PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
        else:
            PageInformS = str(Page_start) + " - " + str(Page_End) + " of"
        Footer = (
            '<div class="col-md-12 brdr listContStyle padbthgt30"  ><div class="col-md-4 pager-numberofitem  clear-padding"><span class="pager-number-of-items-item noofitem" id="'
            + str(table_id)
            + '_NumberofItem"  >'
            + str(PageInformS)
            + ' </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
            + str(table_id)
            + '_totalItemCount"  >'
            + str(QueryCount)
            + '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right veralmert"><select onchange="queriedItemsFilter(\'countchange\',\''
            + str(RECORD_ID)
            + "','"
            + str(table_id)
            + '\')" id="'
            + str(table_id)
            + '_PageCountValue"  class="form-control pagecunt"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding totcnt"   data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brdr0"  ><ul class="pagination pagination"><li class="disabled"  ><a href="javascript:void(0)"  onclick="queriedItemsFilter(\'first\',\''
            + str(RECORD_ID)
            + "','"
            + str(table_id)
            + '\')"><i class="fa fa-caret-left fnt14bold"  ></i><i class="fa fa-caret-left fnt14"  ></i></a></li><li class="disabled"><a href="javascript:void(0)" onclick="queriedItemsFilter(\'previous\',\''
            + str(RECORD_ID)
            + "','"
            + str(table_id)
            + '\')" ><i class="fa fa-caret-left fnt14"  "></i>PREVIOUS</a></li><li class="disabled"><a href="javascript:void(0)" class="disabledPage"  onclick="queriedItemsFilter(\'next\',\''
            + str(RECORD_ID)
            + "','"
            + str(table_id)
            + '\')">NEXT<i class="fa fa-caret-right fnt14"  ></i></a></li><li class="disabled"><a href="javascript:void(0)" onclick="queriedItemsFilter(\'last\',\''
            + str(RECORD_ID)
            + "','"
            + str(table_id)
            + '\')" class="disabledPage" ><i class="fa fa-caret-right fnt14"  ></i><i class="fa fa-caret-right fnt14bold"  ></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"  > <span id="'
            + str(table_id)
            + '_page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2"  >Page </span></div></div>'
        )
        cls = "eq(3)"
        RelatedDrop_str = (
            '$("'
            + str(table_ids)
            + '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");$("'+str(table_ids)+' > thead > tr > th.bs-checkbox.wth45 > div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>");$("'
            + str(table_ids)
            + "\").on('sort.bs.table', function (e, name, order) {  localStorage.setItem('"
            + str(table_ids)
            + "_SortColumn', name); localStorage.setItem('"
            + str(table_ids)
            + "_SortColumnOrder', order); queriedItemsFilter('sort', 'SYOBJR-98883', '"
            + str(table_id)
            + "');});"
        )
        Objd_Obj = Sql.GetList(
                "select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE,FIELD_SHORT_LABEL from  SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQICO'"
            )
        if Objd_Obj:
            checkbox_list = [
                    inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
                ]
        for key, col_name in enumerate(list(columnList)):            
            StringValue_list = []
            DropDownList = [] #A055S000P01-20922-M
            objss_obj = Sql.GetFirst(
                "SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM  SYOBJD (nolock) WHERE OBJECT_NAME='SAQICO' and API_NAME = '"
                + str(col_name)
                + "'"
            )
            if col_name in checkbox_list:
                DropDownList.append(["True", "False"])
            elif str(objss_obj.PICKLIST).upper() == "TRUE":
                xcdStr = (
                    "SELECT DISTINCT TOP 10000000 "
                    + str(col_name)
                    + " FROM SAQICO (nolock) where QUOTE_RECORD_ID = '"
                    + str(self.contract_quote_record_id)
                    + "' AND QTEREV_RECORD_ID = '"
                    + str(self.quote_revision_record_id)
                    + "' AND STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') ORDER BY "
                    + str(col_name)
                )
                xcd = Sql.GetList(xcdStr)
                try:
                    if xcd is not None:
                        StringValue_list = [
                            str(eval("ins." + str(col_name))) for ins in xcd if eval("ins." + str(col_name)) != ""
                        ]						
                        StringValue_list = filter(None, list(set(StringValue_list)))
                        if len(StringValue_list) == 0:
                            StringValue_list = [""]
                    else:
                        StringValue_list = [""]
                    StringValue_list.sort()
                except:
                    StringValue_list = [""]
                all_items = ["Select All"] if len(StringValue_list) > 1 else []
                for string in StringValue_list:
                    all_items.append(string)
                DropDownList.append(all_items)
            else:
                DropDownList = []
            if len(DropDownList) != 0:
                for item in DropDownList:
                    for values in item:
                        col_name = str(col_name).strip()
                        if len(item) == 1:
                            dropdowndiv= (
                                '<div class="multiselect-qtlist-cntryofacc"><div class="selectBox" onclick="showMultiChkbox(\''+str(col_name)+'\')"><div id="listchekSec"><div id="listcheckacc_'+str(col_name)+'" class="spanMultichkBox"></div><i class="selectArrow down"></i></div></div><div id="selectallmultichkbox_'+str(col_name)+'" style="display: none;"><label class="selectConfig"><input type="checkbox" name="check-box-each-type" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="choosealltecheckbox(this,\''+str(col_name)+'\')" value="'+str(values)+'"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class="country_chkbox_data">'
                                +str(values)
                                +'</span></label>'
                            )
                        elif len(item) > 1:
                            if values == "Select All":
                                dropdowndiv= (
                                    '<div class="multiselect-qtlist-cntryofacc"><div class="selectBox" onclick="showMultiChkbox(\''+str(col_name)+'\')"><div id="listchekSec"><div id="listcheckacc_'+str(col_name)+'" class="spanMultichkBox"></div><i class="selectArrow down"></i></div></div><div id="selectallmultichkbox_'+str(col_name)+'" style="display: none;"><label class="selectallcheckbox"><input type="checkbox" name="qtelist-country" class="custom qtlist-th-checkbox-align-left custom-td-chkbox qtSelectAllCheck chkboxselectall" onclick="selectallcheckbox(\''+str(col_name)+'\')" value="SelectAll"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class="wrap-prod-val">Select All</span></label>'
                                )
                            else:
                                dropdowndiv+= (
                                    '<label class="selectConfig"><input type="checkbox" name="check-box-each-type" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="choosealltecheckbox(this,\''+str(col_name)+'\')" value="'+str(values)+'"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class="country_chkbox_data">'
                                    +str(values)
                                    +'</span></label>'
                                )
                    cv_list.append(dropdowndiv)
            else:
                filter_clas_name = (
                    '<input type="text"   class="width100_vis form-control bootstrap-table-filter-control-'
                    + str(col_name)
                    + '">'
                )
                cv_list.append(filter_clas_name)
        RelatedDrop_str += (
            "try {debugger; if( document.getElementById('"
            + str(table_id)
            + "') ) { var listws = document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control')[i].innerHTML = dataset.CV_LIST[i];  } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control')[i].innerHTML = dataset.CV_LIST[i];  } }, 10); }"
        )
        response = {
            "TABLE_CONTENT":table_content,"TABLE_DATA":table_data,"CV_LIST":cv_list,"FILTER_LEVEL_LIST":filter_level_list,"DROPDOWN_LIST":DropDownList,"RELATED_DROP_STR":RelatedDrop_str,"TABLE_ID":table_id, "FOOTER":Footer
        }
        return response
    
    def get_search_condition(self,SEARCH_DICT):
        result_item = ""
        res = ()
        allQueriedItems = ()
        result = dict((a.strip(), b.strip()) for a, b in (element.split(':') for element in SEARCH_DICT.split(', ')))
        search_condition = ""
        for key,value in result.items():
            columnName = "items.{}".format(str(key).replace("'",""))
            if str(value) == "''" or str(value) == "'Select All'":
                pass
            else:
                #A055S000P01-20922-Start-M
                picklist_query = Sql.GetFirst("select API_NAME from SYOBJD (nolock) where ((DATA_TYPE = 'PICKLIST' or FORMULA_DATA_TYPE = 'PICKLIST') OR UPPER(PICKLIST) = 'TRUE' ) and OBJECT_NAME = 'SAQICO' and API_NAME = '"+str(key).replace("'","")+"'") 
                if str(key).replace("'","") =="TOLCFG":
                    search_condition += "( "
                    sl = [" TOLCFG like '%"+str(val).lstrip(' ').replace("'",'')+"%'" for val in value.split('|')]
                    search_condition += " OR ".join(sl)
                    search_condition += ") AND "
                #INC09092287 - Start - M
                elif picklist_query is not None:
                    search_condition += "SAQICO."+str(key).replace("'","")+" in ("+str(value).replace(",","','").replace("'Select All',","")+") AND "
                else:
                    search_condition += "SAQICO."+str(key).replace("'","")+" like '%"+str(value).replace("'","")+"%' AND "
                #INC09092287 - End - M
                #A055S000P01-20922-End-M
        return str(search_condition)

    def construct_impacts_grid(self,SEARCH_DICT):
        table_id = 'impacts_grid'
        search_condition = self.get_search_condition(SEARCH_DICT)
        api_names = ["AIATCM","AIANCM","AICNCM","AINCCM","AINPCM","AIUICC","AMNCPI"]
        field_labels = ["Annualized Item Additional Target KPI {} Impact","Annualized Item Additional Target KPI (Non-Std) {} Impact","Annualized Item Consumable {} Impact","Annualized Item Non Consumable {} Impact","Annualized Item New Parts Only {} Impact","Annualized Item Uptime Improvement {} Impact","Annualized Item Additional Manual {} Impact"]

        table_data = []
        getcount = self.get_count_dict(search_condition)
        for key,api_name in enumerate(api_names):
            data = {}
            data["COST_IMPACT_FIELD"]="<abbr title = '"+str(field_labels[key].format("Cost"))+"' name = '"+str(api_name)+"'>"+str(field_labels[key].format("Cost"))+"</abbr>"
            data["PRICE_IMPACT_FIELD"]="<abbr title = '"+str(field_labels[key].format("Price"))+"' name = '"+str(api_name)+"'>"+str(field_labels[key].format("Price"))+"</abbr>"
            data["COST_ROW_COUNT"]= getcount[api_name]
            data["PRICE_ROW_COUNT"]= getcount[api_name]
            data["COST_IMPACT_VALUE"] = data["TOTAL_COST_IMPACT"] = data["PRICE_IMPACT_VALUE"] = data["TOTAL_PRICE_IMPACT"] = ''
            table_data.append(data)

        table_header = ""

        columns = ["COST IMPACT FIELD","COUNT","COST IMPACT VALUE","TOTAL COST IMPACT","PRICE IMPACT FIELD","COUNT","PRICE IMPACT VALUE","TOTAL PRICE IMPACT"]
        api_names = ["COST_IMPACT_FIELD","COST_ROW_COUNT","COST_IMPACT_VALUE","TOTAL_COST_IMPACT","PRICE_IMPACT_FIELD","PRICE_ROW_COUNT","PRICE_IMPACT_VALUE","TOTAL_PRICE_IMPACT"]

        for api_name,lable in zip(api_names,columns):
            table_header += ("""<th title = {title} data-title-tooltip="{title}" data-field = "{api_name}" ><div>{title}</div></th>""".format(api_name=api_name,title = str(lable)))
        table_content = """<table id="{table_id}" data-pagination="false" data-filter-control="true" data-locale = "en-US">
                <thead>
                    <tr id='getbannername' >
                        {table_header}
                    </tr>
                </thead>
                <tbody onclick="Table_Onclick_Scroll(this)">
                    <tr>
                        
                    </tr>
                </tbody>
            </table>
        """.format(table_id = table_id,table_header = table_header)
        RelatedDrop_str = ''
        response = {
            "TABLE_CONTENT":table_content,"TABLE_DATA":table_data,"RELATED_DROP_STR":RelatedDrop_str,"TABLE_ID":table_id
        }
        return response

    def get_count_dict(self,search_condition):
        #A055S000P01-20746 - Start - M
        getlines = Sql.GetList("SELECT ATGKEY,NWPTON,CNSMBL_ENT,SERVICE_ID,NCNSMB_ENT,TGKPNS,AMNCPE,STATUS,AMNCCI,AMNPPI,AIUICC,AIUICI,AIUIPI FROM SAQICO (NOLOCK) WHERE {search_condition}  QUOTE_RECORD_ID = '{quote_record_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') AND SERVICE_ID not in ('Z0117','Z0116','Z0101','Z0046','Z0048','Z0123') ".format(search_condition = search_condition,quote_record_id = self.contract_quote_record_id,rev_rec_id = self.quote_revision_record_id))
        count_dict = {
            "AIATCM":0,
            "AIANCM":0,
            "AICNCM":0,
            "AINCCM":0,
            "AINPCM":0,
            "AIUICC":0,
            "AMNCPI":0
        }
        for line_values in getlines:
            if(line_values.ATGKEY != 'Excluded' and line_values.ATGKEY != 'Exception' and str(line_values.ATGKEY) != ''):
                count_dict['AIATCM']+=1
                
            if(line_values.NWPTON == 'Yes'):
                count_dict['AINPCM']+=1
            #A055S000P01-20741 - Start - M
            if((line_values.CNSMBL_ENT in ('Some Exclusions','Some Inclusions') and line_values.SERVICE_ID != 'Z0100') or (line_values.CNSMBL_ENT in ('Included','Some Inclusions') and line_values.SERVICE_ID == 'Z0100') ) and not (line_values.CNSMBL_ENT == 'Some Inclusions' and line_values.SERVICE_ID == 'Z0092'):#A055S000P01-20741 - End - M
                count_dict['AICNCM']+=1
                
            if(line_values.NCNSMB_ENT in ('Some Inclusions','Some Exclusions') and line_values.SERVICE_ID != 'Z0100'):
                count_dict['AINCCM']+=1
                
            if(line_values.TGKPNS != 'Excluded' and str(line_values.TGKPNS) != ''):
                count_dict['AIANCM']+=1
                
            if((line_values.AMNCPE == "1" or line_values.AMNCPE == True) and line_values.SERVICE_ID != 'Z0100') or line_values.STATUS == 'PRR-ON HOLD PRICING' or (line_values.AMNCCI > 0 or line_values.AMNPPI > 0):
                count_dict['AMNCPI']+=1
                
            if(line_values.AIUICC == "0" or line_values.AIUICC == False) or (line_values.AIUICI > 0 or line_values.AIUIPI > 0):
                count_dict['AIUICC']+=1
            #A055S000P01-20746 - End - M
        return count_dict

    def query_filter(self,SEARCH_CONDITION,PER_PAGE,RECORD_START):
        table_columns = self.get_columns()
        COLUMNS = table_columns.COLUMNS.replace('[','').replace(']','').replace("'",'')
        get_data = Sql.GetList("SELECT {columns} FROM SAQICO (NOLOCK) WHERE {search_condition} QUOTE_RECORD_ID = '{quote_record_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}'  AND STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') ORDER BY {sort_column} {sort_order} OFFSET {offset} ROWS FETCH NEXT {count} ROWS ONLY ".format(columns = COLUMNS,count = PER_PAGE,search_condition = SEARCH_CONDITION,quote_record_id = self.contract_quote_record_id,rev_rec_id = self.quote_revision_record_id,sort_column=self.sort_column,sort_order = self.sort_order,offset = (int(RECORD_START)/10)*10))
        get_count = Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQICO (NOLOCK) WHERE {search_condition} QUOTE_RECORD_ID = '{quote_record_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}'  AND STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') ".format(search_condition = SEARCH_CONDITION,quote_record_id = self.contract_quote_record_id,rev_rec_id = self.quote_revision_record_id))
        count = get_count.CNT
        table_data = []
        domain_name = str(Sql.getDomainDetails())
        status = {
                'ACQUIRED':'<img title="Acquired" src="/mt/'+str(domain_name)+'/Additionalfiles/Green_Tick.svg">',
                'CFG-ON HOLD TKM':'<img title="ON-HOLD-TKM" src="/mt/'+str(Sql.getDomainDetails())+'/Additionalfiles/icons/on_hold_tkm.svg">',
                'OFFLINE PRICING':'<img title="OFFLINE PRICING" src="/mt/'+str(domain_name)+'/Additionalfiles/manual_pricing.svg">', 
                'PRR-ON HOLD PRICING':'<img title="PRR-ON HOLD PRICING" src="/mt/'+str(domain_name)+'/Additionalfiles/pricing_on_hold.svg">'
            }
        for record in get_data:
            row = {}
            for column in COLUMNS.split(','):
                value = eval('record.'+str(column))
                if column == "STATUS":
                    row[column] = status.get(value)
                else:
                    row[column] = str(value)
            row['ACTIONS'] = ''
            table_data.append(row)
        response = {"TABLE_DATA":table_data,"COUNT":count}
        return response

    def bulk_edit_save(self,IMPACT_VALUES,SEARCH_CONDITION):
        query_table_info = SqlHelper.GetTable("SAQIBE")
        get_quote_detail = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
        get_query_id = Sql.GetFirst("SELECT MAX(BULK_EDIT_FILTERQUERY_ID) AS MAX FROM SAQIBE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
        query_id = "1"
        if get_query_id.MAX:
            query_id = int(get_query_id.MAX)+1
        query_record = {
                "QUOTE_BULK_EDIT_FILTERQUERY_RECORD_ID": str(Guid.NewGuid()).upper(),
                "QUOTE_ID": str(get_quote_detail.QUOTE_ID),
                "QUOTE_RECORD_ID": self.contract_quote_record_id,
                "QTEREV_ID": str(get_quote_detail.QTEREV_ID),
                "QTEREV_RECORD_ID": self.quote_revision_record_id,
                "BULK_EDIT_FILTERQUERY_VALUE": str(SEARCH_CONDITION),
                "BULK_EDIT_FILTERQUERY_ID": query_id
            }
        for item in IMPACT_VALUES:
            row = str(item).replace("Dictionary[str, object]({","").replace("})","").replace("'","")
            result = dict((a.strip(), b.strip()) for a, b in (element.split(':') for element in row.split(', ')))
            if result.get('API_NAME') == "AIATCM":
                query_record.update(
                        {
                            "ANNITMS_ADDTNL_TGT_KPI_CI": result.get('COST_IMPACT'),
                            "ANNITMS_ADDTNL_TGT_KPI_PI": result.get('PRICE_IMPACT'),
                            
                        }
                    )
            elif result.get('API_NAME') == "AIANCM":
                query_record.update(
                        {
                            "ANNITMS_ADDTNL_TGT_KPI_NS_CI": result.get('COST_IMPACT'),
                            "ANNITMS_ADDTNL_TGT_KPI_NS_PI": result.get('PRICE_IMPACT'),
                            
                        }
                    )
            elif result.get('API_NAME') == "AICNCM":
                query_record.update(
                        {
                            "ANNITMS_CONSUMABLE_CI": result.get('COST_IMPACT'),
                            "ANNITMS_CONSUMABLE_PI": result.get('PRICE_IMPACT'),
                            "ANNITMS_CONSUMABLE_TOTAL_CI": result.get('TOTAL_COST_IMPACT'),
                            "ANNITMS_CONSUMABLE_TOTAL_PI": result.get('TOTAL_PRICE_IMPACT')
                        }
                    )
            elif result.get('API_NAME') == "AINCCM":
                query_record.update(
                        {
                            "ANNITMS_NONCONSUMABLE_CI": result.get('COST_IMPACT'),
                            "ANNITMS_NONCONSUMABLE_PI": result.get('PRICE_IMPACT'),
                            "ANNITMS_NONCONSUMABLE_TOTAL_CI": result.get('TOTAL_COST_IMPACT'),
                            "ANNITMS_NONCONSUMABLE_TOTAL_PI": result.get('TOTAL_PRICE_IMPACT')
                        }
                    )
            elif result.get('API_NAME') == "AINPCM":
                query_record.update(
                        {
                            "ANNITMS_NEW_PARTS_ONLY_CI": result.get('COST_IMPACT'),
                            "ANNITMS_NEW_PARTS_ONLY_PI": result.get('PRICE_IMPACT'),
                            "ANNITMS_NEW_PARTS_ONLY_TOTAL_CI": result.get('TOTAL_COST_IMPACT'),
                            "ANNITMS_NEW_PARTS_ONLY_TOTAL_PI": result.get('TOTAL_PRICE_IMPACT')
                        }
                    )
            elif result.get('API_NAME') == "AIUICC":
                query_record.update(
                        {
                            "ANNITMS_UPTIME_IMPROVEMENT_CI": result.get('COST_IMPACT'),
                            "ANNITMS_UPTIME_IMPROVEMENT_PI": result.get('PRICE_IMPACT'),
                            "ANNITMS_UPTIME_IMPROVEMENT_TOTAL_CI": result.get('TOTAL_COST_IMPACT'),
                            "ANNITMS_UPTIME_IMPROVEMENT_TOTAL_PI": result.get('TOTAL_PRICE_IMPACT')
                        }
                    )
            elif result.get('API_NAME') == "AMNCPI":
                query_record.update(
                        {
                            "ANNITMS_ADDTNL_MANUAL_TOTAL_PI": result.get('TOTAL_PRICE_IMPACT'),
                            "ANNITMS_ADDTNL_MANUAL_TOTAL_CI": result.get('TOTAL_COST_IMPACT'),
                            "ANNITMS_ADDTNL_MANUAL_PI" : result.get('PRICE_IMPACT'),
                            "ANNITMS_ADDTNL_MANUAL_CI" : result.get('COST_IMPACT')
                        }
                    )
        query_table_info.AddRow(query_record)
        Sql.Upsert(query_table_info)
        self.recalculate_iflow(get_quote_detail.QUOTE_ID)
        return True
    def recalculate_iflow(self,QUOTE_ID):
        requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><QUOTE_RECORD_ID>{}</QUOTE_RECORD_ID><QTEREV_RECORD_ID>{}</QTEREV_RECORD_ID></CPQ_Columns></soapenv:Body></soapenv:Envelope>'.format(self.contract_quote_record_id,self.quote_revision_record_id)
        )    
        LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT User_name as Username,Password,Domain,URL FROM SYCONF (NOLOCK) where External_Table_Name='BULK UPDATE RECALCULATE PRICING'")
        if LOGIN_CREDENTIALS is not None:
            Login_Username = str(LOGIN_CREDENTIALS.Username)
            Login_Password = str(LOGIN_CREDENTIALS.Password)
            URL = str(LOGIN_CREDENTIALS.URL)
            authorization = Login_Username + ":" + Login_Password
            from System.Text.Encoding import UTF8

            binaryAuthorization = UTF8.GetBytes(authorization)
            from System import Convert

            authorization = Convert.ToBase64String(binaryAuthorization)
            authorization = "Basic " + authorization    
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
        response = webclient.UploadString(URL, requestdata)
    
    def get_button_visibility(self):
        visible = False
        get_all_lines =Sql.GetList("Select STATUS,AMNCCI,AMNPPI from SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' ".format(contract_quote_rec_id = self.contract_quote_record_id,quote_revision_rec_id = self.quote_revision_record_id))
        get_rev_status = Sql.GetFirst("select REVISION_STATUS from SAQTRV (nolock) where QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' ".format(contract_quote_rec_id = self.contract_quote_record_id,quote_revision_rec_id = self.quote_revision_record_id))
        revision_status = get_rev_status.REVISION_STATUS
        for line_values in get_all_lines:
            if ("OFFLINE PRICING" in line_values.STATUS or "PRR-ON HOLD PRICING" in line_values.STATUS or ("ACQUIRED" in line_values.STATUS and ( line_values.AMNCCI not in ('',None) or line_values.AMNPPI not in ('',None) ))) and str(revision_status) in ('PRR-ON HOLD PRICING','PRR-PRICING REVIEWED'):
                visible = True
        return str(visible)

    def pricing_reviewed(self):
        pricing_flag = False
        User_name = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
        #A055S000P01-20931 -A start
        get_usertype = Sql.GetFirst("SELECT COUNT(C4C_PARTNERFUNCTION_ID) AS CNT FROM SAQDLT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND MEMBER_ID = '{username}' AND C4C_PARTNERFUNCTION_ID IN ('PRICING PERSON','BD','BD HEAD','BD MANAGER')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id,username=User_name))
        #A055S000P01-20931 -A end
        if get_usertype.CNT > 0:
            items_status = []
            reviewed_flag = True
            items_obj = Sql.GetList("SELECT ISNULL(STATUS,'') as STATUS FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id))
            if items_obj:
                items_status = [item_obj.STATUS for item_obj in items_obj]
            for sts in items_status:
                if sts not in ('ACQUIRED','CFG-ON HOLD TKM'):
                    reviewed_flag = False
            if reviewed_flag:
                Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = 'PRI-PRICING',WORKFLOW_STATUS='PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id))
                pricing_flag = True
                self.writeback()
        return True,pricing_flag
    
    def writeback(self):
        import CQCPQC4CWB
        import CQREVSTSCH
        #A055S000P01-20566
        CQCPQC4CWB.writeback_to_c4c("quote_header",self.contract_quote_record_id,self.quote_revision_record_id)
        CQCPQC4CWB.writeback_to_c4c("opportunity_header",self.contract_quote_record_id,self.quote_revision_record_id)
        CQREVSTSCH.Revisionstatusdatecapture(self.contract_quote_record_id,self.quote_revision_record_id)
        return True
try:
    ACTION = Param.ACTION
except Exception as e:
    Trace.Write('Exception : '+str(e))
    ACTION = None
try:
    RECORD_ID = Param.RECORD_ID
except:
    RECORD_ID = "SYOBJR-98883"
try:
    SEARCH_DICT = Param.SEARCH_DICT
    Trace.Write("Search Dict :"+str(SEARCH_DICT))
    SEARCH_DICT = str(SEARCH_DICT).replace("Dictionary[str, object]({","").replace("})","")
except Exception as e:
    Trace.Write(e)
    SEARCH_DICT = ''
ann_obj = AnnualizedItemsQuery()
if ACTION == "ITEMS_QUERY":
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.load_query_grid())
elif ACTION == "IMPACTS_GRID":
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.construct_impacts_grid(SEARCH_DICT))
elif ACTION =="SAVE":
    IMPACT_VALUES = Param.IMPACT_VALUES
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.bulk_edit_save(IMPACT_VALUES,ann_obj.get_search_condition(SEARCH_DICT)))
elif ACTION =="QUERY_FILTER":
    PER_PAGE = Param.PER_PAGE
    RECORD_START = Param.RECORD_START
    SORT_COLUMN = Param.SORT_COLUMN
    SORT_ORDER = Param.SORT_ORDER
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.query_filter(ann_obj.get_search_condition(SEARCH_DICT),PER_PAGE,RECORD_START))
elif ACTION == "BUTTON VISIBILITY":
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.get_button_visibility())
elif ACTION == "PRICING REVIEWED":
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.pricing_reviewed())
elif ACTION == "WRITEBACK":
    ApiResponse = ApiResponseFactory.JsonResponse(ann_obj.writeback())
