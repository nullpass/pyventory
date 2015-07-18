Pyventory - A not-ready-for-primetime Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**

### Next:
* REFACTOR:
    * Remove ENV from ticket url and attr; keep company attr
    * Add SLA attr to domain
    * Explain SLA relation to domain during ticket creation
        * Select by company then domain or just domain? 
    * Match changes in install wizard
* Auth: Basic local log(in|out), profile
* Tickets: check for inventory.applications in link_related()
* Tickets: put undo url in success message from unlink_related()
* Reply: success url should include #shortcut to comment that was added/updated. Don't need messages() there.
* Other: Audit FKs and add `, null=True, on_delete=models.SET_NULL` where needed.
* Inventory: inventory object should themselves have can_link_related attrs to allow/block them being linked. Use case:
"We were dumb and named a server 'outage', now it gets auto-linked all the time, we need to be able to stop it ever
 being linked"
* Tickets: I hate the way the views.Sieze() works, need a diff approach
