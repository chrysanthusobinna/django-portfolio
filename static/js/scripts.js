$(document).ready(function () {
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    $("#navbarToggler").click(function () {
        $("#navbarNav").toggleClass("show");
    });

    // When a "View Project" link is clicked
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
 
    // Edit portfolio button click
    $('.edit-portfolio-btn').on('click', function() {
        var url = $(this).data('url');
        var title = $(this).data('title');
        var description = $(this).data('description');
        var link = $(this).data('link');

        $('#editPortfolioForm').attr('action', url);
        $('#editPortfolioModal #editPortfolioTitle').val(title);
        $('#editPortfolioModal #editPortfolioDescription').val(description);
        $('#editPortfolioModal #editPortfolioLink').val(link);
    });

    // Delete portfolio button click
    $('.delete-portfolio-btn').on('click', function() {
        var url = $(this).data('url');
        var title = $(this).data('title');

        $('#deletePortfolioForm').attr('action', url);
        $('#deletePortfolioModal #deletePortfolioTitle').text(title);

    });
 
    // Edit certification button click
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

    // Delete certification button click
    $('.delete-certification-btn').on('click', function() {
        var url = $(this).data('url');
        var name = $(this).data('name');

        $('#deleteCertificationForm').attr('action', url);
        $('#deleteCertificationModal #deleteCertificationName').text(name);
    });
 
    // Edit education button click
    $('.edit-education-btn').on('click', function() {
        var url = $(this).data('url');
        var qualification = $(this).data('qualification');
        var institution = $(this).data('institution');
        var start = $(this).data('start');
        var end = $(this).data('end');

        $('#editEducationForm').attr('action', url);
        $('#editEducationModal #editQualification').val(qualification);
        $('#editEducationModal #editInstitutionName').val(institution);
        $('#editEducationModal #editStartDate').val(start);
        $('#editEducationModal #editEndDate').val(end);

    });

    // Delete education button click
    $('.delete-education-btn').on('click', function() {
        var url = $(this).data('url');
        var qualification = $(this).data('qualification');

        $('#deleteEducationForm').attr('action', url);
        $('#deleteEducationModal #deleteEducationName').text(qualification);

    });
 
    // Edit employment button click
    $('.edit-employment-btn').on('click', function() {
        var url = $(this).data('url');
        var employer = $(this).data('employer');
        var title = $(this).data('title');
        var description = $(this).data('description');
        var start = $(this).data('start');
        var end = $(this).data('end');

        $('#editEmploymentForm').attr('action', url);
        $('#editEmploymentModal #editEmployerName').val(employer);
        $('#editEmploymentModal #editJobTitle').val(title);
        $('#editEmploymentModal #editDescriptionOfDuties').val(description);
        $('#editEmploymentModal #editStartDate').val(start);
        $('#editEmploymentModal #editEndDate').val(end);
    });

    // Delete employment button click
    $('.delete-employment-btn').on('click', function() {
        var url = $(this).data('url');
        var employer = $(this).data('employer');

        $('#deleteEmploymentForm').attr('action', url);
        $('#deleteEmploymentModal #deleteEmploymentName').text(employer);
    });
 
    $('#confirmSaveAbout').on('click', function() {
        $('#aboutForm').submit();
    });

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


