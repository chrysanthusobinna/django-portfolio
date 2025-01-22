
// npm test -- previewUploadPhoto.test.js

// Import necessary libraries
const $ = require('jquery');

// Make jQuery globally available
global.$ = global.jQuery = $;


// Mock the FileReader
global.FileReader = jest.fn().mockImplementation(() => {
    return {
        onload: jest.fn(),
        readAsDataURL: jest.fn(),
    };
});

// Import the function to test
const { previewUploadPhoto } = require('../../js/scripts');

describe('previewUploadPhoto', () => {
    let fileInput;
    let previewImage;

    beforeEach(() => {
        // Set up the DOM for testing
        document.body.innerHTML = `
            <input type="file" id="test_photo" />
            <img id="test_PreviewPhoto" />
        `;

        // Create a mock file
        fileInput = document.getElementById('test_photo');
        previewImage = document.getElementById('test_PreviewPhoto');

        // Simulate a file selection
        const file = new Blob(['dummy content'], { type: 'image/jpeg' });
        Object.defineProperty(fileInput, 'files', {
            value: [file],
        });
    });

    it('should set the preview image source when a file is selected', () => {

        // Mock the FileReader
        const mockFileReader = {
            onloadend: jest.fn(),
            readAsDataURL: jest.fn(function() {
                this.result = 'data:image/jpeg;base64,dummybase64data'; // Mock result
                this.onloadend(); // Simulate onloadend callback
            })
        };
        global.FileReader = jest.fn(() => mockFileReader);

        // Call the function to trigger the file reading process
        previewUploadPhoto('test_photo', 'test_PreviewPhoto');
 
        // Check if FileReader's readAsDataURL method was called
        expect(mockFileReader.readAsDataURL).toHaveBeenCalledWith(fileInput.files[0]);


        // Check if the preview image src is set correctly
        expect(previewImage.src).toBe('data:image/jpeg;base64,dummybase64data');
    });

});
