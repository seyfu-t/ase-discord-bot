import coloredlogs


def setup_logger():
    fmt = '%(asctime)s %(levelname)-8s %(name)s %(message)s'
    # Root logger setup
    coloredlogs.install(level='INFO', fmt=fmt)
