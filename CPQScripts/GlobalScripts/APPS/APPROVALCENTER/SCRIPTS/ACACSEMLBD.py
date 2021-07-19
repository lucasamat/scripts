"""Using for Approval Center Email."""

# =========================================================================================================================================
#   __script_name : ACACSEMLBD.PY
#   __script_description : THIS SCRIPT IS USED TO DYNAMICALLY LOAD THE E-MAIL CONTENT IN CHAIN STEP.
#   __primary_author__ : VETRIVEL PALANIVEL
#   __create_date :21-07-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import ACVIORULES
from SYDATABASE import SQL

Sql = SQL()
violationruleInsert = ACVIORULES.ViolationConditions()


class EmailContentForChainStep:
    """Using for Approval Center Email."""

    def __init__(self, CurrentRecordId=None):
        """Approvalcenter Email initializer."""
        self.CurrentRecordId = CurrentRecordId

    def EmailTemplateLoad(self):
        """Approvalcenter Email Template Loading."""
        HtmlStr = jsstr = ""
        listsecId = ["RequestRichTextArea", "RecallRichTextArea", "ApprovalRichTextArea", "RejectionRichTextArea"]
        jsstr = """$("#RequestRichTextArea").jqxEditor({height: "350px !important", disabled: true});
        $("#RecallRichTextArea").jqxEditor({height: "350px !important",disabled: true});
        $("#ApprovalRichTextArea").jqxEditor({height: "350px !important",disabled: true});
        $("#RejectionRichTextArea").jqxEditor({height: "350px !important",disabled: true});"""
        secTextdict = {
            "APPROVAL REQUEST TEMPLATE": "REQUEST_TEMPLATE_RECORD_ID",
            "APPROVAL REQUEST NOTIFICATION TEMPLATE": "RECALL_TEMPLATE_RECORD_ID",
            "APPROVAL NOTIFICATION TEMPLATE": "APPROVE_TEMPLATE_RECORD_ID",
            "REJECTION NOTIFICATION TEMPLATE": "REJECT_TEMPLATE_RECORD_ID",
        }
        i = 0
        for key, value in secTextdict.items():
            ReqQuery_eml = Sql.GetFirst(
                """ SELECT ACEMTP.MESSAGE_BODY,ACEMTP.MESSAGE_BODY_2,ACEMTP.MESSAGE_BODY_3,
                    ACEMTP.MESSAGE_BODY_4,ACEMTP.MESSAGE_BODY_5,ACEMTP.EMAIL_TEMPLATE_RECORD_ID
                    FROM ACEMTP (NOLOCK)
                    INNER JOIN ACACST (NOLOCK) ON ACACST.{value} = ACEMTP.EMAIL_TEMPLATE_RECORD_ID
                    WHERE  ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = '{CurrentRecordId}' """.format(
                    CurrentRecordId=CurrentRecordId, value=value
                )
            )
            HtmlStr += """<div id="container" class="wdth100 g4 {recId}">
            <div class="dyn_main_head master_manufac glyphicon pointer glyphicon-chevron-down"
            onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sec_{recId}" data-toggle="collapse"
            aria-expanded="true" ><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown">
            <div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i>
            <ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li id="li_{currentsectid}"class="edit_list">
            <a id="{recId}" class="dropdown-item" href="#" onclick="EailSectionEdit(this)">EDIT</a></li></ul>
            </div></div>{key}</div> </label> </div> <div id="sec_{recId}" class="collapse in"
            aria-expanded="true"><div id="{currentsectid}"></div></div></div>""".format(
                recId=str(ReqQuery_eml.EMAIL_TEMPLATE_RECORD_ID), key=key, currentsectid=listsecId[i]
            )
            reqestbody = (
                str(ReqQuery_eml.MESSAGE_BODY)
                + ""
                + str(ReqQuery_eml.MESSAGE_BODY_2)
                + ""
                + str(ReqQuery_eml.MESSAGE_BODY_3)
                + ""
                + str(ReqQuery_eml.MESSAGE_BODY_4)
                + ""
                + str(ReqQuery_eml.MESSAGE_BODY_5)
            )
            jsstr += "$('#{currentsectid}').val(`{reqestbody}`);".format(
                reqestbody=str(reqestbody).strip(), currentsectid=listsecId[i]
            )
            i += 1
        Trace.Write(str(HtmlStr))
        Trace.Write(str(jsstr))
        return HtmlStr, jsstr

    def EmailSectionSave(self, msgbody):
        """Email section edit save function."""
        GetCpqId = Sql.GetFirst(
            """SELECT CpqTableEntryId FROM ACEMTP (NOLOCK)
        WHERE EMAIL_TEMPLATE_RECORD_ID = '{CurrentRecordId}' """.format(
                CurrentRecordId=self.CurrentRecordId
            )
        )
        row = {}
        tableInfoH = Sql.GetTable("ACEMTP")
        if len(msgbody) <= 8000:
            row["MESSAGE_BODY"] = str(msgbody)
            row["MESSAGE_BODY_2"] = ""
            row["MESSAGE_BODY_3"] = ""
            row["MESSAGE_BODY_4"] = ""
            row["MESSAGE_BODY_5"] = ""
        elif len(msgbody) < 16000:
            msgsplit = str(msgbody).split("@!#$@!")
            row["MESSAGE_BODY"] = str(msgsplit[0][0:8000])
            row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:])
            row["MESSAGE_BODY_3"] = ""
            row["MESSAGE_BODY_4"] = ""
            row["MESSAGE_BODY_5"] = ""
        elif len(msgbody) < 24000:
            msgsplit = str(msgbody).split("@!#@!")
            row["MESSAGE_BODY"] = str(msgsplit[0][0:8000])
            row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
            row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:])
            row["MESSAGE_BODY_4"] = ""
            row["MESSAGE_BODY_5"] = ""
        elif len(msgbody) < 32000:
            msgsplit = str(msgbody).split("@!#@!")
            row["MESSAGE_BODY"] = str(msgsplit[0][0:8000])
            row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
            row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:24000])
            row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:])
            row["MESSAGE_BODY_5"] = ""
        elif len(msgbody) < 40000:
            msgsplit = str(msgbody).split("@!#@!")
            row["MESSAGE_BODY"] = str(msgsplit[0][0:8000])
            row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
            row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:24000])
            row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:32000])
            row["MESSAGE_BODY_5"] = str(msgsplit[0][32000:])
        row["CpqTableEntryId"] = str(GetCpqId.CpqTableEntryId)
        tablerow = row
        tableInfoH.AddRow(tablerow)
        Sql.Upsert(tableInfoH)
        return True


Action = Param.Action
CurrentRecordId = Param.CurrentRecordId

objDef = eval(violationruleInsert.Factory(Action))(CurrentRecordId=CurrentRecordId)

if str(Action) == "EmailContent":
    ApiResponse = ApiResponseFactory.JsonResponse(objDef.EmailTemplateLoad())
elif str(Action) == "SecEmailContentsave":
    emailbody = Param.emailbody
    ApiResponse = ApiResponseFactory.JsonResponse(objDef.EmailSectionSave(emailbody))
