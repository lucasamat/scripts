# =========================================================================================================================================
#   __script_name : SYCNGEGUID.PY
#   __script_description : THIS SCRIPT IS USED TO GET THE CPQTABLEENTRYID OR RECORD_ID FROM A TABLE.
#                          THIS SCRIPT IS CALLED IN CHANGE_RECORDID_TO_CPQID GLOBAL SCRIPT WHEN CONVERTING THE GUID TO TABLE NAME_RECORD ID
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import sql_get_first


class KeyCPQId:
    @staticmethod
    def GetCPQId(table_id, rec_id):
        key_id = ""
        if table_id:

            rec_name_obj = sql_get_first(
                "SELECT RECORD_NAME FROM SYOBJH WITH (NOLOCK) WHERE OBJECT_NAME = '{}'".format(table_id)
            )
            if rec_name_obj:
                rec_id_obj = sql_get_first(
                    "SELECT CpqTableEntryId FROM {} (NOLOCK) WHERE {}='{}' ".format(
                        table_id, rec_name_obj.RECORD_NAME, rec_id
                    )
                )
                if rec_id_obj:
                    cpqid = rec_id_obj.CpqTableEntryId
                    if cpqid:
                        key_id = "{}-{}".format(table_id, str(cpqid).rjust(5, "0"))
        return key_id

    @staticmethod
    def GetKEYId(table_id, key_id):
        rec_id = ""
        if table_id:
            rec_name_obj = sql_get_first(
                "SELECT RECORD_NAME FROM SYOBJH WITH (NOLOCK) WHERE OBJECT_NAME = '{}'".format(table_id)
            )
            if rec_name_obj:
                cpqid = key_id.split("-")[1].lstrip("0") if "-" in key_id else key_id  ###jira id 6303
                rec_id_obj = sql_get_first(
                    "SELECT {} AS RECID FROM {} (NOLOCK) WHERE CpqTableEntryId='{}' ".format(
                        rec_name_obj.RECORD_NAME, table_id, cpqid
                    )
                )
                if rec_id_obj:
                    rec_id = str(rec_id_obj.RECID)
        return rec_id


KeyCPQId = KeyCPQId()
