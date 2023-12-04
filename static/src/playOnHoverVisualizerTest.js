//// codepen example working

// Load module from Skypack CDN
import AudioMotionAnalyzer from "https://cdn.skypack.dev/audiomotion-analyzer?min";
// const AudioMotionAnalyzer = require("https://cdn.skypack.dev/audiomotion-analyzer?min");




document.getElementById('play-button').addEventListener('click', () => {
  const audioElements = document.getElementsByTagName('audio');
  for (const audioElement of audioElements) {
    audioElement.play();
  }
});

document.getElementById('pause-button').addEventListener('click', () => {
  const audioElements = document.getElementsByTagName('audio');
  for (const audioElement of audioElements) {
    audioElement.pause();
  }
});



// Create an AudioContext
const audioContext = new AudioContext();
// Get the audio element
const audioElements = document.getElementsByTagName('audio');


const audioMotion = new AudioMotionAnalyzer(
  document.getElementById("visualizer"),
  {
    source: audioElements[0],
    height: 400,
    ansiBands: false,
    showScaleX: false,
    bgAlpha: 0,
    overlay: true,
    mode: 6,
    frequencyScale: "log",
    showPeaks: false,
    smoothing: 0.5, //0-1. higher is more smoothing
    ledBars: true,
    gradient: "prism"
  }
);

// const audioMotion12 = new AudioMotionAnalyzer(
//   document.getElementById("container-12"),
//   {
//     source: audioElements[11],
//     height: 400,
//     ansiBands: false,
//     showScaleX: false,
//     bgAlpha: 0,
//     overlay: true,
//     smoothing: 0.7,
//     mode: 0,
//     channelLayout: "single",
//     frequencyScale: "bark",
//     gradient: "prism",
//     linearAmplitude: true,
//     linearBoost: 1.8,
//     mirror: 0,
//     radial: false,
//     reflexAlpha: 0.25,
//     reflexBright: 1,
//     reflexFit: true,
//     reflexRatio: 0.3,
//     showPeaks: true,
//     weightingFilter: "D"
//   }
// );
