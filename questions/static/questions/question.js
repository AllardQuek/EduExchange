document.addEventListener('DOMContentLoaded', () => {
    upIcons = document.querySelectorAll('.vote-icon');
    upIcons.forEach(icon => {
        icon.onclick = () => {
            console.log(icon.dataset.ansid);
            console.log(icon.dataset.vote);
            // submitVote(icon);
        }
    })
})


function submitVote(icon) {
    fetch(`/vote/${icon.dataset.ansid}/${icon.dataset.vote}`)
    .then(response => response.text())      // New vote count should be returned
    .then(text => {                         // Take response as input to function
        console.log(text);
        if (text.includes("Already")) {
            return;
        } else {
            document.querySelector(`#ans-${icon.dataset.ansid}`).innerHTML = text;
        }
    });
}