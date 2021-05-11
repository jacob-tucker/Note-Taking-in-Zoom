window.onload = function () {
    var fileInput = document.getElementById('fileInput');
    var fileDisplayArea = document.getElementById('demoContainer');

    fileInput.addEventListener('change', function (e) {
        var file = fileInput.files[0];
        var textType = /text.*/;

        if (file.type.match(textType)) {
            var reader = new FileReader();

            var substrings = []
            reader.onload = function (e) {
                var contents = reader.result;
                var firstHashtag = false
                var substring = ''

                // This essentially reads through the contents of
                // the uploaded file and skips the "# stop (timestamp)" lines
                for (let i = 0; i < contents.length; i++) {
                    // If you encounter a new section
                    if (contents[i] == '#' && !firstHashtag) {
                        firstHashtag = true
                        // This i++ is to skip the space following the #
                        i++
                    }
                    else if (contents[i] == '#' && firstHashtag) {
                        substrings.push(substring)
                        substring = ''
                        // Skip the stop message
                        i += 19
                        firstHashtag = false
                    }
                    else if (i == contents.length - 1) {
                        substrings.push(substring)
                    }
                    // If you've started reading this section
                    else {
                        substring = substring.concat(contents[i])
                    }
                }
                putInHTML(substrings)
            }

            reader.readAsText(file);
        } else {
            fileDisplayArea.innerText = "File not supported!"
        }
    });
}

function putInHTML(substrings) {
    demo = document.getElementById("demoContainer")
    for (let i = 0; i < substrings.length; i++) {
        var text = substrings[i]

        var newText = text.split("\r\n")

        var paragraphText = ''
        for (let j = 0; j < newText.length; j++) {
            paragraphText += newText[j] + "<br>"
        }

        demo.innerHTML += `
        <div class="noteSection">
            <p>${paragraphText}</p>
            <video id="${i}_video" src="../postProcessing/${i}_video.mp4" controls></video>
        </div>
        `
    }
    var vids = document.querySelectorAll("video");

    // for all the videos in the page
    for (var x = 0; x < vids.length; x++) {
        // add an event listening for errors
        vids[x].addEventListener('error', function (e) {
            // if the error is caused by the video not loading
            if (this.networkState > 2) {
                // add an image with the message "video not found"
                this.style.display = 'none';
            }
        }, true);

    }
}
