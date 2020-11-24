from viikkokuva import PictureChoice, create_task

def lambda_handler(event, context):
    create_task(PictureChoice.week)
