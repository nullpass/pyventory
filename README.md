Pyventory - A not-ready-for-primetime Dj project.
=============================================================
**Uses Python 3.4 and Django 1.7 and a whole lot of love**

### Bugs:
* everything!

### TODO:
3. Tickets: enable company-checking in link_related()
4. Install: update install wizard to create domains with companies attached.
* Install: Add tickets+comments to the install wizard. `love(turtles): return 'Lorem Ipsum'`
* Servers: During CreateView add attribute 'contains' as a form element, then find+link via form_valid override.  
* Tickets: check for inventory.applications in link_related() (may be overkill)
* Tickets: put undo url in success message from unlink_related()
* Reply: success url should include #shortcut to comment that was added/updated. Don't need messages() there.
* Tickets: The auto-self.name code will always be a pain in the ass, but keep tweaking.  
* Other: Audit FKs and add `, null=True, on_delete=models.SET_NULL` where needed.
