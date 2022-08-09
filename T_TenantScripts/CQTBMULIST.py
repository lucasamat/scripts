import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()

import Webcom.Configurator.Scripting.Test.TestProduct

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
GETCLICKEDID = Param.GETCLICKID
Action = "Back To List"
Trace.Write('GETCLICKEDID---'+str(GETCLICKEDID))
Log.Info(str(TestProduct)+' -----GETCLICKEDID---'+str(GETCLICKEDID))

Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue(Action)
if GETCLICKEDID == "Approvals":
	GETCLICKEDID = 'Quotes'
elif GETCLICKEDID =="Approval Chains":
	Log.Info("inside app chain")
	GETCLICKEDID = 'Approval Chains'
elif GETCLICKEDID =="Approvalsettings":
	Log.Info("inside app chain")
	GETCLICKEDID = 'Approval Chains'
elif GETCLICKEDID == "Teamapprovalqueue":
	Log.Info("inside team chain")
	GETCLICKEDID = 'Team Approval Queue'
Log.Info('GETCLICKEDID--23---'+str(GETCLICKEDID))
if str(GETCLICKEDID) != "":
	TestProduct.ChangeTab(str(GETCLICKEDID))