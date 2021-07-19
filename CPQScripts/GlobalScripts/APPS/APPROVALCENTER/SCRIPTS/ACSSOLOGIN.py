"""Using for Approval Center Actions."""

# =========================================================================================================================================
#   __script_name : ACSSOLOGIN.PY
#   __script_description : THIS SCRIPT IS USED TO PERFORM LOGIN ACTION FOR THE SSO USERS.
#   __primary_author__ : VIJAYAKUMAR THANGARASU
#   __create_date :14-02-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================


# import Webcom

try:
    UserType = SqlHelper.GetFirst("select * from users (nolock) where id ='" + str(User.Id) + "' ")
    if str(UserType.TYPE) == "17":
        Req = Request["QUERY_STRING"]
        valuesplit = str(Req).split("&")
        Querydict = {}
        for query in valuesplit:
            qrysplit = query.split("=")
            Querydict[qrysplit[0]] = qrysplit[1]
        Action = Querydict.get("ACTION")
        ApproveDesc = Querydict.get("ApproveDesc")
        CurrentTransId = Querydict.get("CurrentTransId")
        approvalrecId = Querydict.get("approvalrecid")
        PriceagreementRevId = Querydict.get("PriceagreementRevId")
        AllParams = '{"none":"none"}'
        if str(Action) != "VIEWBTN":
            result = ScriptExecutor.ExecuteGlobal(
                "ACSECTACTN",
                {
                    "ACTION": str(Action),
                    "QuoteNumber": str(approvalrecId),
                    "AllParams": str(AllParams),
                    "ApproveDesc": str(ApproveDesc),
                    "CurrentTransId": str(CurrentTransId),
                },
            )
        Product.SetGlobal("ApprovalMasterRecId", str(approvalrecId))
        Product.SetGlobal("PriceagreementRevId", str(PriceagreementRevId))
        Product.SetGlobal("ApprovalMasterAction", str(Action))
    else:
        Product.SetGlobal("ApprovalMasterRecId", "")
except Exception, e:
    Log.Info("ACSSOLOGIN: ERROR IN EXCEPTION: " + str(e))
