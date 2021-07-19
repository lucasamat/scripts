# =========================================================================================================================================
#   __script_name : SYSYNCSYPR.PY
#   __script_description : THIS SCRIPT IS USED TO SYNC THE SYSTEM ADMIN SY**** TABLES WITH SYSTEM PROFILE SYPR** TABLES
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================


from SYDATABASE import SQL
import datetime

Sql = SQL()
userId = str(User.Id)
userName = str(User.UserName)

#APP -SYPRAP STRAT
QueryStatement = """
MERGE SYPRAP SRC
    USING (SELECT APP_LABEL, APP_ID, SYSTEM_ID, PERMISSION_ID, DISPLAY_ORDER FROM SYAPPS MM
            CROSS JOIN CPQ_PERMISSIONS FL WHERE FL.PERMISSION_TYPE = '0') TGT
            ON (SRC.APP_RECORD_ID = TGT.APP_ID AND SRC.PROFILE_RECORD_ID = TGT.PERMISSION_ID
            AND SRC.PROFILE_ID = TGT.SYSTEM_ID)
WHEN MATCHED
    THEN UPDATE SET
        SRC.APP_ID = TGT.APP_LABEL,
        SRC.CPQTABLEENTRYMODIFIEDBY = {userid},
        SRC.CPQTABLEENTRYDATEMODIFIED = '{datetimenow}',
        SRC.ADDUSR_RECORD_ID = {userid}
WHEN NOT MATCHED BY TARGET
    THEN INSERT (PROFILE_APP_RECORD_ID, APP_ID, APP_RECORD_ID, [DEFAULT], PROFILE_ID, PROFILE_RECORD_ID, VISIBLE,
                CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CPQTABLEENTRYMODIFIEDBY,
                CPQTABLEENTRYDATEMODIFIED)
    VALUES (NEWID(), APP_LABEL, APP_ID, 0, SYSTEM_ID, PERMISSION_ID,
            1, '{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}')
WHEN NOT MATCHED BY SOURCE
    THEN DELETE;
""".format(
    datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName
)
Sql.RunQuery(QueryStatement)

QueryStatement = "DELETE FROM SYPRAP WHERE APP_ID = 'Integration_Module'"
Sql.RunQuery(QueryStatement)
#APP -SYPRAP EMD

#TAB -SYPRTB STRAT
QueryStatement = """
MERGE SYPRTB SRC
    USING (SELECT APP_LABEL, APP_RECORD_ID, SYSTEM_ID, PERMISSION_ID,
           TAB_LABEL, RECORD_ID, DISPLAY_ORDER, PRIMARY_OBJECT_NAME, PRIMARY_OBJECT_RECORD_ID FROM SYTABS MM
           CROSS JOIN CPQ_PERMISSIONS FL where FL.PERMISSION_TYPE = '0' ) TGT
           ON (SRC.TAB_RECORD_ID = TGT.RECORD_ID AND SRC.PROFILE_RECORD_ID = TGT.PERMISSION_ID
           AND SRC.PROFILE_ID = TGT.SYSTEM_ID)
WHEN MATCHED
    THEN UPDATE SET
        SRC.APP_ID = TGT.APP_LABEL,
        SRC.APP_RECORD_ID = TGT.APP_RECORD_ID,
        SRC.TAB_ID = TGT.TAB_LABEL,
        SRC.CPQTABLEENTRYMODIFIEDBY = {userid},
        SRC.CPQTABLEENTRYDATEMODIFIED = '{datetimenow}',
        SRC.ADDUSR_RECORD_ID = {userid}
WHEN NOT MATCHED BY TARGET
    THEN INSERT (PROFILE_TAB_RECORD_ID, APP_ID, APP_RECORD_ID, PROFILE_ID, PROFILE_RECORD_ID,
                 TAB_ID, TAB_RECORD_ID, VISIBLE,  CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID,
                 CPQTABLEENTRYMODIFIEDBY, CPQTABLEENTRYDATEMODIFIED)
    VALUES (NEWID(), APP_LABEL, APP_RECORD_ID, SYSTEM_ID, PERMISSION_ID, TAB_LABEL, RECORD_ID,
            1, '{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}')
WHEN NOT MATCHED BY SOURCE
    THEN DELETE;
""".format(
    datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName
)
Sql.RunQuery(QueryStatement)

#TAB -SYPRTB END
# SYNC SECTIONS : SYSECT X CPQ_PERMISSIONS => SYPRSN



QueryStatement = """
MERGE SYPRSN SRC
    USING (SELECT DISTINCT MM.RECORD_ID, MM.SECTION_NAME, SP.TAB_RECORD_ID, SP.TAB_NAME, MM.PRIMARY_OBJECT_RECORD_ID,
            MM.PRIMARY_OBJECT_NAME, SYSTEM_ID, PERMISSION_ID, DISPLAY_ORDER FROM SYSECT MM INNER JOIN SYPAGE SP on SP.RECORD_ID = MM.PAGE_RECORD_ID CROSS JOIN CPQ_PERMISSIONS FL
            WHERE FL.PERMISSION_TYPE = '0') TGT
            ON (SRC.SECTION_RECORD_ID = TGT.RECORD_ID AND SRC.PROFILE_RECORD_ID = TGT.PERMISSION_ID
            AND SRC.PROFILE_ID = TGT.SYSTEM_ID)
WHEN MATCHED
    THEN UPDATE SET
        SRC.SECTION_ID = TGT.SECTION_NAME,
        SRC.TAB_RECORD_ID = TGT.TAB_RECORD_ID,
        SRC.TAB_ID = TGT.TAB_NAME,
        SRC.OBJECT_NAME = TGT.PRIMARY_OBJECT_NAME,
        SRC.OBJECT_RECORD_ID = TGT.PRIMARY_OBJECT_RECORD_ID,
        SRC.CPQTABLEENTRYMODIFIEDBY = {userid},
        SRC.CPQTABLEENTRYDATEMODIFIED = '{datetimenow}',
        SRC.ADDUSR_RECORD_ID = {userid}
WHEN NOT MATCHED BY TARGET
    THEN INSERT (PROFILE_SECTION_RECORD_ID, SECTION_RECORD_ID, SECTION_ID, TAB_RECORD_ID, TAB_ID, OBJECT_RECORD_ID,
                OBJECT_NAME, PROFILE_ID, PROFILE_RECORD_ID,
                VISIBLE, CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID,
                CPQTABLEENTRYMODIFIEDBY, CPQTABLEENTRYDATEMODIFIED)
    VALUES (NEWID(), RECORD_ID, SECTION_NAME, TAB_RECORD_ID,  TAB_NAME, PRIMARY_OBJECT_RECORD_ID,
            PRIMARY_OBJECT_NAME, SYSTEM_ID, PERMISSION_ID, 1,
            '{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}')
WHEN NOT MATCHED BY SOURCE
    THEN DELETE;
""".format(
    datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName
)

Sql.RunQuery(QueryStatement)

QueryStatement = """
MERGE SYPRSN SRC
    USING (SELECT MM.RECORD_ID, MM.SECTION_NAME, '' as TAB_RECORD_ID, '' as TAB_NAME, MM.PRIMARY_OBJECT_RECORD_ID,
            MM.PRIMARY_OBJECT_NAME, SYSTEM_ID, PERMISSION_ID, DISPLAY_ORDER FROM SYSECT MM CROSS JOIN CPQ_PERMISSIONS FL
            WHERE FL.PERMISSION_TYPE = '0' AND MM.PAGE_RECORD_ID = '' ) TGT
            ON (SRC.SECTION_RECORD_ID = TGT.RECORD_ID AND SRC.PROFILE_RECORD_ID = TGT.PERMISSION_ID
            AND SRC.PROFILE_ID = TGT.SYSTEM_ID)
WHEN MATCHED
    THEN UPDATE SET
        SRC.SECTION_ID = TGT.SECTION_NAME,
        SRC.TAB_RECORD_ID = TGT.TAB_RECORD_ID,
        SRC.TAB_ID = TGT.TAB_NAME,
        SRC.OBJECT_NAME = TGT.PRIMARY_OBJECT_NAME,
        SRC.OBJECT_RECORD_ID = TGT.PRIMARY_OBJECT_RECORD_ID,
        SRC.CPQTABLEENTRYMODIFIEDBY = {userid},
        SRC.CPQTABLEENTRYDATEMODIFIED = '{datetimenow}',
        SRC.ADDUSR_RECORD_ID = {userid}
WHEN NOT MATCHED BY TARGET
    THEN INSERT (PROFILE_SECTION_RECORD_ID, SECTION_RECORD_ID, SECTION_ID, TAB_RECORD_ID, TAB_ID, OBJECT_RECORD_ID,
                OBJECT_NAME, PROFILE_ID, PROFILE_RECORD_ID,
                VISIBLE, CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID,
                CPQTABLEENTRYMODIFIEDBY, CPQTABLEENTRYDATEMODIFIED)
    VALUES (NEWID(), RECORD_ID, SECTION_NAME, TAB_RECORD_ID,  TAB_NAME, PRIMARY_OBJECT_RECORD_ID,
            PRIMARY_OBJECT_NAME, SYSTEM_ID, PERMISSION_ID, 1,
            '{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}') ;
""".format(
    datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName
)

Sql.RunQuery(QueryStatement)

QueryStatement = """
                UPDATE SYPRSN SET DEFAULT_EDIT_ACCESS = 1, EDITABLE=1 WHERE SECTION_RECORD_ID IN (SELECT SECTION_RECORD_ID FROM SYPSAC
                    WHERE ACTION_NAME = 'EDIT');
                UPDATE SYPRSN SET EDITABLE = 0, DEFAULT_EDIT_ACCESS = 0 WHERE SECTION_ID = 'AUDIT INFORMATION'
                    OR DEFAULT_EDIT_ACCESS IS NULL OR DEFAULT_EDIT_ACCESS = '' OR DEFAULT_EDIT_ACCESS = ' ';
                UPDATE SYPRSN SET EDITABLE = 0 WHERE EDITABLE IS NULL OR EDITABLE = '' OR EDITABLE = ' '
                    OR DEFAULT_EDIT_ACCESS = 0;"""
Sql.RunQuery(QueryStatement)

# SYNC QUESTIONS : SYSEFL X CPQ_PERMISSIONS --> SYPRSF

QueryStatement = """
MERGE SYPRSF SRC
    USING (SELECT RECORD_ID, FIELD_LABEL, SECTION_RECORD_ID, SECTION_NAME,
            API_NAME, API_FIELD_NAME, SYSTEM_ID, PERMISSION_ID
            FROM SYSEFL MM CROSS JOIN CPQ_PERMISSIONS FL WHERE FL.PERMISSION_TYPE = '0') TGT
            ON (SRC.SECTIONFIELD_RECORD_ID = TGT.RECORD_ID AND SRC.PROFILE_RECORD_ID = TGT.PERMISSION_ID
            AND SRC.PROFILE_ID = TGT.SYSTEM_ID)
WHEN MATCHED
    THEN UPDATE SET
        SRC.SECTION_FIELD_ID = TGT.FIELD_LABEL,
        SRC.SECTION_RECORD_ID = TGT.SECTION_RECORD_ID,
        SRC.OBJECT_NAME = TGT.API_NAME,
        SRC.OBJECTFIELD_API_NAME = TGT. API_FIELD_NAME,
        SRC.SECTION_NAME = TGT.SECTION_NAME,
        SRC.CPQTABLEENTRYMODIFIEDBY = {userid},
        SRC.CPQTABLEENTRYDATEMODIFIED = '{datetimenow}',
        SRC.ADDUSR_RECORD_ID = {userid}
WHEN NOT MATCHED BY TARGET
    THEN INSERT (PROFILE_SECTIONFIELD_RECORD_ID, SECTIONFIELD_RECORD_ID, SECTION_FIELD_ID,
                    SECTION_RECORD_ID, SECTION_NAME, OBJECT_NAME, OBJECTFIELD_API_NAME,
                    PROFILE_ID, PROFILE_RECORD_ID, VISIBLE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,
                    ADDUSR_RECORD_ID, CPQTABLEENTRYMODIFIEDBY, CPQTABLEENTRYDATEMODIFIED)
        VALUES (NEWID(), RECORD_ID, FIELD_LABEL, SECTION_RECORD_ID, SECTION_NAME,
            API_NAME,   API_FIELD_NAME,
            SYSTEM_ID, PERMISSION_ID, 1, '{username}', '{datetimenow}', {userid}, {userid}, '{datetimenow}')
WHEN NOT MATCHED BY SOURCE
    THEN DELETE;
""".format(
    datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName
)
Sql.RunQuery(QueryStatement)

QueryStatement = """UPDATE SYPRSF SET SYPRSF.OBJECT_RECORD_ID = SYOBJH.RECORD_ID FROM SYPRSF
                    JOIN SYOBJH ON SYPRSF.OBJECT_NAME = SYOBJH.OBJECT_NAME"""
a = Sql.RunQuery(QueryStatement)


#SYPROH permissions sync :
QueryStatement = """

MERGE SYPROH SRC
    USING (SELECT RECORD_ID, OBJECT_NAME, SYSTEM_ID, PERMISSION_ID
            FROM SYOBJH MM CROSS JOIN CPQ_PERMISSIONS FL WHERE FL.PERMISSION_TYPE = '0') TGT
            ON (SRC.OBJECT_RECORD_ID = TGT.RECORD_ID AND SRC.PROFILE_RECORD_ID = TGT.PERMISSION_ID
            AND SRC.PROFILE_ID = TGT.SYSTEM_ID)
WHEN MATCHED
    THEN UPDATE SET
        SRC.OBJECT_NAME = TGT.OBJECT_NAME,
        SRC.CPQTABLEENTRYMODIFIEDBY = {userid},
        SRC.CPQTABLEENTRYDATEMODIFIED = '{datetimenow}'
WHEN NOT MATCHED BY TARGET
    THEN INSERT (PROFILE_OBJECT_RECORD_ID, OBJECT_RECORD_ID, OBJECT_NAME, PROFILE_ID, PROFILE_RECORD_ID,
                VISIBLE, CAN_ADD, CAN_EDIT, CAN_DELETE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, ADDUSR_RECORD_ID,
                CPQTABLEENTRYMODIFIEDBY, CPQTABLEENTRYDATEMODIFIED)
    VALUES (NEWID(), RECORD_ID, OBJECT_NAME, SYSTEM_ID, PERMISSION_ID, 1, 1, 1, 0,
            '{username}', '{datetimenow}', {userid},  {userid}, '{datetimenow}')
WHEN NOT MATCHED BY SOURCE
    THEN DELETE;
""".format(
    datetimenow=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName
)
Sql.RunQuery(QueryStatement)
# SYPROH add,edit,delete update
QueryStatement = """UPDATE SYPROH SET SYPROH.CAN_DELETE = SYOBJS.CAN_DELETE,SYPROH.CAN_EDIT = SYOBJS.CAN_EDIT FROM SYPROH
                    JOIN SYOBJS ON SYPROH.OBJECT_NAME = SYOBJS.CONTAINER_NAME WHERE SYOBJS.NAME = 'TAB LIST'"""
Sql.RunQuery(QueryStatement)