// npm test -- editEducationClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Import the function to test
const { editEducationClickHandler } = require('../../js/scripts');

describe('editEducationClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="edit-education-btn" 
                    data-url="/edit-education" 
                    data-qualification="BSc Computer Science" 
                    data-institution="University of Test" 
                    data-start="2020-01-01" 
                    data-end="2023-01-01">
            Edit Education
            </button>
            <form id="editEducationForm" action=""></form>
            <div id="editEducationModal">
                <input id="editQualification" />
                <input id="editInstitutionName" />
                <input id="editStartDate" />
                <input id="editEndDate" />
            </div>
        `;

        // Call the function to initialize the click handler
        editEducationClickHandler('.edit-education-btn');
    });

    it('should populate the modal with the correct education data when the button is clicked', () => {
        const editEducationButton = $('.edit-education-btn');

        // Simulate a click event
        editEducationButton.click();

        // Check if the modal fields are populated correctly
        expect($('#editEducationForm').attr('action')).toBe('/edit-education');
        expect($('#editQualification').val()).toBe('BSc Computer Science');
        expect($('#editInstitutionName').val()).toBe('University of Test');
        expect($('#editStartDate').val()).toBe('2020-01-01');
        expect($('#editEndDate').val()).toBe('2023-01-01');
    });
});
