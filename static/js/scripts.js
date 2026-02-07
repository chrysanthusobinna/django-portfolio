
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


// Function to handle the "Edit Contact" button click event
function editContactClickHandler() {
    $('.edit-contact-btn').on('click', function() {
        var phone = $(this).data('phone');
        var email = $(this).data('email');
        var linkedin = $(this).data('linkedin');

        $('#editModal #id_phone_number').val(phone);
        $('#editModal #id_email_address').val(email);
        $('#editModal #id_linkedin').val(linkedin);
    });
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

    editContactClickHandler();
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

        editContactClickHandler, 
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

 