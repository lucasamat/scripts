# =========================================================================================================================================
#   __script_name : SYMCALLPOP.PY
#   __script_description : THIS SCRIPT IS USED IN SYSTEM ADMIN ACTIONS TAB TO SELECT THE VISIBILITY VARIABLE, SCRIPT AND TAB
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL

Sql = SQL()


def MM_ACT_POPUP_TAB():
    Tab_obj = Sql.GetList("SELECT TAB_LABEL, RECORD_ID FROM SYTABS")
    tab_list = []
    for ins in Tab_obj:
        tab_dict = {}
        ids = str(ins.RECORD_ID) + "|" + str(ins.TAB_LABEL)
        tab_dict["ids"] = ids
        tab_dict["TAB_LABEL"] = ins.TAB_LABEL
        tab_dict["RECORD_ID"] = ins.RECORD_ID
        tab_list.append(tab_dict)
    return tab_list


def MM_ACT_POPUP_SCRIPT():
    Script_obj = Sql.GetList("SELECT SCRIPT_NAME, RECORD_ID FROM SYSCRP")
    scr_list = []
    for scr_ins in Script_obj:
        scr_dict = {}
        ids = str(scr_ins.RECORD_ID) + "|" + str(scr_ins.SCRIPT_NAME)
        scr_dict["ids"] = ids
        scr_dict["SCRIPT_NAME"] = scr_ins.SCRIPT_NAME
        scr_dict["RECORD_ID"] = scr_ins.RECORD_ID
        scr_list.append(scr_dict)
    return scr_list


def MM_ACT_VIS_VAR_POPUP():
    VAR_obj = Sql.GetList("SELECT VARIABLE_NAME, RECORD_ID FROM SYVABL WHERE VARIABLE_TYPE='ACTION VISIBILITY VARIABLE'")
    var_list = []
    for obj in VAR_obj:
        var_dict = {}
        ids = str(obj.RECORD_ID) + "|" + str(obj.VARIABLE_NAME)
        var_dict["ids"] = ids
        var_dict["VARIABLE_NAME"] = obj.VARIABLE_NAME
        var_dict["RECORD_ID"] = obj.RECORD_ID
        var_list.append(var_dict)
    return var_list


FIELD = Param.FIELD
RecID = Param.RecID

if FIELD == "Section Record ID":
    ApiResponse = ApiResponseFactory.JsonResponse(MM_ACT_POPUP_TAB())
elif FIELD == "Section Record ID Onchange":
    RecordID = RecID.split("|")[0]
    RecordName = RecID.split("|")[1]
    RecordID_No = RecordID + ", " + RecordName
    Product.Attributes.GetByName("MM_ACT_TAB_NAME").AssignValue(str(RecordName))
    Product.Attributes.GetByName("MM_ACT_TAB_REC_ID").AssignValue(str(RecordID_No))
    ApiResponse = ApiResponseFactory.JsonResponse("")

elif FIELD == "Script_Rec_ID1":
    ApiResponse = ApiResponseFactory.JsonResponse(MM_ACT_POPUP_SCRIPT())

elif FIELD == "Script_Rec_ID_Onchange1":
    RecordID1 = RecID.split("|")[0]
    RecordName1 = RecID.split("|")[1]
    RecordID_No1 = RecordID1 + ", " + RecordName1
    Log.Info("ACT SCRIPT NAME " + str(RecordID_No1))
    Log.Info("ACT SCRIPT ID " + str(RecordName1))
    Product.Attributes.GetByName("MM_ACT_SCRIPT_NAME").AssignValue(str(RecordName1))
    Product.Attributes.GetByName("MM_ACT_SCR_REC_ID").AssignValue(str(RecordID_No1))
    ApiResponse = ApiResponseFactory.JsonResponse("")

elif FIELD == "Vis_Rec_ID2":
    ApiResponse = ApiResponseFactory.JsonResponse(MM_ACT_VIS_VAR_POPUP())

elif FIELD == "Vis_Rec_ID_Onchange2":
    if RecID != "":
        RecordID2 = RecID.split("|")[0]
        RecordName2 = RecID.split("|")[1]
        RecordID_No2 = RecordID2 + ", " + RecordName2
        Product.Attributes.GetByName("MM_ACT_VIS_VAR").AssignValue(str(RecordName2))
        Product.Attributes.GetByName("MM_ACT_VIS_VARIABLE_REC_ID").AssignValue(str(RecordID_No2))
    else:
        Product.Attributes.GetByName("MM_ACT_VIS_VAR").AssignValue("")
        Product.Attributes.GetByName("MM_ACT_VIS_VARIABLE_REC_ID").AssignValue("")
    ApiResponse = ApiResponseFactory.JsonResponse("")
