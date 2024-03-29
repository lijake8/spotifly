document.addEventListener('DOMContentLoaded', function() {
  const audioList = document.getElementById('audioList');
  const audioElements = audioList.querySelectorAll('audio');

  const playButton = document.getElementById('playButton');
  const pauseButton = document.getElementById('pauseButton');
  const skipButton = document.getElementById('skipButton');

  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const gainNode = audioContext.createGain();
  let currentIndex = 0;
  let isPaused = false; // Track pause state

  // Connect the gain node to the audio context
  gainNode.connect(audioContext.destination);
  console.log('gainNode connected', gainNode);

  // play button starts playing sequentially
  playButton.addEventListener('click', function() {
      audioContext.suspend();
      isPaused = true;
      playSequentially();
  });

  // pause button pauses the audio context
  pauseButton.addEventListener('click', function() {
      // Pause the Web Audio API context and set the pause state
      audioContext.suspend();
      isPaused = true;
  });

  // resume button resumes the audio context
  resumeButton.addEventListener('click', function() {
      // Resume the Web Audio API context and set the pause state
      audioContext.resume();
      isPaused = false;
  });

  // skip button skips to the next track
  skipButton.addEventListener('click', function() {
      // If the "Skip" button is pressed, pause the current audio, reset its time, and move to the next track
      if (currentIndex < audioElements.length) {
          // If the audio is playing, pause it
          if (!audioElements[currentIndex].paused) {
              audioElements[currentIndex].pause();
          }

          // Increment the index
          // audioElements[currentIndex].currentTime is time that passed on current track before pressing skip
          currentIndex++;

          // cancel future gainnode events: https://developer.mozilla.org/en-US/docs/Web/API/AudioParam/cancelScheduledValues
          gainNode.gain.cancelScheduledValues(audioContext.currentTime);

          playSequentially();
      }
  });

  function playSequentially() {
      console.log('called playSequentially')

      if (currentIndex < audioElements.length) {
          console.log('debug!!!', audioElements[currentIndex]);
          const source = audioContext.createMediaElementSource(audioElements[currentIndex]);
          source.connect(gainNode);
          console.log('source is ', source)

          const fadeTime = 1;

          console.log('audiocontext time', audioContext.currentTime);
          // fade in
          // Start with a zero gain
          gainNode.gain.setValueAtTime(0, audioContext.currentTime);
          gainNode.gain.linearRampToValueAtTime(1, audioContext.currentTime + fadeTime);

          // fade out
          gainNode.gain.setValueAtTime(1, audioContext.currentTime + audioElements[currentIndex].duration - fadeTime);
          gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + audioElements[currentIndex].duration);

          // Resume the Web Audio API context if it was paused
          if (isPaused) {
              audioContext.resume();
              isPaused = false;
          }

          audioElements[currentIndex].play();

          // Schedule the next audio to play after the current one finishes
          audioElements[currentIndex].onended = function() {
              currentIndex++;

              // Delay the next audio play to ensure a smooth transition
              setTimeout(playSequentially, 0); //was 500
          };
      } else {
          // Reset the index for the next play
          currentIndex = 0;
      }
  }
});