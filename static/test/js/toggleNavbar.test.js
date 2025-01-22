//npm test -- toggleNavbar.test.js
 
/// Import jQuery and Bootstrap
const $ = require('jquery');
 
// Make jQuery globally available
global.$ = global.jQuery = $;

 // Import the function to test
const { toggleNavbar } = require('../../js/scripts');

describe('toggleNavbar', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button id="navbarToggler"></button>
            <div id="navbarNav"></div>
        `;
        // Call the function to initialize the event listener
        toggleNavbar();
    });

    it('should toggle the "show" class on #navbarNav when #navbarToggler is clicked', () => {
        const navbarToggler = $('#navbarToggler');
        const navbarNav = $('#navbarNav');

        // Initially, the "show" class should not be present
        expect(navbarNav.hasClass('show')).toBe(false);

        // Simulate a click event
        navbarToggler.click();

        // After the first click, the "show" class should be added
        expect(navbarNav.hasClass('show')).toBe(true);

        // Simulate another click event
        navbarToggler.click();

        // After the second click, the "show" class should be removed
        expect(navbarNav.hasClass('show')).toBe(false);
    });
});

