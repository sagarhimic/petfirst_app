def total_price(amount, cgst, sgst, service_tax):
    cgst_fee = round((amount * cgst) / 100, 2)
    sgst_fee = round((amount * sgst) / 100, 2)
    service_tax_fee = round((amount * service_tax) / 100, 2)

    total_amount = amount + cgst_fee + sgst_fee + service_tax_fee

    return {
        "cgst_fee": cgst_fee,
        "sgst_fee": sgst_fee,
        "service_tax": service_tax_fee,
        "total_amount": round(total_amount, 2)
    }
