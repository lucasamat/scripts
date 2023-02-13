# =========================================================================================================================================
#   __script_name : SYUGETGUID.PY
#   __script_description : THIS SCRIPT IS USED TO CONVERT THE GUID TO RECORD ID
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def val(RECORDID):
    if RECORDID:
        RECORD_ID = RECORDID.split("-")
        if len(RECORD_ID) > 1:
            cpqid = RECORD_ID[1].lstrip("0")
            Get_API_NAME = Sql.GetFirst(
                "SELECT API_NAME FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='" + RECORD_ID[0] + "' AND DATA_TYPE='AUTO NUMBER'"
            )
            if Get_API_NAME is not None:
                Get_RECID = Sql.GetFirst(
                    "SELECT {}  FROM {} (NOLOCK) WHERE CpqTableEntryId='{}' ".format(
                        Get_API_NAME.API_NAME, RECORD_ID[0], cpqid
                    )
                )
                if Get_RECID is not None:
                    return getattr(Get_RECID, Get_API_NAME.API_NAME)