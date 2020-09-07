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


// send form details
const modalCloseButton = document.getElementById('modal-close-button');
const infoForm = document.forms['update-info-form'];
const submitInfoButton = document.getElementById('info-submit-button');
const modalCloseCallback = (event) => {
    submitInfoButton.disabled = true;
    document.getElementById(event.target.dataset.modalId).style.display = 'none';
}

if (infoForm) {
    infoForm.addEventListener('change', () => submitInfoButton.disabled = false);

    infoForm.addEventListener('submit', (event) => {
        event.preventDefault();
        modalCloseButton.disabled = true;
        const title = document.getElementById('modal-title-1');
        title.innerHTML = '<h2>Updating info...</h2>';
        submitInfoButton.disabled = true;

        const infoOptions = {
            url: infoForm.action,
            responseType: 'json',
            error: () => {
                document.getElementById('info-update-error').style.display = 'block';
                submitInfoButton.disabled = false;
            },
            success: () => {
                document.getElementById('info-stream').innerText = 'Stream : New Stream';
                document.getElementById('info-branch').innerText = 'Branch : New Branch';
                document.getElementById('info-year').innerText = 'Year : New Year';
                title.innerHTML = '<h2>Update info</h2>';
                modalCloseButton.disabled = false;
                modalCloseCallback(event);
            },
            form: infoForm
        };

        ajax.post(infoOptions);
    });    
};


// close update form
modalCloseButton.addEventListener('click', modalCloseCallback);



/* 
    Bio submition
*/
const bioForm = document.forms['bio-form'];

if (bioForm) {
    const submitInfoButton = document.getElementById('bio-form-sub');
    bioForm.onchange = () => submitInfoButton.disabled = false;

    bioForm.onsubmit = (event) => {
        event.preventDefault();
        submitInfoButton.innerText = 'Updating...';

        const options = {
            url: bioForm.action,
            responseType: 'json',
            error: () => {
                submitInfoButton.innerText = 'Could not update!';
                document.getElementById('bio-error').style.display = 'block';
                bioForm[1].disabled = true;
            },
            success: () => {
                document.getElementById('bio-div').innerText = bioForm[1].value;
                submitInfoButton.innerText = 'Update bio'
                toogleForm(document.getElementById('bio-form-toogle'));
            },
            form: bioForm
        };
    
        ajax.post(options);
    };

};


/* 
    Delete skill
*/

const skillDeleteCallback = (skillDeleteButton) => {
    // delete skill
    const skillDeleteOptions = {
        url: skillDeleteButton.parentElement.action,
        responseType: 'json',
        error: () => {
            document.getElementById(skillDeleteButton.dataset.errorId).style.display = 'block';
        },
        success: () => {
            document.getElementById(skillDeleteButton.dataset.formId).innerText = 'Skill deleted!'
        },
        form: skillDeleteButton.parentElement
    };   
    
    ajax.post(skillDeleteOptions);
};


[...document.getElementsByClassName('delete-skill')].forEach((skillDeleteButton) => {
    skillDeleteButton.addEventListener('click', () => {
        skillDeleteCallback(skillDeleteButton);
    });
});


/* 
    add skill
*/
const skillForm = document.forms['skill-form'];

if (skillForm) {
    const submitSkillButton = [...skillForm.elements].find((element) => element.type === 'submit');
    skillForm.addEventListener('change', () => {
        submitSkillButton.disabled = false;
    });

    skillForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const skillAddOptions = {
            url: skillForm.action,
            responseType: 'json',
            error: () => {
                if (submitSkillButton) {
                    submitSkillButton.value = 'Could not add skill!';
                    submitSkillButton.disabled = true;
                }
                document.getElementById('skill-error').style.display = 'block';
                skillForm[1].disabled = true;
            },
            success: () => {
                const token = skillForm.elements['csrfmiddlewaretoken']? skillForm.elements.csrfmiddlewaretoken.value: '';
                // add correct details to the function call below
                createSkill('Test', 10, token, '/account/mock');
                const noSkills = document.getElementById('no-skills-div');
                if (noSkills) {
                    noSkills.style.display = 'none';
                };
                toogleForm(document.getElementById('add-skill-toogle'));
            },
            form: skillForm
        };

        ajax.post(skillAddOptions);
    });
};


/* 
    create a new skill div
*/
function createSkill(skillText, skillId, formToken, formAction) {
    console.log(formToken)
    const topDiv = document.createElement('div');
    topDiv.id = `skill-${skillId}`;

    const deleteError = document.createElement('span');
    deleteError.id = `skill-${skillId}-del-error`;
    deleteError.style.display = 'none';
    deleteError.innerText = 'Could Delete skill, please refresh the page and try again';
    topDiv.appendChild(deleteError);

    const skillRow = document.createElement('div');
    skillRow.className = "skill-row";

    const skillTitle = document.createElement('span');
    skillTitle.innerText = skillText;
    skillTitle.className = "skill-title";
    skillRow.appendChild(skillTitle);


    const deleteForm = document.createElement('form');
    deleteForm.action = formAction;
    deleteForm.className = "skill-delete-form";
    deleteForm.method = 'POST';
    [['csrfmiddlewaretoken', formToken], ['skill-id', skillId]].forEach((input) => {
        const _input = document.createElement('input');
        _input.type = 'hidden';
        _input.name = input[0];
        _input.value = input[1];
        deleteForm.appendChild(_input);
    });
    const submitSpan = document.createElement('span');
    submitSpan.classList = 'fa fa-trash delete-skill';
    submitSpan.dataset.formId = topDiv.id;
    submitSpan.dataset.errorId = deleteError.id;
    deleteForm.appendChild(submitSpan);
    submitSpan.addEventListener('click', () => skillDeleteCallback(submitSpan));
    skillRow.appendChild(deleteForm);

    topDiv.appendChild(skillRow);
    topDiv.appendChild(document.createElement('hr'));
    document.getElementById('all-skills').appendChild(topDiv);
};