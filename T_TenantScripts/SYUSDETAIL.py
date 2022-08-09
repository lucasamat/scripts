# ====================================================================================================
#   __script_name : SYUSDETAIL.PY
#   __script_description : This script is used to get the User Details from Module Scripts
#   __primary_author__ :
#   __create_date : 08/27/2020
#   Â© BOSTON HARBOR CONSULTING INC - ALL RIGHTS RESERVED
# ====================================================================================================

UserDetails = {
    "USERNAME": "UserName",
    "USERID": "Id",
    "EMAIL": "Email",
    "FIRSTNAME": "FirstName",
    "LASTNAME": "LastName",
    "NAME": "Name",
    "ISADMIN": "IsAdmin",
}

_detail_param = UserDetails.get(Param.upper())

Result = eval("User.{}".format(_detail_param)) if _detail_param else None
