# ====================================================================================================
#   __script_name : SYREQFIDSB.PY
#   __script_description : This script is used fetch the Required/Mandatory Field Symbol for all the Fields
#   __primary_author__ : JOE EBENEZER
#   __create_date : 27/08/2020
# ====================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()


def get_required_fields(obj_name):
    fields_list = []
    query_str = "SELECT FIELD_LABEL FROM  SYOBJD (NOLOCK) WHERE REQUIRED = 'TRUE' AND OBJECT_NAME = '{}'".format(obj_name)
    objd_records_obj = Sql.GetList(query_str)
    if objd_records_obj is not None:
        fields_list = [objd_record.FIELD_LABEL for objd_record in objd_records_obj]
    return fields_list


obj_name = Param.objName
ApiResponse = ApiResponseFactory.JsonResponse(get_required_fields(str(obj_name)))