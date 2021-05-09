
function toggleLike(post_id) {
    fetch("/toggle-like/" + post_id, {
        method: "POST"
    })
    .then(response => response.json())
    .then(res => {
        const btn = document.getElementById("like-btn-" + post_id);
        const btn_icon = document.getElementById("like-btn-icon-" + post_id);
        const btn_text = document.getElementById("like-btn-text-" + post_id);
        if (res.status == "liked") {
            //remove unliked classes
            btn.classList.remove("btn-outline-secondary");
            btn_icon.classList.remove("bi-heart");
            // add like classes
            btn.classList.add("btn-outline-danger");
            btn_icon.classList.add("bi-heart-fill");
        } else if (res.status == "unliked") {
            //remove like classes
            btn.classList.remove("btn-outline-danger");
            btn_icon.classList.remove("bi-heart-fill");
            // add unliked classes
            btn.classList.add("btn-outline-secondary");
            btn_icon.classList.add("bi-heart");
        }
        //update data
        btn_text.innerText = " " + res.likes + (res.likes == 1 ? " like" : " likes");
    });
}

function toggleFollow(follow_id) {
    fetch("/toggle-follow/" + follow_id, {
        method: "POST"
    })
    .then(response => response.json())
    .then(res => {
        const btn = document.getElementById("follow-btn");
        const btn_icon = document.getElementById("follow-btn-icon");
        const btn_text = document.getElementById("follow-btn-text");
        if (res.status == "followed") {
            //remove unliked classes
            btn.classList.remove("btn-outline-secondary");
            btn_icon.classList.remove("bi-plus");
            // add like classes
            btn.classList.add("btn-outline-danger");
            btn_icon.classList.add("bi-check");
            //update data
            btn_text.innerText = " Following";
        } else if (res.status == "unfollowed") {
            //remove like classes
            btn.classList.remove("btn-outline-danger");
            btn_icon.classList.remove("bi-check");
            // add unliked classes
            btn.classList.add("btn-outline-secondary");
            btn_icon.classList.add("bi-plus");
            //update data
            btn_text.innerText = " Follow";
        }
    });
}

function editPost(post_id) {
    const header = document.getElementById("post-card-header-" + post_id);
    const content = document.getElementById("post-content-" + post_id);
    const btn_row = document.getElementById("post-btn-row-" + post_id);
    const post_text = document.getElementById("post-text-" + post_id);

    //create elements for edit mode
    const new_header = document.createElement("h4");
    const save_btn = document.createElement("button");
    const edit_textarea = document.createElement("textarea");

    //change required classes
    save_btn.classList.add("btn");
    save_btn.classList.add("btn-primary");
    save_btn.classList.add("mt-3");
    save_btn.classList.add("form-control");
    edit_textarea.classList.add("form-control");
    edit_textarea.rows = 4;

    //add id to fetch data later
    edit_textarea.id = "post-edit-textarea-" + post_id;

    //add necessary data to elements
    new_header.innerText = "Edit Post";
    save_btn.innerText = "Save";
    edit_textarea.innerText = post_text.innerText;

    //add save on click listener
    save_btn.addEventListener("click", () => savePost(post_id));

    //remove old elements and add new elements to DOM
    header .innerHTML = "";
    content.innerHTML = "";
    btn_row.innerHTML = "";
    header.appendChild(new_header);
    content.appendChild(edit_textarea);
    btn_row.appendChild(save_btn);

}

function savePost(post_id) {
    post_update = {
        text: document.getElementById("post-edit-textarea-" + post_id).value
    }
    fetch("/post-edit/" + post_id, {
        method: "POST",
        body: JSON.stringify(post_update)
    })
    .then(response => response.json())
    .then(res => {
        post = res.post;

        // fetch all necessary elements to modify
        const header = document.getElementById("post-card-header-" + post_id);
        const content = document.getElementById("post-content-" + post_id);
        const btn_row = document.getElementById("post-btn-row-" + post_id);

        // create elements for return to normal post
        const header_link = document.createElement("a");
        const new_header = document.createElement("h4");
        const text_div = document.createElement("div");
        const timestamp_div = document.createElement("div");
        const like_btn = document.createElement("button");
        const like_btn_icon = document.createElement("i");
        const like_btn_text = document.createElement("span");
        //since we are working in the edit function already,
        //we can assume the edit but will need to be restored
        const edit_btn = document.createElement("button");
        const edit_btn_icon = document.createElement("i");
        const edit_btn_text = document.createElement("span");

        //add data
        new_header.innerText = post.poster;
        header_link.href = "profile/" + post.poster + "/1";
        text_div.innerText = post.text;
        text_div.id = "post-text-" + post.id;
        timestamp_div.innerText = post.timestamp;
        like_btn.id = "like-btn-" + post.id;
        like_btn_icon.id = "like-btn-icon-" + post.id;
        like_btn_text.id = "like-btn-text-" + post.id;
        like_btn_text.innerText = " " + post.likes.length + " " + (post.likes.length == 1 ? "Like" : "Likes");
        edit_btn.id = "edit-btn-" + post.id;
        edit_btn_text.innerText = " Edit";

        //add necessary classes
        header_link.classList.add("mb-2");
        text_div.classList.add("mb-2");
        timestamp_div.classList.add("mb-4");
        timestamp_div.classList.add("grey-text");
        timestamp_div.classList.add("timestamp-size");
        edit_btn.classList.add("btn");
        edit_btn.classList.add("btn-link");
        edit_btn_icon.classList.add("bi");
        edit_btn_icon.classList.add("bi-pencil-square");
        like_btn.classList.add("btn");
        like_btn_icon.classList.add("bi");
        if (post.likes.includes(post.poster_id)) {
            like_btn.classList.add("btn-outline-danger");
            like_btn_icon.classList.add("bi-heart-fill");
        } else {
            like_btn.classList.add("btn-outline-secondary");
            like_btn_icon.classList.add("bi-heart");
        }

        //add event listeners
        like_btn.addEventListener("click", () => toggleLike(post.id));
        edit_btn.addEventListener("click", () => editPost(post.id));

        //add to DOM
        header.innerHTML = "";
        content.innerText = "";
        btn_row.innerHTML = "";

        header_link.appendChild(new_header);
        header.appendChild(header_link);
        content.appendChild(text_div);
        content.appendChild(timestamp_div);
        like_btn.appendChild(like_btn_icon);
        like_btn.appendChild(like_btn_text);
        edit_btn.appendChild(edit_btn_icon);
        edit_btn.appendChild(edit_btn_text);
        btn_row.appendChild(like_btn);
        btn_row.appendChild(edit_btn);

    });
}