# ====================================================================================================
#   __script_name : SYUSDETAIL.PY
#   __script_description : This script is used to get the User Details from Module Scripts
#   __primary_author__ : 
#   __create_date : 08/27/2020
#   Â© BOSTON HARBOR CONSULTING INC - ALL RIGHTS RESERVED
# ====================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
Param = Param  # pylint: disable=E0602
User = User  # pylint: disable=E0602

userDetailParam = Param
if userDetailParam.upper() == "USERNAME":
    Result = User.UserName
elif userDetailParam.upper() == "USERID":
    Result = User.Id
elif userDetailParam.upper() == 'EMAIL':
    Result = User.Email
elif userDetailParam.upper() == 'FIRSTNAME':
    Result = User.FirstName
elif userDetailParam.upper() == 'LASTNAME':
    Result = User.LastName
elif userDetailParam.upper() == 'NAME':
    Result = User.Name
elif userDetailParam.upper() == 'ISADMIN':
    Result = User.IsAdmin
else:
    Result = None