# PiEmailMonitor
requires
pip3 install IMAPClient
pip3 install python-dotenv
//insert additional pi drivers for hardware
need to put myscript.service file in /lib/systemd/system/
and enable with 'sudo systemctl daemon-reload'
and 'sudo systemctl enable myscript.service'
