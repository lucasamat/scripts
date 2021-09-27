# =========================================================================================================================================
#   __script_name : CQENTLVIEW.PY
#   __script_description :
#   __primary_author__ :Dhurga,Selvi
#   __create_date : 21/09/2021
#   ï¿½ BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================


Trace.Write('load ent')


try:
    action = Param.action
except:
    action = ""
try:
    alltreeparam =Param.alltreeparam
except:
    alltreeparam =""

Trace.Write("action--"+str(action))
Trace.Write("AllTreeParam--"+str(alltreeparam))