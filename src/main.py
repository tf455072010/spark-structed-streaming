import logging
import os

import config
from config import base
from ctutil import dclog
from logic import application, handle

app = config.APPLICATION_NAME
env = base.APPLICAITON_ENV
vers = config.APPLICATION_VERS

if __name__ == "__main__":
    dclog.set_app_info(app, env, vers, logging.INFO, application.sc.applicationId)

    handle.execute()
