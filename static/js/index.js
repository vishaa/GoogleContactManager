document.addEventListener('DOMContentLoaded', function() {
  var contact_list = document.getElementById('contact_list');
  var xmlHttp = new XMLHttpRequest();
  var more = true;
  var cursor = "";
  xmlHttp.open('GET', '/contacts?cursor='+ cursor, true);
  xmlHttp.send();
  xmlHttp.onreadystatechange = function () {
     if ( this.readyState == 4) {
       var obj = JSON.parse(this.responseText);
       var contacts = obj.contacts;
       more = obj.more;
       cursor = obj.cursor;
       for ( var contact of contacts ) {
         var name = contact.name;
         var numberList = contact.numbers;
         var numbers="";
         numberList.forEach( function(item,index){
            if(index>0)
               numbers += ('<tr><td>' + item + '</td></tr>')
          });
         contact_list.innerHTML += ('<tr> <td rowspan='+ numberList.length +'>' + name + '</td><td>'+ numberList[0]+'</td></tr>'+ numbers ) ;
       }
     }
 }
});
