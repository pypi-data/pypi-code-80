"""
Contains a set of tools required to monitor and manage glue jobs 
"""

from awscm.aws_client import get_aws_client


def monitor_glue_jobs(**kwargs):
    """
    Fetches job status for all jobs in given/default region.
    --------------------------------------------------------
    Optional Parameter: named argument 'region'
    Ex - 
            monitor_glue_jobs()
            monitor_glue_jobs(region='us-east-1')
    ________________________________________________________
    Returns a list of dictionary with 'JobName' and 'Status'
    --------------------------------------------------------
    Note:-  If the job StartDate doesn't match datetime.date.today(),
            'YET TO START' is returned as status.
            Else 'JobRunState' is returned. 
    """
    aws = get_aws_client('glue', **kwargs)
    job_list = get_job_list(**kwargs)
    job_run_details_list = get_job_run_details(job_list, **kwargs)
    job_status_list = get_job_status(job_run_details_list)
    return job_status_list

def monitor_glue_job(job_name, **kwargs):
    """
    Fetches job status for job_name in given/default region.
    --------------------------------------------------------
    Required Parameter: job_name - type: String
    Optional Parameter: named argument 'region'
    Ex - 
            monitor_glue_job('testJob')
            monitor_glue_job('testJob', region='us-east-1')
    ________________________________________________________
    Returns a dictionary with 'JobName' and 'Status'
    --------------------------------------------------------
    Note:-  If the job StartDate doesn't match datetime.date.today(),
            'YET TO START' is returned as status.
            Else 'JobRunState' is returned. 
    """
    aws = get_aws_client('glue', **kwargs)
    job_run_details = get_job_run_details([job_name], **kwargs)
    job_status = get_job_status(job_run_details)
    return job_status[0]


def get_job_list(**kwargs):
    """
    Fetches names of all glue jobs in given/default region.
    _______________________________________________________
    Optional Parameter: named argument 'region'
    Ex - 
            get_job_list()
            get_job_list(region='us-east-1')
    _______________________________________________________
    Returns: List of all glue jobs.
    -------------------------------------------------------
    """
    aws = get_aws_client('glue', **kwargs)
    job_list = []
    jobs = aws.get_jobs()
    for job in jobs['Jobs']:
        job_list.append(job['Name'])
    return job_list


def get_job_run_details(job_list, **kwargs):
    """
    Fetches latest run details of glue jobs in given list , uses default/given region.
    ----------------------------------------------------------------------------------
    Required Parameter: job_list - type: List
    Optional Parameter: named argument 'region'
    Ex - 
            get_job_run_details(job_list)
            get_job_run_details(job_list, region='us-east-1')
    ----------------------------------------------------------------------------------
    Returns: List of dictionaries of run details for all glue jobs.
    ----------------------------------------------------------------------------------
    """
    aws = get_aws_client('glue', **kwargs)
    job_run_details = []
    for job in job_list:
        job_run_details.append(aws.get_job_runs(JobName=job, MaxResults=1))
    return job_run_details


def get_job_status(job_run_details_list):
    """
    Processes the given list of dictionaries of glue job run details.
    -----------------------------------------------------------------
    Required Parameter: job_run_details_list
    Ex - 
            get_job_status(job_run_details_list)
    ________________________________________________________
    Returns a list of dictionary with 'JobName' and 'Status'
    --------------------------------------------------------
    Note:-  If the job StartDate doesn't match datetime.date.today(),
            'YET TO START' is returned as status.
            Else 'JobRunState' is returned.
    """
    import datetime
    today = datetime.date.today()
    job_status_list = []
    for job in job_run_details_list:
        job_status_details = {}
        job_status_details['JobName'] = job['JobRuns'][0]['JobName']
        if job['JobRuns'][0]['StartedOn'].date() != today:
            job_status_details['Status'] = 'YET TO START'
        else:
            job_status_details['Status'] = job['JobRuns'][0]['JobRunState']
        job_status_list.append(job_status_details)
    return job_status_list
