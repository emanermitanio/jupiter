def process_xlsx(file_path):
    conn = get_db()
    cursor = conn.cursor()
    wb = None  # Initialize wb
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1]]  # Get headers from the first row
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))
            row_data = convert_empty_to_none(row_data)
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
                    row_data['LOB'], row_data['DEPARTMENT'], row_data['WORKGROUP'], row_data['PROCESS'], 
                    row_data['REQUEST_RECEIVED_YEAR'], row_data['REQUEST_RECEIVED_MONTH'], row_data['REQUEST_RECEIVED_DATE'], 
                    row_data['TARGET_SLA_DATE'], row_data['IOS_MANAGER'], row_data['IOS_NAME'], row_data['PACKAGE_TYPE'], row_data['CROSS_BORDER'], 
                    row_data['ENTITY_NAME'], row_data['IR_NUMBER'], row_data['OR_NUMBER'], row_data['DDA_PLI_NUMBER'], row_data['ECID'], row_data['DOC_SOLUTION_CAPTURE'], 
                    row_data['PRIORITY'], row_data['LOCATION'], row_data['PROCESS_LOCATION'], row_data['NO_OF_ENTITIES'], row_data['PLI_ASSIGNED'], 
                    row_data['ASSIGNED_SID'], row_data['ASSIGNED_REVIEWER'], row_data['REVIEW_DATE'], row_data['REVIEW_STATUS'], 
                    row_data['PENDING_REJECT_REASON'], row_data['REVIEWER_COMMENTS'], row_data['ASSIGNED_DATE'], row_data['PARENT_ENTITY']
                )
            )
        conn.commit()
    except Exception as e:
        print(f"Error processing XLSX file: {e}")
    finally:
        if wb:
            wb.close()  # Ensure the workbook is closed
        conn.close()
        os.remove(file_path)
