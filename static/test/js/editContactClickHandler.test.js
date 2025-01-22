//npm test -- editContactClickHandler.test.js
 
/// Import jQuery and Bootstrap
const $ = require('jquery');
 
// Make jQuery globally available
global.$ = global.jQuery = $;

 // Import the function to test
const { editContactClickHandler } = require('../../js/scripts');

describe('editContactClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="edit-contact-btn" 
                    data-phone="1234567890" 
                    data-email="test@example.com" 
                    data-linkedin="https://linkedin.com/in/test">
            Edit Contact
            </button>
            <div id="editModal">
                <input id="id_phone_number" />
                <input id="id_email_address" />
                <input id="id_linkedin" />
            </div>
        `;

        // Call the function to initialize the click handler
        editContactClickHandler();
    });

    it('should populate the modal with the correct contact data when the button is clicked', () => {
        const editContactButton = $('.edit-contact-btn');

        // Simulate a click event
        editContactButton.click();

        // Check if the modal fields are populated correctly
        expect($('#id_phone_number').val()).toBe('1234567890');
        expect($('#id_email_address').val()).toBe('test@example.com');
        expect($('#id_linkedin').val()).toBe('https://linkedin.com/in/test');
    });
});

 