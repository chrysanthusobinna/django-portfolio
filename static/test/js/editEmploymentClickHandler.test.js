//npm test -- editEmploymentClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Import the function to test
const { editEmploymentClickHandler } = require('../../js/scripts');

describe('editEmploymentClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="edit-employment-btn" 
                    data-url="/edit-employment" 
                    data-employer="Tech Corp" 
                    data-title="Software Developer" 
                    data-description="Developed software solutions" 
                    data-start="2021-01-01" 
                    data-end="2023-12-31">
            Edit Employment
            </button>
            <form id="editEmploymentForm" action=""></form>
            <div id="editEmploymentModal">
                <input id="editEmployerName" />
                <input id="editJobTitle" />
                <textarea id="editDescriptionOfDuties"></textarea>
                <input id="editStartDate" />
                <input id="editEndDate" />
            </div>
        `;

        // Initialize the click handler
        editEmploymentClickHandler();
    });

    it('should populate the modal with the correct employment data when the button is clicked', () => {
        const editEmploymentButton = $('.edit-employment-btn');

        // Simulate a click event
        editEmploymentButton.click();

        // Verify the form action and modal content
        expect($('#editEmploymentForm').attr('action')).toBe('/edit-employment');
        expect($('#editEmployerName').val()).toBe('Tech Corp');
        expect($('#editJobTitle').val()).toBe('Software Developer');
        expect($('#editDescriptionOfDuties').val()).toBe('Developed software solutions');
        expect($('#editStartDate').val()).toBe('2021-01-01');
        expect($('#editEndDate').val()).toBe('2023-12-31');
    });
});
