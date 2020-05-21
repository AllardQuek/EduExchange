document.addEventListener('DOMContentLoaded', () => {
    upIcons = document.querySelectorAll('.fa-arrow-alt-circle-up');
    upIcons.forEach(icon => {
        icon.onclick = () => {
            console.log('UPVOTE');
        }
    })
})


