Pyventory - A pet project that's currently 100% broken. :)
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**

### Bugs:
* everything!

### TODO:
* All views require login.
* Tickets: ownership
* Comment: handle form_invalid for views.Reply
* Associate domains with companies, then enable company-checking in link_related()
* ...then update install wizard to create domains with companies attached.
* Servers: During CreateView add attribute 'contains' as a form element, then find+link via form_valid override.  
* Inventory objects will need detail views and more heart later on.
* Get human/recent/core from all apps and send them to git as new repo.
* link_related: check for inventory.applications (may be overkill)
