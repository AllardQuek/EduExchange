document.addEventListener('DOMContentLoaded', () => {
    saveIcons = document.querySelectorAll('.fa-bookmark');
    console.log(saveIcons);
    saveIcons.forEach(icon => {
        icon.onclick = () => {
            console.log("SAVE!");
            console.log(icon.dataset.qnid);
            // saveQn(icon);
        }
    })
})


function saveQn(icon) {
    fetch(`save/${icon.dataset.qnid}`)
    .then(response => response.text())
    .then(text => {
        console.log(text);
        // Query specific bookmark using id
        // Remove old class, add solid style class
    });
}