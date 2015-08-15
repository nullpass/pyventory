Pyventory - A not-ready-for-prime-time Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**


### Next:
* Tickets: refactor numbering scheme now that domains are handled differently.
* Tickets: put undo url in success message from unlink_related()
* Tickets: add link-related form/view to accommodate linking tickets together since we cannot autolink tickets now.
* Tickets: Changing the domain of a ticket should be its own view.  
* All: Add flat/original/raw views to Detail to view an object without html
* Inventory: Set up view for servers<->applications
* Logging: start adding hooks
* All: orphan finders
* Inventory: Add related-object full listing views. 


### Deep thoughts by Jack Example:
* The way domains are presented to attached objects needs some love. Simple bullet options may not work ideally but
 going the whole hand-holding-wizard route would be insulting to most prod users.
* Current server.make_parent is so dumb, like really. Final version will rely on what users expect to see (if anything)
 when it fails.
* Will upgrade to Dj 1.8 once [python-social-auth](https://github.com/omab/python-social-auth) is updated.
* How should we order related objects, (+|-)(pk|modified)?
