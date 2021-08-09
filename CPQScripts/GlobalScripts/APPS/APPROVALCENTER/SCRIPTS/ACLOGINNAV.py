"""Using for Approval Center Actions."""

# =========================================================================================================================================
#   __script_name : ACLOGINNAV.PY
#   __script_description : THIS SCRIPT IS USED TO PERFORM SSO USER AUTO NAVIGATION.
#   __primary_author__ : VIJAYAKUMAR THANGARASU
#   __create_date :14-02-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

# import Webcom
import Webcom.Configurator.Scripting.Test.TestProduct
info = ""
UserType = SqlHelper.GetFirst("select * from users (nolock) where id ='" + str(User.Id) + "' ")
GetVal = Product.GetGlobal("ApprovalMasterRecId")
GetAction = Product.GetGlobal("ApprovalMasterAction")
if str(UserType.TYPE) == "17":
    if GetVal != "":
        ScriptExecutor.ExecuteGlobal(
            "SYALLTABOP",
            {"Primary_Data": str(GetVal), "TabNAME": "My Approval Queue", "ACTION": "VIEW", "RELATED": ""},
        )
        PriceagreementRevId = Product.GetGlobal("PriceagreementRevId")
        if GetAction == "APPROVEBTN":
            info = "Price Agreement Revision ID (" + str(PriceagreementRevId) + ") has been Approved successfully"
        elif GetAction == "REJECTBTN":
            info = "Price Agreement Revision ID (" + str(PriceagreementRevId) + ") has been Rejected successfully"
        if info != "":
            Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
            Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = (
                """<div class="col-md-12"   id="PageAlert" ><div  class="row modulesecbnr brdr"
                data-toggle="collapse" data-target="#Alert49" aria-expanded="true" style="display: block;">
                NOTIFICATIONS<i class="pull-right fa fa-chevron-down"></i>
                <i class="pull-right fa fa-chevron-up"></i></div>
                <div  id="Alert49" class="col-md-12  alert-notification  brdr collapse in" >
                <div  class="col-md-12 alert-info"  > <label >
                <img src="/mt/OCTANNER_DEV/Additionalfiles/infocircle1.svg" alt="Error"> INFO : """
                + str(info)
                + """ </label></div></div></div>"""
            )
