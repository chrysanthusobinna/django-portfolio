//npm test -- viewProjectClickHandler.test.js
 
// Import jQuery and Bootstrap
const $ = require('jquery');
 
// Make jQuery globally available
global.$ = global.jQuery = $;

// Mock the Bootstrap modal functionality
$.fn.modal = jest.fn();  

 // Import the function to test
const { viewProjectClickHandler } = require('../../js/scripts');

describe('viewProjectClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <a class="view-project" 
               data-title="Project Title" 
               data-description="Project Description" 
               data-image="image.jpg" 
               data-link="http://example.com">
            </a>
            <div id="modalTitle"></div>
            <div id="modalDescription"></div>
            <img id="modalImage" />
            <a id="modalLinkButton" href="#" style="display:none;"></a>
            <div id="viewPortfolioModal"></div>
        `;

        // Call the function to initialize the click handler
        viewProjectClickHandler();
    });

    it('should populate the modal with the correct data when a project link is clicked', () => {
        const viewProjectLink = $('.view-project');

        // Simulate a click event
        viewProjectLink.click();

        // Check if the modal content is populated correctly
        expect($('#modalTitle').text()).toBe('Project Title');
        expect($('#modalDescription').text()).toBe('Project Description');
        expect($('#modalImage').attr('src')).toBe('image.jpg');
        expect($('#modalLinkButton').attr('href')).toBe('http://example.com');
        expect($('#modalLinkButton').css('display')).not.toBe('none');
    });

    it('should hide the modal link button if the link is "#"', () => {
        // Modify the link to "#"
        $('.view-project').data('link', '#');

        const viewProjectLink = $('.view-project');

        // Simulate a click event
        viewProjectLink.click();

        // Check if the modal link button is hidden
        expect($('#modalLinkButton').css('display')).toBe('none');
    });

    it('should hide the modal link button when link is "#"', () => {
        $('.view-project').data('link', '#').click();
        expect($('#modalLinkButton').css('display')).toBe('none');
    });
});


