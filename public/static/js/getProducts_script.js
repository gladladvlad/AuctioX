var productIDs;
var products;
var productPage;

var lastQuery;
var pageSize;

var filters = {}

window.onload = function(){
    lastQuery = getHTTPGArg("query");
    if (typeof lastQuery == "undefined")
        lastQuery = "";
    lastQuery = lastQuery.replace("+", " ");

    pageSize = getHTTPGArg("psize");
    if (typeof pageSize == "undefined")
        pageSize = 5;
    else pageSize = parseInt(pageSize);


    document.getElementById("searchBox").value = lastQuery;

    getFiltersFromUrl();
    requestProductIDs(filters);
    updateProductPage(0);

    console.log("onload() finished");
}

function getFiltersFromUrl () {
    /*filters = {"min_price" : getHTTPGArg("min_price"),
                    "max_price" : getHTTPGArg("max_price"),
                    "condition" : getHTTPGArg("condition"),
                    "country" : getHTTPGArg("country"),
                    "city" : getHTTPGArg("city"),
                    "sortby" : getHTTPGArg("sort") }*/
    console.log("fetching filters");

    var tmpObj = getHTTPGArg("min_price")
    if (typeof tmpObj != "undefined")
        filters['min_price'] = tmpObj;
    tmpObj = getHTTPGArg("max_price")
    if (typeof tmpObj != "undefined")
        filters['max_price'] = tmpObj;
    tmpObj = getHTTPGArg("country")
    if (typeof tmpObj != "undefined")
        filters['country'] = tmpObj;
    tmpObj = getHTTPGArg("city")
    if (typeof tmpObj != "undefined")
        filters['city'] = tmpObj;
    tmpObj = getHTTPGArg("sortby")
    if (typeof tmpObj != "undefined")
        filters['sortby'] = tmpObj;
    tmpObj = getHTTPGArg("query")
    if (typeof tmpObj != "undefined")
        filters['query'] = tmpObj;

    console.log(filters);
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


function requestProductIDs(args){
    var request = "/getproductids";

    var firstFlag = 0;
    for (var key in args) {
        if (args[key] == "undefined") {
            console.log("found undefined key")
            continue;
        }

        if (firstFlag == 0) {
            request = request + "?" + key + "=" + args[key];
            firstFlag = 1;
            console.log("first iteration done")
            console.log(request)
        } else {
            request = request + "&" + key + "=" + args[key];
        }
    }
    console.log("request will be " + request)

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

    var request = "/searchpage?prods=" + productIDs.length + "&psize=" + pageSize + "&";
    var argIter = "";

    console.log("request is " + request)
    console.log("argIter is " + argIter)

    console.log("beginning loop")
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
            productPage = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
}

function getHTTPGArg(key) {
    //return window.location.href.split(new RegExp("[?&]" + key + "="))[1];
    try {
            return window.location.href.split(key + "=")[1].split("&")[0];
    } catch (err) {
        if (err == "TypeError")
            return "undefined";
    }
}

