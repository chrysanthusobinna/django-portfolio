//npm test static/test/js/deleteCertificationClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Import the function to test
const { deleteCertificationClickHandler } = require('../../js/scripts');

describe('deleteCertificationClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="delete-certification-btn" 
                    data-url="/delete-certification" 
                    data-name="Certification 1">
            Delete Certification
            </button>
            <form id="deleteCertificationForm" action=""></form>
            <div id="deleteCertificationModal">
                <span id="deleteCertificationName"></span>
            </div>
        `;

        // Initialize the click handler
        deleteCertificationClickHandler();
    });

    it('should populate the modal with the correct certification data when the button is clicked', () => {
        const deleteCertificationButton = $('.delete-certification-btn');

        // Simulate a click event
        deleteCertificationButton.click();

        // Verify the form action and modal content
        expect($('#deleteCertificationForm').attr('action')).toBe('/delete-certification');
        expect($('#deleteCertificationModal #deleteCertificationName').text()).toBe('Certification 1');
    });
});
