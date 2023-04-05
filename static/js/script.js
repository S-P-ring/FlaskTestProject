$(document).ready(function () {
    $('form').submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        var progressBar = $('<div class="progress-bar"></div>');
        var progressText = $('<div class="progress-text"></div>');
        var progressContainer = $('<div class="progress-container"></div>');
        progressContainer.append(progressBar).append(progressText);
        $('form').after(progressContainer);
        $.ajax({
            url: '/',
            type: 'POST',
            data: formData,
            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (event) {
                    if (event.lengthComputable) {
                        var percent = Math.round((event.loaded / event.total) * 100);
                        progressBar.css('width', percent + '%');
                        progressText.text(percent + '%');
                    }
                }, false);
                return xhr;
            },
            success: function (response) {
                console.log(response);
                progressBar.addClass('bg-success');
                progressText.text('Upload complete!');
                var filename = response.filename;
                var fileUrl = response.file_url;
                var downloadLink = $('<a class="btn btn-primary" href="' + fileUrl + '">Download ' + filename + '</a>');
                progressContainer.after(downloadLink);
            },
            error: function (response) {
                progressBar.addClass('bg-danger');
                progressText.text('Upload failed.');
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});