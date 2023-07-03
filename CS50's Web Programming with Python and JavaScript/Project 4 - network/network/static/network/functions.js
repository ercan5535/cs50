function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submit_edit_content(id){
    const text_area_value = document.getElementById(`text_area_${id}`).value
    const content_element = document.getElementById(`post_content_${id}`)
    const modal_element = document.getElementById(`modal_id_${id}`)
    let csrftoken = getCookie('csrftoken');
    fetch(`/edit/${id}`, {
        method: 'POST',
        headers: { "X-CSRFToken": csrftoken },
        body: JSON.stringify({
            new_content: text_area_value
        })
    })
    // update post content
    content_element.innerHTML = text_area_value;

    // close modal
    modal_element.classList.remove('show');
    modal_element.setAttribute('aria-hidden', 'true');
    modal_element.setAttribute('style', 'display: none');

  
    // get modal backdrops
    const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

    // remove every modal backdrop
    for(let i=0; i<modalsBackdrops.length; i++) {
        document.body.removeChild(modalsBackdrops[i]);
    }
}

function like_post(id){
    fetch(`/like/${id}`)
    .then(response => response.json)
    .then(result => {
        console.log(result.message)
    })

    // toggle button
    btn_element = document.getElementById(`like_id_${id}`)
    btn_element.classList.remove("fa-thumbs-up")
    btn_element.classList.add("fa-thumbs-down")
}

function unlike_post(id){
    console.log("unlike")
    fetch(`/unlike/${id}`)
    .then(response => response.json)
    .then(result => {
        console.log(result.message)
    })
    
    // toggle button
    btn_element = document.getElementById(`like_id_${id}`)
    btn_element.classList.remove("fa-thumbs-down")
    btn_element.classList.add("fa-thumbs-up")
}