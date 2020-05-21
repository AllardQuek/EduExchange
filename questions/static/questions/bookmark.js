document.addEventListener('DOMContentLoaded', () => {

    saveIcons = document.querySelectorAll('.fa-bookmark');
        saveIcons.forEach(icon => {
            icon.onclick = () => {
                console.log("SAVE!");
                console.log(`Qn ID: ${icon.dataset.qnid}`);
                saveQn(icon);
            }
        })
})


function saveQn(icon) {
    // NOTE: fetch url will be relative if you don't start with forward slash
    // Start with '/' for absolute path: https://stackoverflow.com/questions/52260498/relative-path-being-added-to-fetch-request
    fetch(`/save/${icon.dataset.qnid}`)
    .then(response => response.text())
    .then(text => {
        console.log(text);
        // Remove old class, add opposite class (DO NOT GET MIXED UP! 's' is for solid)
        if (text === "Saved") {
            icon.classList.remove('far');        
            icon.classList.add('fas');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
        }
    });
}