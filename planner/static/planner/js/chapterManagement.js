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

    chaptersTable.addEventListener('click', function(event) {
        handleTableClick(event, courseId);
    });
}

// Chapter Table Functions
function handleTableClick(event, courseId) {
    const target = event.target;
    const row = target.closest('.selectable-row');
    const checkbox = target.closest('input[type="checkbox"]');

    if (row) {
        selectRow(row);
        const chapterId = row.getAttribute('data-chapter-key');
        fetchChapterDetail(chapterId);
    } else if (checkbox) {
        const chapterId = checkbox.closest('.selectable-row').getAttribute('data-chapter-key');
        completeChapter(courseId, chapterId);
    }
}

function selectRow(row) {
    deselectAllRows();
    row.classList.add('selected-row');
}

function deselectAllRows() {
    document.querySelectorAll('#chaptersTable .selectable-row').forEach(r => r.classList.remove('selected-row'));
}

function updateChaptersTable(courseId) {
    $.ajax({
        url: `api/getchapters/`,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var chapters = JSON.parse(data['chapters']);
            var tableBody = $('#chaptersTable tbody');
            tableBody.empty();  // Clear the existing rows

            chapters.forEach(function(chapter) {
                var row = $(`
                    <tr class="selectable-row" data-chapter-key="${chapter.pk}">
                        <td class="text-center">
                            <input type="checkbox" id="myCheckbox" ${chapter.fields.completed ? 'checked' : ''} style="width: 20px; height: 20px;">
                        </td>
                        <td class="text-center">${chapter.fields.order}</td>
                        <td>${chapter.fields.title}</td>
                        <td class="text-center">${chapter.fields.progress}%</td>
                        <td class="text-center">
                            <button data-url="/course/${courseId}/chapter/${chapter.pk}/update/" class="btn btn-sm btn-primary edit-btn">
                                <i class="bi-pencil"></i> <!-- Bootstrap pencil icon -->
                            </button>
                            <button data-url="/course/${courseId}/chapter/${chapter.pk}/delete/" class="btn btn-sm btn-danger delete-btn">
                                <i class="bi-trash2-fill"></i> <!-- Bootstrap trash icon -->
                            </button>
                        </td>
                    </tr>   
                `);

                row.find('.edit-btn').on('click', function(e) {
                    var updateUrl = $(this).data('url');
                
                    $.get(updateUrl, function(data) {
                        $('#formColumn').html(data);
                        $('#formColumn').find('form').attr('action', updateUrl);
                    });
                });
                
                row.find('.delete-btn').on('click', function(e) {
                    var deleteUrl = $(this).data('url');
                
                    $.get(deleteUrl, function(data) {
                        $('#formColumn').html(data);
                        $('#formColumn').find('form').attr('action', deleteUrl);
                    });
                });
                

                tableBody.append(row);
            });

            attachCheckboxListeners();
        }
    });
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
    fetch(`chapter/${chapterId}/`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('formColumn').innerHTML = html;
        });
}

function completeChapter(courseId, chapterId) {
    let csrftoken = getCookie('csrftoken');

    fetch(`api/completechapter/${chapterId}/`, {
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

