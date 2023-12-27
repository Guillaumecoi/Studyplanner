function populateStudySessions(chapterId) {
    console.log('Populating study sessions');
    const url = `/chapter/${chapterId}/studysession/`;
    console.log('URL:', url);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Data:', data);
        
            if (typeof data.studysessions === 'string') {
                const studysessionsArray = JSON.parse(data.studysessions);
                
                const tbody = document.querySelector('#studysessionTable tbody');
                tbody.innerHTML = '';  // Clear existing rows in tbody only
        
                // Iterate over each study session and add rows to tbody
                studysessionsArray.forEach(studysession => {
                    const row = tbody.insertRow();
                    row.insertCell().textContent = new Date(studysession.fields.date).toLocaleDateString();
                    row.insertCell().textContent = studysession.fields.time_spent;
                    row.insertCell().textContent = studysession.fields.pages_done;
                    row.insertCell().textContent = studysession.fields.slides_done;

                    // Action cell
                    const actionCell = row.insertCell();
                    actionCell.className = 'text-center gap-2';

                    // Flex container for gap between buttons
                    const buttonContainer = document.createElement('div');
                    buttonContainer.className = 'd-flex justify-content-center gap-1';
                    actionCell.appendChild(buttonContainer);

                    // Create edit button
                    const editButton = createButton('btn-primary', 'bi-pencil', () => {
                        editStuddysession(studysession.pk);
                    });
                    buttonContainer.appendChild(editButton);

                    // Create delete button
                    const deleteButton = createButton('btn-danger', 'bi-trash2-fill', () => {
                        deleteStudySession(studysession.pk);
                    });
                    buttonContainer.appendChild(deleteButton);
                });
            } else {
                console.error('studysessions is not a valid JSON string');
            }
        })
        .catch(error => console.error('Error fetching study sessions:', error));      
}

function deleteStudySession(sessionId) {
    console.log('Deleting session:', sessionId);
    if (confirm('Are you sure you want to delete this studysession?')) {
        console.log('Deleting studysession:', sessionId);

        let csrftoken = getCookie('csrftoken');

        fetch(`/studysession/${sessionId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Reload the page
            location.reload();
        })
        .catch(error => {
            console.error('Error deleting studysession:', error);
        });
    }
}

function editStuddysession(sessionId) {
    const updateUrl = `/studysession/${sessionId}/update/`;

    fetch(updateUrl)
        .then(response => response.text())
        .then(html => {
            document.getElementById('formColumn').innerHTML = html;
            const form = document.getElementById('formColumn').querySelector('form');
            form.setAttribute('action', updateUrl);
        })
        .catch(error => console.error('Error loading chapter update form:', error));
}
