// let user = document.getElementById('user').value
// let token = document.getElementById('token').value

window.addEventListener('unload', async (e) => {
  e.preventDefault();
  await sendLog();
})

url = "http://127.0.0.1:8000/"
async function sendLog() {
  let resp = await fetch(url + "logout/", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  console.log(resp)
}
