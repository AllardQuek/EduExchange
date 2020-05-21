document.addEventListener('DOMContentLoaded', () => {
    upIcons = document.querySelectorAll('.vote-icon');
    upIcons.forEach(icon => {
        icon.onclick = () => {
            console.log(`Ans id: ${icon.dataset.ansid}`);
            console.log(`Vote: ${icon.dataset.vote}`);
            submitVote(icon);
        }
    })
})


function submitVote(icon) {
    fetch(`/vote/${icon.dataset.ansid}/${icon.dataset.vote}`)
    .then(response => response.text())      // New vote count should be returned
    .then(text => {                         // Take response as input to function
        console.log(`New vote count: ${text}`);
        document.querySelector(`#ans-${icon.dataset.ansid}`).innerHTML = text;
    });
}