document.addEventListener('DOMContentLoaded', function() {
  if(document.getElementById('success').value === 'true') {
    opener.importContacts();
  }
});
