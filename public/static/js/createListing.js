
photoFiles = []
previewDict = {}
data = {}

window.onload = function(){

    inputTitle = document.getElementById("inputTitle");
    inputCategory = document.getElementById("inputCategory");
    inputDesc = document.getElementById("textareaDesc");
    inputTags = document.getElementById("inputTags");
    photos = document.getElementById("inputPhotos");
    inputListingType = document.getElementById("inputListingType");
    inputPrice = document.getElementById("inputPrice");
    inputCurrency = document.getElementById("selectCurrency");
    inputCondition = document.getElementById("inputCondition");
    preview = document.getElementById("preview");

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
        photo.onclick = function () {removePhoto(event);}
        photoFiles.push(currentFiles[i])
        preview.append(photo)
    }
}

function readMultiFiles(files) {
    resultList = []
    var reader = new FileReader();
    function readFile(index) {
        if( index >= files.length || !files[index]) {
            console.log("Finished reading");
            data["photos"] = resultList
            console.log("Sending data:")
            console.log(data)
            sendRequest(data)
            return
        }
        console.log("Reading " + index + " from " + files[index].type)
        var file = files[index];
        reader.onload = function() {
            b64 = reader.result
            resultList.push(b64)
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
    if (inputListingType.value == "Auction")
        data["is_auction"] = 1;
    else
        data["is_auction"] = 0;
    data["price"] = inputPrice.value;
    data["currency"] = inputCurrency.value;
    data["condition"] = inputCondition.value;
    readMultiFiles(photoFiles);
}


function sendRequest(data) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            response = JSON.parse(xhr.responseText)
            console.log(response)
            if(response["success"])
            {
                alert("Product created!")
                window.location = "/product?prodid=" + response["prodId"]
            }
        }
    }

    xhr.open("POST", "/createlistingrequest", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(data));
}

function removePhoto(e) {
    src = e.target.src
    imgList = preview.children
    index = null
    for(i = 0; i < imgList.length; i++) {
        if (imgList[i].src == src) {
            index = i
            break
        }
    }

    if (index == null) {
        console.log("Index null")
    }
    else {
        console.log(index)
    }
    delete photoFiles.splice(index, 1);
    e.target.parentElement.removeChild(e.target);
}