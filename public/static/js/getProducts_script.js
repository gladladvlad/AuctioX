var productIDs;
var products;

window.onload = function(){
    requestProductIDs();
    requestProducts(0, 4);

    console.log("onload() finished");
}


function requestProductIDs(){
    var request = "/getproductids";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            productIDs = JSON.parse(xhr.responseText);
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
}

function requestProducts(fromIndex, toIndex){
    if (fromIndex > toIndex) throw "Inverted indexes!";
    if (fromIndex < 0) throw "Left index lower than 0!";
    if (toIndex > (productIDs.length - 1)) throw "Right index higher than productIDs.length!";

    var request = "/getproducts";

    request = request + "?";
    var argIter = "";

    for (var i = fromIndex; i <= toIndex; i++) {
        argIter = "item" + i.toString() + "=" + productIDs[i].toString();

        request = request + argIter;
        if (i != toIndex) {
            request = request + "&";
        }
    }

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            products = JSON.parse(xhr.responseText);
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
}
