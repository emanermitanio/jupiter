def convert_empty_to_none(row):
    return {key: (value if value != '' else None) for key, value in row.items()}

def process_csv(file_path):
    conn = get_db()
    cursor = conn.cursor()
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = convert_empty_to_none(row)
                cursor.execute("""
                    INSERT INTO TBL_PIPELINE (
                        LOB, DEPARTMENT, WORKGROUP, PROCESS, 
                        REQUEST_RECEIVED_YEAR, REQUEST_RECEIVED_MONTH, REQUEST_RECEIVED_DATE, 
                        TARGET_SLA_DATE, IOS_MANAGER, IOS_NAME, PACKAGE_TYPE, CROSS_BORDER, 
                        ENTITY_NAME, IR_NUMBER, OR_NUMBER, DDA_PLI_NUMBER, ECID, DOC_SOLUTION_CAPTURE, 
                        PRIORITY, LOCATION, PROCESS_LOCATION, NO_OF_ENTITIES, PLI_ASSIGNED, 
                        ASSIGNED_SID, ASSIGNED_REVIEWER, REVIEW_DATE, REVIEW_STATUS, 
                        PENDING_REJECT_REASON, REVIEWER_COMMENTS, ASSIGNED_DATE, PARENT_ENTITY
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        row['LOB'], row['DEPARTMENT'], row['WORKGROUP'], row['PROCESS'], 
                        row['REQUEST_RECEIVED_YEAR'], row['REQUEST_RECEIVED_MONTH'], row['REQUEST_RECEIVED_DATE'], 
                        row['TARGET_SLA_DATE'], row['IOS_MANAGER'], row['IOS_NAME'], row['PACKAGE_TYPE'], row['CROSS_BORDER'], 
                        row['ENTITY_NAME'], row['IR_NUMBER'], row['OR_NUMBER'], row['DDA_PLI_NUMBER'], row['ECID'], row['DOC_SOLUTION_CAPTURE'], 
                        row['PRIORITY'], row['LOCATION'], row['PROCESS_LOCATION'], row['NO_OF_ENTITIES'], row['PLI_ASSIGNED'], 
                        row['ASSIGNED_SID'], row['ASSIGNED_REVIEWER'], row['REVIEW_DATE'], row['REVIEW_STATUS'], 
                        row['PENDING_REJECT_REASON'], row['REVIEWER_COMMENTS'], row['ASSIGNED_DATE'], row['PARENT_ENTITY']
                    )
                )
        conn.commit()
    except Exception as e:
        print(f"Error processing CSV file: {e}")
    finally:
        conn.close()
        os.remove(file_path)