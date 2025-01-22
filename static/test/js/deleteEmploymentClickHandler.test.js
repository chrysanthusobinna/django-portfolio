//npm test -- deleteEmploymentClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Import the function to test
const { deleteEmploymentClickHandler } = require('../../js/scripts');

describe('deleteEmploymentClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="delete-employment-btn" 
                    data-url="/delete-employment" 
                    data-employer="Tech Corp">
            Delete Employment
            </button>
            <form id="deleteEmploymentForm" action=""></form>
            <div id="deleteEmploymentModal">
                <span id="deleteEmploymentName"></span>
            </div>
        `;

        // Initialize the click handler
        deleteEmploymentClickHandler();
    });

    it('should populate the modal with the correct employment data when the button is clicked', () => {
        const deleteEmploymentButton = $('.delete-employment-btn');

        // Simulate a click event
        deleteEmploymentButton.click();

        // Verify the form action and modal content
        expect($('#deleteEmploymentForm').attr('action')).toBe('/delete-employment');
        expect($('#deleteEmploymentModal #deleteEmploymentName').text()).toBe('Tech Corp');
    });
});
