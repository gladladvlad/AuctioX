photoFiles = []

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

    console.log("Onload() finished.")
}

function submitPhoto(){


    var currentFiles = photos.files;

    console.log(currentFiles);

    if (currentFiles.length == 0){
        return
    }

    for(i = 0; i < currentFiles.length; i++){

        if(photos.children.length >= 20) {
            return
        }
        photo = document.createElement('img');
        console.log(i + " " + currentFiles[i])
        photo.src = URL.createObjectURL(currentFiles[i]);
        photoFiles.push(currentFiles[i])
        preview.append(photo)
    }
}

function createListing(){



    data = {}
    data["title"] = inputTitle.value;
    data["category"] = inputCategory.value;
    data["description"] = inputDesc.value;
    data["price"] = inputPrice.value;
    data["currency"] = inputCurrency.value;
    data["photos"] = []


    for (var i = 0; i < photoFiles.length; i++){
        var reader = new FileReader();
        console.log(photoFiles[0])
        data["photos"].push(reader.readAsArrayBuffer(photoFiles[i]));
    }

    console.log(data);

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {

        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            //body = document.getElementsByTagName("body")[0].innerHTML = xhr.response;
            console.log(xhr.response);
            return;
        }
    }

    xhr.open("POST", "/createlistingrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(data);
}
