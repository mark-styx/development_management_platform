-- create trigger to auto-populate the task_id and create_date

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


-- create trigger to auto-populate the total_tasks,completed_tasks and est_completion

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
            sum(case when task_status = 'completed' then 1 else 0 end) as comptsk,
            max(est_completion) as estcomp
		from dmp.project_outlines
        group by project
	) outln
	where proj = project
end
;


-- create trigger to auto-populate dev_status

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


-- trigger to add date to table
create trigger dmp.bug_reports_timestamp
on dmp.bug_reports after insert
as
begin
	set nocount on;
	
	update dmp.bug_reports
    set
        dmp.bug_reports.reported_date = getdate(),
        dmp.bug_reports.status = 'Open'
    where dmp.bug_reports.reported_date is null

end
;