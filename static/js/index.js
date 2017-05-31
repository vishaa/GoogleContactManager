document.addEventListener('DOMContentLoaded', function() {
  var more = true;
  var cursor = '';
  var loadingContacts = false;
  var contacts_elm;
  var contactsPermission;
  var importButton;
  const loadingGif = `<li id="loading" style="text-align: center">
                        <img src="/static/gif/loading.gif"/>
                      </li>`;
  const noMoreElm = `<li style="text-align: center; text-color: #C0C0C0">
                      No more contacts
                     </li>`;

  if(document.getElementById('loadContacts')){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET','/importStatus',true);
    xmlHttp.send();
    xmlHttp.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200){
        var obj = JSON.parse(this.responseText);
        var importStatus = obj.import_status;
        if(importStatus === 'imported'){
          startLoadingContacts();
        }
      }
    };
  }


  if(document.getElementById('importButton')){
    importButton = document.getElementById('importButton');
    importButton.addEventListener('click',function() {
      contactsPermission = window.open('/oauthPermission',
                                       'contactsPermission',
                                       'width=500, height=600');
    });
  }

  window.importContacts = function() {
    contactsPermission.close();
    importButton.remove();
    startLoadingContacts();
  };


  function startLoadingContacts() {
    document.body.innerHTML+= "<ul class='demo-list-control mdl-list' id='contacts'></ul>";
    contacts_elm = document.getElementById('contacts');
    showLoader(true);
    fetchContacts();
    contacts_elm.addEventListener('scroll', loadMore);
  }


  function loadMore() {
    const scrolledHeight = contacts_elm.scrollTop + contacts_elm.clientHeight;
    const scrolled = (scrolledHeight / contacts_elm.scrollHeight) >= 0.95;
    if (scrolled && !loadingContacts && more ) {
      showLoader(true);
      fetchContacts();
    }
  }

  function showLoader(show) {
    if (show) {
      return contacts_elm.innerHTML += loadingGif;
    }
    contacts_elm.removeChild(document.getElementById('loading'));
  }

  function showInfo() {
    contacts_elm.innerHTML += noMoreElm;
  }


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
    showLoader(false);

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

    if (!more) {
      showInfo();
    }

    loadingContacts = false;
  }

});
