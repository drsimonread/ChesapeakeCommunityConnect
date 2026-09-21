# QA \- Test to-do list

As far as I can tell, these tests are going to mainly be recognition programs to verify the below requirements are being met.

 Forums

* Forum creation  
  * When created, forum must go into ‘pending’ state  
  * In ‘pending’ state, forum is not visible on website  
    * Need a way to verify the visibility status  
  * When approved of denied, forum is removed from the ‘pending’ state  
  * Only Admin or Mod can approve or deny  
  * Approved forums are made visible  
  * Denied forums remain invisible, and the proposing contributor is notified the reason why  
  * Contributors should be able to appeal denied forums  
  * Approved forums are visible to all users  
  * Forums can be tagged as public or private to indicate access  
* Forum access  
  * Users are able to view accessibility to forum (public, private (uninvited), private (invited))  
  * All users are able to access public forums  
  * Admins, Mods, and forum creator can access all forums  
  * Admins, Mods, and forum creator can grant or remove access to forums  
  * Private forums inaccessible to uninvited users, and accessible to invited users  
  * Uninvited users can request access to private forums, notifying forum creator  
    * This is via the ‘request access’ button, which will indicate private forums  
* Forum content  
  * Forums contain Posts, which contain Comments

Posts

* Post must contain Title, Body, Date created, and Date edited  
* Post may contain additional Media and user-defined Tags  
* Can be reported to Admin/Mod/Creator

Comments

* Comment must contain Body  
* Comment must contain Reference if it is in reference to another comment  
  * This is experimental  
* Can be reported to Admin/Mod/Creator

Search function

*  Forums can be searched by Date posted   
  * This is the date the forum is approved and made visible, not when first created and pending approval  
* Posts can be searched in Forum by Date created and Date edited  
* Comments can be searched in Post by Date created

Administrators

* Can appoint and remove moderators  
* Can create/edit/remove all forums/posts/comments  
  * Can modify tags  
* Can ban users from forum/website  
  * Banned user should be notified of when/why

