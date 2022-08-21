#=========================================================================================================================================
#   __script_name : CQBKTBLDEL.PY
#   __script_description : Iflow script used for deleting backup table periodically (CRON JOB)
#   __primary_author__ :
#   __create_date : 07/07/2022
#   Ã¯Â¿Â½ BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL

Sql = SQL()

def _deleting_backup_table():
    Log.Info("deleting_backup_table")
    get_temp_table_count = Sql.GetFirst(
    "select name,crdate,count(*) as cnt from sysobjects where name like '%_BKP_%' and convert(varchar(11),crdate,121) < convert(varchar(11),getdate()) group by name,crdate")
    if get_temp_table_count:
        get_total_count,remainder = divmod(get_temp_table_count.cnt,1000)
        get_total_count = get_total_count + (1 if remainder > 0 else 0)
        cnt = 1
        fetch_count = 0
        end_count = 1000
        while cnt <= get_total_count:
            get_temp_table = Sql.GetList(
                 "select name,crdate as cnt from sysobjects where name like '%_BKP_%' and convert(varchar(11),crdate,121) < convert(varchar(11),getdate()) ORDER BY crdate ASC OFFSET {} ROWS FETCH NEXT {} ROWS ONLY".format(fetch_count, end_count))
            for temp_table in get_temp_table:
                temp_drop_query = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_table.name)+"'' ) BEGIN DROP TABLE "+str(temp_table.name)+" END  ' ")
            cnt += 1
            fetch_count +=1000
            end_count += 1000
    
    return True

_deleting_backup_table()


