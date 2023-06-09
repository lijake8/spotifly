// Get all elements with the class 'hoverElement'
const hoverElements = document.getElementsByClassName('hoverElement');

// Add event listeners to each hover element
Array.from(hoverElements).forEach((element) => {
    const audioPlayer = element.getElementsByTagName('audio')[0];
    const audioSourceUrl = element.dataset.audioUrl; //By using the dataset property, you can access custom data attributes prefixed with "data-". The dataset property is an object that contains all the custom data attributes of the element as properties. The dataset property automatically converts the kebab-case format (data-audio-url) of the custom attribute name into camelCase format (audioUrl) when accessed as a property

    element.addEventListener('mouseenter', () => {
        audioPlayer.src = audioSourceUrl;
        audioPlayer.play();
    });

    element.addEventListener('mouseleave', () => {
        audioPlayer.pause();
        audioPlayer.src = '';
    });
});
