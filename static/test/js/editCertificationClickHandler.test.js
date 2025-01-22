//npm test -- editCertificationClickHandler.test.js
 
/// Import jQuery and Bootstrap
const $ = require('jquery');
 
// Make jQuery globally available
global.$ = global.jQuery = $;

 // Import the function to test
const { editCertificationClickHandler } = require('../../js/scripts');

describe('editCertificationClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="edit-certification-btn" 
                    data-url="/edit-certification" 
                    data-name="Certification Name" 
                    data-issuer="Issuer Name" 
                    data-date="2025-01-01">
            Edit Certification
            </button>
            <form id="editCertificationForm"></form>
            <div id="editCertificationModal">
                <input id="editCertificationName" />
                <input id="editCertificationIssuer" />
                <input id="editCertificationDate" />
            </div>
        `;

        // Initialize the click handler
        editCertificationClickHandler();
    });

    it('should populate the form and modal with the correct certification data when the button is clicked', () => {
        const editButton = $('.edit-certification-btn');

        // Simulate a click event
        editButton.click();

        // Verify the form action and modal input values
        expect($('#editCertificationForm').attr('action')).toBe('/edit-certification');
        expect($('#editCertificationModal #editCertificationName').val()).toBe('Certification Name');
        expect($('#editCertificationModal #editCertificationIssuer').val()).toBe('Issuer Name');
        expect($('#editCertificationModal #editCertificationDate').val()).toBe('2025-01-01');
    });

});
