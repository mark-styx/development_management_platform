create schema dmp
;


create table dmp.environment_paths (
    usr nvarchar(255),
    env_path nvarchar(255)
)
;


create table dmp.project_list (
    rkey int identity,
    project nvarchar(255),
    project_desc nvarchar(255),
    project_status nvarchar(255),
    total_tasks int,
    completed_tasks int,
    project_lead nvarchar(255),
    create_date date,
    est_completion date,
    dev_status nvarchar(25)
)
;


create table dmp.project_status_list (
    rkey int identity,
    status nvarchar(255),
    description nvarchar(max),
    dev_status nvarchar(25)
)
;


insert into dmp.project_status_list (status,description)
values
    ('Pending Analyst Review','Newly created project; No activity has taken place. Analyst team to review and determine acceptance.'),
    ('Pending Development Plan','Project has been accepted. Analyst team to produce development plan.'),
    ('Pending Plan Approval','Development plan has been submitted and pending approval.'),
    ('Active Development','Plan has been approved and development is in progress.'),
    ('On Hiatus','Project is no longer being actively developed but has not been rejected.'),
    ('Rejected','Project as submitted has been rejected and no further development will take place.'),
    ('Unit Testing','Core developments have been completed, pending successful unit tests.'),
    ('User Testing','Unit testing has been successfully completed, pending successful user tests.'),
    ('Hypercare','Development has been completed, all tests passed, and project has been delivered.'),
    ('Completed','All requirements have been delivered.')
;


update dmp.project_status_list
set dev_status = case
    when [status] in (
        'Pending Analyst Review','Pending Development Plan','Pending Plan Approval',
        'Active Development','Unit Testing','User Testing','Hypercare'
    ) then 'active' else 'inactive' end
;


create table dmp.project_outlines (
    rkey int identity,
    project nvarchar(255),
    task_id int,
    task_name nvarchar(255),
    task_desc nvarchar(max),
    task_dependencies nvarchar(255),
    task_status nvarchar(255),
    owner nvarchar(255),
    create_date date,
    est_completion date,
    tbls_affected nvarchar(max),
    est_risks nvarchar(max),
    est_risk_penalty int
)
;


create table dmp.test_logs (
    rkey int identity,
    project nvarchar(255),
    test_module nvarchar(255),
    test_date date,
    test_runtime int,
    test_outcome nvarchar(255),
    narrative nvarchar(255),
)
;


create table dmp.bug_reports (
    rkey int identity,
    project nvarchar(255),
    title nvarchar(255),
    bug_description nvarchar(max),
    analyst_assigned nvarchar(255),
    reported_by nvarchar(255),
    status nvarchar(255),
    reported_date date,
    last_update date
)
;


create table dmp.project_request_queue (
    rkey int identity,
    title nvarchar(255),
    doc_link nvarchar(500)
)
;


create table dmp.table_references (
    rkey int identity,
    project nvarchar(255),
    table nvarchar(255)
)