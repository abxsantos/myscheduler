from django_q.models import Task


def cpf_validation_hook(task: Task):
    from myscheduler.services.telegram.bot import telegram_bot

    client_id = task.kwargs.get("client_id")
    telegram_bot.send_message(
        chat_id=client_id.replace("-myscheduler_django_bot", ""),
        text=f"Your CPF was successfully validated!"
        if task.success and task.result
        else "You've given an invalid cpf!",
    )
