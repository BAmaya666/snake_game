// mobile.js - Mobile controls for Snake Game

// Mobile controls JavaScript
let touchStartX = 0;
let touchStartY = 0;
let minSwipeDistance = 30;
let currentVolume = 50;

function setupMobileControls() {
    console.log("Snake Game: Setting up mobile controls");
    
    // Update loading text for mobile
    const statusElement = document.getElementById('status');
    if (statusElement && /mobile/i.test(navigator.userAgent)) {
        statusElement.textContent = "Loading Snake Game for Mobile...";
    }
    
    // Button controls
    const upBtn = document.getElementById('btn-up');
    const downBtn = document.getElementById('btn-down');
    const leftBtn = document.getElementById('btn-left');
    const rightBtn = document.getElementById('btn-right');
    const volUpBtn = document.getElementById('btn-vol-up');
    const volDownBtn = document.getElementById('btn-vol-down');
    const volDisplayBtn = document.getElementById('btn-vol-display');
    const pauseBtn = document.getElementById('btn-pause');
    const restartBtn = document.getElementById('btn-restart');
    
    if (upBtn) upBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('w');
        highlightButton(upBtn);
    });
    
    if (downBtn) downBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('s');
        highlightButton(downBtn);
    });
    
    if (leftBtn) leftBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('a');
        highlightButton(leftBtn);
    });
    
    if (rightBtn) rightBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('d');
        highlightButton(rightBtn);
    });
    
    // Volume controls
    if (volUpBtn) volUpBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('=');
        highlightButton(volUpBtn);
        currentVolume = Math.min(100, currentVolume + 10);
        updateVolumeDisplay();
    });
    
    if (volDownBtn) volDownBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('-');
        highlightButton(volDownBtn);
        currentVolume = Math.max(0, currentVolume - 10);
        updateVolumeDisplay();
    });
    
    // Game controls
    if (pauseBtn) pauseBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress(' ');
        highlightButton(pauseBtn);
        // Toggle pause text
        pauseBtn.textContent = pauseBtn.textContent === 'Pause' ? 'Resume' : 'Pause';
    });
    
    if (restartBtn) restartBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simulateKeyPress('r');
        highlightButton(restartBtn);
    });
    
    // Swipe controls
    const touchArea = document.getElementById('touch-area');
    if (touchArea) {
        touchArea.addEventListener('touchstart', handleTouchStart, {passive: false});
        touchArea.addEventListener('touchmove', handleTouchMove, {passive: false});
        touchArea.addEventListener('touchend', handleTouchEnd, {passive: false});
    }
    
    // Detect mobile device and show appropriate controls
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        console.log("Mobile device detected");
        // Show swipe instructions on first load
        if (!localStorage.getItem('snakeGameControlsShown')) {
            showSwipeInstructions();
            localStorage.setItem('snakeGameControlsShown', 'true');
        }
    }
    
    // Initialize volume display
    updateVolumeDisplay();
}

function simulateKeyPress(key) {
    console.log(`Simulating key press: ${key}`);
    
    // Create keyboard event
    const keyCode = key.charCodeAt(0);
    const keyEvent = new KeyboardEvent('keydown', {
        key: key,
        code: 'Key' + key.toUpperCase(),
        keyCode: keyCode,
        which: keyCode,
        bubbles: true,
        cancelable: true
    });
    
    // Dispatch to document
    document.dispatchEvent(keyEvent);
    
    // Also send to canvas if it exists
    const canvas = document.getElementById('canvas');
    if (canvas) {
        canvas.dispatchEvent(keyEvent);
    }
    
    // Play touch feedback sound (optional)
    playTouchSound();
}

function playTouchSound() {
    // Simple touch feedback (could be a click sound)
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        // Audio context not supported, ignore
    }
}

function highlightButton(button) {
    button.style.transform = 'scale(0.92)';
    button.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
    
    setTimeout(() => {
        button.style.transform = '';
        button.style.boxShadow = '';
    }, 150);
}

function updateVolumeDisplay() {
    const volElement = document.getElementById('btn-vol-display');
    if (volElement) {
        volElement.textContent = `Vol: ${currentVolume}%`;
        // Update color based on volume level
        if (currentVolume > 70) {
            volElement.style.background = 'linear-gradient(145deg, rgba(255, 100, 100, 0.8), rgba(200, 50, 50, 0.9))';
        } else if (currentVolume > 30) {
            volElement.style.background = 'linear-gradient(145deg, rgba(255, 200, 100, 0.8), rgba(255, 150, 50, 0.9))';
        } else {
            volElement.style.background = 'linear-gradient(145deg, rgba(100, 255, 100, 0.8), rgba(50, 200, 50, 0.9))';
        }
    }
}

function updateMobileScore(score, highScore) {
    const scoreElement = document.getElementById('mobile-score');
    const highScoreElement = document.getElementById('mobile-high-score');
    
    if (scoreElement) {
        scoreElement.textContent = `Score: ${score}`;
        // Add animation for score increase
        scoreElement.style.transform = 'scale(1.1)';
        setTimeout(() => {
            scoreElement.style.transform = 'scale(1)';
        }, 200);
    }
    
    if (highScoreElement) {
        highScoreElement.textContent = `High: ${highScore}`;
        // Flash animation for new high score
        if (score > 0 && score === highScore) {
            highScoreElement.style.animation = 'pulse 1s';
            setTimeout(() => {
                highScoreElement.style.animation = '';
            }, 1000);
        }
    }
}

// Swipe controls
function handleTouchStart(event) {
    if (event.touches.length === 1) {
        const touch = event.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        event.preventDefault();
    }
}

function handleTouchMove(event) {
    if (!touchStartX || !touchStartY || event.touches.length !== 1) return;
    
    const touch = event.touches[0];
    const touchEndX = touch.clientX;
    const touchEndY = touch.clientY;
    
    const dx = touchEndX - touchStartX;
    const dy = touchEndY - touchStartY;
    
    // Check if swipe distance is sufficient
    if (Math.abs(dx) > minSwipeDistance || Math.abs(dy) > minSwipeDistance) {
        // Determine primary direction
        if (Math.abs(dx) > Math.abs(dy)) {
            // Horizontal swipe
            if (dx > 0) {
                simulateKeyPress('d'); // Right
            } else {
                simulateKeyPress('a'); // Left
            }
        } else {
            // Vertical swipe
            if (dy > 0) {
                simulateKeyPress('s'); // Down
            } else {
                simulateKeyPress('w'); // Up
            }
        }
        
        // Reset start position
        touchStartX = 0;
        touchStartY = 0;
        event.preventDefault();
    }
}

function handleTouchEnd(event) {
    touchStartX = 0;
    touchStartY = 0;
}

function showSwipeInstructions() {
    const instructions = document.createElement('div');
    instructions.id = 'swipe-instructions';
    instructions.innerHTML = `
        <div style="position: fixed; top: 20%; left: 10%; right: 10%; 
                   background: rgba(0,0,0,0.9); color: white; padding: 20px; 
                   border-radius: 15px; z-index: 1000; text-align: center;
                   border: 3px solid #4CAF50;">
            <h3>🎮 Mobile Controls</h3>
            <p><strong>Swipe</strong> on the game area to move the snake</p>
            <p>Or use the <strong>buttons</strong> below</p>
            <p style="color: #4CAF50; margin-top: 20px;">Tap anywhere to continue</p>
        </div>
    `;
    
    document.body.appendChild(instructions);
    
    // Remove instructions when tapped
    instructions.addEventListener('touchstart', () => {
        instructions.remove();
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (instructions.parentNode) {
            instructions.remove();
        }
    }, 5000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for everything to load
    setTimeout(setupMobileControls, 1000);
});

// Export functions for Python to call
window.updateMobileScore = updateMobileScore;
window.setupMobileControls = setupMobileControls;

// Add CSS animation for pulse effect
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);