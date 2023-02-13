# =========================================================================================================================================
#   __script_name : SYCNGEGUID.PY
#   __script_description : THIS SCRIPT IS USED TO GET THE CPQTABLEENTRYID OR RECORD_ID FROM A TABLE.
#                          THIS SCRIPT IS CALLED IN CHANGE_RECORDID_TO_CPQID GLOBAL SCRIPT WHEN CONVERTING THE GUID TO TABLE NAME_RECORD ID
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================


from SYDATABASE import SQL
#import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


class KeyCPQId:
    @staticmethod
    def GetCPQId(TABLEID, REC_ID):
        KeyId = ""
        if TABLEID != "":

            RecNameObj = Sql.GetFirst("SELECT RECORD_NAME FROM SYOBJH WITH (NOLOCK) WHERE OBJECT_NAME = '" + TABLEID + "'")
            if RecNameObj is not None:
                RecName = str(RecNameObj.RECORD_NAME)
                RecIDObj = Sql.GetFirst(
                    "SELECT CpqTableEntryId FROM " + TABLEID + " (NOLOCK) WHERE " + RecName + "='" + REC_ID + "' "
                )
                if RecIDObj is not None:
                    CPQID = RecIDObj.CpqTableEntryId
                    if CPQID != "":
                        KeyId = str(TABLEID) + "-" + str(CPQID).rjust(5, "0")
        return KeyId

    @staticmethod
    def GetKEYId(TABLEID, KeyId):
        RecID = ""
        if TABLEID != "":
            RecNameObj = Sql.GetFirst("SELECT RECORD_NAME FROM SYOBJH WITH (NOLOCK) WHERE OBJECT_NAME = '" + TABLEID + "'")
            if RecNameObj is not None:
                CPQID = KeyId.split("-")[1].lstrip("0") if "-" in KeyId else KeyId  ###jira id 6303
                RecName = str(RecNameObj.RECORD_NAME)
                RecIDObj = Sql.GetFirst(
                    "SELECT " + RecName + " AS RECID FROM " + TABLEID + " (NOLOCK) WHERE CpqTableEntryId='" + CPQID + "' "
                )
                if RecIDObj is not None:
                    RecID = str(RecIDObj.RECID)
        return RecID


KeyCPQId = KeyCPQId()