Pyventory - A not-ready-for-prime-time Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**


### Next:
* Human: Department views
* Auth: (no 3pa yet) auth schemes and cascading ownership
* Inventory: Keep updating querysets to restrict company scope
* Tickets: put undo url in success message from unlink_related()
* Tickets: add link-related form/view to accommodate linking tickets together since we cannot autolink tickets now.
* Tickets: Changing the domain of a ticket should be its own view.  
* All: Add flat/original/raw views to Detail to view an object without html
* Inventory: Set up view for servers<->applications
* Logging: start adding hooks
* All: orphan finders
* Inventory: Limit related object listing, but convert title to URL where all objs can be seen. ex: If there are 250
Applications for a company only show the first 10, but make the "Application" row title a link to 
'inventory/company/{pk}/applications' which would show all 250. Add '...' if total created than shown. 


### Deep thoughts by Jack Example:
* The way domains are presented to attached objects needs some love. Simple bullet options may not work ideally but
 going the whole hand-holding-wizard route would be insulting to most prod users.
* I hate the way the views.Sieze() works, need a diff approach. 
* Current server.make_parent is so dumb, like really. Final version will rely on what users expect to see (if anything)
 when it fails.
* Will upgrade to Dj 1.8 once python-social-auth is updated.
* How should we order related objects, (+|-)(pk|modified)?
