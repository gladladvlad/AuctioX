var productIDs = [];
var products;
var productPage;

var args = {}

var conditionKey = "cond"
var condMin = 0, condMax = 4;

window.onload = function(){
    getArgsFromUrl();

    if (typeof args['query'] != "undefined")
        document.getElementById("searchBox").value = args['query'];

    requestProductIDs(args);
    updateProductPage(0);

    console.log("onload() finished");
}

function getArgsFromUrl() {
    console.log("fetching args");

    tmpObject = getHTTPGArg("query");
    if (typeof tmpObject != "undefined")
            tmpObject = decodeURIComponent(tmpObj).replace(/\+/g, " ");

    tmpObject = getHTTPGArg("psize");
    if (typeof tmpObject == "undefined")
        tmpObject = 5;
    else tmpObject = parseInt(pageSize);
    args['psize'] = tmpObject;


    var tmpObj = getHTTPGArg("min_price")
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['min_price'] = tmpObj;
    tmpObj = getHTTPGArg("max_price")
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['max_price'] = tmpObj;
    tmpObj = getHTTPGArg("country")
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['country'] = tmpObj;
    tmpObj = getHTTPGArg("city")
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['city'] = tmpObj;
    tmpObj = getHTTPGArg("sortby")
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['sortby'] = tmpObj;
    tmpObj = getHTTPGArg("query")
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['query'] = tmpObj;
    tmpObj = getHTTPGArg("categ");
    if (typeof tmpObj != "undefined" && tmpObj != "")
        args['category'] = decodeURIComponent(tmpObj).replace(/\+/g, " ");


    tmpObj = getHTTPGArg("sort");
    if (typeof tmpObj != "undefined" && tmpObj != "") {
        tmpObj = decodeURIComponent(tmpObj).split("+");

        // this really shouldn't be here but...
        if (tmpObj[0] == "conditie") {
            if (tmpObj[1] == "desc") tmpObj[1] = "asc";
            else tmpObj[1] = "desc";
        }
        // necessary; condition is stored as int with lower
        // being a better condition

        args['sort'] = [tmpObj[0], tmpObj[1]];
    }


    tmpCondList = []
    for (i = condMin; i < condMax; i++) {
       tmpObj = getHTTPGArg(conditionKey + "_" + i);
       if (typeof tmpObj != "undefined")
            tmpCondList.push(parseInt(tmpObj));
    }

    if (tmpCondList.length != 0) {
        args['conditie'] = tmpCondList;
    }

    console.log(args);
}

function updateProductPage(page) {
    var pageSize = parseInt(args['psize']);
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

    /*
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
    */

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            productIDs = JSON.parse(xhr.responseText);
        }
    }

    xhr.open("POST", request, false);
    xhr.setRequestHeader("Content-type", "application/json");
    console.log("requesting /getproductids with: ");
    console.log(args);
    xhr.send(JSON.stringify(args));
}

function requestProductPage(fromIndex, toIndex){
    console.log("requestProductPage(); (from, to) = (" + fromIndex + ", " + toIndex + ")");
    if (toIndex > (productIDs.length - 1)) throw "Right index higher than productIDs.length!";
    if (fromIndex < 0) throw "Left index lower than 0!";
    if (fromIndex > toIndex) throw "Inverted indexes!";

    var request = "/searchpage?prods=" + productIDs.length + "&psize=" + args['psize'] + "&";
    var argIter = "";

    console.log("request is " + request)
    console.log("argIter is " + argIter)

    document.getElementsByClassName("navbar")[0].scrollIntoView();

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
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
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

