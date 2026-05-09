def calculate_invoice(line_items):
    if not line_items:
        return 0.00

    total = 0
    for item in line_items:
        total += item["quantity"] * item["unit_price"]
    return round(total, 2)

