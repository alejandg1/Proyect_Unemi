let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');

async function collage() {
  let url = "http://127.0.0.1:8000/mkcol/"
  let resp = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  let data = await resp.json()
  // let collage = data.collage
  console.log(data)
  // let img = new Image()
  // img.src = collage
  // img.onload = () => {
  //   ctx.drawImage(img, 0, 0)
  // }
}
