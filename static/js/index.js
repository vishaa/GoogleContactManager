document.addEventListener('DOMContentLoaded',function() {
  contact_list = document.getElementById('contact_list');
  xmlHttp = new XMLHttpRequest();
  xmlHttp.open('GET','/contacts',true);
  xmlHttp.send();
  xmlHttp.onreadystatechange = function () {
    if ( this.readyState == 4){
      obj = JSON.parse(this.responseText);
      contacts = obj.contacts;
      more = obj.more;
      cursor = obj.cursor;
      for(var i = 0; i < contacts.length ; i++){
        var name = contacts[i].name;
        var numberList = contacts[i].numbers;
        var numbers="";
        for(var j=0 ; j<numberList.length; j++ ){
          numbers += ('<tr><td>' + numberList[j] + '</td></tr>');
        }
        contact_list.innerHTML += ('<tr> <td>' + name + '</td><td>'+ numbers +'</td></tr>') ;
      }
    }
  }
});
