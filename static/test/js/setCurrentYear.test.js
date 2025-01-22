//npm test -- setCurrentYear.test.js
 
/// Import jQuery and Bootstrap
const $ = require('jquery');
 
// Make jQuery globally available
global.$ = global.jQuery = $;

 // Import the function to test
const { setCurrentYear } = require('../../js/scripts');

// Set up the DOM and perform the tests
describe('setCurrentYear', () => {
    beforeEach(() => {
        // Set up the DOM
        document.body.innerHTML = '<div id="currentYear"></div>';
    });

    it('should set the current year to the specified element', () => {
        const currentYear = new Date().getFullYear();
        setCurrentYear();

        const element = document.getElementById('currentYear');
        expect(element.textContent).toBe(currentYear.toString());
    });
});
