# import pyodbc
# from langchain.tools import Tool
# from sentence_transformers import SentenceTransformer, util
# from langchain.agents import initialize_agent
# from langchain_groq import ChatGroq


# def connect_to_ssms(server, database, username=None, password=None, trusted_connection=True):
#     try:
#         if trusted_connection:
#             conn_str = (
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#                 f'SERVER={server};'
#                 f'DATABASE={database};'
#                 'Trusted_Connection=yes;'
#             )
#         else:
#             conn_str = (
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#                 f'SERVER={server};'
#                 f'DATABASE={database};'
#                 f'UID={username};'
#                 f'PWD={password};'
#             )
#         conn = pyodbc.connect(conn_str)
#         print("✅ Connection successful")
#         return conn
#     except Exception as e:
#         print("❌ Connection failed:", str(e))
#         return None
    

# model = SentenceTransformer('all-MiniLM-L6-v2')

# schema = {'__EFMigrationsHistory': ['MigrationId', 'ProductVersion'], 'Addresses': ['Id', 'PersonId', 'AddressType', 'AddressLine1', 'AddressLine2', 'AddressLine3', 'StateId', 'CountryId', 'CityId'], 'Appraisal': ['Id', 'EmployeeId', 'AppraisalAmount', 'OldCTC', 'AppraisalDate'], 'AssetCarryToHome': ['Id', 'AssetId', 'UserId', 'StartDate', 'EndDate', 'Reason'], 'Assets': ['Id', 'CategoryId', 'AssetId', 'AssetName', 'Description', 'Brand', 'Status', 'IsActive', 'CreatedAt', 'UpdatedAt', 'CreatedBy', 'UpdatedBy'], 'AssetsAssignment': ['Id', 'AssetId', 'UserId', 'AssignmentDate', 'ReturnDate', 'Remark', 'AssignBy'], 'AssetSpecifications': ['Id', 'SpecificationName', 'SpecificationValue', 'AssetId'], 'AttendanceDetails': ['Id', 'AttendanceId', 'CheckInOutTime', 'Status', 'IpAddress', 'Duration', 'BreakTime', 'CreatedBy'], 'AttendanceRequest': ['Id', 'PersonId', 'LeaveType', 'RequestDate', 'StartDate', 'EndDate', 'StartHalf', 'EndHalf', 'InTime', 'OutTime', 'Status', 'Reason', 'RejectReason', 'AttendanceDetailId', 'ActualTime', 'RequestType'], 'Attendances': ['Id', 'PersonId', 'Date', 'OnBreak', 'Counter'], 'auth_group': ['id', 'name'], 'auth_group_permissions': ['id', 'group_id', 'permission_id'], 'auth_permission': ['id', 'name', 'content_type_id', 'codename'], 'auth_user': ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'], 'auth_user_groups': ['id', 'user_id', 'group_id'], 'auth_user_user_permissions': ['id', 'user_id', 'permission_id'], 'BankDetails': ['Id', 'PersonId', 'AccountName', 'AccountNumber', 'BankName', 'BankBranch', 'IFSCCode'], 'Bonus': ['Id', 'Title', 'CalculationType', 'Amount', 'Status', 'OrganizationId'], 'BroadcastNotification': ['Id', 'OrganizationId', 'Name', 'Description', 'IsActive', 'StartDate', 'EndDate'], 'BulkDocuments': ['Id', 'PersonId', 'DocumentName', 'DocumentPath', 'UploadedOn', 'UploadedBy'], 'Categories': ['Id', 'CategoryId', 'CategoryName'], 'CategorySpecifications': ['Id', 'SpecificationName', 'CategoryId'], 'Cities': ['Id', 'CityName', 'StateId'], 'Client': ['Id', 'ClientName', 'ClientEmail', 'ClientContactNumber', 'ExternalStakeholders', 'CreatedDate', 'CreatedBy'], 'CompanyAddress': ['Id', 'Address', 'City', 'State', 'Country', 'Zipcode', 'PersonId'], 'CompanyPersons': ['Id', 'Name', 'Email', 'PhoneNumber', 'Status', 'IsPublic', 'Description', 'AlternateNumber', 'WebSite'], 'CompanyPolicy': ['Id', 'OrganizationId', 'Name', 'PolicyTypeId', 'Description', 'IsActive', 'CreatedBy', 'CreatedAt', 'ModifiedBy', 'ModifiedAt'], 'CompanySocialMedias': ['Id', 'Facebook', 'Twitter', 'Linkedin', 'Skype', 'Whatsapp', 'Instagram', 'PersonId'], 'ContactAddress': ['Id', 'Address', 'City', 'State', 'Country', 'Zipcode', 'ContactPersonId'], 'ContactPerson': ['Id', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'Status', 'IsPublic', 'Description', 'AlternateNumber'], 'ContactSocialMedia': ['Id', 'Facebook', 'Twitter', 'Linkedin', 'Skype', 'Whatsapp', 'Instagram', 'ContactPersonId'], 'Countries': ['Id', 'CountryName'], 'Deduction': ['Id', 'OrganizationId', 'Name', 'CalculationType', 'CalculationAmount', 'IsActive', 'IsApplyRule', 'ConditionAmount', 'Condition', 'CreatedBy', 'CreatedDate'], 'Departments': ['Id', 'DepartmentName'], 'Designation': ['Id', 'Name', 'Description', 'Level', 'IsActive', 'OrganizationId'], 'django_admin_log': ['id', 'action_time', 'object_id', 'object_repr', 'action_flag', 'change_message', 'content_type_id', 'user_id'], 'django_content_type': ['id', 'app_label', 'model'], 'django_migrations': ['id', 'app', 'name', 'applied'], 'django_session': ['session_key', 'session_data', 'expire_date'], 'DocumentTemplate': ['Id', 'Name', 'Subject', 'Body', 'OrganizationId'], 'Earning': ['Id', 'OrganizationId', 'Name', 'CalculationType', 'CalculationAmount', 'IsActive', 'IsApplyRule', 'ConditionAmount', 'Condition', 'CreatedBy', 'CreatedDate'], 'EmailSetting': ['Id', 'OrganizationId', 'MailType', 'SMTPFromEmail', 'SMTPPassword', 'SMTPFromName', 'SendGridAPIKey', 'SendGridSenderEmail', 'SendGridName', 'ZeptoBounceAddress', 'ZeptoAPIKey', 'ZeptoFromEmail', 'ZeptoFromName', 'ZeptoSMTPEmailAPI', 'IsDefault'], 'EmployeeInsurance': ['Id', 'PersonsId', 'InsuranceId', 'OrganizationsId', 'StartDate', 'NextRenewalDate', 'Amount', 'CreatedAt', 'CreatedBy', 'ModifyBy', 'ModifyAt', 'DeletedAt', 'DeletedBy'], 'EmployeeLeaveDetail': ['Id', 'PersonId', 'CutLeave', 'CarryForwardLeave', 'CompOff', 'Year', 'Month', 'PaidOff', 'WeekOff', 'PresentDays', 'AbsentDays', 'PaidLeave', 'PaidDays', 'PendingLeave'], 'EmployeeLeaves': ['Id', 'PersonId', 'LeaveType', 'StartDate', 'EndDate', 'StartHalf', 'EndHalf', 'Reason', 'Approval', 'ApprovedBy', 'ApprovedOn', 'RejectionReason', 'LeaveFile', 'LeaveRequestDate'], 'EmployeeLoan': ['Id', 'LoanAmount', 'LoanTenure', 'MonthlyAmount', 'IsActive', 'PersonId', 'OrganizationsId', 'CreatedAt', 'CreatedBy', 'ModifyAt', 'ModifyBy', 'DeletedAt', 'DeletedBy', 'Reason', 'StartDate', 'EndDate', 'LoanStatus', 'Remarks', 'ApprovedBy'], 'EmployeePersonalInsurance': ['Id', 'CompanyName', 'PlanName', 'PersonId', 'CoverAmount', 'InsuranceType'], 'EmployeeSalaryDeductionDetail': ['Id', 'EmployeeSalaryDetailId', 'DeductionId', 'Amount'], 'EmployeeSalaryDetail': ['Id', 'PersonId', 'ActualSalary', 'PaidSalary', 'Year', 'Month'], 'EmployeeSalaryEarningDetail': ['Id', 'EmployeeSalaryDetailId', 'EarningId', 'Amount'], 'EmployeeTimesheetDetails': ['Id', 'EmployeeTimesheetId', 'TimesheetDate', 'TimeType', 'Regulation', 'TotalHours', 'Comments'], 'EmployeeTimesheetDetails_bkup': ['Id', 'EmployeeTimesheetId', 'TimesheetDate', 'TimeType', 'Regulation', 'TotalHours', 'Comments'], 'EmployeeTimesheetDetails_History': ['Id', 'EmployeeTimesheetId', 'TimesheetDate', 'TimeType', 'Regulation', 'TotalHours', 'Comments'], 'EmployeeTimesheets': ['Id', 'PersonId', 'WeekDay', 'Comments', 'Status', 'ApprovedBy', 'LastModifiedAt'], 'employeetimesheets_bkup': ['Id', 'PersonId', 'WeekDay', 'Comments', 'Status', 'ApprovedBy', 'LastModifiedAt'], 'EmployeeTimesheets_History': ['Id', 'PersonId', 'WeekDay', 'Comments', 'Status', 'ApprovedBy', 'LastModifiedAt'], 'Expense': ['Id', 'ExpenseDate', 'Amount', 'Description', 'Bill', 'TypeId', 'Vendor', 'Status', 'ExpenseBy', 'PaidBy', 'Remarks'], 'ExpenseType': ['Id', 'TypeName'], 'Goal': ['Id', 'GoalTypeId', 'PersonId', 'Subject', 'StartDate', 'EndDate', 'Description', 'Status', 'Progress'], 'GoalType': ['Id', 'Type', 'Description', 'Status'], 'HolidayMasters': ['Id', 'Date', 'Description', 'Optional'], 'Inquiry': ['Id', 'Name', 'PhoneNumber', 'Email', 'Country', 'Requirement', 'Designation', 'Organization', 'InquiryFor', 'DemoRequest', 'CreatedDate'], 'Insurance': ['Id', 'CompanyName', 'PlanType', 'CoverAmount', 'CoveragePeriod', 'Cover', 'OrganizationsId', 'CreatedAt', 'CreatedBy', 'ModifyAt', 'ModifyBy', 'DeletedAt', 'DeletedBy'], 'Invoice': ['Id', 'InvoiceDate', 'Amount', 'Description', 'Invoice', 'ProjectId', 'Status'], 'JobInquiry': ['Id', 'FullName', 'Email', 'PositionOfInterest', 'PhoneNumber', 'Location', 'Message', 'Remarks', 'Date', 'IsActive', 'CVFile', 'JobInquiryStatus', 'ResumeText'], 'MeetingRoom': ['Id', 'Name', 'Capacity', 'Amenities', 'OrganizationsId', 'IsActive'], 'Modules': ['Id', 'Module', 'Description', 'ModuleTypeId'], 'ModuleType': ['Id', 'TypeName', 'ModuleOrder'], 'Notification': ['Id', 'UserId', 'Title', 'IsRead', 'Description', 'NotificationType'], 'OrganizationAuthentication': ['Id', 'OrganizationId', 'Authenticationtype', 'ApiKey', 'ApiSecretKey', 'IsDisplay'], 'OrganizationProfile': ['Id', 'OrganizationId', 'Detail'], 'Organizations': ['Id', 'Name', 'Code', 'Email', 'Title', 'Logo', 'Favicon', 'Description', 'PrimaryColorCode', 'SecondaryColorCode', 'CreatedAt', 'IsActive', 'PackageId', 'PackageExpiryDate', 'IsTimer'], 'OrganizationSettings': ['Id', 'OrganizationId', 'Title', 'TitleKey', 'Value', 'SerialNumber'], 'OrganizationStorage': ['Id', 'OrganizationId', 'StorageType', 'APIKey', 'APISecret', 'APIURL'], 'Overtime': ['Id', 'PersonId', 'OTDate', 'OTHour', 'Status', 'Description', 'ApprovedBy'], 'Package': ['Id', 'Name', 'Price', 'AllowUser'], 'PackageDuration': ['Id', 'Duration', 'Discount'], 'PackageModule': ['Id', 'PackageId', 'ModuleId'], 'Payment': ['Id', 'OrganizationId', 'PaymentDate', 'PackageId', 'PackageDurationId', 'Price'], 'PayRoll': ['Id', 'PersonId', 'AnnualCTC', 'IsActive', 'CreatedDate', 'CreatedBy'], 'PayRollDetail': ['Id', 'PayrollId', 'EarningId', 'Amount'], 'PersonDocument': ['Id', 'PersonId', 'DocumentNumber', 'ExpiryDate', 'Remarks', 'DocumentType', 'Path', 'Description'], 'PersonEducations': ['Id', 'PersonId', 'Degree', 'PassingYear', 'Grade', 'Institution', 'Address'], 'PersonExperiences': ['Id', 'PersonId', 'CompanyName', 'StartDate', 'EndDate'], 'PersonFamilyDetails': ['Id', 'PersonId', 'RelationshipType', 'FirstName', 'MiddleName', 'LastName', 'DOB', 'ContactNumber', 'BloodGroup', 'Gender'], 'Persons': ['Id', 'PersonCode', 'FirstName', 'MiddleName', 'LastName', 'Email', 'DOB', 'DOJ', 'ContactNumber', 'EmergencyNumber', 'BloodGroup', 'MaritalStatus', 'Gender', 'DepartmentId', 'DesignationId', 'RoleId', 'OrganizationId', 'LoginType', 'Password', 'ReportingPerson', 'IsActive', 'LastWorkingDay', 'IsPolicyConsent', 'PolicyConsentDate', 'ProfilePicture', 'CreatedDate', 'CreatedBy', 'Otp', 'QuickOtp', 'IsCaptured', 'IsTrained'], 'PersonSkills': ['Id', 'PersonId', 'SkillName', 'Proficiency', 'LastUsedDate', 'TotalExperience'], 'PolicyType': ['Id', 'Name', 'IsActive', 'CreatedAt', 'ModifiedAt'], 'Poll': ['Id', 'Title', 'Status', 'EndDate', 'DepartmentId', 'CreatedBy', 'CreatedDate'], 'PollChoice': ['Id', 'PollId', 'Choice'], 'PollUserChoice': ['Id', 'PollChoiceId', 'UserId'], 'ProjectAttachments': ['Id', 'ProjectId', 'Name', 'Path'], 'ProjectCategory': ['Id', 'Name', 'Description', 'IsActive'], 'ProjectManagement': ['Id', 'OrganizationId', 'ProjectName', 'ProjectCode', 'Description', 'StartDate', 'EndDate', 'ProjectManager', 'ProjectOwner', 'TechnologySpecification', 'Status', 'Priority', 'ProjectCategoryId', 'Notes', 'IsActive', 'ClientId', 'CreatedDate', 'CreatedBy'], 'ProjectMembers': ['Id', 'ProjectId', 'PersonId', 'StartDate', 'EndDate', 'IsActive', 'DesignationId'], 'Promotion': ['Id', 'EmployeeId', 'OldDesignationid', 'NewDesignationId', 'PromotionDate'], 'Question': ['Id', 'DepartmentId', 'QuestionType', 'Questions', 'IsActive'], 'Resignation': ['Id', 'EmployeeId', 'Reason', 'NoticeDate', 'ResignationDate', 'CreatedBy', 'CreatedOn', 'ApprovedBy', 'ApprovedOn', 'CancellationReason', 'CancellationDate'], 'Review': ['Id', 'DepartmentId', 'Title', 'Type', 'ReviewDate', 'IsActive', 'DueOn'], 'ReviewQuestion': ['Id', 'ReviewId', 'QuestionId'], 'RolePermission': ['Id', 'RoleId', 'ModuleId', 'CanView', 'CanAdd', 'CanEdit', 'CanDelete'], 'Roles': ['Id', 'Name', 'Description', 'OrganizationId', 'CreatedAt', 'UpdatedAt', 'DeletedAt'], 'RoomBooking': ['Id', 'PersonId', 'MeetingRoomId', 'StartDate', 'EndDate', 'Reason', 'IsRecurring', 'RecurringStartDate', 'RecurringEndDate', 'StartTime', 'EndTime'], 'ShiftManagement': ['Id', 'Name', 'StartTime', 'EndTime', 'RotationDays', 'IsRotation', 'LastRotationDate', 'MaxStartTime', 'MinStartTime', 'MaxEndTime', 'MinEndTime', 'IsActive', 'RotationNumber'], 'SMSSetting': ['Id', 'OrganizationId', 'TwillioAccountSid', 'TwillioAuthtoken', 'TwillioFromName'], 'Sprint': ['Id', 'SprintCode', 'ProjectId', 'Week', 'CreatedBy', 'CreatedDate', 'Status', 'StartDate', 'EndDate', 'SprintName'], 'SprintTaskMapping': ['SprintId', 'TaskId', 'Id'], 'States': ['Id', 'StateName', 'CountryId'], 'StickyNotes': ['Id', 'PersonId', 'Date', 'Description'], 'Suggestion': ['Id', 'Subject', 'Comment', 'Attachment', 'Status', 'CreatedBy', 'CreatedOn', 'Remarks', 'ApprovedBy', 'ApprovedOn', 'SuggestionType', 'IsApproved'], 'TaskAssigment': ['Id', 'TaskId', 'AssignedId', 'CreatedDate', 'CreatedBy'], 'TaskAttachment': ['Id', 'TaskId', 'FilePath', 'CreatedDate', 'CreatedBy'], 'TaskConversion': ['Id', 'TaskId', 'Comment', 'CreatedBy', 'CreatedDate'], 'TaskConversionAttachment': ['Id', 'TaskConversionId', 'FilePath'], 'TaskFollowers': ['Id', 'TaskId', 'EmployeeId', 'CreatedBy', 'CreatedDate'], 'TaskManagement': ['Id', 'ProjectId', 'Subject', 'Description', 'Priority', 'Status', 'DueDate', 'CreatedBy', 'CreatedDate', 'TaskCode', 'TaskType'], 'TaskTimeline': ['Id', 'TaskId', 'TimelineType', 'Comment', 'CreatedDate'], 'Template': ['Id', 'Name', 'Subject', 'Body', 'OrganizationId'], 'Termination': ['Id', 'EmployeeId', 'TerminationType', 'Reason', 'NoticeDate', 'TerminationDate'], 'Ticket': ['Id', 'Subject', 'Description', 'Priority', 'Status', 'TicketCode', 'ClientId', 'ProjectId', 'DueDate', 'CreatedDate', 'CreatedBy'], 'TicketAssignment': ['Id', 'TicketId', 'AssignedId', 'CreatedDate', 'CreatedBy'], 'TicketAttachment': ['Id', 'TicketId', 'FilePath', 'CreatedDate', 'CreatedBy'], 'TicketConversion': ['Id', 'TicketId', 'Comment', 'CreatedBy', 'CreatedDate'], 'TicketConversionAttachment': ['Id', 'TicketConversionId', 'FilePath'], 'TicketFollowers': ['Id', 'TicketId', 'EmployeeId', 'CreatedBy', 'CreatedDate'], 'TicketTimeline': ['Id', 'TicketId', 'TimelineType', 'Comment', 'CreatedDate'], 'ToDoList': ['Id', 'PersonId', 'Title', 'Description', 'DueDate', 'IsImportant', 'IsCompleted'], 'UserBonus': ['Id', 'EmployeeId', 'BonusId', 'Amount', 'BonusDate'], 'UserDocumentTemplate': ['Id', 'UserId', 'DocumentTemplateId', 'CreatedDate', 'CreatedBy', 'UserTemplate'], 'UserPermission': ['Id', 'PersonId', 'RoleId', 'ModuleId', 'CanView', 'CanAdd', 'CanEdit', 'CanDelete'], 'UserReview': ['Id', 'ReviewId', 'ReviewerId', 'EmployeeId', 'ApplyDate', 'DueDate'], 'UserReviewDetail': ['Id', 'ReviewerId', 'ReviewDate', 'EmployeeId', 'Status', 'ReviewId'], 'UserReviewQuestionAnswerDetail': ['Id', 'UserReviewDetailId', 'ReviewQuestionId', 'Answer'], 'UserShift': ['Id', 'UserId', 'ShiftId'], 'Warning': ['Id', 'EmployeeId', 'CompanyPolicyId', 'CreatedBy', 'CreatedAt', 'Comment']}

# table_descriptions = [f"Table {table} with columns: {', '.join(cols)}" for table, cols in schema.items()]
# table_names = list(schema.keys())
# schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

# def get_relevant_tables(question: str, top_n=3):
#     question_embedding = model.encode(question, convert_to_tensor=True)
#     similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
#     top_indices = similarities.argsort(descending=True)[:top_n]
#     return [table_names[i] for i in top_indices]



# def query_ssms_with_context(natural_question: str) -> str:
#     # Step 1: Get top 3 relevant tables
#     relevant_tables = get_relevant_tables(natural_question)

#     # Step 2: Build schema context
#     context_lines = []
#     for table in relevant_tables:
#         cols = schema[table]
#         context_lines.append(f"{table}: {', '.join(cols)}")
#     schema_context = "\n".join(context_lines)

#     # Step 3: Form prompt to ask LLM to generate SQL query
#     prompt = f"""You are a SQL expert. Use only the following tables and columns to generate a SQL SELECT query:

# {schema_context}

# Question: {natural_question}
# Return only the SQL query, nothing else.
# """

#     sql_query = llm.invoke(prompt).content.strip().replace("`", "")

#     # Step 4: Execute the query
#     conn = connect_to_ssms(
#         server='LAPTOP-KRHSE4BT\\SQLEXPRESS',
#         database='SkyHR',
#         trusted_connection=True
#     )
#     if conn is None:
#         return "Connection failed."

#     try:
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
#         rows = cursor.fetchall()
#         columns = [column[0] for column in cursor.description]
#         result = [dict(zip(columns, row)) for row in rows]

#         return (
#             f"🔍 Top relevant tables: {', '.join(relevant_tables)}\n"
#             f"🧠 SQL Generated:\n{sql_query}\n\n"
#             f"📊 Query Result:\n{str(result)}"
#         )
#     except Exception as e:
#         return f"Error executing query: {str(e)}"
#     finally:
#         conn.close()
        
        
        
# ssms_query_tool = Tool(
#     name="SSMSQueryTool",
#     func=query_ssms_with_context,
#     description="Use this tool to query SQL Server database using SQL. Input should be a valid SQL SELECT statement."
# )

# api_key="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"

# llm = ChatGroq(api_key=api_key,model_name="Llama3-8b-8192",streaming=True)      

# agent = initialize_agent(
#     tools=[ssms_query_tool],
#     llm=llm,
#     agent="zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True

# )

# response = agent.invoke({"input": "give me email address for bhaumik patel in persons table"})
# print(response["output"])

# import pyodbc
# import ast
# from langchain.tools import Tool
# from sentence_transformers import SentenceTransformer, util
# from langchain.agents import initialize_agent
# from langchain_groq import ChatGroq
# from urllib.parse import quote_plus
# from langchain.sql_database import SQLDatabase
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit


# def load_schema_from_file(file_path: str) -> dict:
#     with open(file_path, 'r') as f:
#         content = f.read()
#     return ast.literal_eval(content)

# def connect_to_ssms(server, database, username=None, password=None, trusted_connection=True):
#     try:
#         if trusted_connection:
#             conn_str = (
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#                 f'SERVER={server};'
#                 f'DATABASE={database};'
#                 'Trusted_Connection=yes;'
#             )
#         else:
#             conn_str = (
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#                 f'SERVER={server};'
#                 f'DATABASE={database};'
#                 f'UID={username};'
#                 f'PWD={password};'
#             )
#         conn = pyodbc.connect(conn_str)
#         print("Connection successful")
#         return conn
#     except Exception as e:
#         print("Connection failed:", str(e))
#         return None

# model = SentenceTransformer('all-MiniLM-L6-v2')

# schema = load_schema_from_file("schema_output.txt")
# # print("schema",schema)
# table_descriptions = [f"Table {table} with columns: {', '.join(cols)}" for table, cols in schema.items()]
# table_names = list(schema.keys())
# schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

# def get_relevant_tables(question: str, top_n=3):
#     question_embedding = model.encode(question, convert_to_tensor=True)
#     similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
#     top_indices = similarities.argsort(descending=True)[:top_n]
#     return [table_names[i] for i in top_indices]

# def query_ssms_with_context(natural_question: str) -> str:
#     relevant_tables = get_relevant_tables(natural_question)
#     print("relevant_tables",relevant_tables)

#     context_lines = []
#     for table in relevant_tables:
#         cols = schema[table]
#         context_lines.append(f"{table}: {', '.join(cols)}")
#     schema_context = "\n".join(context_lines)
#     print("schema_context",schema_context)
    
# #     prompt = f"""You are a SQL expert. Use only the following tables and columns to generate a SQL SELECT query:

# # {schema_context}

# # Question: {natural_question}
# # Return only the SQL query, nothing else.
# # """

#     prompt = f"""
# You are an expert SQL query generator. Based only on the tables and columns listed below, write a syntactically correct and semantically accurate SQL SELECT query that answers the given question.

# ### Available Schema:
# {schema_context}

# ### Question:
# {natural_question}

# ### Instructions:
# - Only use the tables and columns provided in the schema above.
# - Use appropriate JOINs based on column/foreign key relationships if needed.
# - Do NOT make up any table or column names.
# - Do NOT explain anything; return only the final SQL SELECT query.

# ### Output:
# """


#     sql_query = llm.invoke(prompt).content.strip().replace("`", "")

#     # Execute query
#     conn = connect_to_ssms(
#         server='LAPTOP-KRHSE4BT\\SQLEXPRESS',
#         database='SkyHR',
#         trusted_connection=True
#     )
#     if conn is None:
#         return "Connection failed."

#     try:
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
#         rows = cursor.fetchall()
#         columns = [column[0] for column in cursor.description]
#         result = [dict(zip(columns, row)) for row in rows]

#         return (
#             f"Top relevant tables: {', '.join(relevant_tables)}\n"
#             f"SQL Generated:\n{sql_query}\n\n"
#             f"Query Result:\n{str(result)}"
#         )
#     except Exception as e:
#         return f"Error executing query: {str(e)}"
#     finally:
#         conn.close()

# api_key = "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"
# llm = ChatGroq(api_key=api_key, model_name="Llama3-8b-8192", streaming=True)


# ssms_query_tool = Tool(
#     name="SSMSQueryTool",
#     func=query_ssms_with_context,
#     description="Use this tool to query SQL Server database using SQL. Input should be a valid SQL SELECT statement."
# )


# params = quote_plus(
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=LAPTOP-KRHSE4BT\\SQLEXPRESS;"
#     "DATABASE=SkyHR;"
#     "Trusted_Connection=yes;"
# )
# db_url = f"mssql+pyodbc:///?odbc_connect={params}"
# sql_db = SQLDatabase.from_uri(db_url)
# sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
# sql_tools = sql_toolkit.get_tools()


# agent = initialize_agent(
#     tools= sql_tools + [ssms_query_tool],
#     llm=llm,
#     agent="zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True
# )

# if __name__ == "__main__":
#     user_query = "What are the salary details of the person Apurva Patel?"
#     response = agent.invoke({"input": user_query})
#     print(response["output"])





# Semantic search using SentenceTransformer

# LangChain agent with tools

# SQL execution via pyodbc

# LLM query generation via ChatGroq

# import pyodbc
# from langchain.tools import Tool
# from sentence_transformers import SentenceTransformer, util
# from langchain.agents import initialize_agent
# from langchain_groq import ChatGroq
# import re
# from langchain.sql_database import SQLDatabase
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from urllib.parse import quote_plus


# def load_schema_text(file_path: str) -> str:
#     with open(file_path, 'r', encoding="utf-8") as f:
#         return f.read()
    
# def parse_schema_to_table_blocks(schema_text: str) -> dict:
#     blocks = schema_text.strip().split('\n\n')  
#     table_blocks = {}
#     for block in blocks:
#         lines = block.strip().splitlines()
#         if not lines:
#             continue
#         match = re.match(r"^(\w+):", lines[0])
#         if match:
#             table_name = match.group(1)
#             table_blocks[table_name] = block
#     return table_blocks


# def connect_to_ssms(server, database, username=None, password=None, trusted_connection=True):
#     try:
#         print("****Connection****")
#         if trusted_connection:
#             conn_str = (
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#                 f'SERVER={server};'
#                 f'DATABASE={database};'
#                 'Trusted_Connection=yes;'
#             )
#         else:
#             conn_str = (
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#                 f'SERVER={server};'
#                 f'DATABASE={database};'
#                 f'UID={username};'
#                 f'PWD={password};'
#             )
#         conn = pyodbc.connect(conn_str)
#         print("Connection successful")
#         return conn
#     except Exception as e:
#         print("Connection failed:", str(e))
#         return None

# model = SentenceTransformer('all-MiniLM-L6-v2')

# schema_text = load_schema_text("schema_output_llm.txt")
# schema = parse_schema_to_table_blocks(schema_text)
# table_names = list(schema.keys())
# table_descriptions = list(schema.values())

# schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

# def get_relevant_tables(question: str, top_n=10):
#     question_embedding = model.encode(question, convert_to_tensor=True)
#     similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
#     top_indices = similarities.argsort(descending=True)[:top_n]
#     return [table_names[i] for i in top_indices]

# def query_ssms_with_context(natural_question: str) -> str:
#     relevant_tables = get_relevant_tables(natural_question)
#     print("relevant_tables",relevant_tables)

#     context_blocks = [schema[table] for table in relevant_tables if table in schema]
#     schema_context = "\n\n".join(context_blocks)
#     print("schema_context", schema_context)

#     prompt = f"""
# You are an expert SQL query generator. Based only on the tables and columns listed below, write a syntactically correct and semantically accurate SQL SELECT query that answers the given question.

# ### Available Schema:
# {schema_context}

# ### Question:
# {natural_question}

# ### Instructions:
# - Only use the tables and columns provided in the schema above.
# - Use appropriate JOINs based on column/foreign key relationships if needed.
# - Do NOT make up any table or column names.
# - Do NOT explain anything; return only the final SQL SELECT query.
# - Only use tables listed in the schema below.
# - If a person's name is queried, refer to the `Persons` table where `FirstName` and `LastName` exist (if applicable).


# ### Output:
# """


#     sql_query = llm.invoke(prompt).content.strip().replace("`", "")
#     print("sql_query",sql_query)
#     # Execute query
#     conn = connect_to_ssms(
#         server='LAPTOP-KRHSE4BT\\SQLEXPRESS',
#         database='SkyHR',
#         trusted_connection=True
#     )
#     if conn is None:
#         return "Connection failed."

#     try:
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
#         rows = cursor.fetchall()
#         columns = [column[0] for column in cursor.description]
#         result = [dict(zip(columns, row)) for row in rows]

#         return (
#             f"Top relevant tables: {', '.join(relevant_tables)}\n"
#             f"SQL Generated:\n{sql_query}\n\n"
#             f"Query Result:\n{str(result)}"
#         )
#     except Exception as e:
#         return f"Error executing query: {str(e)}"
#     finally:
#         conn.close()

# api_key = "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"
# llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192", streaming=True)

# ssms_query_tool = Tool(
#     name="SSMSQueryTool",
#     func=query_ssms_with_context,
#     description="Use this tool to query SQL Server database using SQL. Input should be a valid SQL SELECT statement."
# )


# params = quote_plus(
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=LAPTOP-KRHSE4BT\\SQLEXPRESS;"
#     "DATABASE=SkyHR;"
#     "Trusted_Connection=yes;"
# )
# db_url = f"mssql+pyodbc:///?odbc_connect={params}"
# sql_db = SQLDatabase.from_uri(db_url)
# sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
# sql_tools = sql_toolkit.get_tools()

# agent = initialize_agent(
#     tools= sql_tools + [ssms_query_tool],
#     llm=llm,
#     agent_type="zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True,
# )

# if __name__ == "__main__":
#     user_query = "Get the salary details for the employee named Ami Damania."
#     response = agent.invoke({"input": user_query})
#     print(response["output"])


# agent_type : "zero-shot-react-description" when:

# You want the agent to reason and decide which tool to use


# agent_type="zero-shot-react-description" is used when:

# You want the agent to:

    # Read the user’s input (a natural language question)

    # Think step-by-step

    # Choose the right tool to use (from the tools you gave it)

    # Possibly combine multiple tools

    # Return the final answer
    
    
    
    
import streamlit as st
from langchain.agents import initialize_agent
from langchain.tools import Tool
from sentence_transformers import SentenceTransformer, util
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from urllib.parse import quote_plus
import pyodbc
import re
import os
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"

import streamlit as st

def load_schema_text(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()

def parse_schema_to_table_blocks(schema_text: str) -> dict:
    blocks = schema_text.strip().split('\n\n')
    table_blocks = {}
    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue
        match = re.match(r"^(\w+):", lines[0])
        if match:
            table_name = match.group(1)
            table_blocks[table_name] = block
    return table_blocks

def connect_to_ssms(server, database, username=None, password=None, trusted_connection=True):
    try:
        if trusted_connection:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                'Trusted_Connection=yes;'
            )
        else:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password};'
            )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None


def build_agent(api_key):
    llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192", streaming=True)

    schema_text = load_schema_text("schema_output_llm.txt")
    schema = parse_schema_to_table_blocks(schema_text)
    table_names = list(schema.keys())
    table_descriptions = list(schema.values())

    model = SentenceTransformer('all-MiniLM-L6-v2')
    schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

    def get_relevant_tables(question: str, top_n=10):
        question_embedding = model.encode(question, convert_to_tensor=True)
        similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
        top_indices = similarities.argsort(descending=True)[:top_n]
        return [table_names[i] for i in top_indices]

    def query_ssms_with_context(natural_question: str) -> str:
        relevant_tables = get_relevant_tables(natural_question)
        context_blocks = [schema[table] for table in relevant_tables if table in schema]
        schema_context = "\n\n".join(context_blocks)

        prompt = f"""
You are an expert SQL query generator. Based only on the tables and columns listed below, write a syntactically correct and semantically accurate SQL SELECT query that answers the given question.

### Available Schema:
{schema_context}

### Question:
{natural_question}

### Instructions:
- Only use the tables and columns provided in the schema above.
- Use appropriate JOINs based on column/foreign key relationships if needed.
- Do NOT make up any table or column names.
- Do NOT explain anything; return only the final SQL SELECT query.
- Only use tables listed in the schema below.
- If a person's name is queried, refer to the `Persons` table where `FirstName` and `LastName` exist (if applicable).

### Output:
"""

        sql_query = llm.invoke(prompt).content.strip().replace("`", "")

        conn = connect_to_ssms(
            server='DESKTOP-HEB09TT\SQLEXPRESS',
            database='SkyHR',
            trusted_connection=True
        )
        if conn is None:
            return "Connection failed."

        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return (
                f"Top relevant tables: {', '.join(relevant_tables)}\n"
                f"SQL Generated:\n{sql_query}\n\n"
                f"Query Result:\n{result}"
            )
        except Exception as e:
            return f"Error executing query: {str(e)}"
        finally:
            conn.close()

    ssms_query_tool = Tool(
        name="SSMSQueryTool",
        func=query_ssms_with_context,
        description="Use this tool to query the SQL Server database. Input must be a valid SQL SELECT statement. The tool returns only formatted results, not the query."
    )

    params = quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-KRHSE4BT\\SQLEXPRESS;"
        "DATABASE=SkyHR;"
        "Trusted_Connection=yes;"
    )
    db_url = f"mssql+pyodbc:///?odbc_connect={params}"
    sql_db = SQLDatabase.from_uri(db_url)
    sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
    sql_tools = sql_toolkit.get_tools()
    
    prefix = """
    You are an assistant that helps retrieve data from a SQL Server database.
    You MUST use the tools provided to execute SQL queries and return ONLY the results.
    NEVER show the raw SQL query in your final answer.
    If the result is empty, just respond: "No data found in the database for the given input."

    After retrieving the result, respond in **clear and professional natural language**.

    Avoid showing any raw data structures like tuples, lists, or SQL queries.
    Only provide the final answer in a human-readable format.

    If no result is found, respond with:
    "No data found in the database for the given input."
    """

    agent = initialize_agent(
        tools=sql_tools + [ssms_query_tool],
        llm=llm,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={"prefix": prefix}

    )
    return agent

st.set_page_config(page_title="SkyHR Chatbot", layout="wide")
st.title("🤖 SkyHR Chatbot")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

st.sidebar.subheader("🧠 Conversation History")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm SkyHR Chatbot. Ask me anything about your employee data!"}
    ]
for msg in st.session_state["messages"]:
    prefix = "🧑" if msg["role"] == "user" else "🤖"
    st.sidebar.markdown(f"**{prefix} {msg['role'].capitalize()}:** {msg['content'][:40]}{'...' if len(msg['content']) > 40 else ''}")

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask about employee data..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        st.chat_message("assistant").write("Please enter your Groq API Key in the sidebar.")
    else:
        agent = build_agent(api_key)

        with st.chat_message("assistant"):
            response = agent.invoke({"input": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            st.write(response["output"])