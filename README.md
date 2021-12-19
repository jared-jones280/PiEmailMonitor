# PiEmailMonitor
requires<br>
pip3 install IMAPClient<br>
pip3 install python-dotenv<br>
//insert additional pi drivers for hardware<br>
need to put myscript.service file in /lib/systemd/system/<br>
and enable with 'sudo systemctl daemon-reload'<br>
and 'sudo systemctl enable myscript.service'<br>
<br>
<br>
Can send messages to a gmail in the subject line of up to 18 characters x 5 lines (seperated by [hashtag])<br>
