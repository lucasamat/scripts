# =========================================================================================================================================
#   __script_name : CQENTLVIEW.PY
#   __script_description :
#   __primary_author__ :Dhurga,Selvi
#   __create_date : 21/09/2021
#   ï¿½ BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================



class EntitlementView():
    def __init__(self):
        self.treeparam = TreeParam
        self.treeparentparam = TreeParentParam
        self.treesuperparentparam = TreeSuperParentParam
        self.treetopsuperparentparam = TreeTopSuperParentParam
        self.treesupertopparentparam = TreeSuperTopParentParam
        ##TreeParentLevel4 added for addon product
        self.treetopsupertopparentparam = TreeTopSuperTopParentParam
        self.ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
        self.revision_recordid = Quote.GetGlobal("quote_revision_record_id")
    def test(self):
        return 'test','value'









try:
    action = Param.action
except:
    action = ""

try:
    alltreeparam =eval(Param.alltreeparam)
    
    TreeParam = alltreeparam["TreeParam"]
    

    try:
        TreeParentParam = alltreeparam["TreeParentLevel0"]
    except:
        TreeParentParam = ""
    try:
        TreeSuperParentParam = alltreeparam["TreeParentLevel1"]
    except:
        TreeSuperParentParam = ""
    try:
        TreeTopSuperParentParam = alltreeparam["TreeParentLevel2"]
    except:
        TreeTopSuperParentParam = ""
    try:
        TreeSuperTopParentParam = alltreeparam["TreeParentLevel3"]
    except:
        TreeSuperTopParentParam = ""
    try:
        TreeTopSuperTopParentParam = alltreeparam["TreeParentLevel4"]
    except:
        TreeTopSuperTopParentParam = ""

except:
    Trace.Write("inside except")
    try:
        TreeParam = Param.TreeParam
    except:
        TreeParam = ""
    try:
        TreeParentParam = Param.TreeParentParam
    except:
        TreeParentParam = ""
    try:
        TreeSuperParentParam = Param.TreeSuperParentParam
    except:
        TreeSuperParentParam = ""
    try:
        TreeTopSuperParentParam = Param.TreeTopSuperParentParam
    except:
        TreeTopSuperParentParam = ""




Trace.Write("action--"+str(action))
entview = EntitlementView()
Result = entview.test()
