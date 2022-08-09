def phphighlight():
    tagbuild = Firsttab = ""
    count = 0
    Query = SqlHelper.GetList("SELECT Top 1000 TAB_LABEL FROM SYTABS  WHERE APP_ID = 'QT' ORDER BY DISPLAY_ORDER")
    tagbuild = '<ul id="carttabs_head" class="nav-tabs" >'
    for label in Query:
        if count == 0:
            Firsttab = label.TAB_LABEL.replace(" ", "")
        count += 1
        Trace.Write(label.TAB_LABEL)
        tagbuild += '<li id="'+label.TAB_LABEL.replace(" ", "")+'" href="#" class="Quotes" onclick="navigatequotelist(this)"><a href="#" ><span >'+label.TAB_LABEL+'</span></a></li>'
    tagbuild += '</ul>'
    Trace.Write(tagbuild)
    Trace.Write(Firsttab)
    Trace.Write("sales_current_tab"+str(sales_current_tab))
    return tagbuild,Firsttab

try:
    sales_current_tab= Param.sales_current_tab
except:
    sales_current_tab = ""
    
ApiResponse = ApiResponseFactory.JsonResponse(phphighlight())