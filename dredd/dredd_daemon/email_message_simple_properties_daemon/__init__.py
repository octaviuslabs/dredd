from dredd_daemon import DreddDaemon
from event_scorer.email_message_simple_property_scorer import EmailMessageSimplePropertyScorer

# Daemon pattern found http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class EmailMessageSimplePropertiesDaemon(DreddDaemon):
    pid_filename = '/tmp/dredd-simple-properties.pid'
    pub_sub_app_name = 'simple_properties'

    def _score_task(self, task):
        return EmailMessageSimplePropertyScorer(task)

    def get_classifier(self):
        return None 
