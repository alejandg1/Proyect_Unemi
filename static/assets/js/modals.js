function closeModal(id) {
    container = document.getElementById(`info-${id}`)
    container.style.display = "none"
    

    buttonShow = document.getElementById(`buttonShow-${id}`)
    buttonShow.style.display = 'block'

    buttonLess = document.getElementById(`buttonLess-${id}`)
    buttonLess.style.display = 'none'
}

async function openModal(id) {
    try {
        
        const response = await fetch('/data_response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                teacher_id: id
            })

        });
        
        if (!response.ok) {
            throw new Error(`Error al recibir los datos: ${response.status}`);
        }

        const data = await response.json();

        buttonShow = document.getElementById(`buttonShow-${id}`)
        buttonShow.style.display = 'none'

        buttonLess = document.getElementById(`buttonLess-${id}`)
        buttonLess.style.display = 'block'

        container = document.getElementById(`info-${id}`)
        container.innerText = ""

        var dataItem = document.createElement("div");
            dataItem.style.display = "inline-block";
            dataItem.style.textAlign = "center";
            dataItem.style.margin = "20px";

        
        if (data.projects != null) {

                const h5 = document.createElement('h5')
                h5.textContent = "Proyectos"
                h5.style.fontWeight = "bold"
                dataItem.appendChild(h5)
    
    
                data.projects.forEach(element => {
                    var dataProject = document.createElement("p");
                    dataProject.innerText = element.project_name;
                    dataProject.style.textAlign = "center";
                    dataItem.appendChild(dataProject)
                });
    
            }

        if (data.articles != null) {

            const h5 = document.createElement('h5')
            h5.textContent = "Artículos"
            h5.style.fontWeight = "bold"
            dataItem.appendChild(h5)

            data.articles.forEach(element => {
                var dataArticle = document.createElement("p");
                dataArticle.innerText = element.article_name;
                dataArticle.style.textAlign = "center";
                dataItem.appendChild(dataArticle)
            });
        }

        if (data.research != null) { 

            const h5 = document.createElement('h5')
            h5.textContent = "Investigaciones"
            h5.style.fontWeight = "bold"
            dataItem.appendChild(h5)

            data.research.forEach(element => {
                var dataResearch = document.createElement("p");
                dataResearch.innerText = element.research_name;
                dataResearch.style.textAlign = "center";
                dataItem.appendChild(dataResearch)
            });

        }

        container.appendChild(dataItem);

        container.style.display = "block"

    } catch (error) {
      console.error('ERROR:', error)
    }
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}