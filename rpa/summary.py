def build_summary(records: list[dict[str, str]]) -> dict:
    seen = set()
    result = []
    for record in records:
        mail_id = record.get("mail_id")
        status = record.get("status")
        if not isinstance(mail_id, str) or not mail_id.strip():
            raise ValueError("摘要缺少郵件編號。")
        if mail_id in seen:
            raise ValueError(f"{mail_id}：重複的郵件編號。")
        if not isinstance(status, str) or not status.strip():
            raise ValueError(f"{mail_id}：摘要缺少狀態。")
        seen.add(mail_id)
        result.append({"mail_id": mail_id, "status": status})
    return {"ok": True, "records": result}
