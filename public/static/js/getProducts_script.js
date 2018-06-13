var productIDs;
var products;
var productPage;

var productCountKey = "prods";

var queryKey = "query";
var lastQuery;

var pageSizeKey = "psize";
var pageSize;


var minPriceKey = 'min_price';
var minPriceVal;

var maxPriceKey = 'max_price';
var maxPriceVal;

var conditionKey = 'conditie';
var conditionVal;

var countryKey = 'country';
var country;

var cityKey = 'city';
var cityVal;

var sortByKey = '';
var sortByVal;


window.onload = function(){
    lastQuery = getHTTPGArg(queryKey);
    if (typeof lastQuery == "undefined")
        lastQuery = "";

    pageSize = getHTTPGArg(pageSizeKey);
    if (typeof pageSize == "undefined")
        pageSize = 5;
    else pageSize = parseInt(pageSize);

    document.getElementById("searchBox").value = lastQuery;
    document.getElementById("searchForm").action = "";
    document.getElementById("searchForm").onclick = "searchAgain()";



    requestProductIDs();
    updateProductPage(0);

    console.log("onload() finished");
}


function updateProductPage(page) {
    var from = page * pageSize;
    var to = ((page + 1) * pageSize) - 1;
    if (to < 0 || productIDs.length <= 0){
        return;
    }


    if (to > (productIDs.length - 1)) { 
        console.log("updateProductPage() firs if: page is " + page);
        requestProductPage(from, productIDs.length - 1);
    } else {
        console.log("updateProductPage() second if: page is " + page);
        requestProductPage(from, to);
    }

    document.getElementById("content").innerHTML = productPage;
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


function requestProductPage(fromIndex, toIndex){
    console.log("requestProductPage(); (from, to) = (" + fromIndex + ", " + toIndex + ")");
    if (toIndex > (productIDs.length - 1)) throw "Right index higher than productIDs.length!";
    if (fromIndex < 0) throw "Left index lower than 0!";
    if (fromIndex > toIndex) throw "Inverted indexes!";

    var request = "/searchpage?" + productCountKey + "=" + productIDs.length + "&" + pageSizeKey + "=" + pageSize + "&";
    //var request = "/search_page?" + pageSizeKey + "=" + pageSize + "&";
    var argIter = "";

    console.log("request is " + request)
    console.log("argIter is " + argIter)

    console.log("beginning loop")
    for (var i = fromIndex; i <= toIndex; i++) {
        argIter = "item" + i.toString() + "=" + productIDs[i].toString();
        console.log("" + i + "th iteration; argIter is " + argIter)

        request = request + argIter;
        if (i != toIndex) {
            request = request + "&";
        }
        console.log("request becomes " + request);
    }

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            productPage = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
}

function getHTTPGArg(key) {
    return window.location.href.split(new RegExp("[?&]" + key + "="))[1];
}

