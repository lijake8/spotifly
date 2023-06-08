// Get the element that triggers the audio playback on hover
const hoverElement = document.getElementById('hoverElement');

// Get the audio player element
const audioPlayer = document.getElementById('audioPlayer');

// Set the source URL of the audio file
const audioSourceUrl = 'https://p.scdn.co/mp3-preview/4d9bde799eec8913e53c184c45b9fd575690b917?cid=9688e06282ff4043a95d46dee1f7467d';

// Add a hover event listener to the hover element
hoverElement.addEventListener('mouseenter', () => {
    // Set the source URL of the audio player
    audioPlayer.src = audioSourceUrl;
    
    // Play the audio
    audioPlayer.play();
});

hoverElement.addEventListener('mouseleave', () => {
    // Pause the audio
    audioPlayer.pause();
    
    // Reset the audio player source
    audioPlayer.src = '';
});
