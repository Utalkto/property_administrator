from apscheduler.schedulers.background import BackgroundScheduler
from communications.extra_modules import check_organization_emails

scheduler = BackgroundScheduler()

def start():
    
	scheduler.add_job(check_organization_emails, 'interval', seconds=60)	
	# scheduler.start()
 


