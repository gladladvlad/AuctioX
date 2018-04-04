window.onload = function(){

    signInButton == document.getElementById("signInButton");

    signInButton.onclick = SignIn;

    console.log("Onload() finished.")
}

function SignIn(){
    inputUser = document.getElementById("inputEmail");
    inputPass = document.getElementById("inputPassword");

    user = inputUser.value;
    pass = inputPass.value;

    console.log(user + ' ' + pass);

    xhr = new XMLHttpRequest();


}