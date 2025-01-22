//npm test static/test/js/confirmSaveProfilePhotoClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Mock the submit method for HTMLFormElement
HTMLFormElement.prototype.submit = jest.fn();

// Import the function to test
const { confirmSaveProfilePhotoClickHandler } = require('../../js/scripts');

describe('confirmSaveProfilePhotoClickHandler', () => {
    let profilePhotoFormSubmitSpy;

    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button id="confirmSaveProfilePhoto">Save</button>
            <form id="profilePhotoForm"></form>
        `;

        // Spy on the form's submit method
        profilePhotoFormSubmitSpy = jest.spyOn(document.getElementById('profilePhotoForm'), 'submit');

        // Initialize the click handler
        confirmSaveProfilePhotoClickHandler();
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    it('should submit the form when the button is clicked', () => {
        const confirmSaveButton = $('#confirmSaveProfilePhoto');

        // Simulate a click event
        confirmSaveButton.click();

        // Verify that the form's submit method was called
        expect(profilePhotoFormSubmitSpy).toHaveBeenCalled();
    });
});
