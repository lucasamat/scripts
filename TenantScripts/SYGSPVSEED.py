# =========================================================================================================================================
#   __script_name : SYGSPVSEED.PY
#   __script_description : THIS SCRIPT IS USED TO SET THE VALUES OF THE FIELDS WHEN EDIT DATA IN A PIVOT TABLE.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def build_modal_setedit(HEADERVALUE, COL_VAL):

    table_data = []
    HEADERVALUES = list(HEADERVALUE)
    # headerval = HEADERVALUES.index('SET QUANTITY')-1
    header1, Att_Header_val = (
        HEADERVALUES[0 : HEADERVALUES.index("SET MATERIAL RECORD ID") - 1],
        HEADERVALUES[HEADERVALUES.index("SET MATERIAL RECORD ID") + 1 : len(HEADERVALUES)],
    )
    #Trace.Write("Att_Header_val---" + str(Att_Header_val))
    result = []

    content_result = []

    for header in Att_Header_val:

        result.append(
            '<tr class="iconhvr brbtpadltmrg" ><td   class="colname ma_text_align_one">{}</td>'.format(header.title())
        )
        result.append("</tr>")
    result = '<table  class="ma_width_marg" id="additional_attributes_pop"><thead><tr> <th >Attribute Name</th><th>Attribute Value</th></tr></thead><tbody>{}</tbody></table>'.format(
        "".join(result)
    )

    for key, value in zip(header1, COL_VAL):
        if key == "ACTIONS" or value == "REMOVE MATERIALEDIT":
            continue
        else:
            table_data.append(
                """<tr class="iconhvr brdbt" >
                <td class="wth350"><label class="pad_l_mar_bot">{KEY}</label></td>
                <td class="wth40"><a href="#" data-placement="top" data-toggle="popover" data-content="{DATA_CONTENT}"  class="bgcccwth10"><i   class="fa fa-info-circle fltlt"></i></a></td>
                <td><input type="text" value="{VALUE}" class="form-control related_popup_css" disabled></td>
                <td class="float_r_bor_bot">
                    <div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div>
                </td>
            </tr>""".format(
                    KEY=key.title(), DATA_CONTENT=key.title(), VALUE=value
                )
            )
    result_str = """<div   class="row modulebnr brdr">EDIT

                        <button type="button"  class="close fltlt" data-dismiss="modal">X</button>
                    </div>
                    <div class="col-md-12">
                        <div class="row pad-10 bg-lt-wt brdr" >
                            <button type="button" class="btnconfig" data-dismiss="modal">CANCEL</button>
                            <button type="button" class="btnconfig" data-dismiss="modal" onclick = "setEditSave(this)">SAVE</button>
                            
                        </div>
                        <div id="Headerbnr" class="mart_col_back"></div>
                    </div>
                    <div id="container" class="g4 pad-10 brdr except_sec">
                        
                        <table class="ma_width_marg">
                            <tbody>{}
                            </tbody>
                        </table>{}
                    </div>""".format(
        "".join(table_data), result
    )
    return result_str


HEADERVALUE = Param.HEADERVALUE
COL_VAL = Param.COL_VAL
# Trace.Write("COL_VAL---" + str(COL_VAL))
# Trace.Write("HEADERVALUE---" + str(HEADERVALUE))
ApiResponse = ApiResponseFactory.JsonResponse(build_modal_setedit(HEADERVALUE, COL_VAL))