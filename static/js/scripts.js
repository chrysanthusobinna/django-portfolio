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

        // Show the modal
        $('#viewPortfolioModal').modal('show');
    });
});

 