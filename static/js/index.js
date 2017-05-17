document.addEventListener('DOMContentLoaded', function() {
  var contact_list = document.getElementById('contacts');
  var xmlHttp = new XMLHttpRequest();
  var more = true;
  var cursor = "";
  var fetchingMore = false;
  xmlHttp.open('GET', '/contacts?cursor='+ cursor, true);
  xmlHttp.send();
  xmlHttp.onreadystatechange = function () {
     if ( this.readyState == 4) {
       var obj = JSON.parse(this.responseText);
       var contacts = obj.contacts;
       more = obj.more;
       cursor = obj.cursor;
       contacts.forEach(function(contact) {
         if (contact && typeof contact.numbers == 'object') {
          contact_list.innerHTML += `<li class="mdl-list__item">
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

     }
 }
});
