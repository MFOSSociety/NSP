/* 
    This function toggles the display status of a form
    pass it a button that's used to toogle
    the button should have 2 attributes
        1. 'data-form-id': id of the form to toogle display.
        2. 'data-og-text': the original text on the button.
*/
function toogleForm (target) {
    const formId = target.dataset.formId;
    const form = document.getElementById(formId);

    if (form) {
        if (form.style.display === 'none' || !form.style.display) {
            form.style.display = 'block';
            target.innerText = 'close form';
        } else {
            form.style.display = 'none';
            target.innerText = target.dataset.ogText;
        };
    };
};


// add listener to buttons to show forms
[...document.getElementsByClassName('toggle-form')].forEach((button) => {
    button.addEventListener('click', (event) => {
        toogleForm(event.target);
    });
});


/* 
    Profile pic upload
*/
function uploadPic () {
    document.getElementById('profile-pic').click();
};


document.getElementById('profile-pic').addEventListener('change', (event) => {
    // preview new profile pic for the user
    const reader = new FileReader();
    reader.onload = (event) => document.getElementById('user-profile-pic').src = event.target.result;
    reader.readAsDataURL(event.target.files[0]);

    // choose another picture
    document.getElementById('profile-pic-upload').innerText = 'choose another picture';
    // save button
    document.getElementById('profile-pic-save').style.display = 'block';
    document.getElementById('preview-warning').style.display = 'block';
});


/* 
    update info now
*/

// open update-form
document.getElementById('update-info-btn').addEventListener('click', () => {
    document.getElementById('update-info-now').style.display = 'block';
})


// close update form
document.getElementById('modal-close-button').addEventListener('click', (event) => {
    document.getElementById(event.target.dataset.modalId).style.display = 'none';
});



/* 
    Bio submition
*/
const bioForm = document.forms['bio-form'];

if (bioForm) {
    const submitButton = document.getElementById('bio-form-sub');
    bioForm.onchange = () => submitButton.disabled = false;

    bioForm.onsubmit = (event) => {
        event.preventDefault();
        submitButton.innerText = 'Updating...';

        const options = {
            url: bioForm.action,
            responseType: 'json',
            error: () => {
                submitButton.innerText = 'Could not update!';
                document.getElementById('bio-error').style.display = 'block';
                bioForm[1].disabled = true;
            },
            success: () => {
                document.getElementById('bio-div').innerText = bioForm[1].value;
                submitButton.innerText = 'Update bio'
                toogleForm(document.getElementById('bio-form-toogle'));
            },
            form: bioForm
        };
    
        ajax.post(options);
    };

};