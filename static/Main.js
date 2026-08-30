const postList = document.getElementById("post-list");

if (postList) {
    const numberOfPosts = document.querySelectorAll(".post-preview").length;
    const postWord = numberOfPosts === 1 ? " post" : " posts";
    document.getElementById("post-count").textContent = numberOfPosts + postWord;
}

const deleteForms = document.querySelectorAll(".delete-form");

deleteForms.forEach(function (deleteForm) {
    deleteForm.addEventListener("submit", function (event) {
        const shouldDelete = confirm("Delete this post?");
        if (!shouldDelete) {
            event.preventDefault();
        }
    });
});
