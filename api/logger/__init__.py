from ...logger import logger, Logger, \
	debug, info, warning, warn, error, \
	crit, critical


__all__ = [
	# -----------------------
	#    class and objects
	# -----------------------

	'logger','Logger',

	# ---------------------
	#      functions
	# ---------------------
	
	'debug', 'info', 'warning',
	'error', 'critical', 'catch_exc',
	
	# ---------------
	#  	   CNAME
	# ---------------

	'warn', 'crit',
]