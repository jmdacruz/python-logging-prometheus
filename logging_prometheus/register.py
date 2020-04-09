from logging_prometheus.core import export_stats_on_root_logger

# Just importing this module should make us export the metrics for the
# root logger.
export_stats_on_root_logger()
