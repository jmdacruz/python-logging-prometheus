import prometheus_client
import logging


class ExportingLogHandler(logging.Handler):
    """A LogHandler that exports logging metrics for Prometheus.io."""
    def __init__(self, level=logging.NOTSET, extra=None):
        logging.Handler.__init__(self, level=level)
        
        labels = ['logger', 'level']
        self.extra = []
        if extra:
            if not isinstance(extra, list):
                raise Exception("Argument 'extra' must be a list")
            labels = labels + extra
            self.extra = extra
        
        self.log_entries = prometheus_client.Counter(
            'python_logging_messages_total',
            'Count of log entries by logger and level.',
            labels)

    def emit(self, record):
        labels = [record.name, record.levelname] + [getattr(record, v, "unknown") for v in self.extra]
        self.log_entries.labels(*labels).inc()


def export_stats_on_root_logger(extra=None):
    """Attaches an ExportingLogHandler to the root logger.

    This should be sufficient to get metrics about all logging in a
    Python application, unless a part of the application defines its
    own logger and sets this logger's `propagate` attribute to
    False. The `propagate` attribute is True by default, which means
    that by default all loggers propagate all their logged messages to
    the root logger.
    """
    logger = logging.getLogger()
    logger.addHandler(ExportingLogHandler(extra=extra))
