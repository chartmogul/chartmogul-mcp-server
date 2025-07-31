# ChartMogul's MCP Server

## Supported Tools

### Account & Data Sources
- `retrieve_account` - Get account information
- `list_sources` - List all data sources with optional filtering
- `retrieve_source` - Get specific data source by UUID

### Customer Management
- `list_customers` - List customers with filtering options
- `search_customers` - Search customers by email
- `retrieve_customer` - Get customer by UUID
- `create_customer` - Create new customer
- `update_customer` - Update customer attributes
- `list_customer_subscriptions` - Get customer's subscriptions
- `list_customer_activities` - Get customer activities
- `list_customer_attributes` - Get customer attributes
- `add_customer_tags` - Add tags to customer
- `add_customer_custom_attributes` - Add custom attributes to customer

### Contacts
- `list_contacts` - List all contacts
- `retrieve_contact` - Get contact by UUID
- `create_contact` - Create new contact
- `update_contact` - Update contact information

### Customer Notes
- `list_customer_notes` - List customer notes and calls
- `retrieve_customer_note` - Get specific note by UUID
- `create_customer_note` - Create new note or call log
- `update_customer_note` - Update existing note

### Sales & CRM
- `list_opportunities` - List sales opportunities
- `retrieve_opportunity` - Get opportunity by UUID
- `create_opportunity` - Create new opportunity
- `update_opportunity` - Update opportunity details
- `list_tasks` - List customer tasks
- `retrieve_task` - Get task by UUID
- `create_task` - Create new task
- `update_task` - Update task information

### Plans
- `list_plans` - List subscription plans
- `retrieve_plan` - Get plan by UUID
- `create_plan` - Create new plan
- `update_plan` - Update plan details
- `list_plan_groups` - List plan groups
- `retrieve_plan_group` - Get plan group by UUID
- `create_plan_group` - Create new plan group
- `update_plan_group` - Update plan group
- `list_plan_group_plans` - List plans in a group

### Analytics & Metrics
- `all_metrics` - Get all key metrics (MRR, ARR, ARPA, ASP, customer count, churn rates, LTV)
- `mrr_metrics` - Get Monthly Recurring Revenue metrics
- `arr_metrics` - Get Annual Run Rate metrics
- `arpa_metrics` - Get Average Revenue Per Account metrics
- `asp_metrics` - Get Average Sale Price metrics
- `customer_count_metrics` - Get customer count metrics
- `customer_churn_rate_metrics` - Get customer churn rate metrics
- `mrr_churn_rate_metrics` - Get MRR churn rate metrics
- `ltv_metrics` - Get Customer Lifetime Value metrics

### Data Operations
- `list_subscription_events` - List subscription events
- `create_subscription_event` - Create new subscription event
- `update_subscription_event` - Update subscription event details
- `list_invoices` - List invoices with filtering
- `import_invoices` - Create new invoice
- `retrieve_invoice` - Get invoice by UUID
- `list_activities` - List business activities (new_biz, expansion, churn, etc.)

## Usage
1. Open the Claude Desktop configuration file located at:
   * On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   * On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following:

```json
{
  "mcpServers": {
    "mcp-chartmogul": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/local/chartmogul-mcp-server",
        "run",
        "main.py"
      ],
      "env": {
        "CHARTMOGUL_TOKEN": "<YOUR-CHARTMOGUL-TOKEN>"
      }
    }
  }
}
```

3. Run `which uv` to locate the command entry for `uv` and replace it with the absolute path to the `uv` executable. 

4. Restart Claude Desktop to apply the changes.

## Development

1. Run `cp example.env .env` in the root of the repository to create a `.env` file.

2. Update it with the following env variables.
```bash
CHARTMOGUL_TOKEN=<YOUR-CHARTMOGUL-TOKEN>
```
3. Install `uv` by following the instructions [here](https://docs.astral.sh/uv/).

4. Run `uv sync` to install the dependencies. 

5. Run `source .venv/bin/activate` to activate the created virtual environment.

6. Run `mcp dev main.py:cm_mcp` to start the development MCP server. This command will need Node.js and npm installation.

7. Inspect and connect to the MCP server at http://127.0.0.1:6274
