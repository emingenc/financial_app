import uuid


def generate_financial_record_id() -> str:
    """
    Return unique string for financial_record id.
    """
    return uuid.uuid4().hex


def remove_non_digit(val):
    if val == None:
        return 0
    if type(val) != str :
        return val
    res =  "".join([char for char in val if char.isdigit() or char == "."])
    if res == "":
        return 0
    return res

def preprocess_obj(obj):
        processed_obj = {}
        processed_obj["segment"] = obj.get("segment")
        processed_obj["country"] = obj.get("country")
        processed_obj["product"] = obj.get("product")
        processed_obj["discount_band"] = str(obj.get("discount_band"))
        processed_obj["units_sold"] = float(remove_non_digit(obj.get("units_sold")))

        print(obj.get('manufacturing_price'),type(obj.get('manufacturing_price')))
        processed_obj['currency'] = obj.get('currency')

        if not processed_obj.get('currency'):
            #make sure to get the currency
            if obj.get('manufacturing_price') and not obj.get('manufacturing_price')[0].isdigit():
                processed_obj["currency"] = obj.get('manufacturing_price')[0]

            if obj.get('sale_price') and not obj.get('sale_price')[0].isdigit() and not processed_obj.get('currency'):
                processed_obj["currency"] = obj.get('sale_price')[0]

            if processed_obj.get('gross_sales') and not processed_obj.get('gross_sales')[0].isdigit() and not processed_obj.get('currency'):
                processed_obj["currency"] = obj.get('gross_sales')[0]

            if processed_obj.get('discounts') and not processed_obj.get('discounts')[0].isdigit() and not processed_obj.get('currency'):
                processed_obj["currency"] = obj.get('discounts')[0]
            
            #if no currency is found, set it to empty string
            if not processed_obj.get('currency'):
                processed_obj["currency"] = ""

        processed_obj["manufacturing_price"] = float(remove_non_digit(obj.get("manufacturing_price")))
        
        processed_obj["sale_price"] = float(remove_non_digit(obj.get("sale_price")))
        processed_obj["gross_sales"] = float(remove_non_digit(obj.get("gross_sales")))
        processed_obj["discounts"] = float(remove_non_digit(obj.get("discounts")))
        processed_obj["sales"] = float(remove_non_digit(obj.get("sales")))
        processed_obj["cogs"] = obj.get("cogs")
        print(obj)
        processed_obj["profit"] = float(remove_non_digit(obj.get("profit")))
        processed_obj["date"] = obj.get("date")
        processed_obj["month_number"] = int(remove_non_digit(obj.get("month_number")))
        processed_obj["month_name"] = obj.get("month_name")
        processed_obj["year"] = int(remove_non_digit(obj.get("year")))


        return processed_obj
