# =========================================================================================================================================
#   __script_name : ACCRTABAQU.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY THE ALL THE TAB NAMES IN THE CART PAGE
#   __primary_author__ : VIJAYAKUMAR THANGARASU
#   __create_date :14-02-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import re
import datetime
import math
import ACVIORULES
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()
violationruleInsert = ACVIORULES.ViolationConditions()

# A043S001P01-8665 Start


class ProductDetailLoading:
    def __init__(self, CurrentRecordId=None):
        self.CurrentRecordId = CurrentRecordId

    def GetProductDetails(self, RecordId, WhereCondition, Current_type, PerPage, startPage, endPage):
        if str(PerPage) == "":
            PerPage = 24
        else:
            PerPage = int(PerPage)
        totalCount = 1
        if str(startPage) == "":
            startCount = 1
            endCount = int(PerPage)
        else:
            endCount = int(PerPage) * int(startPage)
            startCount = int(endCount) - int(int(PerPage) - 1)
        Quote = ""
        QuoteNumber = ""
        # A043S001P01-11259 start
        GetProdsCount = ""
        GetProdsDetails = ""
        # A043S001P01-11259 end
        TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
        Product_Name = TestProduct.Name
        TabName = str(TestProduct.CurrentTab)
        if TabName == "Category":
            Object = "CACTPR"
            RecAtt = Product.Attributes.GetByName(str("QSTN_SYSEFL_CA_05421"))
        else:
            Object = "CASPCC"
            RecAtt = Product.Attributes.GetByName(str("QSTN_SYSEFL_CA_00522"))
        if RecAtt is not None:
            RecAttValue = RecAtt.GetValue()
        # A043S001P01-11259 start
        if RecAtt is not None:
            if Current_type == "Parent":
                if Object == "CASPCC":
                    GetProdsDetails = Sql.GetList(
                        """SELECT TOP {PerPage} m.*
                            FROM (
                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY c.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                FROM CASPCC(NOLOCK) a
                                INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                    AND b.PAR_CATEGORY_ID LIKE '{RecordId}%'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                GROUP BY c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC

                                UNION

                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY c.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                FROM CASPCC(NOLOCK) a
                                INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                    AND b.CATEGORY_ID = '{RecordId}'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                GROUP BY c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                ) m
                            WHERE m.ROW BETWEEN {startCount}
                                    AND {endCount}""".format(
                            PerPage=PerPage,
                            RecAttValue=RecAttValue,
                            RecordId=RecordId,
                            startCount=startCount,
                            endCount=endCount,
                        )
                    )
                    GetProdsCount = Sql.GetFirst(
                        """SELECT DISTINCT count(c.MATERIAL_RECORD_ID) AS cnt
                                FROM CASPCC(NOLOCK) a
                                INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                    AND b.PAR_CATEGORY_ID LIKE '{RecordId}%'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                """.format(
                            RecAttValue=RecAttValue, RecordId=RecordId
                        )
                    )

                elif Object == "CACTPR":
                    GetProdsDetails = Sql.GetList(
                        """SELECT TOP {PerPage} m.*
                            FROM (
                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY c.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,d.LNGMAT_SHORTDESC
                                    ,a.CATEGORY_RECORD_ID
                                FROM CACTPR(NOLOCK) a
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATEGORY_RECORD_ID = '{RecAttValue}'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                GROUP BY c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,d.LNGMAT_SHORTDESC
                                    ,a.CATEGORY_RECORD_ID
                                ) m
                            WHERE m.ROW BETWEEN {startCount}
                                    AND {endCount}
                            """.format(
                            PerPage=PerPage, RecAttValue=RecAttValue, startCount=startCount, endCount=endCount
                        )
                    )
                    GetProdsCount = Sql.GetFirst(
                        """SELECT DISTINCT count(c.MATERIAL_RECORD_ID) AS cnt
                            FROM CACTPR(NOLOCK) a
                            INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                            INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                            WHERE a.CATEGORY_RECORD_ID = '{RecAttValue}'
                                AND c.IMAGE_SIZE = '1200Wx1200H'
                                AND c.Rank = '1'
                                AND d.LANGUAGENAME = 'English (US)'
                            """.format(
                            RecAttValue=RecAttValue
                        )
                    )
            elif Current_type == "AllProduct":
                if Object == "CASPCC":
                    GetProdsDetails = Sql.GetList(
                        """SELECT TOP {PerPage} m.*
                            FROM (
                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY c.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                FROM CASPCC(NOLOCK) a
                                INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                GROUP BY c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                ) m
                            WHERE m.ROW BETWEEN {startCount}
                                    AND {endCount}
                            """.format(
                            PerPage=PerPage, RecAttValue=RecAttValue, startCount=startCount, endCount=endCount
                        )
                    )
                    GetProdsCount = Sql.GetFirst(
                        """SELECT DISTINCT count(c.MATERIAL_RECORD_ID) AS cnt
                            FROM CASPCC(NOLOCK) a
                            INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                            INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                            INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                            WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                AND c.IMAGE_SIZE = '1200Wx1200H'
                                AND c.Rank = '1'
                                AND d.LANGUAGENAME = 'English (US)'
                            """.format(
                            RecAttValue=RecAttValue
                        )
                    )

                elif Object == "CACTPR":
                    GetProdsDetails = Sql.GetList(
                        """SELECT TOP {PerPage} m.*
                            FROM (
                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY c.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,d.LNGMAT_SHORTDESC
                                    ,a.CATEGORY_RECORD_ID
                                FROM CACTPR(NOLOCK) a
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATEGORY_RECORD_ID = '{RecAttValue}'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                GROUP BY c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,d.LNGMAT_SHORTDESC
                                    ,a.CATEGORY_RECORD_ID
                                ) m
                            WHERE m.ROW BETWEEN {startCount}
                                    AND {endCount}
                            """.format(
                            PerPage=PerPage, RecAttValue=RecAttValue, startCount=startCount, endCount=endCount
                        )
                    )
                    GetProdsCount = Sql.GetFirst(
                        """SELECT DISTINCT count(c.MATERIAL_RECORD_ID) AS cnt
                            FROM CACTPR(NOLOCK) a
                            INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                            INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                            WHERE a.CATEGORY_RECORD_ID = '{RecAttValue}'
                                AND c.IMAGE_SIZE = '1200Wx1200H'
                                AND c.Rank = '1'
                                AND d.LANGUAGENAME = 'English (US)'
                            """.format(
                            RecAttValue=RecAttValue
                        )
                    )
            else:
                if Object == "CASPCC":
                    GetProdsDetails = Sql.GetList(
                        """SELECT TOP {PerPage} m.*
                            FROM (
                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY c.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                FROM CASPCC(NOLOCK) a
                                INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                                WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                    AND b.CATEGORY_RECORD_ID = '{RecordId}'
                                    AND c.IMAGE_SIZE = '1200Wx1200H'
                                    AND c.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)'
                                GROUP BY c.MATERIAL_RECORD_ID
                                    ,c.IMAGE_URL
                                    ,c.MATERIAL_IMAGE_RECORD_ID
                                    ,c.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,a.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                ) m
                            WHERE m.ROW BETWEEN {startCount}
                                    AND {endCount}
                            """.format(
                            PerPage=PerPage,
                            RecAttValue=RecAttValue,
                            RecordId=RecordId,
                            startCount=startCount,
                            endCount=endCount,
                        )
                    )
                    GetProdsCount = Sql.GetFirst(
                        """SELECT DISTINCT count(c.MATERIAL_RECORD_ID) AS cnt
                            FROM CASPCC(NOLOCK) a
                            INNER JOIN CACTPR(NOLOCK) b ON a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                            INNER JOIN CAMAIM(NOLOCK) c ON a.SAP_PART_NUMBER = c.SAP_PART_NUMBER
                            INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                            WHERE a.CATALOG_RECORD_ID = '{RecAttValue}'
                                AND b.CATEGORY_RECORD_ID = '{RecordId}'
                                AND c.IMAGE_SIZE = '1200Wx1200H'
                                AND c.Rank = '1'
                                AND d.LANGUAGENAME = 'English (US)'
                            """.format(
                            RecAttValue=RecAttValue, RecordId=RecordId
                        )
                    )
                else:
                    GetProdsDetails = Sql.GetList(
                        """SELECT TOP {PerPage} m.*
                            FROM (
                                SELECT DISTINCT ROW_NUMBER() OVER (
                                        ORDER BY a.MATERIAL_RECORD_ID
                                        ) AS ROW
                                    ,a.MATERIAL_RECORD_ID
                                    ,a.IMAGE_URL
                                    ,a.MATERIAL_IMAGE_RECORD_ID
                                    ,a.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,c.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                FROM CAMAIM(NOLOCK) a
                                INNER JOIN CACTPR(NOLOCK) b ON a.SAP_PART_NUMBER = b.SAP_PART_NUMBER
                                    AND a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN {Object}(NOLOCK) c ON c.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                                INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = a.MATERIAL_RECORD_ID {WhereCondition}
                                    AND b.CATEGORY_RECORD_ID = '{RecordId}'
                                    AND a.IMAGE_SIZE = '1200Wx1200H'
                                    AND a.Rank = '1'
                                    AND d.LANGUAGENAME = 'English (US)' {Quote}
                                GROUP BY a.MATERIAL_RECORD_ID
                                    ,a.IMAGE_URL
                                    ,a.MATERIAL_IMAGE_RECORD_ID
                                    ,a.SAP_DESCRIPTION
                                    ,b.CATEGORY_RECORD_ID
                                    ,c.CATCLC_PRICE_INPTS
                                    ,d.LNGMAT_SHORTDESC
                                ) m
                            WHERE m.ROW BETWEEN {startCount}
                                    AND {endCount}
                            """.format(
                            PerPage=PerPage,
                            Object=Object,
                            WhereCondition=WhereCondition,
                            RecordId=RecordId,
                            Quote=Quote,
                            startCount=startCount,
                            endCount=endCount,
                        )
                    )
                    GetProdsCount = Sql.GetFirst(
                        """SELECT DISTINCT count(a.MATERIAL_RECORD_ID) AS cnt
                            FROM CAMAIM(NOLOCK) a
                            INNER JOIN CACTPR(NOLOCK) b ON a.SAP_PART_NUMBER = b.SAP_PART_NUMBER
                                AND a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                            INNER JOIN {Object}(NOLOCK) c ON c.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                            INNER JOIN MALGMA(NOLOCK) d ON d.MATERIAL_RECORD_ID = a.MATERIAL_RECORD_ID {WhereCondition}
                                AND b.CATEGORY_RECORD_ID = '{RecordId}'
                                AND a.IMAGE_SIZE = '1200Wx1200H'
                                AND a.Rank = '1'
                                AND d.LANGUAGENAME = 'English (US)' {Quote}
                            """.format(
                            Quote=Quote, RecordId=RecordId, WhereCondition=WhereCondition, Object=Object
                        )
                    )
        # A043S001P01-11259 end
        if GetProdsCount is not None and len(GetProdsCount) > 0:
            totalCount = int(GetProdsCount.cnt)
            pageCount = int(totalCount) / int(PerPage)
            if int(pageCount) <= 0:
                pageCount = 1
        else:
            pageCount = 1
        produ_str = """<div class="row prdsecli"><div class="col-md-7 flt_rt"  >
        <div class="col-md-6 sortingsec"><select class="form-control " >
        <option>Relevance</option><option>Price High-to-Low</option>
        <option selected>Price Low-to-High</option><option>Name A-to-Z</option>
        <option>Name Z-to-A</option></select></div><div class="col-md-6 sortingbtn">
        <select id="test" class="form-control"><option value="1">All Awards</option>
        <option value="2">Awards in my range</option></select></div></div>
        </div><div class="row clear-padding	clearfix product-details-main-container">"""
        if GetProdsDetails is not None:
            for GetProduct in GetProdsDetails:
                if GetProduct.LNGMAT_SHORTDESC != "":
                    Desc = GetProduct.LNGMAT_SHORTDESC.encode("ASCII", "ignore")
                else:
                    Desc = GetProduct.SAP_DESCRIPTION
                produ_str += """<div class="product-detail-view col-xl-4 col-lg-4 col-md-4 col-sm-4 col-xs-12">
                    <div class="product-box" > <div class="clearfix"></div>
                    <div class="mtrlimg-recordId" style="display: none;">
                    {MATERIAL_IMAGE_RECORD_ID}</div><img onclick = "ProductDetailview(this)"
                    src = "{IMAGE_URL}" class ="ImagePopView" title="{Desc}"></img>
                    <div id = "product_desc">{Desc}</div><div class="clearfix"></div>
                    <div id = "materialid" style = "display:none;">{MATERIAL_RECORD_ID}</div>
                    <div id = "Categoryid" style = "display:none;">{CATEGORY_RECORD_ID}</div>""".format(
                    MATERIAL_IMAGE_RECORD_ID=str(GetProduct.MATERIAL_IMAGE_RECORD_ID),
                    IMAGE_URL=str(GetProduct.IMAGE_URL),
                    Desc=Desc,
                    MATERIAL_RECORD_ID=str(GetProduct.MATERIAL_RECORD_ID),
                    CATEGORY_RECORD_ID=str(GetProduct.CATEGORY_RECORD_ID),
                )
                if Object != "CACTPR":
                    produ_str += """<div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-xs-12 p-0 cust_points">
                    {CATCLC_PRICE_INPTS}Points</div><div class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-xs-12 p-0 cust_fav">
                    <i class="fa fa-heart" aria-hidden="true"></i></div>""".format(
                        CATCLC_PRICE_INPTS=str(GetProduct.CATCLC_PRICE_INPTS)
                    )
                produ_str += "</div></div>"
        produ_str += '</div><div id="paginationdetails" class="row previeroecont previesec"></div>'
        pagination_str = """<div class="col-md-6"></div>
            <div class="col-md-6">
                <div class="col-md-6 pagesize">
                    <select name="pageSize" id="productperpage" onchange="productcountchange()"
                            class="pagination-dropdown form-control">
                        <option value="24">View 24 per page</option>
                        <option value="48">View 48 per page</option>
                        <option value="72">View 72 per page</option>
                        <option value="96">View 96 per page</option>
                    </select>
                </div>
                <p id="pagination-here"></p>
            </div>"""
        pagination_ui = (
            " perpage = $('#productperpage').val(); if(perpage == '' || perpage == null){perpage = 24};"
            + "$('#productperpage').val(perpage); currentpage = ''; $('#pagination-here').bootpag({total: "
            + str(pageCount)
            + ", maxVisible: 4 }).on('page', function(event, num){console.log(num);EndPage = parseInt(perpage)*num;"
            + " cpq.server.executeScript(\"ACCRTABAQU\", {'Action': 'PoductDetails','RecoedId': CurrentRecordId,"
            + "'wherecondition': wherecondition,'Current_type': Current_type,'PerPage':perpage,'startPage':num,"
            + "'endPage':'' }, function (dataset) {ProducDetails = dataset[0]; PaginationDetail = dataset[1]; "
            + " PaginationUI = dataset[2]; if (document.getElementById('Right_div_CTR_Countries')) { "
            + " document.getElementById('Right_div_CTR_Countries').innerHTML = ProducDetails; "
            + " document.getElementById('paginationdetails').innerHTML = PaginationDetail; "
            + " eval(PaginationUI); currentpage = num; console.log('num---> ',num);"
            + " } "
            + " if(currentpage ==''){currentpage = 1};$('#pagination-here').bootpag({total: "
            + str(pageCount)
            + ",page:currentpage, maxVisible: 4 }); });});"
        )

        return produ_str, pagination_str, pagination_ui

    def ProductDetailView(self, MaterilId):
        Object = "CASPCC"
        GetDetail = Sql.GetFirst(
            """select a.SAP_PART_NUMBER,b.LNGMAT_SHORTDESC,
                a.IMAGE_URL,a.SAP_DESCRIPTION,b.LNGMAT_LONGDESC,c.CATCLC_PRICE_INPTS
                from CAMAIM (nolock) a
                inner join MALGMA (nolock) b on
                a.MATERIAL_RECORD_ID = b.MATERIAL_RECORD_ID
                and a.SAP_PART_NUMBER = b.SAP_PART_NUMBER
                inner join CASPCC (nolock) c on a.MATERIAL_RECORD_ID = c.MATERIAL_RECORD_ID
                where a.MATERIAL_RECORD_ID = '{MaterilId}'
                and LANGUAGE_ID = 'en_US' AND a.IMAGE_SIZE = '1200Wx1200H' """.format(
                MaterilId=MaterilId
            )
        )
        desc = ""
        if GetDetail is not None:
            Point = ""
            if str(GetDetail.CATCLC_PRICE_INPTS) != "":
                Point = "{:20,}".format(GetDetail.CATCLC_PRICE_INPTS)
            short_desc = GetDetail.LNGMAT_SHORTDESC.encode("ASCII", "ignore")
            long_desc = GetDetail.LNGMAT_LONGDESC.encode("ASCII", "ignore")
            desc = """<div class="col-md-6 prdimgsec"  ><img   src="{IMAGE_URL}" class="ImagePopView"></div>
                <div class="col-md-6 cust_prodetails_right"> "<div class="row"> <h3 class="mrg_top10">{short_desc}</h3>
                <h4>{CATCLC_PRICE_INPTS}Points</h4> <h5>In Stock</h5> <div class="row prbtn">
                <button class="btnconfig cust_add_cart"><i class="fa fa-shopping-cart" aria-hidden="true"></i>
                ADD TO CART</button> <button class="btnconfig  cust_wish_list"><i class="fa fa-heart" aria-hidden="true">
                </i> SAVE TO WISHLIST</button> </div> <hr/> <h4 class="cust_pro_des_head">Product Description</h4>
                <p class="cust_pro_des_para">{long_desc}<h4 class="cust_pro_code_head">Product Code:</h4> </p>
                <p class="cust_pro_code">{SAP_PART_NUMBER}</p> </div> </div>""".format(
                IMAGE_URL=str(GetDetail.IMAGE_URL),
                short_desc=short_desc,
                CATCLC_PRICE_INPTS=str(GetDetail.CATCLC_PRICE_INPTS),
                long_desc=long_desc,
                SAP_PART_NUMBER=str(GetDetail.SAP_PART_NUMBER),
            )
        return desc


# A043S001P01-8665 End
class QueryBuilder:
    def __init__(self, CurrentRecordId=None):
        self.CurrentRecordId = CurrentRecordId

    def ConstructQueryBuilder(self, OnEdit):
        
        if str(OnEdit) == "OnEdit":
            DefaultData = self.check_previous_data()
            if DefaultData is None or str(DefaultData) == "":
                return ["TRUE", self.build_default()]
            else:
                return list(self.build_dynamic_data_to_qb(OnEdit))
        else:
            return list(self.build_dynamic_data_to_qb(OnEdit))
        return True

    def check_previous_data(self):
        checkPreviousData = None
        checkPreviousDataQuery = Sql.GetFirst(
            "select CRITERIA_01, CRITERIA_02, CRITERIA_03, CRITERIA_04, CRITERIA_05 from ACACST (NOLOCK) where "
            + " APPROVAL_CHAIN_STEP_RECORD_ID = '{}' ".format(self.CurrentRecordId)
        )
        if checkPreviousDataQuery:
            checkPreviousData = (
                str(checkPreviousDataQuery.CRITERIA_01)
                + str(checkPreviousDataQuery.CRITERIA_02)
                + str(checkPreviousDataQuery.CRITERIA_03)
                + str(checkPreviousDataQuery.CRITERIA_04)
                + str(checkPreviousDataQuery.CRITERIA_05)
            )
        return checkPreviousData

    def build_default(self):
        productDefaultData = ""
        return productDefaultData

    def build_dynamic_data_to_qb(self, EditEvent):
        # global avaialable_for_use_found
        filters = []
        defaultData = None
        fromProduct = False
        TableObjQuery = Sql.GetFirst(
            "select SYOBJH.RECORD_ID, SYOBJH.PLURAL_LABEL, SYOBJH.OBJECT_NAME from SYOBJH (nolock) "
            + " inner join ACACST (nolock) on ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID where "
            + " ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = '{}' ".format(self.CurrentRecordId)
        )
        table_dict = {str(TableObjQuery.OBJECT_NAME): str(TableObjQuery.PLURAL_LABEL).upper()}
        table_list = [str(TableObjQuery.OBJECT_NAME)]
        if len(table_list) > 0:
            for table_name in table_list:
                global count
                count = 0
                filters.append(
                    {"id": table_name, "label": table_dict.get(table_name), "children": self.build_data(table_name)}
                )
        productDefaultData = ""
        getPreviousData = None
        DefaultData = self.check_previous_data()
        if DefaultData is not None and str(DefaultData) != "":
            defaultData = self.check_previous_data()
            segment_response = RestClient.DeserializeJson(str(defaultData))
            if EditEvent == "":
                segment_response["flags"] = RestClient.DeserializeJson(
                    '{"condition_readonly": false}'
                )
                # segment_response["flags"] = RestClient.DeserializeJson(str(AddGroupRule))
                segment_response = self.build_non_editable_json_response("VIEW", segment_response)
            else:
                segment_response["flags"] = RestClient.DeserializeJson(
                    '{"no_add_rule": false,"no_add_group": false,"no_delete": true}'
                )
                # segment_response["flags"]["no_add_group"] = RestClient.DeserializeJson(str(AddGroupRule))
                segment_response = self.build_non_editable_json_response("EDIT", segment_response)
            defaultData = RestClient.SerializeToJson(segment_response)
            if not defaultData:
                defaultData = self.build_default()
        now = datetime.datetime.now()
        return filters, defaultData, fromProduct

    def build_non_editable_json_response(self, MODE, api_response):
        rule_count = api_response["rules"].Count
        for index in range(rule_count):
            try:
                if api_response["rules"][index]["rules"]:
                    api_response["rules"][index]["flags"] = RestClient.DeserializeJson(
                        '{"condition_readonly": false}'
                    )
                    self.build_non_editable_json_response(MODE, api_response["rules"][index])
                    continue
            except Exception, e:
                pass
            try:
                if not api_response["rules"][index]["values"]["flags"] and MODE == "EDIT":
                    api_response["rules"][index]["values"]["flags"] = RestClient.DeserializeJson(
                        '{"filter_readonly":false,"operator_readonly":false,"value_readonly":false,'
                        + ' "no_delete":false,"active_readonly": true}'
                    )
                elif MODE == "VIEW":
                    api_response["rules"][index]["values"]["flags"] = RestClient.DeserializeJson(
                        '{"filter_readonly":true,"operator_readonly":true,"value_readonly":true,'
                        + '"no_delete":true,"active_readonly": true}'
                    )
            except Exception, e:
                api_response["rules"][index]["values"]["flags"] = RestClient.DeserializeJson(
                    '{"filter_readonly":true,"operator_readonly":true,"value_readonly":true,'
                    + '"no_delete":true,"active_readonly": true}'
                )
        return api_response

    def build_data(self, table_name):
        children = []
        if count < 1:
            where_price_material = ""
            if table_name == "PRPBMA":
                where_price_material = " AND API_NAME IN ('AVAILABLE_FORUSE', 'PROCEDURE_ID', 'PRICEMODEL_ID', "
                +" 'PRICE_METHOD_NAME', 'PRICECLASS_TYPE', 'PRODUCT_TYPE')"

            table_details_obj = Sql.GetList(
                """ SELECT TOP(1000) API_NAME,LOOKUP_OBJECT,FIELD_LABEL,DATA_TYPE
                    FROM SYOBJD (NOLOCK)
                    WHERE OBJECT_NAME = '{table_name}'                    
                    {where_price_material}
                    ORDER BY FIELD_LABEL
                """.format(
                    table_name=table_name, where_price_material=where_price_material
                )
            )
            if table_details_obj is not None:
                lookup_details = {}
                formula_columns = {}
                for table_detail in table_details_obj:
                    if table_detail.DATA_TYPE == "LOOKUP":
                        if table_detail.LOOKUP_OBJECT:
                            lookup_details[table_detail.API_NAME] = {
                                "table": table_detail.LOOKUP_OBJECT,
                                "label": table_detail.FIELD_LABEL,
                            }
                    else:
                        children.append(
                            {
                                "id": table_name + "." + table_detail.API_NAME,
                                "label": table_detail.FIELD_LABEL,
                                "children": "null",
                                "custom_values": ["Constant", "Values"],
                                "values": [
                                    self.get_rule_values(
                                        table_name, table_detail.API_NAME, table_detail.FIELD_LABEL, table_detail.DATA_TYPE,
                                    )
                                ],
                                "right_custom_filter": "null",
                            }
                        )
                        DropVal = """function(rule, name) {
                            var $container = rule.$el.find('.rule-value-container');
                            $container.on('change', '[name='+ name +'_1]', function(){
                                var h = '';
                                switch ($(this).val()) {                                
                                case 'Constant':
                                    h = '<input type="text" id="dunamicval" name="'+ name +'_2">';
                                    break;
                                case 'Values':
                                    h = '<select name="'+name+'_2" style=""><option value="-1">-</option> <option value="1">1</option> <option value="2">2</option></select>';
                                    break;
                                }
                                $container.find('[name$=noclassdiv]')
                                .html(h).toggle(!!h)
                                .val('-1').trigger('change');
                            });
                                return '\
                            <select name="'+ name +'_1" > \
                                <option value="-1">-</option> \
                                <option value="Constant">Constant</option> \
                                <option value="Values">Values</option> \
                            </select> <span class="noclass" name="noclassdiv" ></span>\
                            '; 
                            }"""
                        # children.append(
                        #     {
                        #         "id": table_name + "." + table_detail.API_NAME,
                        #         "label": table_detail.FIELD_LABEL,
                        #         "children": "null",
                        #         "type": "string",
                        #         "input": DropVal,
                        #         "valueGetter": "function(rule) { return rule.$el.find('.rule-value-container [name$=_2]').val() }",
                        #         "valueSetter": "function(rule, value) { if (rule.operator.nb_inputs > 0) { var val = value.split('.'); rule.$el.find('.rule-value-container [name$=_1]').val(val[0]).trigger('change'); rule.$el.find('.rule-value-container [name$=_2]').val(val[1]).trigger('change'); } }",
                        #     }
                        # )

                if lookup_details:
                    global count
                    count += 1
                    for key, value in lookup_details.items():
                        if count == 1:
                            children.append(
                                {
                                    "id": value.get("table") + "." + key,
                                    "label": value.get("label"),
                                    "children": "null",
                                    "custom_values": ["Constant", "Values"],
                                    "values": [
                                        {
                                            "id": value.get("table") + "." + key,
                                            "label": value.get("label"),
                                            "type": "string",
                                        }
                                    ],
                                    "right_custom_filter": "null",
                                }
                            )
                        else:
                            children.append(
                                {
                                    "id": table_name + "." + key,
                                    "label": value.get("label"),
                                    "children": self.build_data(value.get("table")),
                                }
                            )
            return children
        return "null"

    def get_rule_values(self, table_name, api_name, rule_label, data_type):
        rule = {"id": table_name + "." + api_name, "label": rule_label}
        if data_type == "CHECKBOX":
            rule.update(
                {
                    "type": "integer",
                    "input": "select",
                    "values": {"1": "True", "0": "False"},
                    "operators": ["equal", "not_equal", "is_null", "is_not_null"],
                }
            )
        elif data_type == "FORMULA":
            if table_name == "PRPBMA" and api_name == "SAP_PART_NUMBER":
                rule["type"] = "string"
            else:
                rule.update(self.build_dynamic_selection_data_to_qb(table_name, api_name))
        elif data_type == "TEXT" and api_name == "SAP_PART_NUMBER":
            rule.update(self.build_dynamic_selection_data_to_qb(table_name, api_name))
        elif data_type == "PICKLIST":
            values_dict = {}
            result_obj = Sql.GetFirst(
                "SELECT PICKLIST_VALUES	FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME = '{table_name}' AND API_NAME = '{api_name}' AND DATA_TYPE = 'PICKLIST' ".format(
                    table_name=table_name, api_name=api_name
                )
            )
            if result_obj is not None:
                if result_obj.PICKLIST_VALUES:
                    for index, val in enumerate(result_obj.PICKLIST_VALUES.split(",")):
                        try:
                            values_dict[str(val)] = val
                        except Exception, e:
                            values_dict[val] = val
            result = {
                "type": "string",
                "input": "select",
                "plugin": "selectize",
                "multiple": "true",
                "plugin_config": {"plugins": ["remove_button"], "sortField": [{"field": "text", "direction": "asc"}]},
                "values": values_dict,
            }
            rule.update(result)
        else:
            if table_name in ["PRPRCL", "CACATG", "MAMPFC"] and api_name.endswith("_ID"):
                rule.update(self.build_dynamic_selection_data_to_qb(table_name, api_name))
            else:
                rule["type"] = "string"
        return rule

    def build_dynamic_selection_data_to_qb(self, table, selection_column):
        result = {}
        #Trace.Write("selection_column before -----> " + str(selection_column))
        data = {selection_column: []}
        #Trace.Write("selection_column after -----> " + str(selection_column))
        where_condition_string = ""
        if selection_column.endswith("_ID"):
            get_foreign_key_tbl_obj = Sql.GetFirst(
                "SELECT	LOOKUP_OBJECT FROM	SYOBJD (NOLOCK) WHERE LOOKUP_API_NAME = '{selection_column}' AND LOOKUP_OBJECT <> '{table}' AND OBJECT_NAME = '{table}' ".format(
                    selection_column=selection_column, table=table
                )
            )
            if get_foreign_key_tbl_obj is not None or selection_column == "SUPERCLASS_ID":
                if get_foreign_key_tbl_obj is not None:
                    foreign_key_tbl = get_foreign_key_tbl_obj.LOOKUP_OBJECT
                else:
                    foreign_key_tbl = "PRPRCL"

                if foreign_key_tbl == "SAACNT":
                    foreign_key_tbl_column = "ACCOUNT_ID"
                    foreign_key_tbl_name_column = foreign_key_tbl_column[:-2] + "NAME"
                elif foreign_key_tbl == "MAMTST":
                    foreign_key_tbl_column = selection_column
                    foreign_key_tbl_name_column = "DESCRIPTION"
                elif foreign_key_tbl == "PRPRCL":
                    foreign_key_tbl_column = selection_column
                    foreign_key_tbl_name_column = "NAME"
                else:
                    foreign_key_tbl_column = selection_column
                    foreign_key_tbl_name_column = foreign_key_tbl_column[:-2] + "NAME"

                get_concatenate_val = "{}.{}+'-'+{}.{}".format(
                    foreign_key_tbl, foreign_key_tbl_column, foreign_key_tbl, foreign_key_tbl_name_column
                )

                try:
                    remove_empty_records_where = "ISNULL({}.{},'') <> '' AND  ISNULL({}.{},'') <> '' ".format(
                        foreign_key_tbl, foreign_key_tbl_column, foreign_key_tbl, foreign_key_tbl_name_column
                    )
                    if where_condition_string:
                        where_condition_string += " AND " + remove_empty_records_where
                    else:
                        where_condition_string += " WHERE " + remove_empty_records_where
                    result_obj = Sql.GetList(
                        "SELECT DISTINCT {} as {} FROM {} (NOLOCK) INNER JOIN {} ON	{}.{} = {}.{} {} ".format(
                            get_concatenate_val,
                            selection_column,
                            table,
                            foreign_key_tbl,
                            foreign_key_tbl,
                            foreign_key_tbl_column,
                            table,
                            selection_column,
                            where_condition_string,
                        )
                    )
                except Exception, e:
                    result_obj = Sql.GetList(
                        "SELECT DISTINCT {0} FROM {1} (NOLOCK) {2} ".format(selection_column, table, where_condition_string)
                    )
            else:
                try:
                    # if str(selection_column[:-2]) == "ACCTAXCLA_" or str(selection_column[:-2]) == "ACCTAXCAT_":
                    #     remove_empty_records_where = "ISNULL({},'') <> '' AND  ISNULL({},'') <> '' ".format(
                    #         selection_column, "DESCRIPTION" if selection_column == "PRICECLASS_ID" else selection_column[:-2] + "DESCRIPTION"
                    #     )
                    # else:
                    if selection_column == "DOCTYP_ID":
                        remove_empty_records_where = "ISNULL({},'') <> ''".format(
                            selection_column
                        )
                    else:
                        remove_empty_records_where = "ISNULL({},'') <> '' AND  ISNULL({},'') <> '' ".format(
                            selection_column, "NAME" if selection_column == "PRICECLASS_ID" else selection_column[:-2] + "NAME"
                        )
                    if where_condition_string:
                        where_condition_string += " AND " + remove_empty_records_where
                    else:
                        where_condition_string += " WHERE " + remove_empty_records_where
                    Trace.Write("CHK_J "+str(selection_column)+" - "+str(selection_column[:-2])+ " - "+str(table)+ " - "+str(where_condition_string))
                    # if str(selection_column[:-2]) == "ACCTAXCLA_" or str(selection_column[:-2]) == "ACCTAXCAT_":
                    #     result_obj = Sql.GetList(
                    #         "SELECT DISTINCT {0}+'-'+{1} AS {2}	FROM {3} (NOLOCK) {4} ".format(
                    #             selection_column,
                    #             "DESCRIPTION" if selection_column == "DESCRIPTION" else selection_column[:-2] + "DESCRIPTION",
                    #             selection_column,
                    #             table,
                    #             where_condition_string,
                    #         )
                    #     )
                    # else:
                    Trace.Write("selection_column_J "+str(selection_column)+" - "+str(table))
                    if selection_column == "DOCTYP_ID":
                        result_obj = Sql.GetList(
                            "SELECT DISTINCT {0} FROM {1} (NOLOCK) {2} ".format(
                                selection_column,
                                table,
                                where_condition_string,
                            )
                        )
                    else:
                        result_obj = Sql.GetList(
                            "SELECT DISTINCT {0}+'-'+{1} AS {2}	FROM {3} (NOLOCK) {4} ".format(
                                selection_column,
                                "NAME" if selection_column == "PRICECLASS_ID" else selection_column[:-2] + "NAME",
                                selection_column,
                                table,
                                where_condition_string,
                            )
                        )
                except Exception, e:
                    result_obj = Sql.GetList(
                        "SELECT DISTINCT {0} FROM {1} (NOLOCK) {2} ".format(selection_column, table, where_condition_string)
                    )
        else:
            Trace.Write("where_condition_string_J "+str(where_condition_string))
            result_obj = Sql.GetList(
                "SELECT DISTINCT {Columns} FROM {TableName} (NOLOCK) WHERE ISNULL({Columns},'')<>''".format(Columns=selection_column, TableName=table)
            )
        if result_obj is not None:
            for data_obj in result_obj:
                for obj in data_obj:
                
                    if obj.Value and obj.Value != "-":
                        if obj.Key in data:
                            data[obj.Key].append(obj.Value)
                        else:
                            data[obj.Key] = [obj.Value]
                            
                        # data[obj.Key] = obj.Value
                    

        for key, value in data.items():
            values_dict = {}
            for index, val in enumerate(value):
                try:
                    if key.endswith("_ID"):
                        values_dict[str(val.split("-")[0])] = val
                    else:
                        if selection_column == "PRODUCT_TYPE" and table == "PRPBMA":
                            modified_val = str(val).replace(" ", "_")
                            values_dict[modified_val] = val
                        else:
                            values_dict[str(val)] = val
                except Exception, e:
                    if selection_column == "PRODUCT_TYPE" and table == "PRPBMA":
                        modified_val = str(val).replace(" ", "_")
                        values_dict[modified_val] = val
                    else:
                        values_dict[val] = val
            if key == "MATERIALSTATUS_ID":
                for k, v in values_dict.items():
                    if k not in ["AC", "DI", "UO"]:
                        del values_dict[k]
            result = {
                "type": "string",
                "input": "select",
                "plugin": "selectize",
                "multiple": "true",
                "plugin_config": {"plugins": ["remove_button"], "sortField": [{"field": "text", "direction": "asc"}]},
                "values": values_dict,
            }
        return result

    def SaveQueryBuilder(self, QbJsonData, QbWhereCondition, QbCallFromPricing):
        CpqIdQuery = Sql.GetFirst(
            "select CpqTableEntryId,APRCHN_ID,APRCHN_RECORD_ID,APRCHNSTP_NAME,APRCHNSTP_NUMBER from ACACST (nolock) where APPROVAL_CHAIN_STEP_RECORD_ID = '"
            + str(self.CurrentRecordId)
            + "'"
        )
        tableInfo = Sql.GetTable("ACACST")
        tableInfoACACSF = Sql.GetTable("ACACSF")
        updaterow = {
            "CpqTableEntryId": CpqIdQuery.CpqTableEntryId,
            "CRITERIA_01": QbJsonData,
            "WHERE_CONDITION_01": QbWhereCondition,
        }
        
        Trace.Write(str(updaterow))
        tableInfo.AddRow(updaterow)
        Sql.Upsert(tableInfo)
        QbJsonData = QbJsonData.replace("null","None")
        QbJsonData = QbJsonData.replace("true","True")
        QbJsonData = QbJsonData.replace("false","False") 
        QbJsonData = eval(QbJsonData)
        Trace.Write(str(QbJsonData))
        #Trace.Write("--"+str(QbJsonData['rules'][0]['rules'][0]['values']['id']))
        
        if "(" in QbWhereCondition:
            objName = str(QbJsonData['rules'][0]['rules'][0]['values']['id']).split(".")[0]
            if QbJsonData["condition"] == "OR":
                QbWhereCondition = QbWhereCondition.split("OR")
                l = []
                count = 0
                for x in QbWhereCondition:
                    if x.find("AND") != -1:
                        y = x.split("AND")
                        Trace.Write("y--->"+str(y))
                        for i in y:
                            i=i.strip().strip("(").strip(")")
                            l.append(i.split(objName+"."))
                for x in range(0,len(l)):
                    getFieldLabel = Sql.GetFirst("SELECT FIELD_LABEL,RECORD_ID FROM SYOBJD(NOLOCK) WHERE OBJECT_NAME ='{}' AND API_NAME = '{}'".format(objName.strip(),str(l[x][1]).split(" '")[0].strip("=").strip("<").strip(">").strip("!=").strip("") ))
                    getObjLabel = Sql.GetFirst("SELECT LABEL,RECORD_ID FROM SYOBJH(NOLOCK) WHERE OBJECT_NAME ='{}'".format(objName.strip()))
                    if getFieldLabel and getObjLabel:
                        row={}
                        row = {
                        "APRCHNSTP_TESTEDFIELD_RECORD_ID":str(Guid.NewGuid()).upper(),
                        "APRCHN_ID":CpqIdQuery.APRCHN_ID,
                        "APRCHN_RECORD_ID":CpqIdQuery.APRCHN_RECORD_ID,
                        "APRCHNSTP_NUMBER":CpqIdQuery.APRCHNSTP_NUMBER,
                        "APRCHNSTP_RECORD_ID":self.CurrentRecordId,
                        "TSTOBJ_TESTEDFIELD_LABEL":getFieldLabel.FIELD_LABEL,
                        "TSTOBJ_TESTEDFIELD_RECORD_ID":getFieldLabel.RECORD_ID,
                        "TSTOBJ_LABEL":getObjLabel.LABEL,
                        "TSTOBJ_RECORD_ID":getObjLabel.RECORD_ID
                        }
                        tableInfoACACSF.AddRow(row)
                Sql.Upsert(tableInfoACACSF)
                Trace.Write("L--->"+str(l))
            elif QbJsonData["condition"] == "AND":
                QbWhereCondition = QbWhereCondition.split("AND")
        else:

            Trace.Write("where-"+str(QbWhereCondition))
            if "AND" in QbWhereCondition or "OR" in QbWhereCondition:
                if "AND" in QbWhereCondition:
                    QbWhereCondition =QbWhereCondition.split("AND")
                elif "OR" in QbWhereCondition:
                    QbWhereCondition =QbWhereCondition.split("OR")
                l=[]
                count = 0
                Trace.Write("976-"+str(QbWhereCondition))
                for i in QbWhereCondition:
                    l.append(i.split("."))
                    count += 1
                Trace.Write("LIST---"+str(l))
                Trace.Write("count---"+str(count))
                for x in range(0,count):
                    getFieldLabel = Sql.GetFirst("SELECT FIELD_LABEL,RECORD_ID FROM SYOBJD(NOLOCK) WHERE OBJECT_NAME ='{}' AND API_NAME = '{}'".format(str(l[x][0]).strip(),str(l[x][1]).split("=")[0].strip()))
                    getObjLabel = Sql.GetFirst("SELECT LABEL,RECORD_ID FROM SYOBJH(NOLOCK) WHERE OBJECT_NAME ='{}'".format(str(l[x][0]).strip()))
                    if getFieldLabel and getObjLabel:
                        row={}
                        row = {
                            "APRCHNSTP_TESTEDFIELD_RECORD_ID":str(Guid.NewGuid()).upper(),
                            "APRCHN_ID":CpqIdQuery.APRCHN_ID,
                            "APRCHN_RECORD_ID":CpqIdQuery.APRCHN_RECORD_ID,
                            "APRCHNSTP_NUMBER":CpqIdQuery.APRCHNSTP_NUMBER,
                            "APRCHNSTP_RECORD_ID":self.CurrentRecordId,
                            "TSTOBJ_TESTEDFIELD_LABEL":getFieldLabel.FIELD_LABEL,
                            "TSTOBJ_TESTEDFIELD_RECORD_ID":getFieldLabel.RECORD_ID,
                            "TSTOBJ_LABEL":getObjLabel.LABEL,
                            "TSTOBJ_RECORD_ID":getObjLabel.RECORD_ID
                        }
                        tableInfoACACSF.AddRow(row)
                Sql.Upsert(tableInfoACACSF) 
            else:
                objName = QbWhereCondition.split(".")[0].strip()
                getFieldLabel = Sql.GetFirst("SELECT FIELD_LABEL,RECORD_ID FROM SYOBJD(NOLOCK) WHERE OBJECT_NAME ='{}' AND API_NAME = '{}'".format(objName,QbWhereCondition.split(".")[1].split(" '")[0].strip("=").strip("<").strip(">").strip("!=").strip("")))
                getObjLabel = Sql.GetFirst("SELECT LABEL,RECORD_ID FROM SYOBJH(NOLOCK) WHERE OBJECT_NAME ='{}'".format(objName))
                if getFieldLabel and getObjLabel:
                    row={}
                    row = {
                        "APRCHNSTP_TESTEDFIELD_RECORD_ID":str(Guid.NewGuid()).upper(),
                        "APRCHN_ID":CpqIdQuery.APRCHN_ID,
                        "APRCHN_RECORD_ID":CpqIdQuery.APRCHN_RECORD_ID,
                        "APRCHNSTP_NUMBER":CpqIdQuery.APRCHNSTP_NUMBER,
                        "APRCHNSTP_RECORD_ID":self.CurrentRecordId,
                        "TSTOBJ_TESTEDFIELD_LABEL":getFieldLabel.FIELD_LABEL,
                        "TSTOBJ_TESTEDFIELD_RECORD_ID":getFieldLabel.RECORD_ID,
                        "TSTOBJ_LABEL":getObjLabel.LABEL,
                        "TSTOBJ_RECORD_ID":getObjLabel.RECORD_ID
                    }
                    tableInfoACACSF.AddRow(row)
                    Sql.Upsert(tableInfoACACSF)
        return True


class PriceFactor:
    def __init__(self, CurrentRecordId=None):
        self.CurrentRecordId = CurrentRecordId

    def build_pricebook_table(
        self,
        attribute_name=None,
        attribute_value=None,
        AllParams=None,
        fetch_count=20,
        offset_skip_count=0,
        table_id_from_js="",
    ):
        table_content_json = []
        table_string = ""
        filter_control_function = ""
        filter_drop_down = ""
        main_table_name = ""
        AllParams = eval(AllParams)
        tree_param = AllParams.get("TreeParam")
        tree_parent_level_0 = AllParams.get("TreeParentLevel0")
        tree_parent_level_1 = AllParams.get("TreeParentLevel1")
        tree_parent_level_2 = AllParams.get("TreeParentLevel2")
        Var_obj = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00277").GetValue()
        Query_obj = Sql.GetFirst(
            "Select PRICEAGREEMENT_RECORD_ID,AGMREV_ID from PASGRV (nolock) where PRICEAGREEMENT_REVISION_RECORD_ID = '"
            + str(Var_obj)
            + "' "
        )
        if Query_obj is not None:
            segment_rec_id = str(Query_obj.PRICEAGREEMENT_RECORD_ID)
            revision_id = str(Query_obj.AGMREV_ID)
        where_string = ""

        if "Calculation Factors" in (tree_param, tree_parent_level_0):
            main_table_name = "PASRPB"
            if tree_param.upper() == "FIXED FACTOR" or "ff" in table_id_from_js:
                ordered_keys = ["PRICEAGM_REV_PRICEBOOK_RECORD_ID", "PRICECLASS_ID"]
                table_id = "pricefactor_ff_result_table"
            elif tree_param.upper() == "LOWEST PRICE ADJUSTMENT FACTOR" or "lpaf" in table_id_from_js:
                ordered_keys = ["PRICEAGM_REV_PRICEBOOK_RECORD_ID", "PRICECLASS_ID"]
                table_id = "pricefactor_lpaf_result_table"
            elif tree_param.upper() == "MARKUP FACTOR" or "mf" in table_id_from_js:
                ordered_keys = ["PRICEAGM_REV_PRICEBOOK_RECORD_ID", "PRICECLASS_ID"]
                table_id = "pricefactor_mf_result_table"
            elif tree_param.upper() == "NON MARKET BASED COMMISSION VOLUME FACTOR" or "ncvf" in table_id_from_js:
                ordered_keys = ["PRICEAGM_REV_PRICEBOOK_RECORD_ID", "PRICECLASS_ID"]
                table_id = "pricefactor_ncvf_result_table"
            elif tree_param.upper() == "TRANSFER FACTOR" or "tf" in table_id_from_js:
                ordered_keys = ["PRICEAGM_REV_PRICEBOOK_RECORD_ID", "PRICECLASS_ID"]
                table_id = "pricefactor_tf_result_table"
        else:
            ordered_keys = [
                "LIST_PRICEBOOK_RECORD_ID",
                "LIST_PRICEBOOKSET_ID",
                "LIST_PRICEBOOK_ID",
                "SALESORG_ID",
                "SALESORG_RECORD_ID",
                "CURRENCY",
                "PRICECLASS_RECORD_ID",
                "PRICECLASS_ID",
                "LOCKED",
                "ACTIVE",
            ]
            main_table_name = "PRLPBK"
            table_id = "pricebook_result_table"

        objd_details_obj = Sql.GetList(
            "SELECT API_NAME, FIELD_LABEL FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME = '%s' AND API_NAME IN %s"
            % (main_table_name, tuple(ordered_keys))
        )
        column_details = {}
        if objd_details_obj:
            column_details = {objd_detail_obj.API_NAME: objd_detail_obj.FIELD_LABEL for objd_detail_obj in objd_details_obj}
        columns = ordered_keys
        pagination_total_count = 0
        filter_tags = []
        filter_types = []
        filter_values = []
        multi_select_where = ""
        # Filter based on table textbox column - Start
        if attribute_name and attribute_value:

            attribute_name = [main_table_name + "." + str(attr_name) for attr_name in attribute_name]

            filter_dict = dict(zip(attribute_name, attribute_value))
            if "PRLPBK.LIST_PRICEBOOK_RECORD_ID" in filter_dict.keys():
                if filter_dict.get("PRLPBK.LIST_PRICEBOOK_RECORD_ID"):
                    filter_dict["PRLPBK.LIST_PRICEBOOK_RECORD_ID"] = CPQID.KeyCPQId.GetKEYId(
                        "PRLPBK", str(filter_dict.get("PRLPBK.LIST_PRICEBOOK_RECORD_ID"))
                    )
            if "PASRPB.PRICEAGM_REV_PRICEBOOK_RECORD_ID" in filter_dict.keys():
                if filter_dict.get("PASRPB.PRICEAGM_REV_PRICEBOOK_RECORD_ID"):
                    filter_dict["PASRPB.PRICEAGM_REV_PRICEBOOK_RECORD_ID"] = CPQID.KeyCPQId.GetKEYId(
                        "PASRPB", str(filter_dict.get("PASRPB.PRICEAGM_REV_PRICEBOOK_RECORD_ID"))
                    )
            filter_str = ""
            for key, value in filter_dict.items():
                if str(value).upper() == "TRUE":
                    value = "1"
                elif str(value).upper() == "FALSE":
                    value = "0"

                if value:
                    if filter_str:
                        filter_str += " and "
                    if str(value).find(",") == -1:
                        filter_str += str(key) + " like '%" + str(value) + "%' "
                    else:
                        value = tuple(value.split(","))
                        filter_str += str(key) + " in " + str(value)
            if filter_str:
                where_string += " and {}".format(filter_str)

        values_list = ""
        filter_class = "#Act_{}".format(table_id)
        for index, invs in enumerate(list(columns)):
            filter_clas = "#" + table_id + " .bootstrap-table-filter-control-" + str(invs)
            values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
            values_list += "attributeValueList.push(" + str(invs) + "); "
            enter_event_class_selector = "bootstrap-table-filter-control-" + str(invs)
            var_name = "attr" + str(index)
            filter_control_function += (
                "var "
                + str(var_name)
                + ' = document.getElementsByClassName("'
                + enter_event_class_selector
                + '"); if ('
                + str(var_name)
                + "[0] != undefined) {"
                + str(var_name)
                + '[0].addEventListener("keydown", function (e) {if(e.keyCode === 13) { document.getElementById("'
                + filter_class[1:]
                + '").click();}})};'
            )
        filter_control_function += (
            '$("'
            + filter_class
            + '").click( function(){ var table_id = $(this).closest("table").attr("id"); attributeValueList = []; '
            + str(values_list)
            + " var attribute_value = $(this).val(); AllParams = JSON.stringify(dict); "
            + ' cpq.server.executeScript("ACCRTABAQU", {"AttributeName": '
            + str(list(columns))
            + ', "AttributeValue": attributeValueList,"AllParams":AllParams,"ShowResultCount": parseInt("'
            + str(fetch_count)
            + '"),"RecordEnd": parseInt("'
            + str(1)
            + '"), "TableId":"'
            + str(table_id)
            + '"}, function(dataset) { data = dataset[0]; data1 = dataset[1]; data2 = dataset[2]; data3=dataset[3]; $("#'
            + str(table_id)
            + '").bootstrapTable("load", data1 ); $("#'
            + str(table_id)
            + '").next("div").remove(); $("#'
            + str(table_id)
            + '").after(data3); }); });'
        )
        # Filter based on table textbox column - End

        # Filter based on table MultiSelect Dropdown column - Start
        for index, api_name in enumerate(ordered_keys):

            obj_data = Sql.GetFirst(
                "SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
                + str(main_table_name)
                + "' and API_NAME = '"
                + str(api_name)
                + "'"
            )
            if obj_data is not None:
                if str(obj_data.PICKLIST).upper() == "TRUE":
                    filter_tag = (
                        '<div id = "'
                        + str(table_id)
                        + "_RelatedMutipleCheckBoxDrop_"
                        + str(index)
                        + '" class="form-control bootstrap-table-filter-control-'
                        + str(api_name)
                        + " RelatedMutipleCheckBoxDrop_"
                        + str(index)
                        + ' "></div>'
                    )
                    filter_tags.append(filter_tag)
                    filter_types.append("select")
                    if obj_data.DATA_TYPE == "CHECKBOX":
                        filter_values.append(["True", "False"])
                    else:
                        data_obj = Sql.GetList(
                            "SELECT DISTINCT {Column} FROM {Table} {WhereString}".format(
                                Column=api_name,
                                Table=main_table_name,
                                WhereString=multi_select_where if api_name == "PRICECLASS_ID" else "",
                            )
                        )
                        if data_obj is not None:
                            filter_values.append([row_data.Value for data in data_obj for row_data in data])
                else:
                    filter_tag = (
                        '<input type="text"  class="wth100visble form-control bootstrap-table-filter-control-'
                        + str(api_name)
                        + '">'
                    )
                    filter_tags.append(filter_tag)
                    filter_types.append("input")
                    filter_values.append("")

        filter_drop_down = (
            "try { if( document.getElementById('"
            + str(table_id)
            + "') ) { var listws = document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) "
            + " { if (data7[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data8[j].length>5){ $('#"
            + str(table_id)
            + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter});"
            + " }else{$('#"
            + str(table_id)
            + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter "
            + " ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() "
            + " { var listws = document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) "
            + " { if (data7[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
            + str(table_id)
            + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, "
            + " scrollBarSize :10 }); } } }, 5000); }"
        )

        # Filter based on table MultiSelect Dropdown column - End
        table_string = "<table id=" + str(table_id) + ' class="table table-bordered CTRBTNSTYLE tbl-sd-left-align"'
        table_string += 'data-pagination="false" data-filter-control="true" data-search-on-enter-key="true"'
        table_string += 'data-pagination-loop = "false" data-locale = "en-US"><thead><tr><th data-field="ACTIONS">'
        table_string += '<div class="action_col txt_center"  >ACTIONS</div><button class="searched_button"'
        table_string += 'id="Act_' + str(table_id) + ">Search</button></th>"

        for index, key in enumerate(ordered_keys):
            if index == 0:
                table_string += '<th  data-field="{}" data-filter-control="input" data-title-tooltip="{}" '
                +' data-formatter="SgmtRelatedListHyperLink" data-sortable="true">{}</th>'.format(
                    key, column_details.get(key), column_details.get(key)
                )
            else:
                table_string += '<th data-field="{}" data-filter-control="input" data-sortable="true">'
                +' <abbr title="{}">{}</abbr></th>'.format(key, column_details.get(key), column_details.get(key))
        table_string += """</tr></thead> <tbody onclick="Table_Onclick_Scroll(this)"></tbody>"""

        if main_table_name == "PRLPBK":
            order_by = "LIST_PRICEBOOK_RECORD_ID"
            if tree_parent_level_1 == "Price Model":
                where_string += "AND PASRPB.LIST_PRICEBOOKSET_ID = '{PricebookSetId}'".format(
                    PricebookSetId=tree_parent_level_0
                )
            else:
                where_string += "AND PASRPB.LIST_PRICEBOOKSET_ID = '{PricebookSetId}'".format(
                    PricebookSetId=tree_parent_level_1
                )
                if "SOR" in tree_param:
                    salesorg = tree_param.split("-")[-1]
                    where_string += "AND INVOICE_SALESORG_ID = '{SalesOrg}'".format(SalesOrg=salesorg)
            query_string = "SELECT DISTINCT {Columns} FROM PRLPBK (NOLOCK) INNER JOIN PASRPB (NOLOCK) ON "
            +" PASRPB.LIST_PRICEBOOK_RECORD_ID = PRLPBK.LIST_PRICEBOOK_RECORD_ID WHERE "
            +" PASRPB.PRICEAGREEMENT_RECORD_ID = '{SegmentRecordId}' "
            +" AND	PASRPB.AGMREV_ID = '{RevisionId}' {Where_Condition}".format(
                Columns=",".join(["PRLPBK.{}".format(column) for column in columns]),
                RevisionId=revision_id,
                SegmentRecordId=segment_rec_id,
                Where_Condition=where_string,
            )
        else:
            updated_columns = []
            for column in columns:
                if column == "PRICECLASS_ID":
                    updated_columns.append("PASRPB.{}".format(column))
                else:
                    updated_columns.append("MAX(PASRPB.{}) as {}".format(column, column))
            order_by = "PRICEAGM_REV_PRICEBOOK_RECORD_ID"
            if tree_param == "Calculation Factors":
                where_string += "AND PASRPB.LIST_PRICEBOOKSET_ID = '{PricebookSetId}'".format(
                    PricebookSetId=tree_parent_level_0
                )
            else:
                where_string += "AND PASRPB.LIST_PRICEBOOKSET_ID = '{PricebookSetId}'".format(
                    PricebookSetId=tree_parent_level_1
                )
            query_string = "SELECT DISTINCT {Columns} FROM PASRPB (NOLOCK) WHERE "
            +" PASRPB.PRICEAGREEMENT_RECORD_ID = '{SegmentRecordId}' AND GSRPB.AGMREV_ID = '{RevisionId}' "
            +" {Where_Condition} GROUP BY PRICECLASS_ID ".format(
                Columns=",".join(updated_columns),
                RevisionId=revision_id,
                SegmentRecordId=segment_rec_id,
                Where_Condition=where_string,
            )

        pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(
            Skip_Count=offset_skip_count, Fetch_Count=offset_skip_count + fetch_count - 1,
        )
        query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
            Inner_Columns=",".join(columns), Query_String=query_string, Order_by=order_by,
        )
        table_count_data = Sql.GetFirst(query_string_for_count)

        if table_count_data is not None:
            pagination_total_count = table_count_data.count
        query_string_with_pagination = "SELECT DISTINCT {Outer_Columns} FROM (SELECT DISTINCT "
        +" {Inner_Columns},ROW_NUMBER()OVER(ORDER BY {Order_by}) AS SNO FROM ({Query_String}) IQ)"
        +" OQ {Pagination_Condition}".format(
            Outer_Columns=",".join(columns),
            Inner_Columns=",".join(columns),
            Query_String=query_string,
            Pagination_Condition=pagination_condition,
            Order_by=order_by,
        )
        table_data = Sql.GetList(query_string_with_pagination)

        if table_data is not None:
            for row_data in table_data:
                data_dict = {}
                Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop">'
                Action_str += '<i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" '
                Action_str += (
                    'aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton">'
                )
                Action_str += '<li><a class="dropdown-item" href="#" data-target="#viewSegmentQbResultModal"'
                Action_str += 'onclick="view_qb_result_modal(this)" data-toggle="modal">VIEW</a></li>'
                Action_str += "</ul></div></div>"
                data_dict["ACTIONS"] = Action_str
                for data in row_data:
                    if data.Key in ("LIST_PRICEBOOK_RECORD_ID", "PRICEAGM_REV_PRICEBOOK_RECORD_ID"):
                        data_dict[data.Key] = CPQID.KeyCPQId.GetCPQId(main_table_name, str(data.Value))
                    elif data.Key in ("LOCKED", "ACTIVE"):
                        data_dict[
                            data.Key
                        ] = '<input type="checkbox" disabled="disabled" class="custom" {}><span class="lbl"></span>'.format(
                            "checked" if data.Value == "true" else ""
                        )
                    else:
                        data_dict[data.Key] = data.Value
                table_content_json.append(data_dict)

        records_end = offset_skip_count + fetch_count - 1
        records_end = pagination_total_count if pagination_total_count < records_end else records_end
        records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
        disable_next_and_last = ""
        disable_previous_and_first = ""
        if records_end == pagination_total_count:
            disable_next_and_last = "class='btn-is-disabled'"
        if offset_skip_count == 1:
            disable_previous_and_first = "class='btn-is-disabled'"
        current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1
        pagination_table_id = "pagination_{}".format(table_id)
        pagination = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30"  >
                        <div class="col-md-4 pager-numberofitem  clear-padding">
                            <span class="pager-number-of-items-item fltltpad2mrg2" id="RecordsStartAndEnd"  >
                            {Records_Start_And_End}</span>
                            <span class="pager-number-of-items-item fltltpad2mrg0" id="TotalRecordsCount" >
                            {Pagination_Total_Count}</span>
                            <div class="clear-padding fltltmrgtp3"  >
                                <div   class="pull-right veralmert">
                                    <select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}')"
                                    id="ShowResultCount"  class="form-control pagecunt">
                                        <option value="10" {Selected_10}>10</option>
                                        <option value="20" {Selected_20}>20</option>
                                        <option value="50" {Selected_50}>50</option>
                                        <option value="100" {Selected_100}>100</option>
                                        <option value="200" {Selected_200}>200</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="col-xs-8 col-md-4  clear-padding inpadtex"   data-bind="visible: totalItemCount">
                            <div class="clear-padding col-xs-12 col-sm-6 col-md-12 brdr0" >
                                <ul class="pagination pagination">
                                    <li class="disabled">
                                        <a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}')" {Disable_First}>
                                        <i class="fa fa-caret-left fnt14bold" ></i><i class="fa fa-caret-left fnt14">
                                        </i></a>
                                    </li>
                                    <li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}')"
                                    {Disable_Previous}><i class="fa fa-caret-left fnt14" ></i>PREVIOUS</a></li>
                                    <li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}')"
                                    {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"  ></i></a></li>
                                    <li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}')"
                                    {Disable_Last}><i class="fa fa-caret-right fnt14"  ></i>
                                    <i class="fa fa-caret-right fnt14bold" >
                                    </i></a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-4 pr_page_pad">
                            <span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
                            <span class="page_right_content pr_page_rt_cnt"  >Page </span>
                        </div>
                    </div>""".format(
            Parent_Div_Id=pagination_table_id,
            Records_Start_And_End=records_start_and_end,
            Pagination_Total_Count=pagination_total_count,
            ShowResultCountFuncTb=pagination_table_id,
            Selected_10="selected" if fetch_count == 10 else "",
            Selected_20="selected" if fetch_count == 20 else "",
            Selected_50="selected" if fetch_count == 50 else "",
            Selected_100="selected" if fetch_count == 100 else "",
            Selected_200="selected" if fetch_count == 200 else "",
            GetFirstResultFuncTb=pagination_table_id,
            Disable_First=disable_previous_and_first,
            GetPreviuosResultFuncTb=pagination_table_id,
            Disable_Previous=disable_previous_and_first,
            GetNextResultFuncTb=pagination_table_id,
            Disable_Next=disable_next_and_last,
            GetLastResultFuncTb=pagination_table_id,
            Disable_Last=disable_next_and_last,
            Current_Page=current_page,
        )
        resize_func = ""
        # For Table Resize start
        if table_id == "product_qb_result_table":
            resize_func += ' try { setTimeout(function(){$( "#product_qb_result_table" ).colResizable({ '
            +' disable : true });$("#product_qb_result_table").colResizable({ liveDrag:true });}, 3000); '
            +' } catch (err) { setTimeout(function(){ $( "#product_qb_result_table" ).colResizable({ '
            +' disable : true });$("#product_qb_result_table").colResizable({ liveDrag:true,'
            +' gripInnerHtml:"<div class=\'grip2\'></div>", draggingClass:"dragging" });}, 3000);} '
        return (
            table_string,
            table_content_json,
            filter_control_function,
            pagination,
            pagination_total_count,
            table_id,
            filter_tags,
            filter_types,
            filter_values,
            filter_drop_down,
            resize_func,
        )


Action = Param.Action
try:
    CurrentRecordId = Param.CurrentRecordId
except Exception, e:
    CurrentRecordId = ""

"""Object Initialization by Factory Method."""
objDef = eval(violationruleInsert.Factory(Action))(CurrentRecordId=CurrentRecordId)
if Action == "PoductDetails":
    Trace.Write(str(Action))
    RecordId = Param.RecoedId
    wherecondition = Param.wherecondition
    Current_type = Param.Current_type
    PerPage = Param.PerPage
    startPage = Param.startPage
    endPage = Param.endPage
    ApiResponse = ApiResponseFactory.JsonResponse(
        objDef.GetProductDetails(RecordId, wherecondition, Current_type, PerPage, startPage, endPage)
    )
elif Action == "ProductDetail":
    Trace.Write(str(Action))
    MaterilId = Param.MaterilId
    ApiResponse = ApiResponseFactory.JsonResponse(objDef.ProductDetailView(MaterilId))
elif Action == "QueryBuilder":
    Trace.Write(str(Action))
    OnEdit = Param.OnEdit
    ApiResponse = ApiResponseFactory.JsonResponse(objDef.ConstructQueryBuilder(OnEdit))
elif Action == "QBSave":
    Trace.Write(str(Action))
    QbJsonData = Param.QbJsonData
    QbWhereCondition = Param.QbWhereCondition
    QbCallFromPricing = Param.QbCallFromPricing
    ApiResponse = ApiResponseFactory.JsonResponse(objDef.SaveQueryBuilder(QbJsonData, QbWhereCondition, QbCallFromPricing))
elif Action == "PriceFactor":
    AllParams = Param.AllParams
    attribute_name = Param.AttributeName
    attribute_value = Param.AttributeValue
    show_result_count = Param.ShowResultCount
    record_end = Param.RecordEnd
    try:
        table_id_from_js = Param.TableId
    except Exception, e:
        table_id_from_js = ""
    ApiResponse = ApiResponseFactory.JsonResponse(
        objDef.build_pricebook_table(
            attribute_name, attribute_value, AllParams, show_result_count, record_end, table_id_from_js
        )
    )
