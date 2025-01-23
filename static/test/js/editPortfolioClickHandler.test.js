// npm test -- editPortfolioClickHandler.test.js

// Import jQuery
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;

// Import the function to test
const { editPortfolioClickHandler } = require('../../js/scripts');

describe('editPortfolioClickHandler', () => {
    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <button class="edit-portfolio-btn" 
                    data-url="/edit-portfolio" 
                    data-title="My Portfolio" 
                    data-description="A description of my portfolio." 
                    data-link="https://example.com" 
                    data-portfolio_photo="https://example.com/photo.jpg">
            Edit Portfolio
            </button>
            <form id="editPortfolioForm" action=""></form>
            <div id="editPortfolioModal">
                <input id="editPortfolioTitle" />
                <textarea id="editPortfolioDescription"></textarea>
                <input id="editPortfolioLink" />
                <img id="profilePortfolioPreview" />
            </div>
        `;

        // Call the function to initialize the click handler
        editPortfolioClickHandler();
    });

    it('should populate the modal with the correct portfolio data when the button is clicked', () => {
        const editPortfolioButton = $('.edit-portfolio-btn');

        // Simulate a click event
        editPortfolioButton.click();

        // Check if the modal fields are populated correctly
        expect($('#editPortfolioForm').attr('action')).toBe('/edit-portfolio');
        expect($('#editPortfolioTitle').val()).toBe('My Portfolio');
        expect($('#editPortfolioDescription').val()).toBe('A description of my portfolio.');
        expect($('#editPortfolioLink').val()).toBe('https://example.com');
        expect($('#profilePortfolioPreview').attr('src')).toBe('https://example.com/photo.jpg');
    });
});
