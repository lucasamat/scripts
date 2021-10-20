# =========================================================================================================================================
#   __script_name : CQENANCOPR.py
#   __script_description : THIS SCRIPT IS USED FOR ANCILLARY PRODUCT OPERATIONS
#   __primary_author__ : 
#   __create_date :8/23/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import time
from SYDATABASE import SQL
Sql = SQL()

import System.Net
import sys

class AncillaryProductOperation:
	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
		self.contract_quote_revision_record_id = kwargs.get('contract_quote_revision_record_id')
		self.action_type = kwargs.get('action_type')
		self.service_id = kwargs.get('service_id')
		self.greenbook_id = kwargs.get('greenbook_id')
		self.fablocation_id = kwargs.get('fablocation_id')
		self.equipment_id = kwargs.get('equipment_id')       
		self.pricing_temp_table = ''
		self.quote_line_item_temp_table = '' 
		self.set_contract_quote_related_details()

parameters = {}
action_type = Param.ActionType
quote_record_id = Param.quote_record_id
revision_rec_id = Param.revision_rec_id
service_id  = Param.service_id
where_string = Param.where_string
auto_ancillary_obj = AncillaryProductOperation(**parameters)
auto_ancillary_obj._do_opertion()