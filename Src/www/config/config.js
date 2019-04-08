function checkError(){
    const url = window.location.href;
    if(url.includes("error")){
        const container = document.getElementById("errorContainer");
        container.style.visibility = "visible" 
    }
    console.log(url)
}
function handlerBtnSave() {

    const essidField = document.getElementById("essid");
    const passwordField = document.getElementById("pass");
    const isCorrect = essidField.checkValidity() && passwordField.checkValidity();
    if(isCorrect){
        const loader = document.getElementById("loaderContainer");
        loader.style.visibility = "visible"   
    }
    
}