import pyuac  # admin privileges probably not needed
import logging

def assert_admin_privileges() -> None:
    if not pyuac.isUserAdmin():
        logging.warning("Admin privileges required! Re-launching as admin...")
        pyuac.runAsAdmin()
    else:        
        logging.info('Running as admin')
