SERVICE_FEES = {"standard": 0, "registered": 20}


def calculate_fee(weight_grams: int, service: str) -> int:
    if type(weight_grams) is not int:
        raise ValueError("重量必須是整數公克。")
    if weight_grams >= 20000:
        raise ValueError("重量必須介於 1 到 20,000 公克。")
    if not isinstance(service, str) or service not in SERVICE_FEES:
        raise ValueError("請選擇有效的寄送服務。")
    extra_steps = max(0, (weight_grams - 1000 + 999) // 1000)
    return 60 + extra_steps * 10 + SERVICE_FEES[service]
