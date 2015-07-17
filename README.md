Pyventory - A not-ready-for-primetime Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**

### Bugs:
* all

### TODO:
* go back to the whiteboard for the domain/company/env flow.
3. Tickets: enable company-checking in link_related()
4. Install: update install wizard to create domains with companies attached.
* Tickets: check for inventory.applications in link_related()
* Tickets: put undo url in success message from unlink_related()
* Reply: success url should include #shortcut to comment that was added/updated. Don't need messages() there.
* Other: Audit FKs and add `, null=True, on_delete=models.SET_NULL` where needed.
* Inventory: inventory object should themselves have can_link_related attrs to allow/block them being linked. Use case:
"We were dumb and named a server 'outage', now it gets auto-linked all the time, we need to be able to stop it ever
 being linked"
* Tickets: I hate the way the views.Sieze() works, need a diff approach
