from landing_page.app import create_celery_app
from landing_page.save_email import save_email_to_db


celery = create_celery_app()



@celery.task()
def celery_start_save_email(email):
    """
    docker container exec -it "container id" bash
    from twitterbot.tasks.twitter import celery_start_twitter_bot
    result = celery_start_twitter_bot.apply_async((data,), queue="twitter")
    result = celery.send_task('twitter.celery_start_twitter_bot', (data,), queue="twitter")    

    """
    response = save_email_to_db(email)
    return {"response": response}



