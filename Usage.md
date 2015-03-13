[gcode-backup]
project = your-project-name-here
username = your-username
password = your-google-password
output-type = zip}}}
  The `project` line is required (of course). `username` and `password` are optional; they only matter if your project uses [http://code.google.com/p/support/wiki/Permissions Permissions] to make some issues invisible to anonymous users (e.g., security bugs). Even if you don't use the permissions feature now, though, I'd recommend putting in your username and password, because if you ever start using permissions in the future, then you'll probably never notice that your backups have become incomplete (until it's too late). The `output-type = zip` line is required, because even though there are no other output types available right now, this way we have the option of changing the default later.
  * If you put your password into the .ini file, make sure that it is not world-readable: `chmod go-rw myproject.ini`
  * Run: `python gcode-backup.py myproject.ini myproject-issues.zip`. Examine `myproject-issues.zip` to make sure that it contains everything you want it to.
  * Set up a cron job or something to run this nightly. Don't forget to also set up a cron job to make backups of your source and wiki (this is pretty easy if you use mercurial).```