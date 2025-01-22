//npm test -- deletePortfolioClickHandler.test.js
 
/// Import jQuery and Bootstrap
const $ = require('jquery');
 
// Make jQuery globally available
global.$ = global.jQuery = $;

 // Import the function to test
const { deletePortfolioClickHandler } = require('../../js/scripts');

describe('deletePortfolioClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="delete-portfolio-btn" 
                    data-url="/delete-portfolio" 
                    data-title="Portfolio Title">
            Delete Portfolio
            </button>
            <form id="deletePortfolioForm"></form>
            <div id="deletePortfolioModal">
                <span id="deletePortfolioTitle"></span>
            </div>
        `;

        // Call the function to initialize the click handler
        deletePortfolioClickHandler();
    });

    it('should populate the modal with the correct portfolio data when the button is clicked', () => {
        const deletePortfolioButton = $('.delete-portfolio-btn');

        // Simulate a click event
        deletePortfolioButton.click();

        // Check if the modal fields are populated correctly
        expect($('#deletePortfolioForm').attr('action')).toBe('/delete-portfolio');
        expect($('#deletePortfolioTitle').text()).toBe('Portfolio Title');
    });

});