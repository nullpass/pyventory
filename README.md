Pyventory - A not-ready-for-prime-time Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**


### Next:
* Inventory: move all submods to inv.models
* Inventory: Set up M2M for servers<->applications
* Tickets: check for inventory.applications in link_related()
* Tickets: put undo url in success message from unlink_related()
* Other: Audit FKs and add `, null=True, on_delete=models.SET_NULL` where needed.
* Tickets: add link-related form/view to accommodate linking tickets together since we cannot autolink tickets now.
* Tickets: Changing the domain of a ticket should be its own view.  
* All: Add flat/original/raw views to Detail to view an object without html


### Deep thoughts by Jack Example:
* The way domains are presented to attached objects needs some love. Simple bullet options may not work ideally but
 going to whole hand-holding-wizard route would be insulting to most prod users.
* I hate the way the views.Sieze() works, need a diff approach. 
* Current server.make_parent is so dumb, like really. Final version will rely on what users expect to see (if anything)
 when it fails.
* Will upgrade to Dj 1.8 once python-social-auth is updated.
