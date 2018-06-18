function sendHomeInfo(how, category) {
    data = {}

    data['how'] = how
    data['category'] = category

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            homePage = xhr.responseText;
        }
    }


    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));
}