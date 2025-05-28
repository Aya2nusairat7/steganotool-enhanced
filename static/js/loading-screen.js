/**
 * Loading Screen with Cybersecurity Theme
 * Displays for 10 seconds when the application starts with simulated server initialization
 */

document.addEventListener('DOMContentLoaded', function() {
    // Create the loading overlay
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';

    // Create cyber background pattern
    const cyberBackground = document.createElement('div');
    cyberBackground.className = 'cyber-background';
    loadingOverlay.appendChild(cyberBackground);

    // Create particles for cybersecurity feel
    const cyberParticles = document.createElement('div');
    cyberParticles.className = 'cyber-particles';
    
    // Create 50 particles with random positions
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('span');
        particle.className = 'cyber-particle';
        
        // Random position and animation delay
        const posX = Math.floor(Math.random() * 100);
        const posY = Math.floor(Math.random() * 100);
        const delay = Math.random() * 15;
        const size = Math.floor(Math.random() * 3) + 1;
        
        particle.style.top = `${posY}%`;
        particle.style.left = `${posX}%`;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.animationDelay = `${delay}s`;
        
        cyberParticles.appendChild(particle);
    }
    loadingOverlay.appendChild(cyberParticles);

    // Create content container
    const content = document.createElement('div');
    content.className = 'loading-content';

    // Add animated security icon
    const iconContainer = document.createElement('div');
    iconContainer.className = 'security-icon-container';
    
    // Create SVG icon with animation
    iconContainer.innerHTML = `
    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="security-icon">
        <defs>
            <linearGradient id="glowGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#4cceac" />
                <stop offset="100%" stop-color="#6a9fdb" />
            </linearGradient>
        </defs>
        <path class="shield-outline" d="M50,10 L85,25 C85,25 85,60 50,90 C15,60 15,25 15,25 L50,10 Z" fill="none" stroke="url(#glowGradient)" stroke-width="2" />
        <path class="shield-fill" d="M50,15 L80,28 C80,28 80,58 50,85 C20,58 20,28 20,28 L50,15 Z" fill="rgba(76, 206, 172, 0.1)" />
        <path class="lock-body" d="M65,50 L65,60 C65,60 65,75 50,75 C35,75 35,60 35,60 L35,50 L65,50 Z" fill="none" stroke="url(#glowGradient)" stroke-width="2" />
        <path class="lock-shackle" d="M42,50 L42,42 C42,36 50,30 50,30 C50,30 58,36 58,42 L58,50" fill="none" stroke="url(#glowGradient)" stroke-width="2" />
        <circle class="pulse-circle" cx="50" cy="58" r="8" fill="none" stroke="url(#glowGradient)" stroke-width="1.5" />
        <g class="data-lines">
            <line x1="50" y1="35" x2="50" y2="40" stroke="url(#glowGradient)" stroke-width="1" />
            <line x1="50" y1="76" x2="50" y2="81" stroke="url(#glowGradient)" stroke-width="1" />
            <line x1="34" y1="58" x2="29" y2="58" stroke="url(#glowGradient)" stroke-width="1" />
            <line x1="71" y1="58" x2="66" y2="58" stroke="url(#glowGradient)" stroke-width="1" />
        </g>
    </svg>
    `;
    
    content.appendChild(iconContainer);

    // Add title
    const title = document.createElement('h1');
    title.className = 'loading-title';
    title.textContent = 'CryptoStealth Security';
    content.appendChild(title);

    // Add subtitle
    const subtitle = document.createElement('p');
    subtitle.className = 'loading-subtitle';
    subtitle.textContent = 'Advanced Steganography & Encryption System Initializing';
    content.appendChild(subtitle);

    // Add progress bar
    const progressContainer = document.createElement('div');
    progressContainer.className = 'loading-progress-container';
    
    const progressBar = document.createElement('div');
    progressBar.className = 'loading-progress-bar';
    progressContainer.appendChild(progressBar);
    content.appendChild(progressContainer);

    // Add loading message that changes
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'loading-message';
    content.appendChild(loadingMessage);
    
    // Add status container
    const statusContainer = document.createElement('div');
    statusContainer.className = 'status-container';
    
    // Create server status display
    const statusDisplay = document.createElement('div');
    statusDisplay.className = 'server-status';
    statusDisplay.innerHTML = `
        <div class="status-header">
            <span class="status-label">System Status</span>
            <span class="status-value online">● ONLINE</span>
        </div>
        <div class="status-details">
            <div class="status-row">
                <span class="detail-label">Server</span>
                <span class="detail-value">127.0.0.1:8080</span>
            </div>
            <div class="status-row">
                <span class="detail-label">API Version</span>
                <span class="detail-value">v2.5.1</span>
            </div>
            <div class="status-row">
                <span class="detail-label">Encryption</span>
                <span class="detail-value">AES-256</span>
            </div>
            <div class="status-row" id="initializing-modules">
                <span class="detail-label">Modules</span>
                <span class="detail-value">Initializing...</span>
            </div>
        </div>
    `;
    
    statusContainer.appendChild(statusDisplay);
    content.appendChild(statusContainer);
    
    // Array of cybersecurity loading messages
    const messages = [
        "Establishing secure connection...",
        "Initializing AES-256 encryption modules...",
        "Loading steganography algorithms...",
        "Preparing cryptographic functions...",
        "Verifying security protocols...",
        "Setting up QR code capabilities...",
        "Validating encryption integrity...",
        "Building secure environment...",
        "Initializing hidden data extractors...",
        "System security check in progress..."
    ];
    
    // Array of module initialization steps
    const modules = [
        "Core",
        "Encryption",
        "Steganography",
        "QR Code",
        "Image Processing",
        "Audio Processing",
        "Security"
    ];
    
    // Add the content to the overlay
    loadingOverlay.appendChild(content);
    
    // Add the overlay to the body
    document.body.appendChild(loadingOverlay);
    
    // Rotate through messages
    let messageIndex = 0;
    let moduleIndex = 0;
    loadingMessage.textContent = messages[messageIndex];
    
    const messageInterval = setInterval(() => {
        messageIndex = (messageIndex + 1) % messages.length;
        loadingMessage.textContent = messages[messageIndex];
        
        // Update module initialization status
        if (moduleIndex < modules.length) {
            const modulesElem = document.getElementById('initializing-modules');
            if (modulesElem) {
                modulesElem.querySelector('.detail-value').textContent = 
                    `${modules.slice(0, moduleIndex + 1).join(', ')} ${moduleIndex < modules.length - 1 ? '...' : '✓'}`;
            }
            moduleIndex++;
        }
    }, 1000);
    
    // Create console output simulation
    const consoleContainer = document.createElement('div');
    consoleContainer.className = 'console-container';
    
    const consoleHeader = document.createElement('div');
    consoleHeader.className = 'console-header';
    consoleHeader.innerHTML = '<span>System Console</span>';
    consoleContainer.appendChild(consoleHeader);
    
    const consoleOutput = document.createElement('div');
    consoleOutput.className = 'console-output';
    consoleContainer.appendChild(consoleOutput);
    
    content.appendChild(consoleContainer);
    
    // Simulated console messages
    const consoleMessages = [
        {text: 'Initializing CryptoStealth v2.5.1...', delay: 300},
        {text: 'Loading configuration files...', delay: 800},
        {text: 'Checking system integrity...', delay: 1200},
        {text: 'Initializing encryption modules...', delay: 2000},
        {text: 'Loading steganography algorithms...', delay: 3000},
        {text: 'Starting Flask web server on port 8080...', delay: 4000},
        {text: 'Setting up API endpoints...', delay: 5000},
        {text: 'Checking database connection...', delay: 6000},
        {text: 'Initializing temporary storage directories...', delay: 7000},
        {text: 'Loading QR code capabilities...', delay: 8000},
        {text: 'System initialized successfully! Ready to process requests.', delay: 9000, class: 'success'}
    ];
    
    // Show console messages with typing effect
    consoleMessages.forEach(msg => {
        setTimeout(() => {
            const line = document.createElement('div');
            line.className = 'console-line';
            if (msg.class) {
                line.classList.add(msg.class);
            }
            
            const prefix = document.createElement('span');
            prefix.className = 'console-prefix';
            prefix.textContent = '[server] ';
            line.appendChild(prefix);
            
            const msgContent = document.createElement('span');
            msgContent.className = 'console-text';
            line.appendChild(msgContent);
            
            consoleOutput.appendChild(line);
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
            
            // Typing effect
            let i = 0;
            const text = msg.text;
            const typeInterval = setInterval(() => {
                if (i < text.length) {
                    msgContent.textContent += text.charAt(i);
                    i++;
                    consoleOutput.scrollTop = consoleOutput.scrollHeight;
                } else {
                    clearInterval(typeInterval);
                }
            }, 20);
            
        }, msg.delay);
    });
    
    // Remove the loading screen after 10 seconds
    setTimeout(() => {
        loadingOverlay.style.opacity = '0';
        clearInterval(messageInterval);
        
        // Remove from DOM after fade out
        setTimeout(() => {
            loadingOverlay.remove();
        }, 500);
    }, 10000);
}); 