# API v2 Contract

Invoice creation now sends customer information as `customer.id`.

The migration must preserve compatibility with the legacy `customer_id` root field until all downstream services are upgraded.

