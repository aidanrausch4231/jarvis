from helperFunctions.auth import get_tasks_service


def list_task_lists():
    service = get_tasks_service()
    result = service.tasklists().list(maxResults=20).execute()
    return result.get("items", [])


def list_tasks(tasklist_id="@default", show_completed=False):
    service = get_tasks_service()
    result = (
        service.tasks()
        .list(tasklist=tasklist_id, showCompleted=show_completed)
        .execute()
    )
    return result.get("items", [])


def get_task(task_id: str, tasklist_id="@default"):
    service = get_tasks_service()
    return service.tasks().get(tasklist=tasklist_id, task=task_id).execute()


def create_task(title: str, notes: str = "", due: str = "", tasklist_id="@default"):
    """due as RFC 3339 timestamp e.g. '2024-01-01T00:00:00.000Z'"""
    service = get_tasks_service()
    body = {"title": title, "notes": notes}
    if due:
        body["due"] = due
    return service.tasks().insert(tasklist=tasklist_id, body=body).execute()


def update_task(task_id: str, updates: dict, tasklist_id="@default"):
    """Pass only the fields you want to change in updates dict"""
    service = get_tasks_service()
    task = get_task(task_id, tasklist_id)
    task.update(updates)
    return service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()


def complete_task(task_id: str, tasklist_id="@default"):
    service = get_tasks_service()
    return (
        service.tasks()
        .patch(tasklist=tasklist_id, task=task_id, body={"status": "completed"})
        .execute()
    )


def delete_task(task_id: str, tasklist_id="@default"):
    service = get_tasks_service()
    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()


def clear_completed_tasks(tasklist_id="@default"):
    service = get_tasks_service()
    service.tasks().clear(tasklist=tasklist_id).execute()
