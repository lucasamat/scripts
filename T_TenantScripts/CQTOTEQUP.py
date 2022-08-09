import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler
import Webcom.Configurator.Scripting.Test.TestProduct



from SYDATABASE import SQL

Sql = SQL()
import SYCNGEGUID as CPQID

def total_equp(equp_id):
    equp_greenbook = Sql.GetFirst("SELECT GREENBOOK, FABLOCATION_ID FROM QTQFEQ WHERE QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '"+str(equp_id)+ "'")
    gb = equp_greenbook.GREENBOOK
    fab = equp_greenbook.FABLOCATION_ID
    return gb, fab
Node = Param.Node
equp_id = Param.equp_id
    
if Node == "Equipment":
    ApiResponse = ApiResponseFactory.JsonResponse(total_equp(equp_id))