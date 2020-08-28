/* project environment variables, project listing, outline, test logs, and bug report tables

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
    bug_description nvarchar(max),
    analyst_assigned nvarchar(255),
    reported_by nvarchar(255),
    status nvarchar(255),
    reported_date date,
    last_update date
)
;

create table dmp.table_references (
    rkey int identity,
    project nvarchar(255),
    table nvarchar(255)
)

*/

/* create trigger to auto-populate the task_id and create_date

create trigger dmp.outline_meta
on dmp.project_outlines after insert
as
begin
	set nocount on;
	
	update dmp.project_outlines
	set
		task_id = rid,
		create_date = cast(getdate() as date)
	from (
		select
			rkey as k,project,task_name,rank() over(
				partition by project
				order by rkey asc
				) as rid
		from dmp.project_outlines
	) rk
	where create_date is null
        and rkey = k
    ;
    
    update dmp.project_outlines
    set owner = project_lead
    from dmp.project_list
    where owner is null

end
;

*/

/* create trigger to auto-populate the total_tasks,completed_tasks and est_completion

create trigger dmp.proj_updates
on dmp.project_outlines after insert,delete,update
as
begin
	set nocount on;
	
	update dmp.project_list
	set
		total_tasks = ttltsk,
        completed_tasks = comptsk,
        est_completion = estcomp
	from (
		select
			project as proj,
            count(task_id) as ttltsk,
            sum(case when task_status = 'complete' then 1 else 0 end) as comptsk,
            max(est_completion) as estcomp
		from dmp.project_outlines
        group by project
	) outln
	where proj = project
end
;

/* create trigger to auto-populate dev_status

create trigger dmp.dev_stat_updates
on dmp.project_list after insert,delete,update
as
begin
	set nocount on;
	
	update dmp.project_list
	set
		dev_status = dstat
	from (
		select status,dev_status as dstat from dmp.project_status_list
	) sl
	where project_status = status
end
;

*/

--exec sp_rename 'dmp.project_outlines.task_dependancies', 'task_dependencies', 'COLUMN';

use dmp_dev_env

select * from dmp.project_list
select * from dmp.project_outlines

insert into dmp.project_outlines (
    project,task_name,task_id
    )
values
    ('testing001','heading',1),
    ('testing001','assign_missing_invs',2),
    ('testing001','data cleansing',3),
    ('testing001','trans categorization',4),
    ('testing001','purge offsets',5),
    ('testing001','single invoice matches - working capital',6),
    ('testing001','single invoice matches - output',7),
    ('testing001','multiple invoice matches',8),
    ('testing001','national cashflow',9),
    ('testing001','spot cashflow',10),
    ('testing001','commit_outputs',11)

;

create table #dates (k int, cd date)
;
insert into #dates
values
    (1,'2020-08-13'),
    (2,'2020-08-17'),
    (3,'2020-08-20'),
    (4,'2020-08-25'),
    (5,'2020-08-20'),
    (6,'2020-08-30'),
    (7,'2020-09-01'),
    (8,'2020-09-13'),
    (9,'2020-09-13'),
    (10,'2020-10-13'),
    (11,'2020-09-10')
;

update dmp.project_outlines
set
    est_completion = cd
from #dates
where k = task_id
    and project = 'testing001'
;

select * from dmp.project_outlines where project = 'testing001'


