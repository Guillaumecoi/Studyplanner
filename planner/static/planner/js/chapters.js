// Declare global variables
let courseId = document.getElementById('parentCourse').getAttribute('course-id');
let chaptersTable = document.getElementById('chaptersTable');
let createChapterButton = document.getElementById('createChapterButton');

document.addEventListener('DOMContentLoaded', function() {
    initialize();
});

function initialize() {
    loadChapterCreateForm(courseId);
    updateChaptersTable(courseId);
    attachEventListeners();
}

function attachEventListeners() {
    createChapterButton.addEventListener('click', function() {
        loadChapterCreateForm(courseId);
        deselectAllRows();
    });

    // Delegate the click event to the chaptersTable
    chaptersTable.addEventListener('click', function(event) {
        // Check if the clicked element is part of a row and not a button or checkbox
        const target = event.target;
        if (target.tagName !== 'BUTTON' && target.type !== 'checkbox') {
            const row = target.closest('tr');
            selectRow(row);
            const chapterId = row.getAttribute('data-chapter-key');
            fetchChapterDetail(chapterId);
        }
    });
}

function selectRow(row) {
    deselectAllRows();
    if (row) {  // Ensure that the row exists
        row.classList.add('selected-row');
    }
}

function deselectAllRows() {
    document.querySelectorAll('#chaptersTable .selectable-row').forEach(r => r.classList.remove('selected-row'));
}

function updateChaptersTable(courseId) {
    $.ajax({
        url: `chapter`,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var chapters = JSON.parse(data['chapters']);
            var tableBody = document.getElementById('chaptersTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = '';  // Clear the existing rows

            chapters.forEach(function(chapter) {
                const row = tableBody.insertRow();
                row.setAttribute('data-chapter-key', chapter.pk);

                // Add a checkbox cell
                const checkboxCell = row.insertCell();
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'large-checkbox';
                checkboxCell.className = 'text-center';
                checkbox.checked = chapter.fields.completed;
                checkboxCell.appendChild(checkbox);

                // Checkbox change event
                checkbox.addEventListener('change', function() {
                    completeChapter(courseId, chapter.pk);
                });

                // Order cell
                const orderCell = row.insertCell();
                orderCell.textContent = chapter.fields.order;
                orderCell.className = 'text-center';

                // Title cell (no center alignment)
                const titleCell = row.insertCell();
                titleCell.textContent = chapter.fields.title;

                // Progress cell
                const progressCell = row.insertCell();
                progressCell.textContent = chapter.fields.progress + '%';
                progressCell.className = 'text-center';

                // Action cell
                const actionCell = row.insertCell();
                actionCell.className = 'text-center gap-2';

                // Flex container for gap between buttons
                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'd-flex justify-content-center gap-1';
                actionCell.appendChild(buttonContainer);

                // Create edit button
                const editButton = createButton('btn-primary', 'bi-pencil', () => {
                    editChapter(chapter.pk);
                });
                buttonContainer.appendChild(editButton);

                // Create delete button
                const deleteButton = createButton('btn-danger', 'bi-trash2-fill', () => {
                    deleteChapter(chapter.pk);
                });
                buttonContainer.appendChild(deleteButton);
            });
        },
        error: function(xhr, status, error) {
            console.error('Error fetching chapters:', error);
        }
    });
}

function deleteChapter(chapterId) {
    if (confirm('Are you sure you want to delete this chapter?')) {
        console.log('Deleting chapter:', chapterId);

        let csrftoken = getCookie('csrftoken');

        fetch(`/chapter/${chapterId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Refresh the table after successful deletion
            updateChaptersTable(courseId);
        })
        .catch(error => {
            console.error('Error deleting chapter:', error);
            alert('Error deleting chapter: ' + error.message);
        });
    } else {
        console.log('Chapter deletion canceled');
    }
}

function editChapter(chapterId) {
    const updateUrl = `/chapter/${chapterId}/update/`;

    fetch(updateUrl)
        .then(response => response.text())
        .then(html => {
            document.getElementById('formColumn').innerHTML = html;
            const form = document.getElementById('formColumn').querySelector('form');
            form.setAttribute('action', updateUrl);
        })
        .catch(error => console.error('Error loading chapter update form:', error));
}



function attachCheckboxListeners() {
    let checkboxes = chaptersTable.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.removeEventListener('change', checkboxChangeHandler); // Remove existing event listener to avoid duplicates
        checkbox.addEventListener('change', checkboxChangeHandler);
    });
}

function checkboxChangeHandler() {
    // Get the chapter id from the row
    let row = this.closest('.selectable-row');
    let chapterId = row.getAttribute('data-chapter-key');

    // Call the completeChapter function
    completeChapter(courseId, chapterId);
}


function loadChapterCreateForm() {
    var baseUrl = document.getElementById('createChapterButton').getAttribute('data-base-url');

    fetch(baseUrl)
        .then(response => response.text())
        .then(html => {
            document.getElementById('formColumn').innerHTML = html;
            var form = formColumn.querySelector('form');
            form.setAttribute('action', baseUrl);
        });
}


function fetchChapterDetail(chapterId) {
    fetch(`/chapter/${chapterId}/`)
        .then(response => response.text())
        .then(html => {
            const formColumn = document.getElementById('formColumn');
            formColumn.innerHTML = html;
            // Now call the function to populate study sessions
            populateStudySessions(chapterId);
        })
        .catch(error => console.error('Error fetching chapter detail:', error));
}


function completeChapter(chapterId) {
    let csrftoken = getCookie('csrftoken');

    fetch(`/chapter/${chapterId}/complete`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Parse the response body as JSON
        return response.json();
    })
    .then(data => {
        // Handle the JSON data
        if (data.status === 'success') {
            fetchChapterDetail(chapterId)
            updateChaptersTable(courseId)
        } else {
            console.error('Chapter could not be completed:', data.error);
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createButton(btnClass, iconClass, onClick) {
    const button = document.createElement('button');
    button.classList.add('btn', 'btn-sm', btnClass);
    const icon = document.createElement('i');
    icon.classList.add('bi', iconClass);
    button.appendChild(icon);
    button.onclick = onClick;
    return button;
}

