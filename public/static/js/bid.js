var answer;

testSuccessRe = new RegExp("Success!")

function bid() {
    bidAmount = document.getElementById("bidAmount").value;
    productID = getHTTPGArg('prodid')
    var request = "/bid?amount=" + bidAmount + "&prodid=" + productID;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            answer = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();

    if (testSuccessRe.test(answer)) {
        document.getElementById("price").innerHTML = bidAmount;
    }

    alert(answer);
}

function buy() {
    productID = getHTTPGArg('prodid')

    var request = "/buy?prodid=" + productID;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            answer = xhr.responseText;
	    console.log("done");
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();

    alert(answer);
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

