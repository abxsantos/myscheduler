from django_q.models import Task


def dispatch_activity_hook(task: Task):
    """
    Use the return value of the task as the task result, to inform the Client about a new activity.

    """
    from myscheduler.services.telegram.bot import telegram_bot

    telegram_bot.send_message(
        chat_id=task.kwargs.get("chat_id"),
        text=f"There is a new activity for you! {task.result}",
    )
