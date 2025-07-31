import datetime
import chartmogul
from functools import wraps
from chartmogul_mcp import utils
from chartmogul_mcp.utils import LOGGER


def handle_api_errors(operation_name=None):
    """
    Decorator to handle ChartMogul API errors consistently.
    Logs errors and returns None on exceptions.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = operation_name or func.__name__.replace("_", " ")
                LOGGER.error(f"Error {error_msg}: {str(e)}", exc_info=True)
                return None

        return wrapper

    return decorator


def init_chartmogul_config():
    return chartmogul.Config(utils.CHARTMOGUL_TOKEN)


# Account Endpoint

@handle_api_errors("retrieving account")
def retrieve_account(config):
    """
    Retrieve the account information.

    """
    LOGGER.info("Retrieve account information.")
    request = chartmogul.Account.retrieve(config)
    account = parse_object(request.get())
    return account


# Data sources Endpoints

@handle_api_errors("listing data sources")
def list_sources(config, name=None, system=None):
    """
    List all data sources from ChartMogul API.

    Returns: A list of ChartMogul data sources.
    """
    LOGGER.info(f"List data sources {name}, {system}.")
    all_sources = []
    request = chartmogul.DataSource.all(config, name=name, system=system)
    sources = request.get()
    all_sources.extend([parse_object(entry) for entry in sources.data_sources])
    return all_sources


@handle_api_errors("retrieving data source")
def retrieve_source(config, data_source_uuid):
    """
    Retrieve a data source from ChartMogul API.

    Returns: The data source.
    """
    LOGGER.info(f"Retrieve data source for {data_source_uuid}.")
    request = chartmogul.DataSource.retrieve(config, uuid=data_source_uuid)
    source = parse_object(request.get())
    return source


# Customers Endpoints

@handle_api_errors("fetching ChartMogul customers")
def list_customers(
        config, data_source_uuid=None, external_id=None, status=None, system=None, limit=20
) -> list:
    """
    List all customers from ChartMogul API.

    Returns: A list of ChartMogul customers.
    """
    LOGGER.info(f"List customers for {data_source_uuid}, {external_id}, {status}, {system}.")
    all_customers = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Customer.all(config,
                                          data_source_uuid=data_source_uuid,
                                          external_id=external_id,
                                          status=status,
                                          system=system,
                                          cursor=cursor,
                                          per_page=per_page)
        customers = request.get()
        all_customers.extend([parse_object(entry) for entry in customers.entries])
        total += per_page
        has_more = customers.has_more
        cursor = customers.cursor
    return all_customers


@handle_api_errors("creating customer")
def create_customer(config, data):
    """
    Create a customer from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating customer {data}.")
    request = chartmogul.Customer.create(config, data=data)
    customer = parse_object(request.get())
    return customer


@handle_api_errors("retrieving customer")
def retrieve_customer(config, uuid):
    """
    Retrieve a customer from ChartMogul API.

    Returns: The customer.
    """
    LOGGER.info(f"Retrieving customer for {uuid}.")
    request = chartmogul.Customer.retrieve(config, uuid=uuid)
    customer = parse_object(request.get())
    return customer


@handle_api_errors("updating customer")
def update_customer(config, uuid, data):
    """
    Update a customer from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating customer {uuid}, {data}.")
    request = chartmogul.Customer.modify(config, uuid=uuid, data=data)
    customer = parse_object(request.get())
    return customer


@handle_api_errors("searching ChartMogul customers")
def search_customers(config, email, limit=20) -> list:
    """
    Search all customers by email from ChartMogul API.

    Returns: A list of ChartMogul customers.
    """
    LOGGER.info(f"Search customers for {email}.")
    all_customers = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Customer.search(config, email=email, cursor=cursor, per_page=per_page)
        customers = request.get()
        all_customers.extend([parse_object(entry) for entry in customers.entries])
        total += per_page
        has_more = customers.has_more
        cursor = customers.cursor
    return all_customers


@handle_api_errors("fetching customer subscriptions")
def list_customer_subscriptions(config, uuid=None, limit=20) -> list:
    """
    List all subscriptions of a customer from ChartMogul API.

    Returns: A list of ChartMogul subscriptions.
    """
    LOGGER.info(f"List subscriptions for {uuid}.")
    all_subscriptions = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.CustomerSubscription.all(config, uuid=uuid, cursor=cursor, per_page=per_page)
        subscriptions = request.get()
        all_subscriptions.extend([parse_object(entry) for entry in subscriptions.entries])
        total += per_page
        has_more = subscriptions.has_more
        cursor = subscriptions.cursor
    return all_subscriptions


@handle_api_errors("fetching customer activities")
def list_customer_activities(config, uuid=None, limit=20) -> list:
    """
    List all activities of a customer from ChartMogul API.

    Returns: A list of ChartMogul activities.
    """
    LOGGER.info(f"List activities for {uuid}.")
    all_activities = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.CustomerActivity.all(config, uuid=uuid, cursor=cursor, per_page=per_page)
        activities = request.get()
        all_activities.extend([parse_object(entry) for entry in activities.entries])
        total += per_page
        has_more = activities.has_more
        cursor = activities.cursor
    return all_activities


@handle_api_errors("fetching customer attributes")
def list_customer_attributes(config, uuid) -> list:
    """
    List all attributes of a customer from ChartMogul API.

    Returns: A list of ChartMogul attributes.
    """
    LOGGER.info(f"List attributes for {uuid}.")
    request = chartmogul.Attributes.retrieve(config, uuid=uuid)
    attributes = parse_object(request.get())
    return attributes


@handle_api_errors("adding customer tags")
def add_customer_tags(config, uuid, data) -> list:
    """
    Add tags to customer using ChartMogul API.

    Returns: A list of ChartMogul tags added.
    """
    LOGGER.info(f"Add tags for {uuid}, {data}.")
    request = chartmogul.Tags.add(config, uuid=uuid, data={"tags": data})
    tags = parse_object(request.get())
    return tags


@handle_api_errors("adding customer custom attributes")
def add_customer_custom_attributes(config, uuid, data) -> list:
    """
    Add custom attributes to customer using ChartMogul API.

    Returns: A list of ChartMogul custom attributes added.
    """
    LOGGER.info(f"Add custom attributes for {uuid}, {data}.")
    request = chartmogul.CustomAttributes.add(config, uuid=uuid, data={"custom": data})
    custom_attributes = parse_object(request.get())
    return custom_attributes


# Contacts Endpoints

@handle_api_errors("fetching contacts")
def list_contacts(config, email=None, customer_external_id=None, limit=20) -> list:
    """
    List all contacts from ChartMogul API.

    Returns: A list of ChartMogul contacts.
    """
    LOGGER.info(f"List contacts for {email}, {customer_external_id}.")
    all_contacts = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Contact.all(config,
                                         email=email,
                                         customer_external_id=customer_external_id,
                                         cursor=cursor,
                                         per_page=per_page)
        contacts = request.get()
        all_contacts.extend([parse_object(entry) for entry in contacts.entries])
        total += per_page
        has_more = contacts.has_more
        cursor = contacts.cursor
    return all_contacts


@handle_api_errors("retrieving contact")
def retrieve_contact(config, uuid):
    """
    Retrieve a contact from ChartMogul API.

    Returns: The contact.
    """
    LOGGER.info(f"Retrieving contact for {uuid}.")
    request = chartmogul.Contact.retrieve(config, uuid=uuid)
    contact = parse_object(request.get())
    return contact


@handle_api_errors("creating contact")
def create_contact(config, data):
    """
    Create a contact from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating contact {data}.")
    request = chartmogul.Contact.create(config, data=data)
    contact = parse_object(request.get())
    return contact


@handle_api_errors("updating contact")
def update_contact(config, uuid, data):
    """
    Update a contact from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating contact {uuid}, {data}.")
    request = chartmogul.Contact.modify(config, uuid=uuid, data=data)
    contact = parse_object(request.get())
    return contact


# Notes and call logs Endpoints

@handle_api_errors("fetching customer notes")
def list_customer_notes(
        config, customer_uuid=None, type=None, author_email=None, limit=20
) -> list:
    """
    List all customer_notes from ChartMogul API.

    Returns: A list of ChartMogul customer_notes.
    """
    LOGGER.info(f"List customer_notes for {customer_uuid}, {type}, {author_email}.")
    all_customer_notes = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.CustomerNote.all(config,
                                              customer_uuid=customer_uuid,
                                              author_email=author_email,
                                              type=type,
                                              cursor=cursor,
                                              per_page=per_page)
        customer_notes = request.get()
        all_customer_notes.extend([parse_object(entry) for entry in customer_notes.entries])
        total += per_page
        has_more = customer_notes.has_more
        cursor = customer_notes.cursor
    return all_customer_notes


@handle_api_errors("retrieving customer note")
def retrieve_customer_note(config, uuid):
    """
    Retrieve a customer_note from ChartMogul API.

    Returns: The customer_note.
    """
    LOGGER.info(f"Retrieving customer_note for {uuid}.")
    request = chartmogul.CustomerNote.retrieve(config, uuid=uuid)
    customer_note = parse_object(request.get())
    return customer_note


@handle_api_errors("creating customer note")
def create_customer_note(config, data):
    """
    Create a customer_note from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating customer note {data}.")
    request = chartmogul.CustomerNote.create(config, data=data)
    customer_note = parse_object(request.get())
    return customer_note


@handle_api_errors("updating customer note")
def update_customer_note(config, uuid, data):
    """
    Update a customer_note from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating customer_note {uuid}, {data}.")
    request = chartmogul.CustomerNote.patch(config, uuid=uuid, data=data)
    customer_note = parse_object(request.get())
    return customer_note


# Opportunities Endpoints

@handle_api_errors("fetching opportunities")
def list_opportunities(
        config,
        customer_uuid=None,
        owner=None,
        pipeline=None,
        pipeline_stage=None,
        estimated_close_date_on_or_after=None,
        estimated_close_date_on_or_before=None,
        limit=20,
) -> list:
    """
    List all opportunities from ChartMogul API.

    Returns: A list of ChartMogul opportunities.
    """
    LOGGER.info(f"List opportunities for {customer_uuid}, {owner}, {pipeline}, {pipeline_stage}, "
                f"{estimated_close_date_on_or_after}, {estimated_close_date_on_or_before}.")
    all_opportunities = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Opportunity.all(config,
                                             customer_uuid=customer_uuid,
                                             owner=owner,
                                             pipeline=pipeline,
                                             pipeline_stage=pipeline_stage,
                                             estimated_close_date_on_or_after=estimated_close_date_on_or_after,
                                             estimated_close_date_on_or_before=estimated_close_date_on_or_before,
                                             cursor=cursor,
                                             per_page=per_page)
        opportunities = request.get()
        all_opportunities.extend([parse_object(entry) for entry in opportunities.entries])
        total += per_page
        has_more = opportunities.has_more
        cursor = opportunities.cursor
    return all_opportunities


@handle_api_errors("retrieving opportunity")
def retrieve_opportunity(config, uuid):
    """
    Retrieve a opportunity from ChartMogul API.

    Returns: The opportunity.
    """
    LOGGER.info(f"Retrieving opportunity for {uuid}.")
    request = chartmogul.Opportunity.retrieve(config, uuid=uuid)
    opportunity = parse_object(request.get())
    return opportunity


@handle_api_errors("creating opportunity")
def create_opportunity(config, data):
    """
    Create a opportunity from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating opportunity {data}.")
    request = chartmogul.Opportunity.create(config, data=data)
    opportunity = parse_object(request.get())
    return opportunity


@handle_api_errors("updating opportunity")
def update_opportunity(config, uuid, data):
    """
    Update a opportunity from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating opportunity {uuid}, {data}.")
    request = chartmogul.Opportunity.patch(config, uuid=uuid, data=data)
    opportunity = parse_object(request.get())
    return opportunity


# Plans Endpoints

@handle_api_errors("fetching plans")
def list_plans(
        config, data_source_uuid=None, external_id=None, system=None, limit=20
) -> list:
    """
    List all plans from ChartMogul API.

    Returns: A list of ChartMogul plans.
    """
    LOGGER.info(f"List plans for {data_source_uuid}, {external_id}, {system}.")
    all_plans = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Plan.all(config,
                                      data_source_uuid=data_source_uuid,
                                      external_id=external_id,
                                      system=system,
                                      cursor=cursor,
                                      per_page=per_page)
        plans = request.get()
        all_plans.extend([parse_object(entry) for entry in plans.plans])
        total += per_page
        has_more = plans.has_more
        cursor = plans.cursor
    return all_plans


@handle_api_errors("retrieving plan")
def retrieve_plan(config, uuid):
    """
    Retrieve a plan from ChartMogul API.

    Returns: The plan.
    """
    LOGGER.info(f"Retrieving plan for {uuid}.")
    request = chartmogul.Plan.retrieve(config, uuid=uuid)
    plan = parse_object(request.get())
    return plan


@handle_api_errors("creating plan")
def create_plan(config, data):
    """
    Create a plan from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating plan {data}.")
    request = chartmogul.Plan.create(config, data=data)
    plan = parse_object(request.get())
    return plan


@handle_api_errors("updating plan")
def update_plan(config, uuid, data):
    """
    Update a plan from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating plan {uuid}, {data}.")
    request = chartmogul.Plan.modify(config, uuid=uuid, data=data)
    plan = parse_object(request.get())
    return plan


# Plan groups Endpoints

@handle_api_errors("fetching plan groups")
def list_plan_groups(config, limit=20) -> list:
    """
    List all plan groups from ChartMogul API.

    Returns: A list of ChartMogul plan groups.
    """
    LOGGER.info("List plan groups.")
    all_plan_groups = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.PlanGroup.all(config, cursor=cursor, per_page=per_page)
        plan_groups = request.get()
        all_plan_groups.extend([parse_object(entry) for entry in plan_groups.plan_groups])
        total += per_page
        has_more = plan_groups.has_more
        cursor = plan_groups.cursor
    return all_plan_groups


@handle_api_errors("fetching plan group plans")
def list_plan_group_plans(config, uuid, limit=20) -> list:
    """
    List all plans of a plan group from ChartMogul API.

    Returns: A list of ChartMogul plans of a plan group.
    """
    LOGGER.info(f"List plans of a plan group {uuid}.")
    all_plans = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.PlanGroup.all(config, uuid=uuid, cursor=cursor, per_page=per_page)
        plans = request.get()
        all_plans.extend([parse_object(entry) for entry in plans.plans])
        total += per_page
        has_more = plans.has_more
        cursor = plans.cursor
    return all_plans


@handle_api_errors("retrieving plan group")
def retrieve_plan_group(config, uuid):
    """
    Retrieve a plan group from ChartMogul API.

    Returns: The plan.
    """
    LOGGER.info(f"Retrieving plan group for {uuid}.")
    request = chartmogul.PlanGroup.retrieve(config, uuid=uuid)
    plan_group = parse_object(request.get())
    return plan_group


@handle_api_errors("creating plan group")
def create_plan_group(config, data):
    """
    Create a plan group from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating plan group {data}.")
    request = chartmogul.PlanGroup.create(config, data=data)
    plan_group = parse_object(request.get())
    return plan_group


@handle_api_errors("updating plan group")
def update_plan_group(config, uuid, data):
    """
    Update a plan group from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating plan group {uuid}, {data}.")
    request = chartmogul.PlanGroup.modify(config, uuid=uuid, data=data)
    plan_group = parse_object(request.get())
    return plan_group


# Tasks Endpoints

@handle_api_errors("fetching tasks")
def list_tasks(
        config,
        customer_uuid=None,
        assignee=None,
        due_date_on_or_after=None,
        estimated_close_date_on_or_before=None,
        completed=None,
        limit=20,
) -> list:
    """
    List all tasks from ChartMogul API.

    Returns: A list of ChartMogul tasks.
    """
    LOGGER.info(
        f"List tasks for {customer_uuid}, {assignee}, {due_date_on_or_after}, {estimated_close_date_on_or_before}, "
        f"{completed}.")
    all_tasks = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Task.all(config,
                                      customer_uuid=customer_uuid,
                                      assignee=assignee,
                                      due_date_on_or_after=due_date_on_or_after,
                                      estimated_close_date_on_or_before=estimated_close_date_on_or_before,
                                      completed=completed,
                                      cursor=cursor,
                                      per_page=per_page)
        tasks = request.get()
        all_tasks.extend([parse_object(entry) for entry in tasks.entries])
        total += per_page
        has_more = tasks.has_more
        cursor = tasks.cursor
    return all_tasks


@handle_api_errors("retrieving task")
def retrieve_task(config, uuid):
    """
    Retrieve a task from ChartMogul API.

    Returns: The task.
    """
    LOGGER.info(f"Retrieving task for {uuid}.")
    request = chartmogul.Task.retrieve(config, uuid=uuid)
    task = parse_object(request.get())
    return task


@handle_api_errors("creating task")
def create_task(config, data):
    """
    Create a task from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating task {data}.")
    request = chartmogul.Task.create(config, data=data)
    task = parse_object(request.get())
    return task


@handle_api_errors("updating task")
def update_task(config, uuid, data):
    """
    Update a task from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating task {uuid}, {data}.")
    request = chartmogul.Task.patch(config, uuid=uuid, data=data)
    task = parse_object(request.get())
    return task


# Metrics API Endpoints

@handle_api_errors("fetching all metrics")
def all_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List all metrics from ChartMogul API.

    Returns: A list of all metrics.
    """
    LOGGER.info(f"Fetching all metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.all(config,
                                     start_date=start_date,
                                     end_date=end_date,
                                     interval=interval,
                                     geo=geo,
                                     plans=plans
                                     )
    metrics = request.get()
    all_metrics = [parse_object(entry) for entry in metrics.entries]
    return all_metrics


@handle_api_errors("fetching MRR metrics")
def mrr_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List MRR metrics from ChartMogul API.

    Returns: A list of MRR metrics.
    """
    LOGGER.info(f"Fetching MRR metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.mrr(config,
                                     start_date=start_date,
                                     end_date=end_date,
                                     interval=interval,
                                     geo=geo,
                                     plans=plans
                                     )
    mrr = request.get()
    all_mrr = [parse_object(entry) for entry in mrr.entries]
    return all_mrr


@handle_api_errors("fetching ARR metrics")
def arr_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List ARR metrics from ChartMogul API.

    Returns: A list of ARR metrics.
    """
    LOGGER.info(f"Fetching ARR metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.arr(config,
                                     start_date=start_date,
                                     end_date=end_date,
                                     interval=interval,
                                     geo=geo,
                                     plans=plans
                                     )
    arr = request.get()
    all_arr = [parse_object(entry) for entry in arr.entries]
    return all_arr


@handle_api_errors("fetching ARPA metrics")
def arpa_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List ARPA metrics from ChartMogul API.

    Returns: A list of ARPA metrics.
    """
    LOGGER.info(f"Fetching ARPA metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.arpa(config,
                                      start_date=start_date,
                                      end_date=end_date,
                                      interval=interval,
                                      geo=geo,
                                      plans=plans
                                      )
    arpa = request.get()
    all_arpa = [parse_object(entry) for entry in arpa.entries]
    return all_arpa


@handle_api_errors("fetching ASP metrics")
def asp_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List ASP metrics from ChartMogul API.

    Returns: A list of ASP metrics.
    """
    LOGGER.info(f"Fetching ASP metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.asp(config,
                                     start_date=start_date,
                                     end_date=end_date,
                                     interval=interval,
                                     geo=geo,
                                     plans=plans
                                     )
    asp = request.get()
    all_asp = [parse_object(entry) for entry in asp.entries]
    return all_asp


@handle_api_errors("fetching customer count metrics")
def customer_count_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List Customer count metrics from ChartMogul API.

    Returns: A list of Customer count metrics.
    """
    LOGGER.info(f"Fetching Customer count metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.customer_count(config,
                                                start_date=start_date,
                                                end_date=end_date,
                                                interval=interval,
                                                geo=geo,
                                                plans=plans
                                                )
    customer_count = request.get()
    all_customer_count = [parse_object(entry) for entry in customer_count.entries]
    return all_customer_count


@handle_api_errors("fetching customer churn rate metrics")
def customer_churn_rate_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List Customer churn rate metrics from ChartMogul API.

    Returns: A list of Customer churn rate metrics.
    """
    LOGGER.info(f"Fetching Customer churn rate metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.customer_churn_rate(config,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     interval=interval,
                                                     geo=geo,
                                                     plans=plans
                                                     )
    customer_churn_rate = request.get()
    all_customer_churn_rate = [parse_object(entry) for entry in customer_churn_rate.entries]
    return all_customer_churn_rate


@handle_api_errors("fetching MRR churn rate metrics")
def mrr_churn_rate_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List MRR churn rate metrics from ChartMogul API.

    Returns: A list of MRR churn rate metrics.
    """
    LOGGER.info(f"Fetching MRR churn rate metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.mrr_churn_rate(config,
                                                start_date=start_date,
                                                end_date=end_date,
                                                interval=interval,
                                                geo=geo,
                                                plans=plans
                                                )
    mrr_churn_rate = request.get()
    all_mrr_churn_rate = [parse_object(entry) for entry in mrr_churn_rate.entries]
    return all_mrr_churn_rate


@handle_api_errors("fetching LTV metrics")
def ltv_metrics(config, start_date, end_date, interval, geo=None, plans=None) -> list:
    """
    List LTV metrics from ChartMogul API.

    Returns: A list of LTV metrics.
    """
    LOGGER.info(f"Fetching LTV metrics for {start_date}, {end_date}, {interval}, {geo}, {plans}.")
    request = chartmogul.Metrics.ltv(config,
                                     start_date=start_date,
                                     end_date=end_date,
                                     interval=interval,
                                     geo=geo,
                                     plans=plans
                                     )
    ltv = request.get()
    all_ltv = [parse_object(entry) for entry in ltv.entries]
    return all_ltv


# Subscription Events

@handle_api_errors("fetching subscription events")
def list_subscription_events(
        config,
        data_source_uuid=None,
        external_id=None,
        customer_external_id=None,
        subscription_external_id=None,
        event_type=None,
        event_date=None,
        effective_date=None,
        plan_external_id=None,
        limit=20,
) -> list:
    """
    List all subscription events from ChartMogul API.

    Returns: A list of ChartMogul subscription events.
    """
    LOGGER.info(
        f"List subscription events for {data_source_uuid}, {external_id}, {customer_external_id}, {event_type}, "
        f"{subscription_external_id}, {event_date}, {effective_date}, {plan_external_id}.")
    all_subscription_events = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.SubscriptionEvent.all(config,
                                                   data_source_uuid=data_source_uuid,
                                                   external_id=external_id,
                                                   customer_external_id=customer_external_id,
                                                   subscription_external_id=subscription_external_id,
                                                   event_type=event_type,
                                                   event_date=event_date,
                                                   effective_date=effective_date,
                                                   plan_external_id=plan_external_id,
                                                   cursor=cursor,
                                                   per_page=per_page)
        subscription_events = request.get()
        all_subscription_events.extend([parse_object(entry) for entry in subscription_events.subscription_events])
        total += per_page
        has_more = subscription_events.has_more
        cursor = subscription_events.cursor
    return all_subscription_events


@handle_api_errors("creating subscription event")
def create_subscription_event(config, data):
    """
    Create a subscription_event from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating subscription_event {data}.")
    request = chartmogul.SubscriptionEvent.create(config, data={"subscription_event": data})
    subscription_event = parse_object(request.get())
    return subscription_event


@handle_api_errors("updating subscription event")
def update_subscription_event(config, data):
    """
    Update a subscription_event from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating subscription_event {data}.")
    request = chartmogul.SubscriptionEvent.modify_with_params(config, data={"subscription_event": data})
    subscription_event = parse_object(request.get())
    return subscription_event


# Invoices

@handle_api_errors("fetching invoices")
def list_invoices(
        config,
        data_source_uuid=None,
        external_id=None,
        customer_uuid=None,
        validation_type=None,
        limit=20,
) -> list:
    """
    List all invoices from ChartMogul API.

    Returns: A list of ChartMogul invoices.
    """
    LOGGER.info(f"List invoices for {data_source_uuid}, {external_id}, {customer_uuid}, {validation_type}.")
    all_invoices = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Invoice.all(config,
                                         data_source_uuid=data_source_uuid,
                                         external_id=external_id,
                                         customer_uuid=customer_uuid,
                                         validation_type=validation_type,
                                         cursor=cursor,
                                         per_page=per_page)
        invoices = request.get()
        all_invoices.extend([parse_object(entry) for entry in invoices.invoices])
        total += per_page
        has_more = invoices.has_more
        cursor = invoices.cursor
    return all_invoices


@handle_api_errors("importing invoices")
def import_invoices(config, data, uuid):
    """
    Import invoices into ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Importing invoices {data}, {uuid}.")
    request = chartmogul.Invoice.create(config, data=data, uuid=uuid)
    invoice = parse_object(request.get())
    return invoice


@handle_api_errors("retrieving invoice")
def retrieve_invoice(config, uuid, validation_type):
    """
    Retrieve an invoice from ChartMogul API.

    Returns: The invoice.
    """
    LOGGER.info(f"Retrieving invoice for {uuid}, {validation_type}.")
    request = chartmogul.Invoice.retrieve(config, uuid=uuid, validation_type=validation_type)
    invoice = parse_object(request.get())
    return invoice


# Activities

@handle_api_errors("fetching activities")
def list_activities(
        config, start_date=None, end_date=None, type=None, order=None, limit=20
) -> list:
    """
    List all activities from ChartMogul API.

    Returns: A list of ChartMogul activities.
    """
    LOGGER.info(f"List activities for {start_date}, {end_date}, {type}, {order}.")
    all_activities = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.Activity.all(config,
                                          start_date=start_date,
                                          end_date=end_date,
                                          type=type,
                                          order=order,
                                          cursor=cursor,
                                          per_page=per_page)
        activities = request.get()
        all_activities.extend([parse_object(entry) for entry in activities.entries])
        total += per_page
        has_more = activities.has_more
        cursor = activities.cursor
    return all_activities


def parse_object(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            result[key] = parse_object(value)
        return result
    elif isinstance(obj, list):
        return [parse_object(item) for item in obj]
    else:
        return obj