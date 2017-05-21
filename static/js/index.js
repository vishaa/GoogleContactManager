document.addEventListener('DOMContentLoaded', function() {
  var more = true;
  var cursor = '';
  var loadingContacts = false;
  var contacts_elm = document.getElementById('contacts');

  fetchContacts();

  contacts_elm.addEventListener('scroll', scrollControl);
  function scrollControl() {
    if( ( ( contacts_elm.scrollTop + contacts_elm.clientHeight ) / contacts_elm.scrollHeight ) >= 0.95 ) {
      if (!loadingContacts && more) {
        fetchContacts();
      }
    }
  }

  function fetchContacts () {
    if (loadingContacts) return;
    loadingContacts = true;

    contacts_elm.innerHTML+= '<li id="loading" style="text-align: center"> <img src="/static/gif/loading.gif"/> </li>';

    var xmlHttp = new XMLHttpRequest();
    var url = '/contacts?cursor='+ cursor;
    xmlHttp.open('GET', url , true);
    xmlHttp.send();
    xmlHttp.onreadystatechange = function () {
       if ( this.readyState == 4 && this.status == 200) {
         var obj = JSON.parse(this.responseText);
         loadContacts(obj);
       }
       else if (this.readyState == 4 && this.status == 500) {
         loadingContacts = false
         fetchContacts();
       }
    }
  }

  function loadContacts(data) {
    if (!data || typeof data.contacts !== 'object') return;

    more = data.more;
    cursor = data.cursor;

    contacts_elm.removeChild(document.getElementById('loading'));

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

    if (!more){
      contacts_elm.innerHTML += '<li style="text-align: center; text-color: #C0C0C0"> No more contacts </li>'
    }

    loadingContacts = false;
  }

});
