// Load module from Skypack CDN
import AudioMotionAnalyzer from "https://cdn.skypack.dev/audiomotion-analyzer?min";
// https://www.npmjs.com/package/audiomotion-analyzer#disconnectinput-node-stoptracks-

// Get all elements with the class 'hoverElement'
const hoverElements = document.getElementsByClassName('hoverElement');

// Get the element that displays the currently playing track name
const currentHoverTrackName = document.getElementById('currentHoverTrackName');

// Get the element that displays the currently playing track image
const currentHoverTrackImage = document.getElementById('currentHoverTrackImage');

//get the right bar
const rightBar = document.getElementById('rightBar');




// Create an AudioContext
const audioContext = new AudioContext();
const audioElements = document.getElementsByTagName('audio');
const audioMotion = new AudioMotionAnalyzer(
    document.getElementById("visualizer"),
    {
      source: audioElements[0], //random placeholder
      height: 100,
      ansiBands: false,
      showScaleX: false,
      bgAlpha: 0,
      overlay: true,
      mode: 7,
      frequencyScale: "log",
      showPeaks: false,
      smoothing: 0.8, //0-1. higher is more smoothing
      ledBars: true,
      gradient: "prism",
    }
);
audioMotion.setLedParams(
  {
    maxLeds: 15, // integer, > 0
    spaceV: 0.5,    // > 0
    spaceH: 0    // >= 0
  }
);
audioMotion.registerGradient( 'prism', {
  bgColor: '#011a35', // background color (optional) - defaults to '#111'
  dir: 'v',           // add this property to create a horizontal gradient (optional)
  colorStops: [       // list your gradient colors in this array (at least one color is required)
    { color: 'white'},
    { color: 'gray'}, // pos is a value between 0.0 and 1.0
  ]
});





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
        console.log('hovered')
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

        // update visualizer to current audio element
        // console.log(audioMotion);
        audioMotion.connectInput(audioPlayer);
        
    });

    element.addEventListener('mouseleave', () => {
        console.log('left')
        audioPlayer.pause();
        audioPlayer.src = '';

        // Reset image opacity
        img.style.opacity = 1;

        // Reset text content
        hoverElementText.textContent = '';

        // Reset currently playing track name
        currentHoverTrackName.textContent = '';

        // Reset currently playing track image
        currentHoverTrackImage.src = '../static/images/blank.jpg'
        // currentHoverTrackImage.style.display='none'; //TODO: remove if necessary when changing to blank image
        
    });

});



