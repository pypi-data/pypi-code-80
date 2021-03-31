from microservice_template_core import Core
from microservice_template_core.settings import ServiceConfig, FlaskConfig, DbConfig, LoggerConfig
from harp_agent.endpoints.notifications import ns as notifications
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from harp_agent.notifications_collectors.push_notification import notification_scraper
import harp_agent.settings as settings
import threading
from harp_agent.logic.config_update import update_configuration
from harp_agent.logic.prepare_service import prepare_service_for_first_start


def schedule_watchdog():
    watchdog_service = threading.Thread(name='Configuration Watchdog', target=update_configuration, daemon=True)
    watchdog_service.start()


def schedule_jobs():
    # https://apscheduler.readthedocs.io/en/stable/userguide.html?highlight=max_instances#limiting-the-number-of-concurrently-executing-instances-of-a-job
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': '1'})
    scheduler.configure(timezone=utc)
    scheduler.start()
    scheduler.add_job(notification_scraper, args=['icinga'], trigger='interval', seconds=settings.NOTIFICATIONS_SCRAPE_INTERVAL_SECONDS)
    scheduler.add_job(notification_scraper, args=['zabbix'], trigger='interval', seconds=settings.NOTIFICATIONS_SCRAPE_INTERVAL_SECONDS)


def main():
    prepare_service_for_first_start()

    ServiceConfig.configuration['namespaces'] = [notifications]
    FlaskConfig.FLASK_DEBUG = False
    DbConfig.USE_DB = False
    ServiceConfig.SERVICE_PORT = 8082  # Only for test
    schedule_watchdog()
    schedule_jobs()

    app = Core()
    app.run()


if __name__ == '__main__':
    main()

