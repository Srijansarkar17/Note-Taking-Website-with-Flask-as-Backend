function deleteNote(noteId){
    fetch('/deleteNote',{ //sends a request to deleteNote end-point
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/";  //reloads/refreshes the window, i.e in this case the home page
    })
}