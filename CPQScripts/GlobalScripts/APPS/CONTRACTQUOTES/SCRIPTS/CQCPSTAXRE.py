# =========================================================================================================================================
#   __script_name : CQCPSTAXRE.PY
#   __script_description : THIS SCRIPT IS USED TO RETURN TAX FOR PRODUCT OFFERINGS
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :30-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED -
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import re
import datetime
from System.Text.Encoding import UTF8
from System import Convert
import sys
from SYDATABASE import SQL
Sql = SQL()