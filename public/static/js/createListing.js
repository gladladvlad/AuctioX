window.onload = function(){

    inputTitle = document.getElementById("inputTitle");
    inputCategory = document.getElementById("inputCategory");
    inputDesc = document.getElementById("textareaDesc");
    inputTags = document.getElementById("inputTags");
    inputPhotos = document.getElementById("inputPhotos");
    inputPrice = document.getElementById("inputPrice");
    inputCurrency = document.getElementById("selectCurrency");

    createListingButton == document.getElementById("createListing");

    createListingButton.onclick = createListing;

    console.log("Onload() finished.")
}

function createListing(){

    var formData = new FormData()
    formData.append("Title", inputTitle.value);
    formData.append("Category", inputCategory.value);
    formData.append("Description", inputDesc.value);
    formData.append("Photos", inputPhotos.value);
    formData.append("Price", inputPrice.value);
    formData.append("Currency", inputCurrency.value);

    console.log("Adding item " + inputTitle.value);

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {

        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            //body = document.getElementsByTagName("body")[0].innerHTML = xhr.response;
            alert(xhr.response);
            return;
        }
    }

    xhr.open("POST", "/createlistinglequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(formData);
}
