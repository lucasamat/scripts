"""Violated date insert Script."""
# ====================================================================================================
#   __script_name : ACVIORULES.PY
#   __script_description : This script is to insert the data to violation rule table
#   __primary_author__ : VIJAYAKUMAR THANGARASU
#   __create_date : 06/04/2020
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================
import CQCPQC4CWB
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
from datetime import datetime

import time
from SYDATABASE import SQL

Sql = SQL()

""" Violation checking condition."""


class ViolationConditions:
    """Violatioin conditions."""

    def __init__(self):
        """Violation condition initializer."""
        self.Get_UserID = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
        self.Get_UserNAME = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
        self.Get_NAME = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "NAME")
        self.datetime_value = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.operators_config = {
            "LESS THAN": " < ",
            "EQUALS": " = ",
            "GREATER THAN": " > ",
            "NOT EQUALS": " != ",
            "LESS OR EQUALS": " <= ",
            "GREATER OR EQUALS": " >= ",
            "STARTS WITH": "",
            "ENDS WITH": "",
            "CONTAINS": "",
            "DOES NOT CONTAIN": "",
        }

        self.snap_query_config = {
            "CONTAINS": "SELECT {} FROM {} (NOLOCK) WHERE {}  LIKE '%{}%'",
            "DOES NOT CONTAIN": "SELECT {} FROM {} (NOLOCK) WHERE {}  NOT LIKE '%{}%'",
            "STARTS WITH": "SELECT {} FROM {} (NOLOCK) WHERE {}  LIKE '{}%'",
            "ENDS WITH": "SELECT {} FROM {} (NOLOCK) WHERE {}  LIKE '%{}'",
            'default': "SELECT {} FROM {} (NOLOCK) WHERE {} {} '{}'",
        }
    def Factory(self, node=None):
        """Create class object factory Method."""
        objects = {
            "approvalCenter": [
                "APPROVE",
                "REJECT",
                "SUBMIT_FOR_APPROVAL",
                "RECALL",
                "RichText",
                "PREVIEW_APPROVAL",
                "GET_SEGMENT_ID",
                "TrackedValues",
                "mailbodyfield",
                "VIEW_COMMENT",
                "EDIT_COMMENT",
                "SAVE_COMMENT",
                "SUBMIT_COMMENT",
                "APPROVE_COMMENT",
                "REJECT_COMMENT",
                "APPROVEBTN",
                "REJECTBTN",
                "BULKAPPROVE",
                "BULKREJECT",
                "CBC_MAIL_TRIGGER"
            ],
            "ProductDetailLoading": ["PoductDetails", "ProductDetail"],
            "QueryBuilder": ["QueryBuilder", "QBSave"],
            "PriceFactor": "PriceFactor",
            "EmailContentForChainStep": ["EmailContent", "SecEmailContentsave"],
        }
        for key, value in objects.items():
            if node in value:
                Trace.Write("keyObj----> " + str(key))
                return key
        return True

    def DeleteforApprovalHeaderTable(self, RecordId, chainId, ChainStep, ObjectName):
        Trace.Write("gggdelete")
        Log.Info("Entered DeleteforApprovalHeaderTable---delete")

        # Delete approval header.
        ApprovalCombinationID = str(RecordId)

        getApprovalId = Sql.GetList(
            "SELECT APPROVAL_ID FROM ACAPMA (NOLOCK) WHERE APRTRXOBJ_RECORD_ID = '" + str(ApprovalCombinationID) + "' "
        )
        if getApprovalId:
            for transdelete in getApprovalId:
                DeleteQueryStatementApprovalTrans = (
                    "DELETE ACAPTX WHERE APPROVAL_ID = '" + str(transdelete.APPROVAL_ID) + "' "
                )
                DeleteApprovalTrans = Sql.RunQuery(DeleteQueryStatementApprovalTrans)
                DeleteQueryStatementTrackedvalue = (
                    "DELETE ACAPFV WHERE APPROVAL_ID = '" + str(transdelete.APPROVAL_ID) + "' "
                )
                DeleteTrackedValue = Sql.RunQuery(DeleteQueryStatementTrackedvalue)
                Log.Info(
                    "User Id:"
                    + str(self.Get_UserID)
                    + "Script Name:ACVIORULES.PY Query Statement:"
                    + str(DeleteQueryStatementApprovalTrans)
                )

        DeleteQueryStatementApprovalHeader = "DELETE FROM ACAPMA WHERE APRTRXOBJ_RECORD_ID = '" + str(ApprovalCombinationID) + "' "
        DeleteApproval = Sql.RunQuery(DeleteQueryStatementApprovalHeader)
        Log.Info(
            "User Id:"
            + str(self.Get_UserID)
            + "Script Name:ACVIORULES.PY Query Statement:"
            + str(DeleteQueryStatementApprovalHeader)
        )
        return True

    def ViolationRuleForApprovals(self, CurrentId, ObjectName, chainid):
        Log.Info("Entered ViolationRuleForApprovals---insert ACAPMA")
        """Approval violations."""
        ApprovalCombinationID = approval_id_auto = ""
        GetObjHPromaryKey = Sql.GetFirst("SELECT RECORD_NAME,RECORD_ID FROM SYOBJH WHERE OBJECT_NAME ='{ObjectName}' ".format(ObjectName = ObjectName))

        GetQuoteId = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID FROM {ObjectName} WHERE {primarykey} = '{CurrentId}'".format(ObjectName = ObjectName,primarykey = str(GetObjHPromaryKey.RECORD_NAME),CurrentId = CurrentId))

        QuoteId = str(GetQuoteId.QUOTE_ID)
        RevisionId = str(GetQuoteId.QTEREV_ID)
        ApprovalCombinationID = str(CurrentId)
        ApprovalCombo = str(ApprovalCombinationID) + "-" + str(chainid)
        Log.Info("Approval Combo----->"+str(ApprovalCombo))
        Getlatestauto = Sql.GetFirst(
            "SELECT APPROVAL_ID FROM ACAPMA (NOLOCK) WHERE APPROVAL_ID LIKE '%"
            + str(ApprovalCombo)
            + "%' ORDER BY APPROVAL_ID DESC "
        )
        if Getlatestauto:
            Getlatestautosplit = str(Getlatestauto.APPROVAL_ID).split("-")
            getsplit = str(Getlatestautosplit[6])
            getsplit = int(getsplit) + 1
            approval_id_auto = str(getsplit).rjust(3, "0")
        else:
            approval_id_auto = "001"
        insertQueryStatement = """INSERT ACAPMA (APPROVAL_RECORD_ID,APROBJ_ID,APRTRXOBJ_ID,APRTRXOBJ_RECORD_ID,APRSTAMAP_RECORD_ID,APRCHN_ID,
            APRCHN_RECORD_ID,APRCHNSTP_RECORD_ID,APPROVAL_ID,APROBJ_LABEL,APRSTAMAP_APPROVALSTATUS,
            APPROVE_TEMPLATE_RECORD_ID,TOTALDAYS_IN_APPROVAL,TOTALDAYS_IN_APRCHNSTP,CUR_APRCHNSTP,
            FIN_APPROVE_USER_ID,FIN_APPROVE_USER_RECORD_ID,FIN_REJECT_USER_ID,FIN_REJECT_USER_RECORD_ID,
            REJECT_TEMPLATE_RECORD_ID,REQUEST_DATE,REQUEST_USER_ID,REQUEST_USER_RECORD_ID,
            REQUEST_TEMPLATE_RECORD_ID,CUR_APRCHNSTP_LASTACTIONDATE,CUR_APPCHNSTP_APPROVER_ID,
            CUR_APRCHNSTP_APPROVER_RECORD_ID,CUR_APRCHNSTP_ENTRYDATE,FIN_APPROVE_DATE,REJECT_DATE,
            APPROVE_TEMPLATE_ID,APROBJ_STATUSFIELD_VALUE,REJECT_TEMPLATE_ID,REQUEST_TEMPLATE_ID,
            ADDUSR_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
            SELECT TOP 1 CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_RECORD_ID
                ,'{recid}' AS APROBJ_ID
                ,'{QuoteId}' AS APRTRXOBJ_ID
                ,'{ApprovalCombinationID}' AS APRTRXOBJ_RECORD_ID
                ,ACACSS.APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID AS APRSTAMAP_RECORD_ID
                ,ACAPCH.APRCHN_ID AS APRCHN_ID
                ,ACAPCH.APPROVAL_CHAIN_RECORD_ID AS APRCHN_RECORD_ID
                ,ACACST.APPROVAL_CHAIN_STEP_RECORD_ID AS APRCHNSTP_RECORD_ID
                ,CONVERT(VARCHAR(4000), SYOBJH.OBJECT_NAME + '-' + '{QuoteId}' + '-' + '{RevisionId}'
                + '-' + ACAPCH.APRCHN_ID + '-'+'{approval_id_auto}') AS APPROVAL_ID
                ,ACAPCH.APROBJ_LABEL AS APROBJ_LABEL
                ,ACACSS.APPROVALSTATUS AS APRSTAMAP_APPROVALSTATUS
                ,ACACST.APPROVE_TEMPLATE_RECORD_ID AS APPROVE_TEMPLATE_RECORD_ID
                ,'0' AS TOTALDAYS_IN_APPROVAL
                ,'0' AS TOTALDAYS_IN_APRCHNSTP
                ,ACACST.APRCHNSTP_NUMBER AS CUR_APRCHNSTP
                ,'' AS FIN_APPROVE_USER_ID
                ,'' AS FIN_APPROVE_USER_RECORD_ID
                ,'' AS FIN_REJECT_USER_ID
                ,'' AS FIN_REJECT_USER_RECORD_ID
                ,ACACST.REJECT_TEMPLATE_RECORD_ID AS REJECT_TEMPLATE_RECORD_ID
                ,null AS REQUEST_DATE
                ,'' AS REQUEST_USER_ID
                ,'' AS REQUEST_USER_RECORD_ID
                ,ACACST.REQUEST_TEMPLATE_RECORD_ID AS REQUEST_TEMPLATE_RECORD_ID
                ,convert(VARCHAR(10), ACACST.CpqTableEntryDateModified, 101) AS CUR_APRCHNSTP_LASTACTIONDATE
                ,ACACSA.APRCHNSTP_APPROVER_ID AS CUR_APPCHNSTP_APPROVER_ID
                ,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID AS CUR_APRCHNSTP_APPROVER_RECORD_ID
                ,convert(VARCHAR(10), '{datetime_value}', 101) AS CUR_APRCHNSTP_ENTRYDATE
                ,null AS FIN_APPROVE_DATE
                ,null AS REJECT_DATE
                ,ACACST.APPROVE_TEMPLATE_ID AS APPROVE_TEMPLATE_ID
                ,ACACSS.APROBJ_STATUSFIELD_VAL AS APROBJ_STATUSFIELD_VALUE
                ,ACACST.REJECT_TEMPLATE_ID AS REJECT_TEMPLATE_ID
                ,ACACST.REQUEST_TEMPLATE_ID AS REQUEST_TEMPLATE_ID
                ,'{Get_UserID}' AS ADDUSR_RECORD_ID
                ,'{UserName}' AS CPQTABLEENTRYADDEDBY
                ,convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED
                ,'{Get_UserID}' AS CpqTableEntryModifiedBy
                ,convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified
            FROM ACAPCH(NOLOCK)
            INNER JOIN ACACST(NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACST.APRCHN_RECORD_ID
            INNER JOIN ACACSA(NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACSA.APRCHN_RECORD_ID
            AND ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID
            INNER JOIN ACACSS(NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACSS.APRCHN_RECORD_ID
            INNER JOIN SYOBJH(NOLOCK) ON ACAPCH.APROBJ_RECORD_ID = SYOBJH.RECORD_ID""".format(
            Get_UserID=self.Get_UserID,
            datetime_value=self.datetime_value,
            ApprovalCombinationID=ApprovalCombinationID,
            UserName=self.Get_UserNAME,
            approval_id_auto=approval_id_auto,
            QuoteId=str(QuoteId),
            RevisionId=str(RevisionId),
            recid=GetObjHPromaryKey.RECORD_ID
        )
        Log.Info("query statement acapma ---"+str(insertQueryStatement))
        return insertQueryStatement

    def ApprovalTranscationDataInsert(self, ApprovalChainRecordId=None,QuoteId=None,RoundKey=None,Round=None):
        #Round = Quote.GetGlobal("Round")
        """ACAPTX date insert script."""
        InsertQueryStatement = """INSERT ACAPTX ( APRCHNRND_RECORD_ID,APPROVAL_ROUND,APRTRXOBJ_ID,APRCHN_ID ,APPROVAL_TRANSACTION_RECORD_ID ,APRCHN_RECORD_ID ,
        APRCHNSTP_APPROVER_ID ,APRCHNSTP_APPROVER_RECORD_ID ,APRCHNSTP_ID ,APRCHNSTP_NAME,APRCHNSTP_RECORD_ID ,
        APRCHNSTP_STATUS_RECORD_ID ,APRCHNSTPTRX_ID ,APPROVAL_ID ,APPROVAL_RECIPIENT ,
        APPROVAL_RECIPIENT_RECORD_ID ,APPROVAL_RECORD_ID ,APPROVALSTATUS ,APPROVE_TEMPLATE_ID ,
        APPROVE_TEMPLATE_RECORD_ID ,APPROVED_BY ,APPROVEDBY_RECORD_ID ,ARCHIVED ,ASSIGNED_GROUP_ID ,
        ASSIGNED_RECIPIENT ,ASSIGNED_TO ,ASSIGNED_TO_ME ,RECIPIENT_COMMENTS ,DELEGATED_APPROVER ,
        REJECTED_BY ,REJECTBY_RECORD_ID ,REJECT_TEMPLATE_ID ,REJECT_TEMPLATE_RECORD_ID ,
        REQUEST_TEMPLATE_ID ,REQUEST_TEMPLATE_RECORD_ID ,REQUIRE_EXPLICIT_APPROVAL ,
        UNANIMOUS_CONSENT ,REQUESTOR_COMMENTS,ADDUSR_RECORD_ID,CPQTABLEENTRYADDEDBY,
        CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified )
        SELECT DISTINCT '{roundkey}' AS APRCHNRND_RECORD_ID
            ,{round} AS APPROVAL_ROUND, '{QuoteId}' AS APRTRXOBJ_ID,ACAPCH.APRCHN_ID AS APRCHN_ID
            ,CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_TRANSACTION_RECORD_ID
            ,ACAPCH.APPROVAL_CHAIN_RECORD_ID AS APRCHN_RECORD_ID
            ,APPRO.APRCHNSTP_APPROVER_ID AS APRCHNSTP_APPROVER_ID
            ,APPRO.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID AS APRCHNSTP_APPROVER_RECORD_ID
            ,ACACST.APRCHNSTP_NUMBER AS APRCHNSTP_ID
            ,ACACST.APRCHNSTP_NAME AS APRCHNSTP_NAME
            ,ACACST.APPROVAL_CHAIN_STEP_RECORD_ID AS APRCHNSTP_RECORD_ID
            ,ACACSS.APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID AS APRCHNSTP_STATUS_RECORD_ID
            ,CONVERT(VARCHAR(4000),ACAPMA.APPROVAL_ID+'-'+CONVERT(VARCHAR(4000),ACACST.APRCHNSTP_NUMBER)
            +'-'+APPRO.APRCHNSTP_APPROVER_ID) AS APRCHNSTPTRX_ID
            ,ACAPMA.APPROVAL_ID AS APPROVAL_ID
            ,APPRO.USER_NAME AS APPROVAL_RECIPIENT
            ,APPRO.USER_RECORD_ID AS APPROVAL_RECIPIENT_RECORD_ID
            ,ACAPMA.APPROVAL_RECORD_ID AS APPROVAL_RECORD_ID
            ,ACACSS.APPROVALSTATUS AS APPROVALSTATUS
            ,ACACST.APPROVE_TEMPLATE_ID AS APPROVE_TEMPLATE_ID
            ,ACACST.APPROVE_TEMPLATE_RECORD_ID AS APPROVE_TEMPLATE_RECORD_ID
            ,'' AS APPROVED_BY
            ,'' AS APPROVEDBY_RECORD_ID
            ,'' AS ARCHIVED
            ,'' AS ASSIGNED_GROUP_ID
            ,'' AS ASSIGNED_RECIPIENT
            ,'' AS ASSIGNED_TO
            ,'' AS ASSIGNED_TO_ME
            ,'' AS RECIPIENT_COMMENTS
            ,APPRO.DELEGATED_APPROVER_ID AS DELEGATED_APPROVER
            ,'' AS REJECTED_BY
            ,'' AS REJECTBY_RECORD_ID
            ,ACACST.REJECT_TEMPLATE_ID AS REJECT_TEMPLATE_ID
            ,ACACST.REJECT_TEMPLATE_RECORD_ID AS REJECT_TEMPLATE_RECORD_ID
            ,ACACST.REQUEST_TEMPLATE_ID AS REQUEST_TEMPLATE_ID
            ,ACACST.REQUEST_TEMPLATE_RECORD_ID AS REQUEST_TEMPLATE_RECORD_ID
            ,ACACST.REQUIRE_EXPLICIT_APPROVAL AS REQUIRE_EXPLICIT_APPROVAL
            ,APPRO.UNANIMOUS_CONSENT AS UNANIMOUS_CONSENT
            ,'' AS REQUESTOR_COMMENTS
            ,'{Get_UserID}' AS ADDUSR_RECORD_ID
            ,'{UserName}' AS CPQTABLEENTRYADDEDBY
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED
            ,'{Get_UserID}' AS CpqTableEntryModifiedBy
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified
        FROM ACAPCH(NOLOCK)
        INNER JOIN ACACST(NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACST.APRCHN_RECORD_ID
        INNER JOIN ACACSS(NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACSS.APRCHN_RECORD_ID
        AND ACACSS.APROBJ_RECORD_ID != ''
        INNER JOIN (
            SELECT ACACSA.APRCHNSTP_APPROVER_ID
                ,ACACSA.APRCHNSTP_RECORD_ID
                ,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID
                ,ACACSA.DELEGATED_APPROVER_ID
                ,ACACSA.UNANIMOUS_CONSENT
                ,usr.USER_NAME
                ,usr.USER_RECORD_ID
            FROM ACACSA(NOLOCK)
            LEFT JOIN (
                SELECT USER_NAME
                    ,SYROUS.USER_RECORD_ID
                    ,ACACSA.APRCHNSTP_APPROVER_ID
                    ,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID
                FROM SYROUS(NOLOCK)
                INNER JOIN ACACSA(NOLOCK) ON SYROUS.ROLE_ID = ACACSA.ROLE_ID
                WHERE ACACSA.APRCHN_RECORD_ID = '{ApprovalChainRecordId}'
                UNION

                SELECT NAME AS USER_NAME
                    ,ID AS USER_RECORD_ID
                    ,ACACSA.APRCHNSTP_APPROVER_ID
                    ,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID
                FROM ACACSA(NOLOCK)
                INNER JOIN USERS_PERMISSIONS (NOLOCK) ON ACACSA.PROFILE_RECORD_ID = USERS_PERMISSIONS.permission_id
                INNER JOIN USERS (NOLOCK) ON USERS.ID =  USERS_PERMISSIONS.user_id 
                WHERE USERS_PERMISSIONS.permission_id = ACACSA.PROFILE_RECORD_ID AND ACACSA.APRCHN_RECORD_ID = '{ApprovalChainRecordId}'

                UNION

                SELECT NAME AS USER_NAME
                    ,ID AS USER_RECORD_ID
                    ,ACACSA.APRCHNSTP_APPROVER_ID
                    ,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID
                FROM USERS(NOLOCK)
                INNER JOIN ACACSA(NOLOCK) ON USERS.USERNAME = ACACSA.USERNAME
                WHERE ACACSA.APRCHN_RECORD_ID = '{ApprovalChainRecordId}'
                ) AS usr ON usr.APRCHNSTP_APPROVER_ID = ACACSA.APRCHNSTP_APPROVER_ID AND usr.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID = ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID
            ) AS APPRO ON APPRO.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID
            INNER JOIN ACAPMA (NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID """.format(
            Get_UserID=self.Get_UserID, datetime_value=self.datetime_value, UserName=self.Get_UserNAME, ApprovalChainRecordId=ApprovalChainRecordId,QuoteId=QuoteId,roundkey=RoundKey,round=Round
        )
        return InsertQueryStatement

    def CustomApprovalTranscationDataInsert(self, ApprovalChainRecordId=None,QuoteId=None,RoundKey=None,Round=None,CustomQuery=None):
        InsertQueryStatement = """INSERT ACAPTX ( APRCHNRND_RECORD_ID,APPROVAL_ROUND,APRTRXOBJ_ID,APRCHN_ID ,APPROVAL_TRANSACTION_RECORD_ID ,APRCHN_RECORD_ID ,
        APRCHNSTP_APPROVER_ID ,APRCHNSTP_ID ,APRCHNSTP_NAME,APRCHNSTP_RECORD_ID ,
        APRCHNSTP_STATUS_RECORD_ID ,APRCHNSTPTRX_ID ,APPROVAL_ID ,APPROVAL_RECIPIENT ,
        APPROVAL_RECIPIENT_RECORD_ID ,APPROVAL_RECORD_ID ,APPROVALSTATUS ,APPROVE_TEMPLATE_ID ,
        APPROVE_TEMPLATE_RECORD_ID ,APPROVED_BY ,APPROVEDBY_RECORD_ID ,ARCHIVED ,ASSIGNED_GROUP_ID ,
        ASSIGNED_RECIPIENT ,ASSIGNED_TO ,ASSIGNED_TO_ME ,RECIPIENT_COMMENTS ,
        REJECTED_BY ,REJECTBY_RECORD_ID ,REJECT_TEMPLATE_ID ,REJECT_TEMPLATE_RECORD_ID ,
        REQUEST_TEMPLATE_ID ,REQUEST_TEMPLATE_RECORD_ID ,REQUIRE_EXPLICIT_APPROVAL  ,REQUESTOR_COMMENTS,ADDUSR_RECORD_ID,CPQTABLEENTRYADDEDBY,
        CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified )
        SELECT DISTINCT '{roundkey}' AS APRCHNRND_RECORD_ID
            ,{round} AS APPROVAL_ROUND, '{QuoteId}' AS APRTRXOBJ_ID,ACAPCH.APRCHN_ID AS APRCHN_ID
            ,CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_TRANSACTION_RECORD_ID
            ,ACAPCH.APPROVAL_CHAIN_RECORD_ID AS APRCHN_RECORD_ID
            ,'USR-'+SAQDLT.MEMBER_ID AS APRCHNSTP_APPROVER_ID
            ,ACACST.APRCHNSTP_NUMBER AS APRCHNSTP_ID
            ,ACACST.APRCHNSTP_NAME AS APRCHNSTP_NAME
            ,ACACST.APPROVAL_CHAIN_STEP_RECORD_ID AS APRCHNSTP_RECORD_ID
            ,ACACSS.APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID AS APRCHNSTP_STATUS_RECORD_ID
            ,CONVERT(VARCHAR(4000),ACAPMA.APPROVAL_ID+'-'+CONVERT(VARCHAR(4000),ACACST.APRCHNSTP_NUMBER)
            +'-'+SAQDLT.MEMBER_ID) AS APRCHNSTPTRX_ID
            ,ACAPMA.APPROVAL_ID AS APPROVAL_ID
            ,SAQDLT.MEMBER_NAME AS APPROVAL_RECIPIENT
            ,SAQDLT.ADDUSR_RECORD_ID AS APPROVAL_RECIPIENT_RECORD_ID
            ,ACAPMA.APPROVAL_RECORD_ID AS APPROVAL_RECORD_ID
            ,ACACSS.APPROVALSTATUS AS APPROVALSTATUS
            ,ACACST.APPROVE_TEMPLATE_ID AS APPROVE_TEMPLATE_ID
            ,ACACST.APPROVE_TEMPLATE_RECORD_ID AS APPROVE_TEMPLATE_RECORD_ID
            ,'' AS APPROVED_BY
            ,'' AS APPROVEDBY_RECORD_ID
            ,'' AS ARCHIVED
            ,'' AS ASSIGNED_GROUP_ID
            ,'' AS ASSIGNED_RECIPIENT
            ,'' AS ASSIGNED_TO
            ,'' AS ASSIGNED_TO_ME
            ,'' AS RECIPIENT_COMMENTS
            ,'' AS REJECTED_BY
            ,'' AS REJECTBY_RECORD_ID
            ,ACACST.REJECT_TEMPLATE_ID AS REJECT_TEMPLATE_ID
            ,ACACST.REJECT_TEMPLATE_RECORD_ID AS REJECT_TEMPLATE_RECORD_ID
            ,ACACST.REQUEST_TEMPLATE_ID AS REQUEST_TEMPLATE_ID
            ,ACACST.REQUEST_TEMPLATE_RECORD_ID AS REQUEST_TEMPLATE_RECORD_ID
            ,ACACST.REQUIRE_EXPLICIT_APPROVAL AS REQUIRE_EXPLICIT_APPROVAL
            ,'' AS REQUESTOR_COMMENTS
            ,'{Get_UserID}' AS ADDUSR_RECORD_ID
            ,'{UserName}' AS CPQTABLEENTRYADDEDBY
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED
            ,'{Get_UserID}' AS CpqTableEntryModifiedBy
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified
        FROM ACAPCH(NOLOCK)
        INNER JOIN ACACST(NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACACST.APRCHN_RECORD_ID
            INNER JOIN ACAPMA (NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID INNER JOIN ACACSS ON ACACSS.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID INNER JOIN SAQDLT(NOLOCK) ON SAQDLT.QTEREV_RECORD_ID = ACAPMA.APRTRXOBJ_RECORD_ID AND {CustomQuery}""".format(
            Get_UserID=self.Get_UserID, datetime_value=self.datetime_value, UserName=self.Get_UserNAME, ApprovalChainRecordId=ApprovalChainRecordId,QuoteId=QuoteId,roundkey=RoundKey,round=Round,CustomQuery=CustomQuery
        )
        return InsertQueryStatement

    def TrackedValueDataInsert(self, objName, trackedfield, TrackedobjectApiName):
        GetKey = SqlHelper.GetList(
            """SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='{objName}' AND IS_KEY = 'True' """.format(
                objName=objName
            )
        )

        combokey = objName + "." + "QUOTE_ID"

        # Tracked value data insert.
        trackedvalue = """INSERT ACAPFV (
            APPROVAL_TRACKED_VALUE_RECORD_ID
            ,APRCHN_ID
            ,APRCHN_RECORD_ID
            ,APRCHNSTP
            ,APRCHNSTP_RECORD_ID
            ,APPROVAL_ID
            ,APPROVAL_RECORD_ID
            ,TRKOBJ_TRACKEDFIELD_LABEL
            ,TRKOBJ_TRACKEDFIELD_RECORD_ID
            ,TRKOBJ_TRACKEDFIELD_OLDVALUE
            ,TRKOBJ_CPQTABLEENTRYID
            ,TRKOBJ_TRACKEDFIELD_NEWVALUE
            ,TRKOBJ_TRKFLDVAL_RECORD_ID
            ,TRKOBJ_NAME
            ,TRKOBJ_KEYCOMBINATIONVAL
            ,OWNER_ID
            ,OWNED_DATE
            ,OWNER_RECORD_ID
            ,CPQTABLEENTRYADDEDBY
            ,ADDUSR_RECORD_ID
            ,CPQTABLEENTRYDATEADDED
            ,CpqTableEntryModifiedBy
            ,CpqTableEntryDateModified
            )
        SELECT CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_TRACKED_VALUE_RECORD_ID
            ,ACACST.APRCHN_ID AS APRCHN_ID
            ,ACACST.APRCHN_RECORD_ID AS APRCHN_RECORD_ID
            ,ACACST.APRCHNSTP_NUMBER AS APRCHNSTP
            ,ACACST.APPROVAL_CHAIN_STEP_RECORD_ID AS APRCHNSTP_RECORD_ID
            ,ACAPMA.APPROVAL_ID AS APPROVAL_ID
            ,ACAPMA.APPROVAL_RECORD_ID AS APPROVAL_RECORD_ID
            ,ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL AS TRKOBJ_TRACKEDFIELD_LABEL
            ,ACAPTF.TRKOBJ_TRACKEDFIELD_RECORD_ID AS TRKOBJ_TRACKEDFIELD_RECORD_ID
            ,'' AS TRKOBJ_TRACKEDFIELD_OLDVALUE
            ,{objName}.CpqTableEntryId AS TRKOBJ_CPQTABLEENTRYID
            ,{objName}.{trackedfield} AS TRKOBJ_TRACKEDFIELD_NEWVALUE
            ,{objName}.{TrackedobjectApiName} AS TRKOBJ_TRKFLDVAL_RECORD_ID
            ,ACAPTF.TRKOBJ_NAME AS TRKOBJ_NAME
            ,{combokey} AS TRKOBJ_KEYCOMBINATIONVAL
            ,'{Get_UserNAME}' AS OWNER_ID
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS OWNED_DATE
            ,'{Get_UserID}' AS OWNER_RECORD_ID
            ,'{Get_UserNAME}' AS CPQTABLEENTRYADDEDBY
            ,'{Get_UserID}' AS ADDUSR_RECORD_ID
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED
            ,'{Get_UserID}' AS CpqTableEntryModifiedBy
            ,convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified FROM ACACST(NOLOCK)
        INNER JOIN ACAPTF(NOLOCK) ON ACACST.APRCHN_RECORD_ID = ACAPTF.APRCHN_RECORD_ID
            AND ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACAPTF.APRCHNSTP_RECORD_ID
        INNER JOIN ACAPMA(NOLOCK) ON ACACST.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID
        CROSS JOIN {objName} """.format(
            datetime_value=self.datetime_value,
            Get_UserID=self.Get_UserID,
            Get_UserNAME=self.Get_UserNAME,
            objName=objName,
            trackedfield=trackedfield,
            TrackedobjectApiName=TrackedobjectApiName,
            combokey=combokey,
        )
        return trackedvalue

    def TrackedValueDataUpdate(self, objName, ApprovelObjectId):
        """Param: objName -> Refere  table table object."""
        """Param: ApprovelObjectId -> Refere APRTRXOBJ_RECORD_ID in approval master table."""
        loopselectcolumn = []
        GetKey = SqlHelper.GetList(
            """SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='{objName}' AND IS_KEY = 'True' """.format(
                objName=objName
            )
        )

        combokey = objName + "." + "QUOTE_ID"
        loopselectcolumn.append("QUOTE_ID")
        loopselectcolumn.append(str(objName + ".CpqTableEntryId"))
        GetAllApprovalMater = SqlHelper.GetList(
            """SELECT DISTINCT SYOBJD.API_NAME
                    ,ACAPTF.TRKOBJ_TRACKEDFIELD_RECORD_ID
                FROM ACAPMA(NOLOCK)
                INNER JOIN ACAPTF ON ACAPMA.APRCHN_RECORD_ID = ACAPTF.APRCHN_RECORD_ID
                INNER JOIN SYOBJD(NOLOCK) ON ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL = SYOBJD.FIELD_LABEL
                INNER JOIN SYOBJH(NOLOCK) ON ACAPMA.APROBJ_LABEL = SYOBJH.LABEL
                WHERE APRTRXOBJ_RECORD_ID = '{ApprovelObjectId}'
                    AND SYOBJD.OBJECT_NAME = '{objName}' """.format(
                objName=objName, ApprovelObjectId=ApprovelObjectId
            )
        )
        for eachAllApprovalMater in GetAllApprovalMater:
            selectcolumn = list(loopselectcolumn)
            if str(eachAllApprovalMater.API_NAME) not in selectcolumn:
                selectcolumn.append(str(eachAllApprovalMater.API_NAME) + " AS TRACKEDVALUE")
            else:
                selectcolumn = str(selectcolumn).replace(
                    str(eachAllApprovalMater.API_NAME), str(eachAllApprovalMater.API_NAME) + " AS TRACKEDVALUE"
                )
            selectcolumn = str(selectcolumn).replace("'", "").replace("[", "").replace("]", "")
            QueryStatement = """UPDATE ACAPFV
                                SET TRKOBJ_TRACKEDFIELD_OLDVALUE = ACAPFV.TRKOBJ_TRACKEDFIELD_NEWVALUE
                                    ,TRKOBJ_TRACKEDFIELD_NEWVALUE = TRACKEDVALUE
                                    ,TRKOBJ_CPQTABLEENTRYID = TST.CpqTableEntryId
                                FROM (
                                    SELECT {selectcolumn}
                                    FROM PAPBEN(NOLOCK)
                                    INNER JOIN ACAPFV(NOLOCK) ON {combokey} = TRKOBJ_KEYCOMBINATIONVAL
                                    INNER JOIN ACAPTF ON
                                        ACAPFV.TRKOBJ_TRACKEDFIELD_RECORD_ID = ACAPTF.TRKOBJ_TRACKEDFIELD_RECORD_ID
                                    INNER JOIN SYOBJD(NOLOCK) ON SYOBJD.FIELD_LABEL = ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL
                                    WHERE AGMREV_ID = '{ApprovelObjectId}'
                                        AND OBJECT_NAME = '{objName}'
                                    ) TST
                                WHERE ACAPFV.TRKOBJ_TRACKEDFIELD_RECORD_ID = '{TrackedFieldRecId}'""".format(
                selectcolumn=selectcolumn,
                TrackedFieldRecId=str(eachAllApprovalMater.TRKOBJ_TRACKEDFIELD_RECORD_ID),
                ApprovelObjectId=ApprovelObjectId,
                objName=objName,
                combokey=combokey,
            )
            TrackedValuesupdate = Sql.RunQuery(QueryStatement)
            selectcolumn = ""

    def InsertAction(self, Objh_Id, RecordId=None, ObjectName=None, method=None):

        """Param: Objh_Id -> Refere SYOBJH table Record Id."""
        """Param: RecordId -> Refere Curresponding object auto number key."""
        """Param: ObjectName -> Refere Curresponding object Name."""
        """Param: method -> Refere Only for Recall Option."""
        rec_name = ""
        Log.Info("Entered Insert Action")
        QuoteId = ""
        if str(ObjectName).strip() == "SAQTRV":
            GetQuoteId = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTRV (NOLOCK) WHERE QTEREV_RECORD_ID = '{}'".format(RecordId))
            QuoteId = GetQuoteId.QUOTE_ID

        CHSqlObjs = Sql.GetList(
            "SELECT APPROVAL_CHAIN_RECORD_ID,APRCHN_ID FROM ACAPCH (NOLOCK) WHERE APROBJ_RECORD_ID = '"
            + str(Objh_Id)
            + "'"
        )
        for index, val in enumerate(CHSqlObjs):
            CSSqlObjs = Sql.GetList(
                "SELECT TOP 1 * FROM ACACST (NOLOCK) WHERE APRCHN_RECORD_ID = '"
                + str(val.APPROVAL_CHAIN_RECORD_ID)
                + "' AND CONDITIONS_MET <> '' ORDER BY APRCHNSTP_NUMBER"
            )
            for result in CSSqlObjs:
                FirstReturn = self.ChainStepConditions(result,RecordId,QuoteId)
                if FirstReturn is not None:
                    where_conditon = (
                        " WHERE ACAPCH.APPROVAL_CHAIN_RECORD_ID = '"
                        + str(val.APPROVAL_CHAIN_RECORD_ID)
                        + "' AND ACACST.APRCHNSTP_NUMBER = '"
                        + str(result.APRCHNSTP_NUMBER)
                        + "' "
                    )
                    if method is None:
                        if index == 0:
                            #Log.Info(" ACVIORULES Inside the delete cal")
                            Rundelete = self.DeleteforApprovalHeaderTable(
                                str(RecordId),
                                str(val.APPROVAL_CHAIN_RECORD_ID),
                                str(result.APPROVAL_CHAIN_STEP_RECORD_ID),
                                str(ObjectName),
                            )
                        where_conditon += "AND ACACSS.APPROVALSTATUS = 'APPROVAL REQUIRED' "
                    else:
                        where_conditon += "AND ACACSS.APPROVALSTATUS = 'REQUESTED' "

                    where_conditon += " ORDER BY ACACST.APRCHNSTP_NUMBER"
                    rulebody = self.ViolationRuleForApprovals(str(RecordId), str(ObjectName), str(val.APRCHN_ID))
                    Rulebodywithcondition = rulebody + where_conditon
                    a = Sql.RunQuery(Rulebodywithcondition)

                    # Approval Rounding - Start
                    primarykey = str(Guid.NewGuid()).upper()
                    roundd = 1
                    if QuoteId!= '':
                        round_obj = Sql.GetFirst("SELECT TOP 1 APPROVAL_ROUND FROM ACACHR WHERE APPROVAL_ID LIKE '%{}%' AND APRCHN_RECORD_ID = '{}' ORDER BY CpqTableEntryId DESC".format(QuoteId,val.APPROVAL_CHAIN_RECORD_ID))
                        if round_obj:
                            roundd = int(round_obj.APPROVAL_ROUND) + 1
                    QueryStatement = """INSERT INTO ACACHR (APPROVAL_CHAIN_ROUND_RECORD_ID,TOTAL_CHNSTP,TOTAL_APRTRX,COMPLETED_DATE,COMPLETEDBY_RECORD_ID,COMPLETED_BY,APPROVAL_ROUND,APPROVAL_RECORD_ID,APPROVAL_ID,APRCHN_RECORD_ID,APRCHN_NAME,APRCHN_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) VALUES ('{primarykey}',0,0,null,'','',{Round},'','','','','','{UserName}','{datetime_value}','{UserId}','{datetime_value}')""".format(primarykey = primarykey,UserId=self.Get_UserID, UserName=self.Get_UserNAME,Round=roundd,datetime_value=self.datetime_value, Name=self.Get_NAME)

                    Sql.RunQuery(QueryStatement)
                    # Approval Rounding - End

                    CheckViolaionRule2 = Sql.GetList(
                        "SELECT ACACST.APPROVAL_CHAIN_STEP_RECORD_ID,ACACST.APRCHN_ID,ACACST.APRCHNSTP_NAME,ACAPCH.APPROVAL_METHOD,ACAPCH.APPROVAL_CHAIN_RECORD_ID,ACACST.APRCHNSTP_NUMBER,ACACST.WHERE_CONDITION_01,ACACST.CONDITIONS_MET,"
                        + " ACACST.APROBJ_LABEL,ACACST.TSTOBJ_RECORD_ID FROM ACAPCH INNER JOIN ACACST ON "
                        + " ACAPCH.APPROVAL_CHAIN_RECORD_ID = "
                        + " ACACST.APRCHN_RECORD_ID WHERE ACAPCH.APROBJ_RECORD_ID = '"
                        + str(Objh_Id)
                        + "' AND CONDITIONS_MET <> '' AND ACAPCH.APPROVAL_CHAIN_RECORD_ID = '"
                        + str(val.APPROVAL_CHAIN_RECORD_ID)
                        + "' "
                    )

                    if CheckViolaionRule2:
                        for result in CheckViolaionRule2:
                            SecondReturn = self.ChainStepConditions(result,RecordId,QuoteId)
                            if SecondReturn:

                                where_conditon = (
                                    " WHERE ACAPCH.APPROVAL_CHAIN_RECORD_ID = '"
                                    + str(result.APPROVAL_CHAIN_RECORD_ID)
                                    + "' AND ACACST.APRCHNSTP_NUMBER = '"
                                    + str(result.APRCHNSTP_NUMBER)
                                    + "'  "
                                )
                                GetLatestApproval = Sql.GetFirst(
                                    "SELECT TOP 1 APPROVAL_RECORD_ID FROM ACAPMA (NOLOCK) ORDER BY CpqTableEntryId DESC "
                                )
                                where_conditon += (
                                    " AND ACAPMA.APPROVAL_RECORD_ID = '"
                                    + str(GetLatestApproval.APPROVAL_RECORD_ID)
                                    + "' "
                                )
                                if method is None:
                                    where_conditon += " AND ACACSS.APPROVALSTATUS = 'APPROVAL REQUIRED' "
                                    flag = 0
                                else:
                                    where_conditon += " AND ACACSS.APPROVALSTATUS = 'REQUESTED' "
                                    if result.APPROVAL_METHOD == "SERIES STEP APPROVAL":
                                        flag = 1
                                    else:
                                        flag = 0

                                getCustomQuery = Sql.GetFirst("SELECT CpqTableEntryId,CUSTOM_QUERY,APRCHN_ID FROM ACACSA (NOLOCK) WHERE APPROVER_SELECTION_METHOD = ' CUSTOM QUERY' AND APRCHN_RECORD_ID = '{}' AND APRCHNSTP_RECORD_ID = '{}'".format(str(val.APPROVAL_CHAIN_RECORD_ID),result.APPROVAL_CHAIN_STEP_RECORD_ID))
                                if getCustomQuery is not None:
                                    CustomQuery = str(getCustomQuery.CUSTOM_QUERY).upper()
                                    CustomQuery = str(CustomQuery.split("WHERE")[1]).lstrip()
                                    CustomQuery = "SAQDLT." + CustomQuery

                                    where_conditon = where_conditon.replace("WHERE", "AND")
                                    Transcationrulebody = self.CustomApprovalTranscationDataInsert(ApprovalChainRecordId=result.APPROVAL_CHAIN_RECORD_ID,QuoteId=QuoteId,RoundKey=primarykey,Round=roundd,CustomQuery=CustomQuery)
                                    Rulebodywithcondition = Transcationrulebody + where_conditon
                                    #Trace.Write("777777 ACAPTX--------->"+str(Rulebodywithcondition))
                                    b = Sql.RunQuery(Rulebodywithcondition)

                                    if getCustomQuery.APRCHN_ID == 'SELFAPPR':
                                        Sql.RunQuery("UPDATE ACAPTX SET APPROVALSTATUS = 'REQUESTED' WHERE APPROVAL_RECORD_ID = '{}'".format(GetLatestApproval.APPROVAL_RECORD_ID))

                                        Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = 'APR-APPROVAL PENDING' WHERE QUOTE_REVISION_RECORD_ID ='{}'".format(RecordId))
                                        CQCPQC4CWB.writeback_to_c4c("quote_header",QuoteId,RecordId)
                                        #time.sleep(3)
                                        CQCPQC4CWB.writeback_to_c4c("opportunity_header",QuoteId,RecordId)
                                else:
                                    where_conditon += """GROUP BY APPRO.USER_RECORD_ID,ACAPCH.APRCHN_ID,
                                ACAPCH.APPROVAL_CHAIN_RECORD_ID ,APPRO.APRCHNSTP_APPROVER_ID ,
                                APPRO.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,ACACST.APRCHNSTP_NUMBER ,
                                ACACST.APPROVAL_CHAIN_STEP_RECORD_ID,ACACSS.APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID,
                                ACAPMA.APPROVAL_ID,APPRO.USER_NAME,ACAPMA.APPROVAL_RECORD_ID,ACACSS.APPROVALSTATUS,
                                ACACST.APPROVE_TEMPLATE_ID,ACACST.APPROVE_TEMPLATE_RECORD_ID,APPRO.DELEGATED_APPROVER_ID,
                                ACACST.REJECT_TEMPLATE_ID,ACACST.REJECT_TEMPLATE_RECORD_ID,ACACST.REQUEST_TEMPLATE_ID,
                                ACACST.REQUEST_TEMPLATE_RECORD_ID,ACACST.REQUIRE_EXPLICIT_APPROVAL,
                                APPRO.UNANIMOUS_CONSENT,ACACST.APRCHNSTP_NAME,ACAPMA.APRTRXOBJ_ID ORDER BY ACACST.APRCHNSTP_NUMBER"""
                                    Transcationrulebody = self.ApprovalTranscationDataInsert(ApprovalChainRecordId=result.APPROVAL_CHAIN_RECORD_ID,QuoteId=QuoteId,RoundKey=primarykey,Round=roundd)
                                    Rulebodywithcondition = Transcationrulebody + where_conditon

                                    b = Sql.RunQuery(Rulebodywithcondition)

                                    self.SnapshotConditions(result,RecordId,QuoteId,GetLatestApproval.APPROVAL_RECORD_ID)

                                GetTrackedFields = Sql.GetList(
                                    """SELECT APPROVAL_TRACKED_FIELD_RECORD_ID,API_NAME,OBJECT_NAME FROM ACAPTF (NOLOCK)
                                    INNER JOIN SYOBJD (NOLOCK)
                                    ON ACAPTF.TRKOBJ_TRACKEDFIELD_RECORD_ID = SYOBJD.RECORD_ID
                                    WHERE ACAPTF.APRCHN_RECORD_ID = '{chainrecordId}'
                                    AND ACAPTF.APRCHNSTP = '{chainstep}' """.format(
                                        chainrecordId=str(result.APPROVAL_CHAIN_RECORD_ID),
                                        chainstep=str(result.APRCHNSTP_NUMBER),
                                    )
                                )
                                for trackedfield in GetTrackedFields:
                                    TrackedFieldPrimayId = str(trackedfield.APPROVAL_TRACKED_FIELD_RECORD_ID)
                                    TrackedFieldName = str(trackedfield.API_NAME)
                                    Trackedobject = str(trackedfield.OBJECT_NAME)
                                    TrackedobjectApiNameQry = Sql.GetFirst(
                                        """select RECORD_NAME
                                    from SYOBJH (nolock) where
                                    OBJECT_NAME = '{Trackedobject}'
                                    """.format(
                                            Trackedobject=Trackedobject
                                        )
                                    )
                                    TrackedobjectApiName = str(TrackedobjectApiNameQry.RECORD_NAME)
                                    TackedRuleBody = self.TrackedValueDataInsert(
                                        Trackedobject, TrackedFieldName, TrackedobjectApiName
                                    )
                                    Tracked_where_conditon = """WHERE ACAPTF.APRCHN_RECORD_ID = '{chainrecordId}'
                                        AND ACAPTF.APRCHNSTP = '{chainstep}'
                                        AND ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID = '{TrackedFieldPrimayId}'
                                        AND ACAPMA.APPROVAL_RECORD_ID = '{approvalrecordId}'
                                        AND {violationsrule} AND
                                        {Trackedobject}.{ViolatedObjAutoKey} = '{ViolatedObjAutoKeyValue}' """.format(
                                        chainrecordId=str(result.APPROVAL_CHAIN_RECORD_ID),
                                        chainstep=str(result.APRCHNSTP_NUMBER),
                                        TrackedFieldPrimayId=TrackedFieldPrimayId,
                                        approvalrecordId=str(GetLatestApproval.APPROVAL_RECORD_ID),
                                        violationsrule=str(result.WHERE_CONDITION_01),
                                        ViolatedObjAutoKey="QTEREV_RECORD_ID" if Trackedobject != 'SAQTRV' else "QUOTE_REVISION_RECORD_ID",
                                        ViolatedObjAutoKeyValue=str(RecordId),
                                        Trackedobject=Trackedobject,
                                    )
                                    trackedbodywithcondition = TackedRuleBody + Tracked_where_conditon
                                    Trace.Write("trackedbodywithcondition-----> " + str(trackedbodywithcondition))
                                    b = Sql.RunQuery(trackedbodywithcondition)

                    if QuoteId != "":
                        transaction_count_obj = Sql.GetFirst("SELECT count(CpqTableEntryId) as cnt from ACAPTX where APRTRXOBJ_ID='{}' and APRCHNRND_RECORD_ID ='{}' ".format(QuoteId,primarykey))
                        chnstp_count_obj = Sql.GetFirst("SELECT count(distinct APRCHNSTP_ID) as cnt from ACAPTX where APRTRXOBJ_ID='{}' and APRCHNRND_RECORD_ID ='{}' ".format(QuoteId,primarykey))
                        UPDATE_ACACHR = """ UPDATE ACACHR SET ACACHR.TOTAL_APRTRX = {total},ACACHR.TOTAL_CHNSTP={totalchnstp},ACACHR.APRCHN_NAME=ACAPCH.APRCHN_NAME,ACACHR.APPROVAL_RECORD_ID = ACAPTX.APPROVAL_RECORD_ID,ACACHR.APPROVAL_ID = ACAPTX.APPROVAL_ID,ACACHR.APRCHN_RECORD_ID = ACAPTX.APRCHN_RECORD_ID,ACACHR.APRCHN_ID = ACAPTX.APRCHN_ID FROM ACAPTX INNER JOIN ACAPCH (NOLOCK) ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPTX.APRCHN_RECORD_ID INNER JOIN ACACHR ON ACAPTX.APRCHNRND_RECORD_ID = ACACHR.APPROVAL_CHAIN_ROUND_RECORD_ID WHERE ACAPTX.APRTRXOBJ_ID ='{quoteId}' AND ACACHR.APPROVAL_CHAIN_ROUND_RECORD_ID='{primarykey}'""".format(quoteId=QuoteId,primarykey=primarykey,total=transaction_count_obj.cnt,totalchnstp=chnstp_count_obj.cnt)
                        Sql.RunQuery(UPDATE_ACACHR)
                else:
                    Log.Info("else @758")
        return True

    def AutoApproval(self, revisionId, segmentId):
        """Auto Approval Method."""
        sqlObjs = Sql.GetFirst(
            """select
               count(PAPBEN.PRICEAGM_REV_PRODUCTS_RECORD_ID) as cnt
               from PAPBEN (nolock)
               inner join PASPCC (nolock) on
               PAPBEN.AGMREV_ID = PASPCC.AGMREV_ID
               AND PAPBEN.PRICEAGREEMENT_ID = PASPCC.PRICEAGREEMENT_ID
               where PAPBEN.PRICEAGREEMENT_ID = '{segmentId}' AND PAPBEN.AGMREV_ID = '{revisionId}'
               """.format(
                revisionId=revisionId, segmentId=segmentId
            )
        )

        if sqlObjs and int(sqlObjs.cnt) > 0:
            updateAutoApproval = """update QH set
                            REVISION_STATUS = 'APR-APPROVED FOR PUBLISHING',
                            APR-APPROVED = 'True'
                            from PASGRV (nolock) QH
                            where QH.AGMREV_ID = '{revisionId}' AND QH.PRICEAGREEMENT_ID = '{segmentId}'
                            """.format(
                revisionId=revisionId, segmentId=segmentId
            )
            b = Sql.RunQuery(updateAutoApproval)
        return True


 

    def ChainStepConditions(self, result, RecordId, QuoteId):
        arr = []

        # Get Rows from ACACSF based on chain step
        GetACACSF = Sql.GetList(
            "SELECT * FROM ACACSF (NOLOCK) WHERE APRCHNSTP_RECORD_ID = '{}'".format(result.APPROVAL_CHAIN_STEP_RECORD_ID)
        )
        # Get Operators using dictionary

        # Iterate to form query and check feasibility
        if result.APRCHN_ID != "SELFAPPR":
            for x in GetACACSF:
                # ----------------------------------------
                config_entry = self.snap_query_config.get(x.CMP_OPERATOR)
                if config_entry:
                    selectQuery = config_entry.format(x.TSTOBJ_TESTEDFIELD_LABEL,x.TSTOBJ_LABEL, x.TSTOBJ_TESTEDFIELD_LABEL, x.CMP_VALUE)
                else:
                    selectQuery = self.snap_query_config['default'].format(
                        x.TSTOBJ_TESTEDFIELD_LABEL,x.TSTOBJ_LABEL, x.TSTOBJ_TESTEDFIELD_LABEL, self.operators_config[x.CMP_OPERATOR], x.CMP_VALUE
                    )
                # ----------------------------------------

                # Append Quote and Revision to the Query
                if "SAQ" in x.TSTOBJ_LABEL:
                    selectQuery += " AND QTEREV_RECORD_ID = '{}' AND QUOTE_ID = '{}'".format(RecordId, QuoteId)
                elif "ACAPMA" in x.TSTOBJ_LABEL:
                    selectQuery += " AND APRTRXOBJ_RECORD_ID = '{}' AND APRTRXOBJ_ID = '{}'".format(RecordId, QuoteId)

                QueryResult = Sql.GetFirst(selectQuery)

                arr.append(1 if QueryResult else 0)

            if result.CONDITIONS_MET in ["ANY", "ALL"]:
                if (1 in arr) and result.CONDITIONS_MET == "ANY":
                    return 1
                if len(arr) == arr.count(1) and result.CONDITIONS_MET == "ALL":
                    return 1
                return None

            else:
                getMax = Sql.GetFirst(
                    "SELECT MAX(APRCHNSTP_NUMBER_CONDITION) AS MAX_COUNT FROM ACACSF (NOLOCK) WHERE APRCHNSTP_RECORD_ID = '{}'".format(
                        result.APPROVAL_CHAIN_STEP_RECORD_ID
                    )
                )
                condition = result.ADVANCED_CONDITION
                for i in range(1, int(getMax.MAX_COUNT) + 1):
                    condition.replace(i, arr[i - 1])

                return bool(condition)

        else:
            for x in GetACACSF:
                selectQuery = "SELECT CpqTableEntryId FROM {} (NOLOCK) WHERE ".format(x.TSTOBJ_LABEL)

                # Append Quote and Revision to the Query
                if "SAQ" in x.TSTOBJ_LABEL:
                    selectQuery += " AND QTEREV_RECORD_ID = '{}' AND QUOTE_ID = '{}'".format(RecordId, QuoteId)
                elif "ACAPTX" in x.TSTOBJ_LABEL:
                    selectQuery += " APRTRXOBJ_ID = '{}'".format(QuoteId)

                QueryResult = Sql.GetFirst(selectQuery)

                if QueryResult:
                    arr.append(0)
                else:
                    arr.append(1)

            if result.CONDITIONS_MET == "ANY":
                if 1 in arr:
                    return 1
                return None


    def SnapshotConditions(self,result,RecordId,QuoteId,ApprovalRecordId):


        # Get Rows from ACACSF based on chain step
        GetACACSF = Sql.GetList("SELECT * FROM ACACSF (NOLOCK) WHERE APRCHNSTP_RECORD_ID = '{}'".format(result.APPROVAL_CHAIN_STEP_RECORD_ID))

        # Get Operators using dictionary

        # Iterate to form query and check feasibility

        for x in GetACACSF:
            # ----------------------------------------
            config_entry = self.snap_query_config.get(x.CMP_OPERATOR)
            if config_entry:
                selectQuery = config_entry.format(x.TSTOBJ_TESTEDFIELD_LABEL,x.TSTOBJ_LABEL, x.TSTOBJ_TESTEDFIELD_LABEL, x.CMP_VALUE)
            else:
                selectQuery = self.snap_query_config['default'].format(
                    x.TSTOBJ_TESTEDFIELD_LABEL,x.TSTOBJ_LABEL, x.TSTOBJ_TESTEDFIELD_LABEL, self.operators_config[x.CMP_OPERATOR], x.CMP_VALUE
                )
            # ----------------------------------------

            # Append Quote and Revision to the Query
            if "SAQ" in x.TSTOBJ_LABEL:
                selectQuery += " AND QTEREV_RECORD_ID = '{}' AND QUOTE_ID = '{}'".format(RecordId,QuoteId)
            elif "ACAPTX" in x.TSTOBJ_LABEL:
                selectQuery += "  AND APRTRXOBJ_ID = '{}'".format(QuoteId)

            QueryResult = Sql.GetFirst(selectQuery)
            result = ""
            if QueryResult:
                result = eval("QueryResult."+str(x.TSTOBJ_TESTEDFIELD_LABEL))

            InsertSnapshot = Sql.RunQuery(""" INSERT ACAPSS(
                                        APPROVAL_TRANSACTION_SNAPSHOT_RECORD_ID,
                                        APRCHN_ID,
                                        APRCHN_RECORD_ID,
                                        APRCHNSTP,
                                        APRCHNSTP_RECORD_ID,
                                        APRCHNSTPTRX_ID,
                                        APRCHNSTPTRX_RECORD_ID,
                                        APPROVAL_ID,
                                        APPROVAL_RECORD_ID,
                                        APRCHNSTP_TESTEDFIELD_LABEL,
                                        APRCHNSTP_TESTEDFIELD_VALUE,
                                        APRCHNSTP_TESTEDFIELD_RECORD_ID
                                        ) SELECT DISTINCT
                                                CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_TRANSACTION_SNAPSHOT_RECORD_ID,
                                                ACAPTX.APRCHN_ID,
                                                ACAPTX.APRCHN_RECORD_ID,
                                                ACAPTX.APRCHNSTP_ID,
                                                ACAPTX.APRCHNSTP_RECORD_ID,
                                                ACAPTX.APRCHNSTPTRX_ID,
                                                ACAPTX.APPROVAL_TRANSACTION_RECORD_ID,
                                                ACAPTX.APPROVAL_ID,
                                                ACAPTX.APPROVAL_RECORD_ID,
                                                ACACSF.TSTOBJ_TESTEDFIELD_LABEL,
                                                '{}',
                                                ACACSF.APRCHNSTP_TESTEDFIELD_RECORD_ID
                                                FROM ACAPTX (NOLOCK) JOIN ACACSF (NOLOCK) ON
                                                ACAPTX.APRCHNSTP_RECORD_ID = ACACSF.APRCHNSTP_RECORD_ID AND ACAPTX.APPROVAL_RECORD_ID = '{}'""".format(result,ApprovalRecordId))
