Pyventory - A pet project that's currently 100% broken. :)
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**

### Bugs:
* Everything!

### TODO:
* May have to make ticket.Comment its own sub-app of /ticket/. Gettin kinda messy. 
* Tickets: auto-set self.name to first line of self.notes. Remove self.name from forms.
* Servers: During CreateView add attribute 'contains' as a form element, then find+link via form_valid override.  
* Merge old cctrl code into ticket as attribute and a dash of business logic.
* Inventory objects will need detail views and more heart later on.
* Get human/recent/core from all apps and send them to git as new repo.
