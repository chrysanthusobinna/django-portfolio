
// Function to set the current year
function setCurrentYear() {
    const element = document.getElementById('currentYear');
    if (element) {
        element.textContent = new Date().getFullYear();
    }
}

// Function to toggle navbar visibility
function toggleNavbar() {
    $('#navbarToggler').click(function () {
        $('#navbarNav').toggleClass('show');
    });
}

// Function to handle the "View Project" link click event
function viewProjectClickHandler() {
    $('.view-project').click(function(e) {
        e.preventDefault();

        // Get the data attributes from the clicked link
        var title = $(this).data('title');
        var description = $(this).data('description');
        var image = $(this).data('image');
        var link = $(this).data('link');

        // Populate the modal with the data
        $('#modalTitle').text(title);
        $('#modalDescription').text(description);
        $('#modalImage').attr('src', image);

        // Check if the link is not empty and display the link button
        if (link !== "#") {
            $('#modalLinkButton').show().attr('href', link);
        } else {
            $('#modalLinkButton').hide();
        }

        $('#viewPortfolioModal').modal('show');
    });
}


// Dynamic label & placeholder mapping per contact type
var contactFieldMeta = {
    phone:     { label: 'Phone Number',       placeholder: 'e.g. +234 801 234 5678' },
    email:     { label: 'Email Address',      placeholder: 'e.g. you@example.com' },
    whatsapp:  { label: 'WhatsApp Number',    placeholder: 'e.g. +234 801 234 5678' },
    instagram: { label: 'Instagram Username', placeholder: 'e.g. your_username' },
    facebook:  { label: 'Facebook Profile',   placeholder: 'e.g. https://facebook.com/yourpage' },
    linkedin:  { label: 'LinkedIn Profile',   placeholder: 'e.g. https://linkedin.com/in/yourname' },
    twitter:   { label: 'Twitter / X Handle', placeholder: 'e.g. @yourhandle' },
    website:   { label: 'Website URL',        placeholder: 'e.g. https://yourwebsite.com' },
    other:     { label: 'Contact Details',    placeholder: 'Enter your contact info' },
};

// Validation patterns per contact type
var contactValidation = {
    phone:     { pattern: /^[+]?[\d\s\-().]{7,20}$/,                         msg: 'Please enter a valid phone number (e.g. +234 801 234 5678)' },
    email:     { pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,                      msg: 'Please enter a valid email address (e.g. you@example.com)' },
    whatsapp:  { pattern: /^[+]?[\d\s\-().]{7,20}$/,                         msg: 'Please enter a valid WhatsApp number (e.g. +234 801 234 5678)' },
    instagram: { pattern: /^@?[a-zA-Z0-9._]{1,30}$/,                        msg: 'Please enter a valid Instagram username (e.g. your_username)' },
    facebook:  { pattern: /^(https?:\/\/(www\.)?facebook\.com\/.+|[a-zA-Z0-9.]+)$/, msg: 'Please enter a Facebook URL (e.g. https://facebook.com/yourpage) or username' },
    linkedin:  { pattern: /^(https?:\/\/(www\.)?linkedin\.com\/.+|[a-zA-Z0-9\-]+)$/, msg: 'Please enter a LinkedIn URL (e.g. https://linkedin.com/in/yourname) or username' },
    twitter:   { pattern: /^@?[a-zA-Z0-9_]{1,15}$/,                         msg: 'Please enter a valid Twitter/X handle (e.g. @yourhandle)' },
    website:   { pattern: /^https?:\/\/.+\..+/,                              msg: 'Please enter a valid URL starting with http:// or https://' },
};

// Validate contact value against the selected type
function validateContactValue(type, value) {
    var rule = contactValidation[type];
    if (!rule) return { valid: true };  // 'other' or unknown — no validation
    if (rule.pattern.test(value.trim())) return { valid: true };
    return { valid: false, msg: rule.msg };
}

// Show or clear validation feedback on an input
function setContactValidationError(inputId, errorMsg) {
    var input = document.getElementById(inputId);
    var feedbackId = inputId + '_feedback';
    var feedback = document.getElementById(feedbackId);

    if (!feedback) {
        // Create feedback element if it doesn't exist
        feedback = document.createElement('div');
        feedback.id = feedbackId;
        feedback.className = 'invalid-feedback';
        input.parentNode.appendChild(feedback);
    }

    if (errorMsg) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = errorMsg;
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '';
    }
}

function clearContactValidation(inputId) {
    var input = document.getElementById(inputId);
    if (input) {
        input.classList.remove('is-invalid', 'is-valid');
    }
    var feedback = document.getElementById(inputId + '_feedback');
    if (feedback) feedback.textContent = '';
}

function updateContactValueField(selectId, labelId, inputId) {
    var type = document.getElementById(selectId).value;
    var meta = contactFieldMeta[type] || contactFieldMeta['other'];
    document.getElementById(labelId).textContent = meta.label;
    document.getElementById(inputId).placeholder = meta.placeholder;
    clearContactValidation(inputId);
}

// Function to handle contact method modal interactions
function contactMethodHandlers() {
    // Add modal: update on type change
    var addType = document.getElementById('add_contact_type');
    if (addType) {
        addType.addEventListener('change', function() {
            updateContactValueField('add_contact_type', 'add_contact_value_label', 'add_contact_value');
        });
    }

    // Edit modal: update on type change
    var editType = document.getElementById('edit_contact_type');
    if (editType) {
        editType.addEventListener('change', function() {
            updateContactValueField('edit_contact_type', 'edit_contact_value_label', 'edit_contact_value');
        });
    }

    // Validate Add Contact form on submit
    var addForm = document.querySelector('#addContactMethodModal form');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            var type = document.getElementById('add_contact_type').value;
            var value = document.getElementById('add_contact_value').value;
            var result = validateContactValue(type, value);
            if (!result.valid) {
                e.preventDefault();
                setContactValidationError('add_contact_value', result.msg);
            } else {
                clearContactValidation('add_contact_value');
            }
        });
    }

    // Validate Edit Contact form on submit
    var editForm = document.getElementById('editContactMethodForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            var type = document.getElementById('edit_contact_type').value;
            var value = document.getElementById('edit_contact_value').value;
            var result = validateContactValue(type, value);
            if (!result.valid) {
                e.preventDefault();
                setContactValidationError('edit_contact_value', result.msg);
            } else {
                clearContactValidation('edit_contact_value');
            }
        });
    }

    // Live validation as user types (Add)
    var addInput = document.getElementById('add_contact_value');
    if (addInput) {
        addInput.addEventListener('input', function() {
            var type = document.getElementById('add_contact_type').value;
            if (!type) return;
            var result = validateContactValue(type, this.value);
            if (this.value.length > 0) {
                setContactValidationError('add_contact_value', result.valid ? null : result.msg);
            } else {
                clearContactValidation('add_contact_value');
            }
        });
    }

    // Live validation as user types (Edit)
    var editInput = document.getElementById('edit_contact_value');
    if (editInput) {
        editInput.addEventListener('input', function() {
            var type = document.getElementById('edit_contact_type').value;
            var result = validateContactValue(type, this.value);
            if (this.value.length > 0) {
                setContactValidationError('edit_contact_value', result.valid ? null : result.msg);
            } else {
                clearContactValidation('edit_contact_value');
            }
        });
    }

    // Populate Edit Contact modal
    document.querySelectorAll('.edit-contact-method-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('editContactMethodForm').action = this.dataset.url;
            document.getElementById('edit_contact_type').value = this.dataset.type;
            document.getElementById('edit_contact_value').value = this.dataset.value;
            document.getElementById('edit_contact_label').value = this.dataset.label || '';
            updateContactValueField('edit_contact_type', 'edit_contact_value_label', 'edit_contact_value');
        });
    });

    // Populate Delete Contact modal
    document.querySelectorAll('.delete-contact-method-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('deleteContactMethodForm').action = this.dataset.url;
            document.getElementById('deleteContactMethodType').textContent = this.dataset.type;
        });
    });

    // Reset Add modal fields when it opens
    var addModal = document.getElementById('addContactMethodModal');
    if (addModal) {
        addModal.addEventListener('show.bs.modal', function() {
            document.getElementById('add_contact_value_label').textContent = 'Contact Details';
            document.getElementById('add_contact_value').placeholder = 'Select a contact type above';
            clearContactValidation('add_contact_value');
        });
    }
}

 
// Function to handle the "Edit Portfolio" button click event
function editPortfolioClickHandler() {
    $('.edit-portfolio-btn').on('click', function() {
        var url = $(this).data('url');
        var title = $(this).data('title');
        var description = $(this).data('description');
        var link = $(this).data('link');
        var portfolioPhoto = $(this).data('portfolio_photo');

        $('#editPortfolioForm').attr('action', url);
        $('#editPortfolioModal #editPortfolioTitle').val(title);
        $('#editPortfolioModal #editPortfolioDescription').val(description);
        $('#editPortfolioModal #editPortfolioLink').val(link);

        $('#editPortfolioModal #profilePortfolioPreview').attr('src', portfolioPhoto);  
    });
}

// Function to handle the "Edit Certification" button click
function editCertificationClickHandler() {
    $('.edit-certification-btn').on('click', function() {
        var url = $(this).data('url');
        var name = $(this).data('name');
        var issuer = $(this).data('issuer');
        var date = $(this).data('date');

        $('#editCertificationForm').attr('action', url);
        $('#editCertificationModal #editCertificationName').val(name);
        $('#editCertificationModal #editCertificationIssuer').val(issuer);
        $('#editCertificationModal #editCertificationDate').val(date);
    });
}

// Function to handle the "Edit Education" button click
function editEducationClickHandler() {
    $('.edit-education-btn').on('click', function () {
        var url = $(this).data('url');
        var qualification = $(this).data('qualification');
        var institution = $(this).data('institution');
        var start = $(this).data('start');
        var end = $(this).data('end');

        $('#editEducationForm').attr('action', url);
        $('#editEducationModal #editQualification').val(qualification);
        $('#editEducationModal #editInstitutionName').val(institution);
        $('#editEducationModal #editEducationStartDate').val(start);
        $('#editEducationModal #editEducationEndDate').val(end);
    });
}


// Function to handle the "Edit Employment" button click
function editEmploymentClickHandler() {
    $('.edit-employment-btn').on('click', function () {
        const url = $(this).data('url');
        const employer = $(this).data('employer');
        const title = $(this).data('title');
        const description = $(this).data('description');
        const start = $(this).data('start');
        const end = $(this).data('end');

        $('#editEmploymentForm').attr('action', url);
        $('#editEmploymentModal #editEmployerName').val(employer);
        $('#editEmploymentModal #editJobTitle').val(title);
        $('#editEmploymentModal #editDescriptionOfDuties').val(description);
        $('#editEmploymentModal #editEmploymentStartDate').val(start);
        $('#editEmploymentModal #editEmploymentEndDate').val(end);
    });
}


// Function to handle the "Delete Portfolio" button click event
function deletePortfolioClickHandler() {
    $('.delete-portfolio-btn').on('click', function() {
        var url = $(this).data('url');
        var title = $(this).data('title');

        $('#deletePortfolioForm').attr('action', url);
        $('#deletePortfolioModal #deletePortfolioTitle').text(title);
    });
}

 

 // Function to handle the "Delete Education" button click
function deleteEducationClickHandler() {
    $('.delete-education-btn').on('click', function () {
        const url = $(this).data('url');
        const qualification = $(this).data('qualification');

        $('#deleteEducationForm').attr('action', url);
        $('#deleteEducationModal #deleteEducationName').text(qualification);
    });
}


// Function to handle the "Delete Employment" button click
function deleteEmploymentClickHandler() {
    $('.delete-employment-btn').on('click', function () {
        const url = $(this).data('url');
        const employer = $(this).data('employer');

        $('#deleteEmploymentForm').attr('action', url);
        $('#deleteEmploymentModal #deleteEmploymentName').text(employer);
    });
}

// Function to handle the "Delete Certification" button click
function deleteCertificationClickHandler() {
    $('.delete-certification-btn').on('click', function () {
        const url = $(this).data('url');
        const name = $(this).data('name');

        $('#deleteCertificationForm').attr('action', url);
        $('#deleteCertificationModal #deleteCertificationName').text(name);
    });
}
 
// Function to handle the "Confirm Save About" button click
function confirmSaveAboutClickHandler() {
    $('#confirmSaveAbout').on('click', function () {
        $('#aboutForm').submit();
    });
}

 // Function to handle the "Confirm Save Profile Photo" button click
function confirmSaveProfilePhotoClickHandler() {
    $('#confirmSaveProfilePhoto').on('click', function () {
        $('#profilePhotoForm').submit();
    });
}
 
function previewUploadPhoto(inputElementId, previewElementId) {
    var file = document.getElementById(inputElementId).files[0];
    var reader = new FileReader();

    reader.onloadend = function() {
        document.getElementById(previewElementId).src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    }
}

// Handle portfolio photo preview for editing
$('#editPortfolioPhoto').on('change', function() {
    previewUploadPhoto(this.id, 'profilePortfolioPreview');
});

// Handle portfolio photo preview for creating (if applicable)
$('#createPortfolioPhoto').on('change', function() {
    previewUploadPhoto(this.id, 'createPortfolioPreview');
});

// Handle portfolio profile photo preview
$('#profile_photo').on('change', function() {
    previewUploadPhoto(this.id, 'profilePhotoPreview');
});
 
function videoPopupHandler() {
    var $thumbnail = $('#videoThumbnail');
    if ($thumbnail.length) {
        $thumbnail.on('click', function () {
            var videoId = $(this).data('video-id');
            var src = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1&rel=0';
            $('#videoIframe').attr('src', src);
            var modal = new bootstrap.Modal(document.getElementById('videoModal'));
            modal.show();
        });
        $('#videoModal').on('hidden.bs.modal', function () {
            $('#videoIframe').attr('src', '');
        });
    }
}

// Document ready handler
$(function () {
    setCurrentYear();
    toggleNavbar();
    viewProjectClickHandler();
    videoPopupHandler();

    contactMethodHandlers();
    editPortfolioClickHandler();
    editCertificationClickHandler();
    editEducationClickHandler();
    editEmploymentClickHandler();

    deletePortfolioClickHandler();
    deleteEducationClickHandler();
    deleteEmploymentClickHandler();
    deleteCertificationClickHandler();

    confirmSaveAboutClickHandler();
    confirmSaveProfilePhotoClickHandler();


    // Show or hide the button when scrolling
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('#scrollToTopBtn').fadeIn();
        } else {
            $('#scrollToTopBtn').fadeOut();
        }
    });

    // Scroll to the top when the button is clicked
    $('#scrollToTopBtn').click(function() {
        $('html, body').animate({ scrollTop: 0 }, '300');
        return false;
    });

});


// Export the functions for testing if running in a Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        setCurrentYear, 
        toggleNavbar, 
        viewProjectClickHandler, 

        contactMethodHandlers, 
        editPortfolioClickHandler, 
        editCertificationClickHandler, 
        editEducationClickHandler, 
        editEmploymentClickHandler, 

        deletePortfolioClickHandler, 
        deleteEducationClickHandler, 
        deleteEmploymentClickHandler,
        deleteCertificationClickHandler,

        confirmSaveAboutClickHandler, 
        confirmSaveProfilePhotoClickHandler,
        previewUploadPhoto,
    };

}

 