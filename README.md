Pyventory - A not-ready-for-prime-time Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**

### Next:
* Tickets: check for inventory.applications in link_related()
* Tickets: put undo url in success message from unlink_related()
* Other: Audit FKs and add `, null=True, on_delete=models.SET_NULL` where needed.
* Inventory: inventory object should themselves have can_link_related attrs to allow/block them being linked. Use case:
"We were dumb and named a server 'outage', now it gets auto-linked all the time, we need to be able to stop it ever
 being linked"
* Tickets: I hate the way the views.Sieze() works, need a diff approach
* Company: move status into the company model
* Tickets: add link-related form/view to accomodate linking tickets together since we cannot autolink tickets now.
* Tickets: Changing the domain of a ticket should be its own view.  
* All: Add flat/original/raw views to Detail to view an object without html


