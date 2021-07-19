# =========================================================================================================================================
#   __script_name : CQSPBLKUPL.PY
#   __script_description : THIS SCRIPT IS USED TO SHOW BULK INSERT MODEL(POP-UP)
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :09-10-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
Trace.Write('bulk add-----------------')
model_html = """
        <div class='row modulebnr brdr ma_mar_btm'>BULK ADD<button type='button' class='close flt_rt' onclick='closepopup_scrl()' data-dismiss='modal'>X</button></div>
        <div id='container' class='g4 pad-10 brdr except_sec spare-parts-bulk-add-ctnr-out'>
            <textarea id='spare-parts-bulk-add-ctnr' name='spare-parts-bulk-add-ctnr' class='form-control txtArea' rows='100' cols='100' tabindex='7' style='width: 100%;height: 200px;'></textarea>
        </div>
        <div id='spare-parts-bulk-add-model-footer'>
            <button type='button' class='btnconfig' data-dismiss='modal' onclick='closepopup_scrl()'>CANCEL</button>    
            <button type='button' id='spare-parts-bulk-add-save-btn' class='btnconfig' onclick='bulkAddSpareParts()' data-dismiss='modal'>ADD</button>                
        </div>
        """

ApiResponse = ApiResponseFactory.JsonResponse([model_html])