//npm test static/test/js/deleteEducationClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Import the function to test
const { deleteEducationClickHandler } = require('../../js/scripts');

describe('deleteEducationClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="delete-education-btn" 
                    data-url="/delete-education" 
                    data-qualification="BSc Computer Science">
            Delete Education
            </button>
            <form id="deleteEducationForm" action=""></form>
            <div id="deleteEducationModal">
                <span id="deleteEducationName"></span>
            </div>
        `;

        // Call the function to initialize the click handler
        deleteEducationClickHandler();
    });

    it('should populate the modal with the correct education data when the button is clicked', () => {
        const deleteEducationButton = $('.delete-education-btn');

        // Simulate a click event
        deleteEducationButton.click();

        // Check if the modal fields are populated correctly
        expect($('#deleteEducationForm').attr('action')).toBe('/delete-education');
        expect($('#deleteEducationModal #deleteEducationName').text()).toBe('BSc Computer Science');
    });
});
