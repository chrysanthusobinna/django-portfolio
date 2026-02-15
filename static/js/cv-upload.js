/**
 * CV Upload form handling:
 * - Reset form
 * - Submit with loading spinner
 * - File validation (size & type)
 */

function resetCVForm() {
    document.getElementById('cvUploadForm').reset();
}

document.addEventListener('DOMContentLoaded', function () {
    // CV Upload Form - show loading state on submit
    var cvForm = document.getElementById('cvUploadForm');
    if (cvForm) {
        cvForm.addEventListener('submit', function () {
            var submitBtn = document.getElementById('uploadCVBtn');
            var originalText = submitBtn.innerHTML;

            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitBtn.disabled = true;

            // Reset button after 10s if page hasn't redirected
            setTimeout(function () {
                if (submitBtn.disabled) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }, 10000);
        });
    }

    // File input validation (PDF and Word, max 10 MB)
    var cvFileInput = document.getElementById('cv_file');
    if (cvFileInput) {
        cvFileInput.addEventListener('change', function (e) {
            var file = e.target.files[0];
            var submitBtn = document.getElementById('uploadCVBtn');

            if (file) {
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size must be less than 10MB.');
                    e.target.value = '';
                    submitBtn.disabled = true;
                    return;
                }

                var fileName = file.name.toLowerCase();
                if (!fileName.endsWith('.pdf') && !fileName.endsWith('.docx')) {
                    alert('Only PDF and Word (.docx) files are allowed.');
                    e.target.value = '';
                    submitBtn.disabled = true;
                    return;
                }

                submitBtn.disabled = false;
            } else {
                submitBtn.disabled = true;
            }
        });
    }
});
