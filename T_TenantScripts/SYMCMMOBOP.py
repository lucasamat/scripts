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

runtime = Python.CreateRuntime()
pe = runtime.GetEngine("python")
pyScope = pe.CreateScope(globals())
try:
	GITdata = ScriptExecutor.ExecuteGlobal("SYGETGHSRC", {"Script":"APPS\SYSTEMADMIN\SCRIPTS\SYMCMMOBOP.py"})
	pythonScript = pe.CreateScriptSourceFromString(GITdata, SourceCodeKind.Statements)
	pythonScript.Execute(pyScope)
except Exception:
	Trace.Write("GITHUB DATA CQCRUDOPTN EXCEPT!!")
	ApiResponse = ApiResponseFactory.JsonResponse("LOADBTI")