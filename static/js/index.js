document.addEventListener('DOMContentLoaded', function() {
  var more = true;
  var cursor = '';
  var loadingContacts = false;
  var contacts_elm = document.getElementById('contacts');

  fetchContacts();

  function fetchContacts () {
    if (loadingContacts) return;
    loadingContacts = true;
    var xmlHttp = new XMLHttpRequest();
    var url = '/contacts?cursor='+ cursor;
    xmlHttp.open('GET', url , true);
    xmlHttp.send();
    xmlHttp.onreadystatechange = function () {
       if ( this.readyState == 4 && this.status == 200) {
         var obj = JSON.parse(this.responseText);
         loadContacts(obj);
       }
       else if (this.readyState == 4 && this.status !=200) {
         loadingContacts = false
         fetchContacts();
       }
       if (more) fetchContacts();
    }
  }

  function loadContacts(data) {
    if (!data || typeof data.contacts !== 'object') return;

    more = data.more;
    cursor = data.cursor;

    data.contacts.forEach(function(contact) {
      if (contact && typeof contact.numbers == 'object') {
        contacts_elm.innerHTML += `<li class="mdl-list__item">
         <span class="mdl-list__item-primary-content">
           <i class="material-icons  mdl-list__item-avatar">person</i>
            ${contact.name}
         </span>
         <span class="mdl-list__item-secondary-action">
           ${contact.numbers[0]}
         </span>
       </li>`
      }
    });

    loadingContacts = false;
  }


});
