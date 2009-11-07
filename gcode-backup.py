# Copyright (C) 2009 Nathaniel Smith <njs@pobox.com>
# Released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

COMPANY_NAME = "vorpus.org"
APPLICATION_NAME = "gcode-backup"
__version__ = "0.0.1"

import os
import os.path
import time
from optparse import OptionParser
from ConfigParser import SafeConfigParser, NoOptionError
from zipfile import ZipFile
from tempfile import NamedTemporaryFile

from gdata.projecthosting.client import ProjectHostingClient, Query

class GCodeFetcher(object):
    def __init__(self, project, username=None, password=None):
        self.project = project
        self.client = ProjectHostingClient()
        if username and password:
            source = "-".join([COMPANY_NAME, APPLICATION_NAME, __version__])
            client.client_login(username, password,
                                source=source, service="code")

    def get_all(self, get_from):
        start = 1
        while True:
            feed = get_from(start)
            if not feed.entry:
                break
            for item in feed.entry:
                yield item
                start += 1

    def issues(self, **kwargs):
        def get_issues_from(start):
            return self.client.get_issues(self.project,
                                          query=Query(pretty_print=True,
                                                      start_index=start,
                                                      **kwargs))
        return self.get_all(get_issues_from)

    def short_id(self, issue_or_comment):
        # All we can directly get from an issue is a string like:
        #   http://code.google.com/feeds/issues/p/support/issues/full/3238
        # But if we want to get that issue's comments, the API won't accept
        # that, it needs the bare "3238".
        #
        # REST FAIL
        return issue_or_comment.id.text.split("/")[-1]

    def comments(self, issue, **kwargs):
        issue_id = self.short_id(issue)
        def get_comments_from(start):
            return self.client.get_comments(self.project,
                                            issue_id,
                                            query=Query(pretty_print=True,
                                                        start_index=start,
                                                        **kwargs))
        return self.get_all(get_comments_from)

    
def main():
    parser = OptionParser(usage="%prog CONFIG OUTPUT")
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.error("Wrong number of arguments")
    config_path, output_path = args
    # Need:
    #   project, username, password
    #   desired output
    config = SafeConfigParser({"username": "", "password": ""})
    config.read(config_path)
    def safe_get(option):
        try:
            return config.get("gcode-backup", option)
        except NoOptionError:
            parser.error("no such entry '%s' in [gcode-backup] section")
    project = safe_get("project")
    username = safe_get("username")
    password = safe_get("password")
    output_type = safe_get("output-type")
    if output_type != "zip":
        parser.error("'output-type' must be set to 'zip' (for now)")
    tmp_output = NamedTemporaryFile(prefix="gcode-backup",
                                    suffix=".zip",
                                    delete=False)
    z = ZipFile(tmp_output, "w", allowZip64=True)
    
    fetcher = GCodeFetcher(project, username, password)
    base_dir = "%s-%s/issues" % (project,
                                 time.strftime("%Y-%m-%d_%H:%M:%S",
                                               time.gmtime()))
    for issue in fetcher.issues():
        issue_id = fetcher.short_id(issue)
        print "Processing issue %s" % (issue_id,)
        issue_dir = os.path.join(base_dir, issue_id)
        z.writestr(os.path.join(issue_dir, "issue"), issue.to_string())
        for comment in fetcher.comments(issue):
            comment_id = fetcher.short_id(comment)
            z.writestr(os.path.join(issue_dir, "comments", comment_id),
                       comment.to_string())
    z.close()
    tmp_output.close()
    os.rename(tmp_output.name, output_path)

if __name__ == "__main__":
    main()
