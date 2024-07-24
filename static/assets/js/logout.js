let user = document.getElementById('user').value
let token = document.getElementById('token').value

window.addEventListener('beforeunload', (e) => {
  e.preventDefault();
  sendLog();
})

url = "http://127.0.0.1:8000/"
async function sendLog() {
  let resp = await fetch(url + "logout/", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      "X-csrftoken": token
    },
    body: JSON.stringify({ user: user })
  })
  console.log(resp)
}
