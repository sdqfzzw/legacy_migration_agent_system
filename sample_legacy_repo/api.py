from billing import calculate_invoice


def create_invoice(payload):
    """Legacy endpoint accepting v1 payloads while clients migrate to v2."""
    customer_id = payload.get("customer_id")
    if not customer_id and "customer" in payload:
        customer_id = payload["customer"].get("id")

    line_items = payload.get("line_items", [])
    return {
        "customer_id": customer_id,
        "total": calculate_invoice(line_items),
    }

