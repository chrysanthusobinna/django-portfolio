//npm test -- confirmSaveAboutClickHandler.test.js

//Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Mock the submit method for HTMLFormElement
HTMLFormElement.prototype.submit = jest.fn();

// Import the function to test
const { confirmSaveAboutClickHandler } = require('../../js/scripts');

describe('confirmSaveAboutClickHandler', () => {
    let aboutFormSubmitSpy;

    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button id="confirmSaveAbout">Save</button>
            <form id="aboutForm"></form>
        `;

        // Spy on the form's submit method
        aboutFormSubmitSpy = jest.spyOn(document.getElementById('aboutForm'), 'submit');

        // Initialize the click handler
        confirmSaveAboutClickHandler();
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    it('should submit the form when the button is clicked', () => {
        const confirmSaveButton = $('#confirmSaveAbout');

        // Simulate a click event
        confirmSaveButton.click();

        // Verify that the form's submit method was called
        expect(aboutFormSubmitSpy).toHaveBeenCalled();
    });
});
