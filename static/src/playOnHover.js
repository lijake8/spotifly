// Get all elements with the class 'hoverElement'
const hoverElements = document.getElementsByClassName('hoverElement');

// Get the element that displays the currently playing track name
const currentHoverTrackName = document.getElementById('currentHoverTrackName');

// Get the element that displays the currently playing track image
const currentHoverTrackImage = document.getElementById('currentHoverTrackImage');

// Add event listeners to each hover element
Array.from(hoverElements).forEach((element) => {
    const audioPlayer = element.getElementsByTagName('audio')[0];
    const audioSourceUrl = element.dataset.audioUrl; //By using the dataset property, you can access custom data attributes prefixed with "data-". The dataset property is an object that contains all the custom data attributes of the element as properties. The dataset property automatically converts the kebab-case format (data-audio-url) of the custom attribute name into camelCase format (audioUrl) when accessed as a property
    const trackName = element.dataset.trackName;
    const albumImg = element.dataset.albumImg;

    // Find the img and h6 elements within the current hoverElement
    const img = element.querySelector('img');
    const hoverElementText = element.querySelector('.hoverElementText');

    // when the user hovers over the element, play audio and display track name and change the opacity
    element.addEventListener('mouseenter', () => {
        audioPlayer.src = audioSourceUrl;
        audioPlayer.play();

        // Change image opacity
        img.style.opacity = 0.5;  // Adjust the opacity as needed

        // Update text content
        hoverElementText.textContent = trackName;
        
        // update currently playing track name
        currentHoverTrackName.textContent = trackName;

        // update currently playing track image
        currentHoverTrackImage.src = albumImg;
        currentHoverTrackImage.style.display='block';
    });

    element.addEventListener('mouseleave', () => {
        audioPlayer.pause();
        audioPlayer.src = '';

        // Reset image opacity
        img.style.opacity = 1;

        // Reset text content
        hoverElementText.textContent = '';

        // Reset currently playing track name
        currentHoverTrackName.textContent = '';

        // Reset currently playing track image
        currentHoverTrackImage.src = '';
        currentHoverTrackImage.style.display='none';
    });

});



