import datetime
import chartmogul
from chartmogul_mcp import utils
from chartmogul_mcp.utils import LOGGER


def init_chartmogul_config():
    return chartmogul.Config(utils.CHARTMOGUL_TOKEN)

## Account Endpoint

def retrieve_account(config):
    """
    Retrieve the account information.

    """
    LOGGER.info(f"Retrieve account information.")
    request = chartmogul.Account.retrieve(config)
    try:
        account = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving customer: {str(e)}", exc_info=True)
        return None
    return account


## Data sources Endpoints

def list_sources(config, name=None, system=None):
    """
    List all data sources from ChartMogul API.

    Returns: A list of ChartMogul data sources.
    """
    LOGGER.info(f"List data sources {name}, {system}.")
    all_sources = []
    request = chartmogul.DataSource.all(config, name=name, system=system)
    try:
        sources = request.get()
        all_sources.extend([parse_object(entry) for entry in sources.data_sources])
    except Exception as e:
        LOGGER.error(f"Error listing data sources: {str(e)}", exc_info=True)
        return None
    return all_sources


def retrieve_source(config, data_source_uuid):
    """
    Retrieve a data source from ChartMogul API.

    Returns: The data source.
    """
    LOGGER.info(f"Retrieve data source for {data_source_uuid}.")
    request = chartmogul.DataSource.retrieve(config, uuid=data_source_uuid)
    try:
        source = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving data source: {str(e)}", exc_info=True)
        return None
    return source


## Customers Endpoints

def list_customers(config, data_source_uuid=None, external_id=None, status=None, system=None, limit=20) -> list:
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
        try:
            customers = request.get()
            all_customers.extend([parse_object(entry) for entry in customers.entries])
            total += per_page
            has_more = customers.has_more
            cursor = customers.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul customers: {str(e)}", exc_info=True)
            return None
    return all_customers


def create_customer(config, data):
    """
    Create a customer from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating customer {data}.")
    request = chartmogul.Customer.create(config, data=data)
    try:
        customer = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating customer: {str(e)}", exc_info=True)
        return None
    return customer

def retrieve_customer(config, uuid):
    """
    Retrieve a customer from ChartMogul API.

    Returns: The customer.
    """
    LOGGER.info(f"Retrieving customer for {uuid}.")
    request = chartmogul.Customer.retrieve(config, uuid=uuid)
    try:
        customer = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving customer: {str(e)}", exc_info=True)
        return None
    return customer


def update_customer(config, uuid, data):
    """
    Update a customer from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating customer {uuid}, {data}.")
    request = chartmogul.Customer.modify(config, uuid=uuid, data=data)
    try:
        customer = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating customer: {str(e)}", exc_info=True)
        return None
    return customer


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
        try:
            customers = request.get()
            all_customers.extend([parse_object(entry) for entry in customers.entries])
            total += per_page
            has_more = customers.has_more
            cursor = customers.cursor
        except Exception as e:
            LOGGER.error(f"Error searching ChartMogul customers: {str(e)}", exc_info=True)
            return None
    return all_customers


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
        try:
            subscriptions = request.get()
            all_subscriptions.extend([parse_object(entry) for entry in subscriptions.entries])
            total += per_page
            has_more = subscriptions.has_more
            cursor = subscriptions.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul subscriptions: {str(e)}", exc_info=True)
            return None
    return all_subscriptions


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
        try:
            activities = request.get()
            all_activities.extend([parse_object(entry) for entry in activities.entries])
            total += per_page
            has_more = activities.has_more
            cursor = activities.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul activities: {str(e)}", exc_info=True)
            return None
    return all_activities


def list_customer_attributes(config, uuid) -> list:
    """
    List all attributes of a customer from ChartMogul API.

    Returns: A list of ChartMogul attributes.
    """
    LOGGER.info(f"List attributes for {uuid}.")
    request = chartmogul.Attributes.retrieve(config, uuid=uuid)
    try:
        attributes = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error fetching attributes: {str(e)}", exc_info=True)
        return None
    return attributes


def add_customer_tags(config, uuid, data) -> list:
    """
    Add tags to customer using ChartMogul API.

    Returns: A list of ChartMogul tags added.
    """
    LOGGER.info(f"Add tags for {uuid}, {data}.")
    request = chartmogul.Tags.add(config, uuid=uuid, data={"tags": data})
    try:
        tags = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error adding tags: {str(e)}", exc_info=True)
        return None
    return tags


def add_customer_custom_attributes(config, uuid, data) -> list:
    """
    Add custom attributes to customer using ChartMogul API.

    Returns: A list of ChartMogul custom attributes added.
    """
    LOGGER.info(f"Add custom attributes for {uuid}, {data}.")
    request = chartmogul.CustomAttributes.add(config, uuid=uuid, data={"custom": data})
    try:
        custom_attributes = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error adding custom attributes: {str(e)}", exc_info=True)
        return None
    return custom_attributes


## Contacts Endpoints

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
        try:
            contacts = request.get()
            all_contacts.extend([parse_object(entry) for entry in contacts.entries])
            total += per_page
            has_more = contacts.has_more
            cursor = contacts.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul contacts: {str(e)}", exc_info=True)
            return None
    return all_contacts


def retrieve_contact(config, uuid):
    """
    Retrieve a contact from ChartMogul API.

    Returns: The contact.
    """
    LOGGER.info(f"Retrieving contact for {uuid}.")
    request = chartmogul.Contact.retrieve(config, uuid=uuid)
    try:
        contact = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving contact: {str(e)}", exc_info=True)
        return None
    return contact


def create_contact(config, data):
    """
    Create a contact from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating contact {data}.")
    request = chartmogul.Contact.create(config, data=data)
    try:
        contact = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating contact: {str(e)}", exc_info=True)
        return None
    return contact


def update_contact(config, uuid, data):
    """
    Update a contact from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating contact {uuid}, {data}.")
    request = chartmogul.Contact.modify(config, uuid=uuid, data=data)
    try:
        contact = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating contact: {str(e)}", exc_info=True)
        return None
    return contact


## Notes and call logs Endpoints

def list_customer_notes(config, customer_uuid=None, type=None, author_email=None, limit=20) -> list:
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
        try:
            customer_notes = request.get()
            all_customer_notes.extend([parse_object(entry) for entry in customer_notes.entries])
            total += per_page
            has_more = customer_notes.has_more
            cursor = customer_notes.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul customer_notes: {str(e)}", exc_info=True)
            return None
    return all_customer_notes


def retrieve_customer_note(config, uuid):
    """
    Retrieve a customer_note from ChartMogul API.

    Returns: The customer_note.
    """
    LOGGER.info(f"Retrieving customer_note for {uuid}.")
    request = chartmogul.CustomerNote.retrieve(config, uuid=uuid)
    try:
        customer_note = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving customer_note: {str(e)}", exc_info=True)
        return None
    return customer_note


def create_customer_note(config, data):
    """
    Create a customer_note from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating contact {data}.")
    request = chartmogul.CustomerNote.create(config, data=data)
    try:
        customer_note = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating contact: {str(e)}", exc_info=True)
        return None
    return customer_note


def update_customer_note(config, uuid, data):
    """
    Update a customer_note from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating customer_note {uuid}, {data}.")
    request = chartmogul.CustomerNote.patch(config, uuid=uuid, data=data)
    try:
        customer_note = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating customer_note: {str(e)}", exc_info=True)
        return None
    return customer_note


## Opportunities Endpoints

def list_opportunities(config, customer_uuid=None, owner=None, pipeline=None, pipeline_stage=None,
                       estimated_close_date_on_or_after=None, estimated_close_date_on_or_before=None,
                       limit=20) -> list:
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
        try:
            opportunities = request.get()
            all_opportunities.extend([parse_object(entry) for entry in opportunities.entries])
            total += per_page
            has_more = opportunities.has_more
            cursor = opportunities.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul opportunities: {str(e)}", exc_info=True)
            return None
    return all_opportunities


def retrieve_opportunity(config, uuid):
    """
    Retrieve a opportunity from ChartMogul API.

    Returns: The opportunity.
    """
    LOGGER.info(f"Retrieving opportunity for {uuid}.")
    request = chartmogul.Opportunity.retrieve(config, uuid=uuid)
    try:
        opportunity = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving opportunity: {str(e)}", exc_info=True)
        return None
    return opportunity


def create_opportunity(config, data):
    """
    Create a opportunity from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating opportunity {data}.")
    request = chartmogul.Opportunity.create(config, data=data)
    try:
        opportunity = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating opportunity: {str(e)}", exc_info=True)
        return None
    return opportunity


def update_opportunity(config, uuid, data):
    """
    Update a opportunity from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating opportunity {uuid}, {data}.")
    request = chartmogul.Opportunity.patch(config, uuid=uuid, data=data)
    try:
        opportunity = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating opportunity: {str(e)}", exc_info=True)
        return None
    return opportunity


## Plans Endpoints

def list_plans(config, data_source_uuid=None, external_id=None, system=None, limit=20) -> list:
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
        try:
            plans = request.get()
            all_plans.extend([parse_object(entry) for entry in plans.plans])
            total += per_page
            has_more = plans.has_more
            cursor = plans.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul plans: {str(e)}", exc_info=True)
            return None
    return all_plans


def retrieve_plan(config, uuid):
    """
    Retrieve a plan from ChartMogul API.

    Returns: The plan.
    """
    LOGGER.info(f"Retrieving plan for {uuid}.")
    request = chartmogul.Plan.retrieve(config, uuid=uuid)
    try:
        plan = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving plan: {str(e)}", exc_info=True)
        return None
    return plan


def create_plan(config, data):
    """
    Create a plan from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating plan {data}.")
    request = chartmogul.Plan.create(config, data=data)
    try:
        plan = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating plan: {str(e)}", exc_info=True)
        return None
    return plan


def update_plan(config, uuid, data):
    """
    Update a plan from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating plan {uuid}, {data}.")
    request = chartmogul.Plan.modify(config, uuid=uuid, data=data)
    try:
        plan = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating plan: {str(e)}", exc_info=True)
        return None
    return plan


## Plan groups Endpoints

def list_plan_groups(config, limit=20) -> list:
    """
    List all plan groups from ChartMogul API.

    Returns: A list of ChartMogul plan groups.
    """
    LOGGER.info(f"List plan groups.")
    all_plan_groups = []
    has_more = True
    cursor = None
    per_page = 20
    total = 0
    while has_more and total < limit:
        request = chartmogul.PlanGroup.all(config, cursor=cursor, per_page=per_page)
        try:
            plan_groups = request.get()
            all_plan_groups.extend([parse_object(entry) for entry in plan_groups.plan_groups])
            total += per_page
            has_more = plan_groups.has_more
            cursor = plan_groups.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul plan groups: {str(e)}", exc_info=True)
            return None
    return all_plan_groups


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
        try:
            plans = request.get()
            all_plans.extend([parse_object(entry) for entry in plans.plans])
            total += per_page
            has_more = plans.has_more
            cursor = plans.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul plans: {str(e)}", exc_info=True)
            return None
    return all_plans


def retrieve_plan_group(config, uuid):
    """
    Retrieve a plan group from ChartMogul API.

    Returns: The plan.
    """
    LOGGER.info(f"Retrieving plan group for {uuid}.")
    request = chartmogul.PlanGroup.retrieve(config, uuid=uuid)
    try:
        plan_group = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving plan group: {str(e)}", exc_info=True)
        return None
    return plan_group


def create_plan_group(config, data):
    """
    Create a plan group from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating plan group {data}.")
    request = chartmogul.PlanGroup.create(config, data=data)
    try:
        plan_group = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating plan group: {str(e)}", exc_info=True)
        return None
    return plan_group


def update_plan_group(config, uuid, data):
    """
    Update a plan group from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating plan group {uuid}, {data}.")
    request = chartmogul.PlanGroup.modify(config, uuid=uuid, data=data)
    try:
        plan_group = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating plan group: {str(e)}", exc_info=True)
        return None
    return plan_group



## Tasks Endpoints

def list_tasks(config, customer_uuid=None, assignee=None, due_date_on_or_after=None,
               estimated_close_date_on_or_before=None, completed=None, limit=20) -> list:
    """
    List all tasks from ChartMogul API.

    Returns: A list of ChartMogul tasks.
    """
    LOGGER.info(f"List tasks for {customer_uuid}, {assignee}, {due_date_on_or_after}, {estimated_close_date_on_or_before}, "
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
        try:
            tasks = request.get()
            all_tasks.extend([parse_object(entry) for entry in tasks.entries])
            total += per_page
            has_more = tasks.has_more
            cursor = tasks.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul tasks: {str(e)}", exc_info=True)
            return None
    return all_tasks


def retrieve_task(config, uuid):
    """
    Retrieve a task from ChartMogul API.

    Returns: The task.
    """
    LOGGER.info(f"Retrieving task for {uuid}.")
    request = chartmogul.Task.retrieve(config, uuid=uuid)
    try:
        task = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving task: {str(e)}", exc_info=True)
        return None
    return task


def create_task(config, data):
    """
    Create a task from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating task {data}.")
    request = chartmogul.Task.create(config, data=data)
    try:
        task = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating task: {str(e)}", exc_info=True)
        return None
    return task


def update_task(config, uuid, data):
    """
    Update a task from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating task {uuid}, {data}.")
    request = chartmogul.Task.patch(config, uuid=uuid, data=data)
    try:
        task = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating task: {str(e)}", exc_info=True)
        return None
    return task


## Metrics API Endpoints

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
    try:
        metrics = request.get()
        all_metrics = [parse_object(entry) for entry in metrics.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching all metrics: {str(e)}", exc_info=True)
        return None
    return all_metrics


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
    try:
        mrr = request.get()
        all_mrr = [parse_object(entry) for entry in mrr.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching MRR metrics: {str(e)}", exc_info=True)
        return None
    return all_mrr


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
    try:
        arr = request.get()
        all_arr = [parse_object(entry) for entry in arr.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching ARR metrics: {str(e)}", exc_info=True)
        return None
    return all_arr


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
    try:
        arpa = request.get()
        all_arpa = [parse_object(entry) for entry in arpa.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching ARPA metrics: {str(e)}", exc_info=True)
        return None
    return all_arpa


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
    try:
        asp = request.get()
        all_asp = [parse_object(entry) for entry in asp.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching ASP metrics: {str(e)}", exc_info=True)
        return None
    return all_asp


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
    try:
        customer_count = request.get()
        all_customer_count = [parse_object(entry) for entry in customer_count.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching Customer count metrics: {str(e)}", exc_info=True)
        return None
    return all_customer_count


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
    try:
        customer_churn_rate = request.get()
        all_customer_churn_rate = [parse_object(entry) for entry in customer_churn_rate.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching Customer churn rate metrics: {str(e)}", exc_info=True)
        return None
    return all_customer_churn_rate


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
    try:
        mrr_churn_rate = request.get()
        all_mrr_churn_rate = [parse_object(entry) for entry in mrr_churn_rate.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching MRR churn rate metrics: {str(e)}", exc_info=True)
        return None
    return all_mrr_churn_rate


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
    try:
        ltv = request.get()
        all_ltv = [parse_object(entry) for entry in ltv.entries]
    except Exception as e:
        LOGGER.error(f"Error fetching LTV metrics: {str(e)}", exc_info=True)
        return None
    return all_ltv


## Subscription Events

def list_subscription_events(config, data_source_uuid=None, external_id=None, customer_external_id=None,
                             subscription_external_id=None, event_type=None, event_date=None, effective_date=None,
                             plan_external_id=None, limit=20) -> list:
    """
    List all subscription events from ChartMogul API.

    Returns: A list of ChartMogul subscription events.
    """
    LOGGER.info(f"List subscription events for {data_source_uuid}, {external_id}, {customer_external_id}, {event_type}, "
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
        try:
            subscription_events = request.get()
            all_subscription_events.extend([parse_object(entry) for entry in subscription_events.subscription_events])
            total += per_page
            has_more = subscription_events.has_more
            cursor = subscription_events.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul subscription events: {str(e)}", exc_info=True)
            return None
    return all_subscription_events


def create_subscription_event(config, data):
    """
    Create a subscription_event from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Creating subscription_event {data}.")
    request = chartmogul.SubscriptionEvent.create(config, data={"subscription_event": data})
    try:
        subscription_event = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error creating subscription_event: {str(e)}", exc_info=True)
        return None
    return subscription_event


def update_subscription_event(config, data):
    """
    Update a subscription_event from ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Updating subscription_event {data}.")
    request = chartmogul.SubscriptionEvent.modify_with_params(config, data={"subscription_event": data})
    try:
        subscription_event = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error updating subscription_event: {str(e)}", exc_info=True)
        return None
    return subscription_event

## Invoices

def list_invoices(config, data_source_uuid=None, external_id=None, customer_uuid=None,
                  validation_type=None, limit=20) -> list:
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
        try:
            invoices = request.get()
            all_invoices.extend([parse_object(entry) for entry in invoices.invoices])
            total += per_page
            has_more = invoices.has_more
            cursor = invoices.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul invoices: {str(e)}", exc_info=True)
            return None
    return all_invoices


def import_invoices(config, data, uuid):
    """
    Import invoices into ChartMogul API.

    Returns:
    """
    LOGGER.info(f"Importing invoices {data}, {uuid}.")
    request = chartmogul.Invoice.create(config, data=data, uuid=uuid)
    try:
        invoice = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error importing invoices: {str(e)}", exc_info=True)
        return None
    return invoice


def retrieve_invoice(config, uuid, validation_type):
    """
    Retrieve an invoice from ChartMogul API.

    Returns: The invoice.
    """
    LOGGER.info(f"Retrieving invoice for {uuid}, {validation_type}.")
    request = chartmogul.Invoice.retrieve(config, uuid=uuid, validation_type=validation_type)
    try:
        invoice = parse_object(request.get())
    except Exception as e:
        LOGGER.error(f"Error retrieving invoice: {str(e)}", exc_info=True)
        return None
    return invoice

## Activities

def list_activities(config, start_date=None, end_date=None, type=None, order=None, limit=20) -> list:
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
        try:
            activities = request.get()
            all_activities.extend([parse_object(entry) for entry in activities.entries])
            total += per_page
            has_more = activities.has_more
            cursor = activities.cursor
        except Exception as e:
            LOGGER.error(f"Error fetching ChartMogul activities: {str(e)}", exc_info=True)
            return None
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