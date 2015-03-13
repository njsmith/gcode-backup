I have a rule -- I never host my own data on other people's servers unless I have a way to run nightly backups.

This is the script I wrote to dump the contents of a Google Code-hosted project's issue tracker. Currently it is very simple -- it just produces a zip file containing all issues and all comments on those issues, as Atom-formatted XML files.

That's sufficient for my needs for now, but I would welcome enhancements of all sorts -- for instance, to allow it to download only recently changed items, rather than pulling down everything every night, or to manage back ups for the wiki, etc., which I currently handle from a separate script.

See the [Usage](Usage.md) page for detailed instructions.