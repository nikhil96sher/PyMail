# https://github.com/raccooniscoding/smtpclient/blob/master/smtp.py

from sender import Mail
from conf import *

mail = Mail("192.168.180.11", port=587, username=username, password=passw,
            use_tls=False, use_ssl=False, debug_level=1)

mail.send_message("IITR EMAIL SERVER VULNERABILITY", fromaddr="sgargfec@iitr.ac.in",
                  to="an9sh.ucs2014@iitr.ac.in", body="Some Mischievous Message")