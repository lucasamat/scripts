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
	bitbucket_data = ScriptExecutor.ExecuteGlobal("SYGETGHSRC", {"Script":"APPS\SYSTEMADMIN\SCRIPTS\SYMCMOBJCL.py"})
	Trace.Write("BITBUCKET DATA SYMCMOBJCL TRY!!")
	pythonScript = pe.CreateScriptSourceFromString(bitbucket_data, SourceCodeKind.Statements)
	pythonScript.Execute(pyScope)
except:
	Trace.Write("BITBUCKET DATA SYMCMOBJCL EXCEPT!!")
	ApiResponse = ApiResponseFactory.JsonResponse("LOADBTI")