var productIDs;
var products;

window.onload = function(){
    requestProductIDs();

    console.log("onload() finished");
}

/*
    ('^/search', searchView),
    ('^/getproductids', searchProductIDsView),
    ('^/getproducts', searchProductsView)*
*/

function requestProductIDs(){
    var request = "/getproductids";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            productIDs = JSON.parse(xhr.responseText);
            alert(productIDs);
            requestProducts();
        }
    }

    xhr.open("GET", request, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
}

function requestProducts(){
    var request = "/getproducts?item0=" + productIDs[0].toString();
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            products = JSON.parse(xhr.responseText);
            alert(products.title);
        }
    }

    xhr.open("GET", request, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
}
