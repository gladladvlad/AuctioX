photoFiles = []
data = {}

window.onload = function(){

    inputTitle = document.getElementById("inputTitle");
    inputCategory = document.getElementById("inputCategory");
    inputDesc = document.getElementById("textareaDesc");
    inputTags = document.getElementById("inputTags");
    photos = document.getElementById("inputPhotos");
    inputPrice = document.getElementById("inputPrice");
    inputCurrency = document.getElementById("selectCurrency");
    preview = document.getElementById("preview");

    createListingButton == document.getElementById("createListing");

    createListingButton.onclick = createListing;
}

function submitPhoto(){


    var currentFiles = photos.files;

    if (currentFiles.length == 0){
        return
    }

    for(i = 0; i < currentFiles.length; i++){

        if(photos.children.length >= 20) {
            return
        }
        photo = document.createElement('img');
        photo.src = URL.createObjectURL(currentFiles[i]);
        photoFiles.push(currentFiles[i])
        preview.append(photo)
    }
}

function readMultiFiles(files) {
    resultList = []
    var reader = new FileReader();
    function readFile(index) {
        if( index >= files.length || files[index] == undefined) {
            console.log("Finished reading");
            console.log(resultList)
            data["photos"] = resultList
            sendRequest(data)
        }
        console.log("Reading " + index + " from " + files[index].type)
        var file = files[index];
        reader.onload = function() {
            b64 = btoa(reader.result)
            resultList.push("data:" + files[index].type + ";base64," + b64)
            readFile(index+1)
        }
        reader.readAsDataURL(file);
    }
    readFile(0);
}

function createListing(){

    data = {}
    data["title"] = inputTitle.value;
    data["category"] = inputCategory.value;
    data["description"] = inputDesc.value;
    data["price"] = inputPrice.value;
    data["currency"] = inputCurrency.value;
    readMultiFiles(photoFiles);
}


function sendRequest(data) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            console.log(xhr.responseText)
            response = JSON.parse(xhr.responseText)
            return;
        }
    }

    xhr.open("POST", "/createlistingrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));
}