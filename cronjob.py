from crontab import CronTab
 
my_cron = CronTab(user='boris')
job = my_cron.new(command='python app.py')
job.minute.every(1)
 
my_cron.write()
