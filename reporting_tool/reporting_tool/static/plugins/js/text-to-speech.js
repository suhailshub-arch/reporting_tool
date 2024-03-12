let ttsMode = false;

// Function to toggle Text-to-Speech mode
document.getElementById('toggle-tts').addEventListener('click', function() {
  ttsMode = !ttsMode;
  document.getElementById('tts-controls').style.display = ttsMode ? 'block' : 'none';

  if (ttsMode) {
    document.body.classList.add('tts-active');
  } else {
    document.body.classList.remove('tts-active');
  }
});

let currentUtterance;

function getTextContent(node) {
  let text = '';
  for (let child of node.childNodes) {
    if (child.nodeType === Node.TEXT_NODE) {
      text += child.textContent.trim() + ' ';
    } else if (child.childNodes.length > 0) {
      text += getTextContent(child) + ' ';
    }
  }
  return text.trim();
}

// General function to initiate speech synthesis
function speakText(text) {
    if (currentUtterance) {
      window.speechSynthesis.cancel(); // Cancel any ongoing speech
    }
    
    currentUtterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(currentUtterance);
  }
  
  // Enhanced speak function that checks for TTS mode
  function speak(element) {
    if (!ttsMode) return; // Ignore if not in TTS mode
    speakText(element.textContent || element.innerText);   
  }
  
  // Add event listener to the document to handle clicks in TTS mode
  document.addEventListener('click', function(event) {
    if (!ttsMode) return;
  
    let target = event.target;
    // Ascend the DOM tree to find the nearest parent marked as 'speakable'
    while (target != null && !target.classList.contains('speakable')) {
      target = target.parentElement;
    }
  
    if (target && target.classList.contains('speakable')) {
      // Process the entire content block for speech
      const textContent = getTextContent(target);
      speakText(textContent);
    }
  }, true);

// Pause speech
function pauseSpeech() {
  if (currentUtterance) {
    window.speechSynthesis.pause();
  }
}

// Resume speech
function resumeSpeech() {
  if (currentUtterance && window.speechSynthesis.paused) {
    window.speechSynthesis.resume();
  }
}

// Stop speech
function stopSpeech() {
  if (currentUtterance) {
    window.speechSynthesis.cancel();
  }
}
