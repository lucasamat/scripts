# =========================================================================================================================================
#   __script_name : CQQUOTEPRE.PY
#   __script_description : THIS SCRIPT IS USED TO VIEW DETAILS IN QUOTE PREVIEW NODE
#   __primary_author__ : KRISHNA CHAITANYA
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
from datetime import datetime
from datetime import timedelta
import datetime
Sql = SQL()
import SYCNGEGUID as CPQID

def Quote_Preview(quote_id,quote_type):       
    Today = datetime.datetime.now().strftime("%m/%d/%Y")
    date_after_month = datetime.datetime.now()+ timedelta(days=90)
    datefor = date_after_month.strftime("%m/%d/%Y")
    QuoteRecordId = Product.GetGlobal("contract_quote_record_id")
    RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
    # recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
    quoteid = Sql.GetFirst("SELECT QUOTE_ID, C4C_QUOTE_ID, CONVERT(varchar,CONTRACT_VALID_FROM,101) as CONTRACT_VALID_FROM,CONVERT(varchar,CONTRACT_VALID_TO,101) as CONTRACT_VALID_TO, CUSTOMER_NOTES FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = QuoteRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))    

    getpaymentterm = Sql.GetFirst("SELECT PAYMENTTERM_NAME FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID =  '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = QuoteRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))    
    
    PO_n = Sql.GetFirst(" SELECT PO_NUMBER FROM SAQRIB (NOLOCK) WHERE QUOTE_ID = '"+str(quote_id)+"' ")
    if PO_n is not None:
        Trace.Write("yes PO")
        PO1 = PO_n.PO_NUMBER
    else:
        Trace.Write("No PO")
        PO1 = ""
    
    cont_1 = Sql.GetFirst(" SELECT PARTY_NAME, EMAIL FROM SAQTIP WHERE PARTY_ROLE = 'CONTRACT MANAGER' AND QUOTE_ID ='"+str(quote_id)+"' ")
    
    cont = Sql.GetFirst(" SELECT PARTY_NAME, PHONE FROM SAQTIP WHERE PARTY_ROLE = 'SALES EMPLOYEE' AND QUOTE_ID ='"+str(quote_id)+"' ")
            
    que_pre = Sql.GetFirst(" SELECT PARTY_NAME, ADDRESS FROM SAQTIP WHERE PARTY_ROLE = 'SHIP TO' AND QUOTE_ID ='"+str(quote_id)+"'  ") 
    
    split2 =  que_pre.ADDRESS.split(", ")
    len(split2)
    if que_pre.ADDRESS!= "":        
        split2 =  que_pre.ADDRESS.split(", ")
    else:        
        split2 = ""
    
    try:        
        if len(split2) == 9:                     
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = split2[6]
            add4 = split2[7]
            add5 = split2[8]
        elif len(split2) == 8:                     
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = split2[6]
            add4 = split2[7]
            add5 = ""
        elif len(split2) == 7:                    
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = split2[6]
            add4 = ""
            add5 = ""
        elif len(split2) == 6:                     
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = ""
            add4 = ""
            add5 = ""
        elif len(split2) == 5:          
                            
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = "" 
            add3 = ""
            add4 = "" 
            add5 = ""        
        elif len(split2) == 4:                                 
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""    
        elif len(split2) == 3:                      
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""
        elif len(split2) == 2:                            
            add1 = split2[0]
            add2 = split2[1]                                     
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""
        elif len(split2) == 1:                          
            add1 = split2[0]
            add2 = ""
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""
        elif str(len(split2)) == '0':                            
            add1 = ""
            add2 = "" 
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""                                                        
    except:
        pass                 
    que_pre1 = Sql.GetFirst(" SELECT PARTY_NAME, ADDRESS FROM SAQTIP WHERE PARTY_ROLE = 'BILL TO' AND QUOTE_ID ='"+str(quote_id)+"'  ")
    split1 =  que_pre1.ADDRESS.split(", ")
    len(split1)
    if que_pre1.ADDRESS!= "":        
        split1 =  que_pre1.ADDRESS.split(", ")
    else:        
        split1 = ""
    try:        
        if len(split1) == 9:                     
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = split1[6]
            add4 = split1[7]
            add5 = split1[8]
        elif len(split1) == 8:                     
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = split1[6]
            add4 = split1[7]
            add5 = ""
        elif len(split1) == 7:                    
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = split1[6]
            add4 = ""
            add5 = ""
        elif len(split1) == 6:                     
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = ""
            add4 = ""
            add5 = ""
        elif len(split1) == 5:         
                            
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = "" 
            add3 = ""
            add4 = "" 
            add5 = ""        
        elif len(split1) == 4:                                
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""    
        elif len(split1) == 3:                       
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = ""
            region = ""
            zcode = "" 
            add3 = ""
            add4 = ""
            add5 = ""
        elif len(split1) == 2:                       
            add1 = split1[0]
            add2 = split1[1]                                     
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""
        elif len(split1) == 1:                           
            add1 = split1[0]
            add2 = "" 
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""
        elif str(len(split1)) == '0':                            
            add1 = ""
            add2 = "" 
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""  
            add5 = ""                                                     
    except:
        pass         
        
    if quoteid != "" and str(cont) != "None" and str(cont_1) != "None" and que_pre != "" and que_pre1 != "" :
        Trace.Write("cm to this if")        
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:86635798888">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:89935793572">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>            
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.C4C_QUOTE_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PHONE)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(getpaymentterm.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(PO1)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.EMAIL)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
            <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(quoteid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>
            

            <div class="col-md-12 p-0">
            <div class="noRecDisp noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>
            
            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif quoteid != "" and str(cont) != "None" and str(cont_1) == "None" and que_pre != "" and que_pre1 != "" :
        Trace.Write("cm to this else")
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:6563117000">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:6563117011">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p> 
            <p class="cust-address-02">"""+str(add5)+"""</p>           
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.C4C_QUOTE_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PHONE)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(getpaymentterm.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
            <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(quoteid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>
            

            <div class="col-md-12 p-0">
            <div class="noRecDisp noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>

            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif quoteid != "" and str(cont) == "None" and str(cont_1) != "None" and que_pre != "" and que_pre1 != "" :
        Trace.Write("cm to this eleeeeeeee")
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:86635798888">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:89935793572">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p> 
            <p class="cust-address-02">"""+str(add5)+"""</p>           
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.C4C_QUOTE_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(getpaymentterm.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.EMAIL)+"""</p>
            </div>
            </div>            

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
          <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(quoteid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>
            

            <div class="col-md-12 p-0">
            <div class="noRecDisp noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>

            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif quoteid != "" and str(cont) == "None" and str(cont_1) == "None" and que_pre != "" and que_pre1 != "" :
        Trace.Write("cm to this elseto")
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:86635798888">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:89935793572">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>            
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>            
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.C4C_QUOTE_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(quoteid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(getpaymentterm.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">QUOTE EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
           <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(quoteid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>
            

            <div class="col-md-12 p-0">
            <div class="noRecDisp noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>

            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          

  
    elif str(quoteid) == "None" and str(cont) == "None" and str(cont_1) == "None" and str(que_pre) == "None" and str(que_pre1) == "None" and PO_n == "None":
        Trace.Write("------>")
        sec_str = """<div class="container-fluid">
                    <div class="col-md-12 p-0">                                
                        <div class="noRecDisp">No Records to Display</div>
                    </div>
                    <div class="col-md-12 p-0">
                            <div class="noRecDisp noRecDisp-head">OFFERINGS</div>
                            <div id="div_Quote"></div>	
                        </div>
                    <div class="col-md-12 p-0 mt-10">
                        <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
                        <div id="Tool_Quote"></div>            	
                    </div>    
                    </div>"""                    
    return sec_str
    
def Contract_Preview(contract_id,contract_type):        
    Today = datetime.datetime.now().strftime("%m/%d/%Y")
    date_after_month = datetime.datetime.now()+ timedelta(days=90)
    datefor = date_after_month.strftime("%m/%d/%Y")
    recid = Product.Attr('QSTN_SYSEFL_QT_016909').GetValue()
    contractid = Sql.GetFirst("SELECT CONTRACT_ID, PAYMENTTERM_NAME,PO_NUMBER, CONVERT(varchar,CONTRACT_VALID_FROM,101) as CONTRACT_VALID_FROM,CONVERT(varchar,CONTRACT_VALID_TO,101) as CONTRACT_VALID_TO, CUSTOMER_NOTES FROM CTCNRT(NOLOCK) WHERE CONTRACT_RECORD_ID =  '"+str(recid)+"'")
    
    cont_1 = Sql.GetFirst(" SELECT PARTY_NAME, EMAIL FROM CTCTIP WHERE PARTY_ROLE = 'CONTRACT MANAGER' AND CONTRACT_ID ='"+str(contract_id)+"' ")
    
    cont = Sql.GetFirst(" SELECT PARTY_NAME, PHONE FROM CTCTIP WHERE PARTY_ROLE = 'SALES EMPLOYEE' AND CONTRACT_ID ='"+str(contract_id)+"' ")
        
    que_pre = Sql.GetFirst(" SELECT PARTY_NAME, ADDRESS FROM CTCTIP WHERE PARTY_ROLE = 'SHIP TO' AND CONTRACT_ID ='"+str(contract_id)+"'  ")    
    
    split2 =  que_pre.ADDRESS.split(", ")
    len(split2)
    if que_pre.ADDRESS!= "":
        split2 =  que_pre.ADDRESS.split(", ")
    else:
        split2 = ""

    try:
        if len(split2) == 9:                    
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = split2[6]
            add4 = split2[7]
            add5 = split2[8]
        elif len(split2) == 8:                    
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = split2[6]
            add4 = split2[7]
            add5 = ""
        elif len(split2) == 7:                     
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = split2[6]
            add4 = ""
            add5 = ""
        elif len(split2) == 6:                     
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = split2[5]
            add3 = ""
            add4 = "" 
            add5 = ""
        elif len(split2) == 5:         
                            
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = split2[4]
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""          
        elif len(split2) == 4:                                 
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = split2[3]
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""      
        elif len(split2) == 3:                      
            add1 = split2[0]
            add2 = split2[1]
            city = split2[2]
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = ""  
        elif len(split2) == 2:                            
            add1 = split2[0]
            add2 = split2[1]                                     
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = "" 
        elif len(split2) == 1:                           
            add1 = split2[0]
            add2 = ""
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""
        elif len(split2) == '0':                            
            add1 = ""
            add2 = ""
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""                                                        
    except:
        pass
    que_pre1 = Sql.GetFirst(" SELECT PARTY_NAME, ADDRESS FROM CTCTIP WHERE PARTY_ROLE = 'BILL TO' AND CONTRACT_ID ='"+str(contract_id)+"'  ")        
    
    
    if que_pre1.ADDRESS!= "":        
        split1 =  que_pre1.ADDRESS.split(", ")
    else:        
        split1 = ""    

    try:        
        if len(split1) == 9:                     
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = split1[6]
            add4 = split1[7]
            add5 = split1[8]
        elif len(split1) == 8:                    
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = split1[6]
            add4 = split1[7]
            add5 = ""
        elif len(split1) == 7:                    
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = split1[6]
            add4 = ""
            add5 = ""
        elif len(split1) == 6:                    
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = split1[5]
            add3 = ""
            add4 = ""
            add5 = "" 
        elif len(split1) == 5:           
                           
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = split1[4]
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""          
        elif len(split1) == 4:                                 
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = split1[3]
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""     
        elif len(split1) == 3:                       
            add1 = split1[0]
            add2 = split1[1]
            city = split1[2]
            country = ""
            region = ""
            zcode = "" 
            add3 = ""
            add4 = "" 
            add5 = ""
        elif len(split1) == 2:                           
            add1 = split1[0]
            add2 = split1[1]                                     
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = ""
            add5 = "" 
        elif len(split1) == 1:                            
            add1 = split1[0]
            add2 = "" 
            city = ""
            country = ""
            region = ""
            zcode = ""
            add3 = ""
            add4 = "" 
            add5 = ""
        elif str(len(split1)) == '0':                           
            add1 = ""
            add2 = "" 
            city = ""
            country = ""
            region = ""
            zcode = "" 
            add3 = ""
            add4 = "" 
            add5 = ""                                                      
    except:
        pass    
    if contractid != "" and str(cont) != "None" and str(cont_1) != "None" and que_pre != "" and que_pre1 != "":
        Trace.Write("cm to this if")        
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:86635798888">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:89935793572">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PHONE)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PO_NUMBER)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.EMAIL)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
            <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(contractid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>


            <div class="col-md-12 p-0">
            <div class="noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>
            
            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif contractid != "" and str(cont) != "None" and str(cont_1) == "None" and que_pre != "" and que_pre1 != "":
        Trace.Write("cm to this elsethis to")
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:6563117000">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:6563117011">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont.PHONE)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PO_NUMBER)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
            <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(contractid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div> 


            <div class="col-md-12 p-0">
            <div class="noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>

            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif contractid != "" and str(cont) == "None" and str(cont_1) != "None" and que_pre != "" and que_pre1 != "":
        Trace.Write("cm to this eleeeeeeee")
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:86635798888">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:89935793572">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PO_NUMBER)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.PARTY_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(cont_1.EMAIL)+"""</p>
            </div>
            </div>            

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
          <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(contractid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>


            <div class="col-md-12 p-0">
            <div class="noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>

            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif contractid != "" and str(cont) == "None" and str(cont_1) == "None" and que_pre != "" and que_pre1 != "":
        Trace.Write("cm to this else")
        sec_str = """
            <div class="container-fluid">
            <div class="col-md-12 header">
            <div class="col-md-6 cust-quto-logo">
            <img src="/mt/appliedmaterials_tst/Additionalfiles/applied-materials-logo.svg">
            </div>	
            <div class="col-md-6 cust-quto-address text-right">
            <address>
            <p class="cust-name">Applied Materials South East Asia.</p>
            <p class="cust-address-1">2F., NO.617,SEC.2,SINHUA RD</p>
            <p class="cust-address-2">32850 TAOYUAN COUNTY</p>
            <p class="cust-city">Taiwan</p>
            <p class="cust-phone"><a href="tel:86635798888">Telephone: 866-3-5798888</a></p>
            <p class="cust-phone"><a href="tel:89935793572">Fax: 899-3-5793572</a></p>
            </address>
            </div>		
            </div>

            <div class="col-md-12 shiping-details p-0">

            <div class="col-md-3 shiping-details-01">
            <address>
            <h3>BILL TO</h3>
            <p class="cust-name">"""+str(que_pre1.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-3 shiping-details-02">
            <address>
            <h3>SHIP TO</h3>
            <p class="cust-name">"""+str(que_pre.PARTY_NAME)+"""</p>
            <p class="cust-address-01">"""+str(add1)+"""</p>
            <p class="cust-address-02">"""+str(add2)+"""</p>
            <p class="cust-address-02">"""+str(city)+"""</p>
            <p class="cust-address-02">"""+str(country)+"""</p>
            <p class="cust-address-02">"""+str(region)+"""</p>
            <p class="cust-address-02">"""+str(zcode)+"""</p>
            <p class="cust-address-02">"""+str(add3)+"""</p>
            <p class="cust-address-02">"""+str(add4)+"""</p>
            <p class="cust-address-02">"""+str(add5)+"""</p>
            </address>
            </div>

            <div class="col-md-6 p-0">
            <div class="shiping-details-03">
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT ID</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_ID)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT REVISION NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT START DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_FROM)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT END DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.CONTRACT_VALID_TO)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES REPRESENTATIVE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">SALES PERSON PHONE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PAYMENT TERMS</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PAYMENTTERM_NAME)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">PURCHASE ORDER NUMBER</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(contractid.PO_NUMBER)+"""</p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT NAME</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CUSTOMER CONTACT EMAIL</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>

            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">CONTRACT DESCRIPTION</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name"></p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">DOCUMENT GENERATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(Today)+"""</p>
            </div>
            </div>
            
            <div class="col-md-12 col-xs-12 p-0">
            <div class="col-md-5 col-xs-6 p-0">
            <p class="left-name">EXPIRATION DATE</p>
            </div>
            <div class="col-md-7 col-xs-6 p-0">
            <p class="right-name">"""+str(datefor)+"""</p>
            </div>
            </div>

            </div>
            </div>

            </div>
           <div class="col-md-12 p-0 mt-10 mb-10">
                <div class="col-md-12 p-0">
                    <div class="cust_stampbox-out">
                        <div class="row">
                            <div class="cust_stampbox_bor col-md-6 bb-0 br-0">                            
                            <h3>NOTES  </h3>
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0 br-0">
                            </div>
                            <div class="cust_stampbox_bor col-md-2 bb-0">
                            </div>
                        </div>
                    
                        <div class="row">
                            <div class="cust_stampbox_bor1 col-md-6 br-0">
                            <p> <span>"""+str(contractid.CUSTOMER_NOTES)+"""</span></p>
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2 br-0">
                            </div>
                            <div class="cust_stampbox_bor1 col-md-2">
                            </div>
                        </div>
                    </div>
                </div> 
                <div class="col-md-12 p-0 cust-foot-content-out">
                    <p class="cust-foot-content">
                    We thank you for your interest in Applied Materials products. Following your recent request, we are pleased to submit you the present quotation for a configuration matching your requirements, The Applied Materials sales team remains at your full services for any further supports and / or clarification you may need.</p>                    
                </div> 
                 
            </div>    


            <div class="col-md-12 p-0">
            <div class="noRecDisp-head">OFFERINGS</div>
            <div id="div_Quote"></div>	
            </div>

            <div class="col-md-12 p-0 mt-10">
            <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
            <div id="Tool_Quote"></div>            	
            </div>			
            </div>"""          


    elif str(contractid) != "None" and str(cont) != "None" and str(cont_1) != "None" and str(que_pre) != "None" and str(que_pre1) != "None":
        Trace.Write("------>")
        sec_str = """<div class="container-fluid">
                    <div class="col-md-12 p-0">                                
                        <div class="noRecDisp">No Records to Display</div>
                    </div>
                    <div class="col-md-12 p-0">
                            <div class="noRecDisp-head">OFFERINGS</div>
                            <div id="div_Quote"></div>	
                        </div>
                    <div class="col-md-12 p-0 mt-10">
                        <div class="noRecDisp noRecDisp-head">APPENDIX A: LINE ITEM DETAILS</div>
                        <div id="Tool_Quote"></div>            	
                    </div>    
                    </div>"""                    
    return sec_str
 
ACTION = Param.ACTION
if ACTION == "QUOTE_PREVIEW":
    quote_id = Param.QUOTE_ID
    quote_type = Param.QUOTE_TYPE           
    ApiResponse = ApiResponseFactory.JsonResponse(Quote_Preview(quote_id,quote_type))
elif ACTION == "CONTRACT_PREVIEW":
    contract_id = Param.QUOTE_ID
    contract_type = Param.QUOTE_TYPE
    ApiResponse = ApiResponseFactory.JsonResponse(Contract_Preview(contract_id,contract_type))