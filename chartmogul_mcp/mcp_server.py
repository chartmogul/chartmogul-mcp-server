import sys
import datetime
from typing import Dict
from mcp.server.fastmcp import FastMCP
from chartmogul_mcp import api_client
from chartmogul_mcp import utils
from chartmogul_mcp.utils import LOGGER
from dotenv import load_dotenv


class ChartMogulMcp:

    def __init__(self):
        load_dotenv()

        # Initialize MCP Server
        self.mcp = FastMCP(utils.MCP_SERVER_NAME, deps=utils.DEPENDENCIES)
        LOGGER.info("ChartMogul MCP Server initialized")

        self.config = api_client.init_chartmogul_config()

        # Register MCP tools
        self._register_tools()


    def _register_tools(self):
        """Register MCP tools to interact with ChartMogul API."""

        ## Account - ChartMogul Account Information
        @self.mcp.tool(name='retrieve_account',
                       description='[ChartMogul API] Retrieve your ChartMogul account information. Returns complete '
                                   'account object with: id (string: account UUID with acc_ prefix like '
                                   '"acc_93b06efd-30f0-2153-890f-709a64cf8292"), name (string: company name), '
                                   'currency (string: ISO 4217 format like "USD", "EUR"), time_zone (string: TZ '
                                   'identifier like "Europe/Berlin"), week_start_on (string: "monday" or "sunday"). '
                                   'No parameters required. Example response: {"id": "acc_93b06...", "name": "ChartMogul", '
                                   '"currency": "USD", "time_zone": "Europe/Berlin", "week_start_on": "monday"}')
        async def retrieve_account() -> Dict:
            return api_client.retrieve_account(self.config)

        ## Data Sources - ChartMogul Billing System Connections
        @self.mcp.tool(name='list_sources',
                       description='[ChartMogul API] List data sources (billing systems connected to ChartMogul like '
                                   'Stripe, Recurly, Custom API). Returns array of data source objects with: uuid (string: '
                                   'data source UUID with ds_ prefix), name (string), created_at (ISO 8601 datetime), '
                                   'status (string), system (string: billing system type). FILTERS: name (string: exact '
                                   'match), system (string: billing system type like "Stripe", "Recurly", "Custom" - '
                                   'case-sensitive). Use data_source_uuid from results to filter other endpoints. '
                                   'Example: system="Stripe" or name="My Custom Source"')
        async def list_sources(name: str = None, system: str = None) -> list:
            return api_client.list_sources(self.config, name, system)

        @self.mcp.tool(name='retrieve_source',
                       description='[ChartMogul API] Retrieve specific data source by UUID. Returns complete data source '
                                   'object with: uuid (string: ds_ prefix), name (string), created_at (ISO 8601 datetime), '
                                   'status (string), system (string: billing system type). REQUIRED: uuid (string: data '
                                   'source UUID like "ds_fef05d54-47b4-431b-aed2-eb6b9e545430")')
        async def retrieve_source(uuid: str) -> Dict:
            return api_client.retrieve_source(self.config, uuid)

        ## Customers - ChartMogul Customer Management
        @self.mcp.tool(name='list_customers',
                       description='[ChartMogul API] List customers with optional filtering. LIMIT WARNING: Default limit 20. '
                                   'Discourage requesting more than 20 items to avoid excessive token usage. '
                                   'Returns customer objects with: id (integer: internal ChartMogul ID), '
                                   'uuid (string: customer UUID with cus_ prefix), external_id (string: your system ID), '
                                   'name (string: customer/company name), email (string), status (string: '
                                   'New_Lead/Working_Lead/Qualified_Lead/Unqualified_Lead/Active/Past_Due/Cancelled), '
                                   'customer_since (ISO 8601 datetime), attributes (object with tags array of strings and '
                                   'custom object with key-value pairs), address (object with address_zip, city, state, country), '
                                   'data_source_uuid (string), data_source_uuids (array), external_ids (array), company (string), '
                                   'country (string: ISO-3166 alpha-2), state (string), city (string), zip (string), '
                                   'lead_created_at (ISO 8601 datetime or null), free_trial_started_at (ISO 8601 datetime or null), '
                                   'mrr (INTEGER CENTS - divide by 100 for actual amount), arr (INTEGER CENTS - divide by 100), '
                                   'billing_system_url (string), chartmogul_url (string), billing_system_type (string), '
                                   'currency (string), currency_sign (string). FILTERS: data_source_uuid (string), '
                                   'external_id (string), status (string: exact match from status values above), '
                                   'system (string: billing system type, case-sensitive). Response includes cursor (string) '
                                   'and has_more (boolean) for pagination. Example: status="Active", system="Stripe"')
        async def list_customers(data_source_uuid: str = None, external_id: str = None, status: str = None,
                                 system: str = None, limit: int = 20) -> list:
            return api_client.list_customers(self.config, data_source_uuid, external_id, status, system, limit)

        @self.mcp.tool(name='search_customers',
                       description='[ChartMogul API] Search customers by email address. LIMIT WARNING: Default limit 20. '
                                   'Discourage requesting more than 20 items to avoid excessive token usage. '
                                   'Returns same customer object structure as list_customers. CRITICAL: mrr/arr values are '
                                   'INTEGER CENTS - divide by 100 for actual currency amounts. Example: mrr=3000 means $30.00. '
                                   'REQUIRED: email (string: exact match like "[email protected]")')
        async def search_customers(email: str, limit: int = 20) -> list:
            return api_client.search_customers(self.config, email, limit)

        @self.mcp.tool(name='retrieve_customer',
                       description='[ChartMogul API] Retrieve specific customer by UUID. Returns complete customer object '
                                   'with all fields from list_customers plus additional nested objects. Key fields: '
                                   'attributes.tags (array of strings like ["vip", "enterprise"]), attributes.custom '
                                   '(object with custom attributes like {"CAC": 213, "channel": "Facebook"}), attributes.stripe '
                                   '(object with Stripe metadata), attributes.clearbit (object with company data), '
                                   'address (object with full address details). CRITICAL: mrr/arr are INTEGER CENTS. '
                                   'REQUIRED: uuid (string: customer UUID with cus_ prefix like "cus_de305d54-75b4-431b-adb2-eb6b9e546012")')
        async def retrieve_customer(uuid: str) -> Dict:
            return api_client.retrieve_customer(self.config, uuid)

        @self.mcp.tool(name='create_customer',
                       description='[ChartMogul API] Create new customer. REQUIRED: data_source_uuid (string: ds_ prefix), '
                                   'external_id (string: your system ID). OPTIONAL: company (string), country (string: '
                                   'ISO-3166 alpha-2 like "US", "DE"), state (string: US states ISO-3166-2 like "US-CA", "US-NY"), '
                                   'city (string), zip (string), lead_created_at (string: ISO 8601 datetime in past), '
                                   'free_trial_started_at (string: ISO 8601), attributes (object with tags array and custom array), '
                                   'owner (string: email), primary_contact (object with first_name, last_name, email, title, '
                                   'phone, linked_in, twitter, notes), website_url (string). Custom attributes format: '
                                   'array of objects with type/key/value/source. Custom types: String (max 255 chars), Integer, '
                                   'Decimal, Timestamp (ISO 8601), Boolean. All fields in data dict. Returns created customer object.')
        async def create_customer(data: dict) -> Dict:
            return api_client.create_customer(self.config, data)

        @self.mcp.tool(name='update_customer',
                       description='[ChartMogul API] Update customer attributes. MODIFIABLE: company, lead_created_at, '
                                   'free_trial_started_at, zip, city, state, country, attributes (nested tags/custom), '
                                   'owner, primary_contact, status, website_url. Provide updates in data dict. '
                                   'attributes format: {"tags": ["new", "tags"], "custom": [{"type": "String", "key": "value"}]}. '
                                   'Returns updated customer object with all fields. REQUIRED: uuid (string), data (dict)')
        async def update_customer(uuid: str, data: dict) -> Dict:
            return api_client.update_customer(self.config, uuid, data)

        @self.mcp.tool(name='list_customer_subscriptions',
                       description='[ChartMogul API] List customer subscriptions. Default limit 20 (discourage >20). '
                                   'Returns subscription objects with: id (integer), external_id (string), plan (string: plan name), '
                                   'quantity (integer), uuid (string: subscription UUID), mrr (INTEGER CENTS), arr (INTEGER CENTS), '
                                   'status (string: "active" or "inactive"), billing_cycle (string: "day", "month", "year"), '
                                   'billing_cycle_count (integer), start_date (ISO 8601 datetime), end_date (ISO 8601 datetime), '
                                   'currency (string), currency_sign (string). CRITICAL: mrr/arr are INTEGER CENTS - divide by 100. '
                                   'Example: mrr=70800 means $708.00. Response includes cursor/has_more. '
                                   'REQUIRED: uuid (string: customer UUID)')
        async def list_customer_subscriptions(uuid: str, limit: int = 20) -> list:
            return api_client.list_customer_subscriptions(self.config, uuid, limit)

        @self.mcp.tool(name='list_customer_activities',
                       description='[ChartMogul API] List customer activities (subscription lifecycle events). LIMIT WARNING: '
                                   'Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage.  '
                                   'Returns activity objects with: id (integer), date (ISO 8601 datetime), activity_type (string), '
                                   'description (string), activity_mrr_movement (INTEGER CENTS: change amount), '
                                   'activity_mrr (INTEGER CENTS: total MRR after change), activity_arr (INTEGER CENTS: total ARR), '
                                   'subscription_external_id (string), plan_external_id (string), customer_name (string), '
                                   'customer_uuid (string), customer_external_id (string), billing_connector_type (string). '
                                   'CRITICAL: All monetary values are INTEGER CENTS - divide by 100. Example: activity_mrr=5000 means $50.00. '
                                   'REQUIRED: uuid (string: customer UUID)')
        async def list_customer_activities(uuid: str, limit: int = 20) -> list:
            return api_client.list_customer_activities(self.config, uuid, limit)

        @self.mcp.tool(name='list_customer_attributes',
                       description='[ChartMogul API] Retrieve customer attributes (tags and custom attributes). Returns '
                                   'attributes object with: tags (array of strings like ["vip", "enterprise"]), '
                                   'custom (object with key-value pairs containing type, key, value, source for each attribute '
                                   'like {"CAC": 213, "channel": "Facebook", "pro": true}), stripe (object with Stripe metadata), '
                                   'clearbit (object with company enrichment data). REQUIRED: uuid (string: customer UUID)')
        async def list_customer_attributes(uuid: str) -> list:
            return api_client.list_customer_attributes(self.config, uuid)

        @self.mcp.tool(name='add_customer_tags',
                       description='[ChartMogul API] Add tags to customer (idempotent - no duplicates created). Provide '
                                   'tags as array of strings. New tags added to existing ones. Returns updated tags object. '
                                   'REQUIRED: uuid (string: customer UUID), tags (array: strings like ["vip", "priority"])')
        async def add_customer_tags(uuid: str, tags: list) -> list:
            return api_client.add_customer_tags(self.config, uuid, tags)

        @self.mcp.tool(name='add_customer_custom_attributes',
                       description='[ChartMogul API] Add custom attributes to customer. Each attribute needs: type (string: '
                                   '"String", "Integer", "Decimal", "Timestamp", "Boolean"), key (string: alphanumeric + underscores), '
                                   'value (matching type), optional source (string: defaults to "API"). Provide as array of attribute '
                                   'objects. Custom types details: String (max 255 characters), Integer (numeric only), '
                                   'Decimal (floating point), Timestamp (ISO 8601 format), Boolean (TRUE/true/t/1/FALSE/false/f/0). '
                                   'Returns updated custom attributes. REQUIRED: uuid (string: customer UUID), '
                                   'custom_attributes (array: objects like [{"type": "String", "key": "channel", "value": "Facebook", "source": "integration"}])')
        async def add_customer_custom_attributes(uuid: str, custom_attributes: list) -> list:
            return api_client.add_customer_custom_attributes(self.config, uuid, custom_attributes)

        ## Contacts - ChartMogul Contact Management
        @self.mcp.tool(name='list_contacts',
                       description='[ChartMogul API] List contacts (individuals associated with customers). LIMIT WARNING: '
                                   'Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage. '
                                   'Returns contact objects with: uuid (string: contact UUID), customer_uuid (string), '
                                   'customer_external_id (string), data_source_uuid (string), first_name (string), '
                                   'last_name (string), position (integer: ordering), email (string), phone (string), '
                                   'linked_in (string: URL), twitter (string: URL), notes (string), custom (array: key-value objects). '
                                   'FILTERS: email (string), customer_external_id (string). Response includes cursor/has_more. '
                                   'Example filters: email="[email protected]", customer_external_id="cus_001"')
        async def list_contacts(email: str = None, customer_external_id: str = None, limit: int = 20) -> list:
            return api_client.list_contacts(self.config, email, customer_external_id, limit)

        @self.mcp.tool(name='retrieve_contact',
                       description='[ChartMogul API] Retrieve specific contact by UUID. Returns complete contact object '
                                   'with all fields including customer associations and custom attributes array. '
                                   'REQUIRED: uuid (string: contact UUID)')
        async def retrieve_contact(uuid: str) -> Dict:
            return api_client.retrieve_contact(self.config, uuid)

        @self.mcp.tool(name='update_contact',
                       description='[ChartMogul API] Update contact information. MODIFIABLE: first_name, last_name, position, '
                                   'title, email, phone, linked_in, twitter, notes, custom (array of key-value objects). '
                                   'Custom format: [{"key": "department", "value": "Sales"}]. Provide in data dict. '
                                   'Returns updated contact object. REQUIRED: uuid (string), data (dict)')
        async def update_contact(uuid: str, data: dict) -> Dict:
            return api_client.update_contact(self.config, uuid, data)

        @self.mcp.tool(name='create_contact',
                       description='[ChartMogul API] Create new contact. REQUIRED: customer_uuid (string), data_source_uuid (string). '
                                   'OPTIONAL: first_name (string), last_name (string), position (integer), title (string), '
                                   'email (string), phone (string), linked_in (string: URL), twitter (string: URL), '
                                   'notes (string), custom (array: key-value objects). All fields in data dict. '
                                   'Returns created contact object.')
        async def create_contact(data: dict) -> Dict:
            return api_client.create_contact(self.config, data)

        ## Customer Notes - ChartMogul Notes and Call Logs
        @self.mcp.tool(name='list_customer_notes',
                       description='[ChartMogul API] List customer notes and call logs. LIMIT WARNING: Default limit 20. '
                                   'Discourage requesting more than 20 items to avoid excessive token usage. Returns '
                                   'note objects with: uuid (string: note UUID), customer_uuid (string), type (string: "note" or "call"), '
                                   'author (string), text (string), call_duration (integer: seconds for type "call"), '
                                   'created_at (ISO 8601 datetime), updated_at (ISO 8601 datetime). FILTERS: customer_uuid (string), '
                                   'type (string: "note" or "call"). Response includes cursor/has_more. '
                                   'Example: type="call", customer_uuid="cus_123..."')
        async def list_customer_notes(customer_uuid: str = None, type: str = None, limit: int = 20) -> list:
            return api_client.list_customer_notes(self.config, customer_uuid, type, limit)

        @self.mcp.tool(name='retrieve_customer_note',
                       description='[ChartMogul API] Retrieve specific customer note by UUID. Returns complete note object '
                                   'with all details including timestamps. REQUIRED: uuid (string: note UUID)')
        async def retrieve_customer_note(uuid: str) -> Dict:
            return api_client.retrieve_customer_note(self.config, uuid)

        @self.mcp.tool(name='update_customer_note',
                       description='[ChartMogul API] Update customer note/call log. MODIFIABLE: author_email (string), '
                                   'text (string), call_duration (integer: seconds for type "call"), created_at (string: ISO 8601), '
                                   'updated_at (string: ISO 8601). Provide in data dict. Returns updated note object. '
                                   'REQUIRED: uuid (string), data (dict)')
        async def update_customer_note(uuid: str, data: dict) -> Dict:
            return api_client.update_customer_note(self.config, uuid, data)

        @self.mcp.tool(name='create_customer_note',
                       description='[ChartMogul API] Create customer note/call log. REQUIRED: customer_uuid (string), '
                                   'type (string: "call" or "note"). OPTIONAL: author_email (string), text (string), '
                                   'call_duration (integer: seconds for type "call"), created_at (string: ISO 8601). '
                                   'All fields in data dict. Returns created note object.')
        async def create_customer_note(data: dict) -> Dict:
            return api_client.create_customer_note(self.config, data)

        ## Opportunities - ChartMogul CRM Opportunities
        @self.mcp.tool(name='list_opportunities',
                       description='[ChartMogul API] List sales opportunities (CRM feature). LIMIT WARNING: Default limit 20. '
                                   'Discourage requesting more than 20 items to avoid excessive token usage.  Returns '
                                   'opportunity objects with: uuid (string: opportunity UUID like "39351ba6-dea0-11ee-ac96-37b2b3de29af"), '
                                   'customer_uuid (string), owner (string: email), pipeline (string), pipeline_stage (string), '
                                   'estimated_close_date (string: YYYY-MM-DD), amount_in_cents (INTEGER CENTS), currency (string), '
                                   'type (string: "recurring" or "one-time"), forecast_category (string: "pipeline", "best_case", '
                                   '"committed", "lost", "won"), win_likelihood (integer: 0-100), custom (object: key-value pairs '
                                   'like {"seats": 3, "product": "CRM"}), created_at (ISO 8601), updated_at (ISO 8601). '
                                   'CRITICAL: amount_in_cents is INTEGER CENTS - divide by 100. Example: amount_in_cents=100000 means $1,000.00. '
                                   'FILTERS: customer_uuid, owner (email), pipeline, pipeline_stage, estimated_close_date_on_or_after '
                                   '(ISO 8601 date), estimated_close_date_on_or_before')
        async def list_opportunities(customer_uuid: str = None, owner: str = None, pipeline: str = None,
                                     pipeline_stage: str = None,
                                     estimated_close_date_on_or_after: datetime.datetime =None,
                                     estimated_close_date_on_or_before: datetime.datetime =None,
                                     limit: int = 20) -> list:
            return api_client.list_opportunities(self.config, customer_uuid, owner, pipeline, pipeline_stage,
                                                 estimated_close_date_on_or_after, estimated_close_date_on_or_before,
                                                 limit)

        @self.mcp.tool(name='retrieve_opportunity',
                       description='[ChartMogul API] Retrieve specific opportunity by UUID. Returns complete opportunity '
                                   'object with amount_in_cents (INTEGER CENTS - divide by 100), currency, custom attributes. '
                                   'REQUIRED: uuid (string: opportunity UUID)')
        async def retrieve_opportunity(uuid: str) -> Dict:
            return api_client.retrieve_opportunity(self.config, uuid)

        @self.mcp.tool(name='update_opportunity',
                       description='[ChartMogul API] Update sales opportunity. MODIFIABLE: owner (string: email), '
                                   'pipeline (string), pipeline_stage (string), estimated_close_date (string: YYYY-MM-DD), '
                                   'amount_in_cents (integer: amount in cents), currency (string: "USD", "EUR", "GBP"), '
                                   'type (string: "recurring" or "one-time"), forecast_category (string: "pipeline", "best_case", '
                                   '"committed", "lost", "won"), win_likelihood (integer: 0-100), custom (object: key-value pairs). '
                                   'Provide in data dict. Returns updated opportunity object. REQUIRED: uuid (string), data (dict)')
        async def update_opportunity(uuid: str, data: dict) -> Dict:
            return api_client.update_opportunity(self.config, uuid, data)

        @self.mcp.tool(name='create_opportunity',
                       description='[ChartMogul API] Create sales opportunity. REQUIRED: customer_uuid (string), '
                                   'owner (string: email), pipeline (string), pipeline_stage (string), '
                                   'estimated_close_date (string: YYYY-MM-DD), amount_in_cents (integer: amount in cents), '
                                   'currency (string: "USD", "EUR", "GBP"). OPTIONAL: type (string: "recurring" or "one-time"), '
                                   'forecast_category (string: "pipeline", "best_case", "committed", "lost", "won"), '
                                   'win_likelihood (integer: 0-100), custom (object: key-value pairs). All fields in data dict. '
                                   'Returns created opportunity object.')
        async def create_opportunity(data: dict) -> Dict:
            return api_client.create_opportunity(self.config, data)

        ## Plans - ChartMogul Subscription Plans
        @self.mcp.tool(name='list_plans',
                       description='[ChartMogul API] List subscription plans (pricing/billing intervals). LIMIT WARNING: '
                                   'Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage.  '
                                   'Returns plan objects with: uuid (string: plan UUID with pl_ prefix), '
                                   'data_source_uuid (string), name (string), interval_count (integer), '
                                   'interval_unit (string: "day", "month", "year"), external_id (string). '
                                   'FILTERS: data_source_uuid (string), external_id (string), system (string: billing system type). '
                                   'Response includes cursor/has_more. Example: system="Stripe", interval_unit="month"')
        async def list_plans(data_source_uuid: str = None, external_id: str = None, system: str = None,
                             limit: int = 20) -> list:
            return api_client.list_plans(self.config, data_source_uuid, external_id, system, limit)

        @self.mcp.tool(name='retrieve_plan',
                       description='[ChartMogul API] Retrieve specific plan by UUID. Returns complete plan object with '
                                   'uuid, data_source_uuid, name, interval_count, interval_unit, external_id. '
                                   'REQUIRED: uuid (string: plan UUID with pl_ prefix like "pl_eed05d54-75b4-431b-adb2-eb6b9e543206")')
        async def retrieve_plan(uuid: str) -> Dict:
            return api_client.retrieve_plan(self.config, uuid)

        @self.mcp.tool(name='update_plan',
                       description='[ChartMogul API] Update subscription plan. MODIFIABLE: name (string), '
                                   'interval_count (integer >0: billing frequency multiplier, e.g. 6 for half-yearly), '
                                   'interval_unit (string: "day", "month", "year"). Provide in data dict. '
                                   'Returns updated plan object. REQUIRED: uuid (string), data (dict)')
        async def update_plan(uuid: str, data: dict) -> Dict:
            return api_client.update_plan(self.config, uuid, data)

        @self.mcp.tool(name='create_plan',
                       description='[ChartMogul API] Create subscription plan. REQUIRED: data_source_uuid (string), '
                                   'name (string), interval_count (integer >0: billing frequency), '
                                   'interval_unit (string: "day", "month", "year"). OPTIONAL: external_id (string). '
                                   'All fields in data dict. Returns created plan object.')
        async def create_plan(data: dict) -> Dict:
            return api_client.create_plan(self.config, data)

        ## Plan Groups - ChartMogul Plan Groupings
        @self.mcp.tool(name='list_plan_groups',
                       description='[ChartMogul API] List plan groups (logical groupings for reporting). LIMIT WARNING: '
                                   'Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage.  '
                                   'Returns plan group objects with: uuid (string), name (string), plans_count (integer). '
                                   'Response includes cursor/has_more.')
        async def list_plan_groups(limit: int = 20) -> list:
            return api_client.list_plan_groups(self.config, limit)

        @self.mcp.tool(name='list_plan_group_plans',
                       description='[ChartMogul API] List plans within specific plan group. Returns plan objects '
                                   'belonging to the group. REQUIRED: uuid (string: plan group UUID). LIMIT WARNING: '
                                   'Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage. ')
        async def list_plan_group_plans(uuid: str = None, limit: int = 20) -> list:
            return api_client.list_plan_group_plans(self.config, uuid, limit)

        @self.mcp.tool(name='retrieve_plan_group',
                       description='[ChartMogul API] Retrieve specific plan group by UUID. Returns complete plan group '
                                   'object with uuid, name, plans_count, associated plans. '
                                   'REQUIRED: uuid (string: plan group UUID)')
        async def retrieve_plan_group(uuid: str) -> Dict:
            return api_client.retrieve_plan_group(self.config, uuid)

        @self.mcp.tool(name='update_plan_group',
                       description='[ChartMogul API] Update plan group. MODIFIABLE: name (string), '
                                   'plans (array: plan UUIDs to include like ["pl_123...", "pl_456..."]). '
                                   'Provide in data dict. Returns updated plan group object. REQUIRED: uuid (string), data (dict)')
        async def update_plan_group(uuid: str, data: dict) -> Dict:
            return api_client.update_plan_group(self.config, uuid, data)

        @self.mcp.tool(name='create_plan_group',
                       description='[ChartMogul API] Create plan group. REQUIRED: name (string), '
                                   'plans (array: plan UUIDs to include). All fields in data dict. '
                                   'Returns created plan group object.')
        async def create_plan_group(data: dict) -> Dict:
            return api_client.create_plan_group(self.config, data)

        ## Tasks - ChartMogul CRM Tasks
        @self.mcp.tool(name='list_tasks',
                       description='[ChartMogul API] List CRM tasks. LIMIT WARNING: Default limit 20. '
                                   'Discourage requesting more than 20 items to avoid excessive token usage. Returns task objects with: '
                                   'uuid (string: task UUID), customer_uuid (string), task_details (string: max 255 chars), '
                                   'assignee (string: email), due_date (string: ISO 8601 date), completed_at (string: ISO 8601 date or null), '
                                   'created_at (string: ISO 8601 datetime). FILTERS: customer_uuid (string), '
                                   'assignee (string: email), due_date_on_or_after (ISO 8601 date), '
                                   'estimated_close_date_on_or_before (ISO 8601 date), completed (boolean: true/false). '
                                   'Response includes pagination. Example: assignee="[email protected]", completed=false')
        async def list_tasks(customer_uuid: str = None, assignee: str = None,
                             due_date_on_or_after: datetime.datetime = None,
                             estimated_close_date_on_or_before: datetime.datetime = None, completed: bool = None,
                             limit: int = 20) -> list:
            return api_client.list_tasks(self.config, customer_uuid, assignee, due_date_on_or_after,
                                         estimated_close_date_on_or_before, completed, limit)

        @self.mcp.tool(name='retrieve_task',
                       description='[ChartMogul API] Retrieve specific CRM task by UUID. Returns complete task object '
                                   'with all details including customer associations and completion status. '
                                   'REQUIRED: uuid (string: task UUID)')
        async def retrieve_task(uuid: str) -> Dict:
            return api_client.retrieve_task(self.config, uuid)

        @self.mcp.tool(name='update_task',
                       description='[ChartMogul API] Update CRM task. MODIFIABLE: task_details (string: max 255 chars), '
                                   'assignee (string: email), due_date (string: ISO 8601 date), '
                                   'completed_at (string: ISO 8601 date). Provide in data dict. Returns updated task object. '
                                   'REQUIRED: uuid (string), data (dict)')
        async def update_task(uuid: str, data: dict) -> Dict:
            return api_client.update_task(self.config, uuid, data)

        @self.mcp.tool(name='create_task',
                       description='[ChartMogul API] Create CRM task. REQUIRED: customer_uuid (string), '
                                   'task_details (string: max 255 chars), assignee (string: email), '
                                   'due_date (string: ISO 8601 date). OPTIONAL: completed_at (string: ISO 8601 date). '
                                   'All fields in data dict. Returns created task object.')
        async def create_task(data: dict) -> Dict:
            return api_client.create_task(self.config, data)

        ## Metrics API - ChartMogul Analytics
        @self.mcp.tool(name='all_metrics',
                       description='[ChartMogul API] Retrieve all key metrics for time period. CRITICAL: ALL MONETARY VALUES '
                                   '(mrr, arr, arpa, asp, ltv) ARE INTEGER CENTS - DIVIDE BY 100 FOR ACTUAL CURRENCY. '
                                   'Returns entries array with: date (string: YYYY-MM-DD), mrr (integer cents), '
                                   'mrr_percentage_change (float), arr (integer cents), arr_percentage_change (float), '
                                   'customer_churn_rate (float percentage), customer_churn_rate_percentage_change (float), '
                                   'mrr_churn_rate (float percentage), mrr_churn_rate_percentage_change (float), '
                                   'ltv (integer cents), ltv_percentage_change (float), customers (integer count), '
                                   'customers_percentage_change (float), asp (integer cents), asp_percentage_change (float), '
                                   'arpa (integer cents), arpa_percentage_change (float). Plus summary object with '
                                   'current/previous/percentage_change for each metric. REQUIRED: start_date (string: YYYY-MM-DD), '
                                   'end_date (string: YYYY-MM-DD), interval (string: "day", "week", "month", "quarter", "year"). '
                                   'OPTIONAL: geo (string: ISO 3166-1 Alpha-2 comma-separated like "US,GB,DE"), '
                                   'plans (string: plan names/UUIDs/external_ids comma-separated, URL-encode spaces like '
                                   '"Silver%20plan,Gold%20plan,pl_abc123,enterprise_plan"). Example: mrr=36981972 means $369,819.72')
        async def all_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                              plans: str = None) -> list:
            return api_client.all_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='mrr_metrics',
                       description='[ChartMogul API] Retrieve Monthly Recurring Revenue metrics. CRITICAL: ALL MRR VALUES '
                                   'ARE INTEGER CENTS - DIVIDE BY 100 FOR ACTUAL CURRENCY AMOUNTS. Returns entries array with: '
                                   'date (string: YYYY-MM-DD), mrr (integer cents: total MRR), percentage_change (float), '
                                   'mrr_new_business (integer cents: from new customers), mrr_expansion (integer cents: from upgrades), '
                                   'mrr_contraction (integer cents: from downgrades, negative value), '
                                   'mrr_churn (integer cents: from cancellations, negative value), '
                                   'mrr_reactivation (integer cents: from returning customers). Plus summary object. '
                                   'MRR components explained: new_business (new customers), expansion (upgrades), '
                                   'contraction (downgrades excluding cancellations), churn (cancellations), '
                                   'reactivation (previously cancelled returning). REQUIRED: start_date (YYYY-MM-DD), '
                                   'end_date (YYYY-MM-DD), interval ("day", "week", "month", "quarter", "year"). '
                                   'OPTIONAL: geo, plans. Example: mrr=363819722 means $3,638,197.22, mrr_new_business=288938 means $2,889.38')
        async def mrr_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                              plans: str = None) -> list:
            return api_client.mrr_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='arr_metrics',
                       description='[ChartMogul API] Retrieve Annual Recurring Revenue metrics. CRITICAL: ARR VALUES ARE '
                                   'INTEGER CENTS - DIVIDE BY 100 FOR ACTUAL CURRENCY AMOUNTS. ARR = MRR × 12. '
                                   'Returns entries array with: date (string), arr (integer cents), arr_percentage_change (float). '
                                   'Plus summary object. REQUIRED: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), '
                                   'interval ("day", "week", "month", "quarter", "year"). OPTIONAL: geo, plans. '
                                   'Example: arr=4076455668 means $40,764,556.68')
        async def arr_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                              plans: str = None) -> list:
            return api_client.arr_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='arpa_metrics',
                       description='[ChartMogul API] Retrieve Average Revenue Per Account metrics. CRITICAL: ARPA VALUES '
                                   'ARE INTEGER CENTS - DIVIDE BY 100 FOR ACTUAL CURRENCY AMOUNTS. ARPA = Total MRR / Total Customers. '
                                   'Returns entries array with: date (string), arpa (integer cents), arpa_percentage_change (float). '
                                   'Plus summary object. REQUIRED: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), '
                                   'interval ("day", "week", "month", "quarter", "year"). OPTIONAL: geo, plans. '
                                   'Example: arpa=84767 means $847.67 average revenue per account')
        async def arpa_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                               plans: str = None) -> list:
            return api_client.arpa_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='asp_metrics',
                       description='[ChartMogul API] Retrieve Average Sale Price metrics. CRITICAL: ASP VALUES ARE '
                                   'INTEGER CENTS - DIVIDE BY 100 FOR ACTUAL CURRENCY AMOUNTS. ASP = Average first invoice '
                                   'amount of new customers. Returns entries array with: date (string), asp (integer cents), '
                                   'asp_percentage_change (float). Plus summary object. REQUIRED: start_date (YYYY-MM-DD), '
                                   'end_date (YYYY-MM-DD), interval (string: "month", "quarter", "year" ONLY - day/week NOT supported). '
                                   'OPTIONAL: geo, plans. Example: asp=152454 means $1,524.54 average sale price')
        async def asp_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                              plans: str = None) -> list:
            return api_client.asp_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='customer_count_metrics',
                       description='[ChartMogul API] Retrieve customer count metrics (total active customers over time). '
                                   'Returns entries array with: date (string), customers (integer count), '
                                   'customers_percentage_change (float). Plus summary object. REQUIRED: start_date (YYYY-MM-DD), '
                                   'end_date (YYYY-MM-DD), interval ("day", "week", "month", "quarter", "year"). '
                                   'OPTIONAL: geo, plans. Example: customers=382 means 382 active customers')
        async def customer_count_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                                         plans: str = None) -> list:
            return api_client.customer_count_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='customer_churn_rate_metrics',
                       description='[ChartMogul API] Retrieve customer churn rate metrics as percentage. '
                                   'Customer Churn Rate = (Churned Customers / Total Customers at Start) × 100. '
                                   'Returns entries array with: date (string), customer_churn_rate (float percentage), '
                                   'customer_churn_rate_percentage_change (float). Plus summary object. '
                                   'REQUIRED: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), interval ("day", "week", "month", "quarter", "year"). '
                                   'OPTIONAL: geo, plans. Example: customer_churn_rate=3.9 means 3.9% customer churn rate')
        async def customer_churn_rate_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                                              plans: str = None) -> list:
            return api_client.customer_churn_rate_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='mrr_churn_rate_metrics',
                       description='[ChartMogul API] Retrieve Net MRR Churn Rate metrics as percentage. '
                                   'Net MRR Churn = (Churned MRR + Contraction MRR - Expansion MRR) / MRR at Start × 100. '
                                   'IMPORTANT: Negative values indicate net negative churn (expansion > churn - EXCELLENT!). '
                                   'Normal range typically -10% to +10%. Values can exceed 100% or be very negative '
                                   '(e.g., -300% means MRR quadrupled). Returns entries array with: date (string), '
                                   'mrr_churn_rate (float percentage), mrr_churn_rate_percentage_change (float). Plus summary object. '
                                   'REQUIRED: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), interval ("day", "week", "month", "quarter", "year"). '
                                   'OPTIONAL: geo, plans. Example: mrr_churn_rate=-5.2 means -5.2% (net negative churn - good!)')
        async def mrr_churn_rate_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                                         plans: str = None) -> list:
            return api_client.mrr_churn_rate_metrics(self.config, start_date, end_date, interval, geo, plans)

        @self.mcp.tool(name='ltv_metrics',
                       description='[ChartMogul API] Retrieve Customer Lifetime Value metrics. CRITICAL: LTV VALUES ARE '
                                   'INTEGER CENTS - DIVIDE BY 100 FOR ACTUAL CURRENCY AMOUNTS. LTV = Average Revenue Per User / '
                                   'Customer Churn Rate. Returns entries array with: date (string), ltv (integer cents), '
                                   'ltv_percentage_change (float). Plus summary object. REQUIRED: start_date (YYYY-MM-DD), '
                                   'end_date (YYYY-MM-DD), interval (any valid value). OPTIONAL: geo, plans. '
                                   'Example: ltv=2977624 means $29,776.24 customer lifetime value')
        async def ltv_metrics(start_date: str, end_date: str, interval: str, geo: str = None,
                              plans: str = None) -> list:
            return api_client.ltv_metrics(self.config, start_date, end_date, interval, geo, plans)

        ## Subscription Events - ChartMogul Subscription Lifecycle
        @self.mcp.tool(name='list_subscription_events',
                       description='[ChartMogul API] List subscription lifecycle events (track subscription changes). '
                                   'LIMIT WARNING: Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage. '
                                   'Returns subscription event objects with event details, dates, '
                                   'subscription/customer info. FILTERS: data_source_uuid (string), external_id (string), '
                                   'customer_external_id (string), subscription_external_id (string), '
                                   'event_type (string: "subscription_start", "subscription_start_scheduled", '
                                   '"scheduled_subscription_start_retracted", "subscription_cancelled", '
                                   '"subscription_cancellation_scheduled", "scheduled_subscription_cancellation_retracted", '
                                   '"subscription_updated", "subscription_update_scheduled", '
                                   '"scheduled_subscription_update_retracted", "subscription_event_retracted"), '
                                   'event_date (ISO 8601 datetime), effective_date (ISO 8601 datetime), plan_external_id (string). '
                                   'Response includes cursor/has_more. Example: event_type="subscription_start"')
        async def list_subscription_events(data_source_uuid: str = None, external_id: str = None, customer_external_id: str = None,
                                           subscription_external_id: str = None, event_type: str = None,
                                           event_date: datetime.datetime = None,
                                           effective_date: datetime.datetime = None, plan_external_id: str = None,
                                           limit: int = 20) -> list:
            return api_client.list_subscription_events(self.config, data_source_uuid, external_id, customer_external_id,
                                                       subscription_external_id, event_type, event_date, effective_date,
                                                       plan_external_id, limit)

        @self.mcp.tool(name='create_subscription_event',
                       description='[ChartMogul API] Create subscription event for Custom API data sources. Used to track '
                                   'subscription lifecycle changes. Provide subscription_event object with: external_id (string), '
                                   'customer_external_id (string), data_source_uuid (string), event_type (string: from list above), '
                                   'event_date (string: ISO 8601), effective_date (string: ISO 8601), '
                                   'subscription_external_id (string), and other event-specific fields like plan_uuid, quantity. '
                                   'Returns created subscription event object.')
        async def create_subscription_event(data: dict) -> Dict:
            return api_client.create_subscription_event(self.config, data)

        @self.mcp.tool(name='update_subscription_event',
                       description='[ChartMogul API] Update existing subscription event for Custom API data sources. '
                                   'Provide subscription_event object with fields to update. Common updates: effective_date, '
                                   'plan_external_id, quantity, other event attributes. Returns updated subscription event object.')
        async def update_subscription_event(data: dict) -> Dict:
            return api_client.update_subscription_event(self.config, data)

        ## Invoices - ChartMogul Invoice Management
        @self.mcp.tool(name='list_invoices',
                       description='[ChartMogul API] List invoices (contain line items generating subscription revenue). '
                                   'LIMIT WARNING: Default limit 20. Discourage requesting more than 20 items to avoid excessive token usage. '
                                   'Returns invoice objects with: uuid (string: invoice UUID with inv_ prefix), '
                                   'customer_uuid (string), external_id (string), date (string: ISO 8601), '
                                   'due_date (string: ISO 8601), currency (string: 3-letter code), '
                                   'line_items (array: line item objects with uuid, external_id, type ("subscription" or "one_time"), '
                                   'subscription_uuid, subscription_external_id, subscription_set_external_id, plan_uuid, '
                                   'prorated (boolean), service_period_start, service_period_end, amount_in_cents (integer), '
                                   'quantity (integer), discount_code, discount_amount_in_cents (integer), '
                                   'tax_amount_in_cents (integer), transaction_fees_in_cents (integer), '
                                   'transaction_fees_currency, discount_description, event_order (integer), account_code), '
                                   'transactions (array: transaction objects with uuid, external_id, type ("payment" or "refund"), '
                                   'date, result ("successful" or "failed"), amount_in_cents (integer)). '
                                   'FILTERS: data_source_uuid, external_id, customer_uuid, validation_type ("valid", "invalid", "all"). '
                                   'Response includes cursor/has_more.')
        async def list_invoices(data_source_uuid: str = None, external_id: str = None, customer_uuid: str = None,
                                validation_type: str = None, limit: int = 20) -> list:
            return api_client.list_invoices(self.config, data_source_uuid, external_id, customer_uuid, validation_type,
                                            limit)

        @self.mcp.tool(name='import_invoices',
                       description='[ChartMogul API] Import invoices for customer (add historical billing data). '
                                   'Provide invoices data structure with invoices array containing invoice objects: '
                                   'external_id (string), date (string: ISO 8601), currency (string: 3-letter code), '
                                   'due_date (string: ISO 8601), customer_external_id (string), data_source_uuid (string), '
                                   'line_items (array: objects with type ("subscription" or "one_time"), '
                                   'subscription_external_id, subscription_set_external_id, plan_uuid, '
                                   'service_period_start, service_period_end, amount_in_cents (integer), '
                                   'prorated (boolean), proration_type ("differential"), quantity (integer), '
                                   'discount_code, discount_amount_in_cents (integer), tax_amount_in_cents (integer), '
                                   'transaction_fees_in_cents (integer), transaction_fees_currency, discount_description), '
                                   'transactions (array: objects with external_id, type ("payment" or "refund"), '
                                   'date (ISO 8601), result ("successful" or "failed"), amount_in_cents (integer)). '
                                   'Use for Custom API data sources. Returns import summary with created invoices and errors. '
                                   'REQUIRED: data (dict), uuid (string: customer UUID)')
        async def import_invoices(data: dict, uuid: str) -> Dict:
            return api_client.import_invoices(self.config, data, uuid)

        @self.mcp.tool(name='retrieve_invoice',
                       description='[ChartMogul API] Retrieve specific invoice by UUID. Returns complete invoice object '
                                   'with: uuid, customer_uuid, external_id, date, due_date, currency, '
                                   'line_items (array with full line item objects including uuid, external_id, type, '
                                   'subscription_uuid, subscription_external_id, subscription_set_external_id, plan_uuid, '
                                   'prorated, service_period_start, service_period_end, amount_in_cents, quantity, '
                                   'discount_code, discount_amount_in_cents, tax_amount_in_cents, transaction_fees_in_cents, '
                                   'transaction_fees_currency, discount_description, event_order, account_code), '
                                   'transactions (array with full transaction objects including uuid, external_id, type, '
                                   'date, result, amount_in_cents), customer details. Specify validation_type to control '
                                   'included invoices. REQUIRED: uuid (string: invoice UUID), '
                                   'validation_type (string: "valid", "invalid", or "all")')
        async def retrieve_invoice(uuid: str, validation_type: str) -> Dict:
            return api_client.retrieve_invoice(self.config, uuid, validation_type)

        ## Activities - ChartMogul Revenue Activities
        @self.mcp.tool(name='list_activities',
                       description='[ChartMogul API] List customer activities across all customers (revenue movements: '
                                   'new subscriptions, upgrades, downgrades, churn). LIMIT WARNING: Default limit 20. '
                                   'Discourage requesting more than 20 items to avoid excessive token usage.  Returns activity '
                                   'objects with: id (integer), date (string: ISO 8601 datetime), activity_type (string), '
                                   'description (string), activity_mrr_movement (INTEGER CENTS: change amount), '
                                   'activity_mrr (INTEGER CENTS: total MRR after change), activity_arr (INTEGER CENTS: total ARR), '
                                   'subscription_external_id (string), plan_external_id (string), customer_name (string), '
                                   'customer_uuid (string), customer_external_id (string), billing_connector_type (string). '
                                   'CRITICAL: All monetary values are INTEGER CENTS - divide by 100. '
                                   'Example: activity_mrr_movement=5000 means $50.00 increase, activity_mrr=15000 means $150.00 total. '
                                   'FILTERS: start_date (ISO 8601 datetime), end_date (ISO 8601 datetime), '
                                   'type (string: "new_biz", "reactivation", "expansion", "contraction", "churn"), '
                                   'order (string: "-date" for descending, "date" for ascending). Response includes cursor/has_more.')
        async def list_activities(start_date: datetime.datetime = None, end_date: datetime.datetime = None,
                                  type: str = None, order: str = None, limit: int = 20) -> list:
            return api_client.list_activities(self.config, start_date, end_date, type, order, limit)


    def run(self):
        """Start the MCP server."""
        try:
            LOGGER.info("Running MCP Server for ChartMogul API interactions")
            self.mcp.run(transport="stdio")
        except Exception as e:
            LOGGER.error(f"Fatal Error in ChartMogul MCP Server: {str(e)}", exc_info=True)
            sys.exit(1)