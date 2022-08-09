import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler


def equipments(CURRREC, SELECTROW, Primary_Data, currentprofilename):
	Trace.Write("EQUIPMENTS_CHECK")
	Trace.Write("SELECTROW---" + str(SELECTROW))

if hasattr(Param, "Primary_Data"):
	Primary_Data = Param.Primary_Data
if hasattr(Param, "Primary_Data"):
	Primary_Data = Param.Primary_Data
else:
	Primary_Data = ""

SELECTROW = list(Param.SELECTROW)

if hasattr(Param, "currentprofilename"):
	currentprofilename = Param.currentprofilename
else:
	currentprofilename = ""

if hasattr(Param, "CURRREC"):
	CURRREC = Param.CURRREC
else:
	CURRREC = ""

ApiResponse = ApiResponseFactory.JsonResponse(equipments(CURRREC, SELECTROW, Primary_Data, currentprofilename))