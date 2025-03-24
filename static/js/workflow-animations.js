/**
 * Workflow Animations
 * Handles the display and animations for the encryption and decryption workflows
 */

document.addEventListener('DOMContentLoaded', function() {
    // Setup workflow animations
    setupWorkflowAnimations();
    
    // Setup workflow tabs
    const workflowTabs = document.querySelectorAll('.workflow-tab');
    if (workflowTabs.length) {
        workflowTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const workflowType = this.dataset.workflow;
                switchWorkflowTab(workflowType);
            });
        });
    }
    
    // Setup intersection observer for step-by-step animations
    setupStepAnimations();
});

/**
 * Setup the SVG workflow animations
 */
function setupWorkflowAnimations() {
    // Get SVG elements and bring them inside the containers
    const encryptWorkflowContainer = document.getElementById('encrypt-workflow-container');
    const decryptWorkflowContainer = document.getElementById('decrypt-workflow-container');
    
    if (encryptWorkflowContainer && decryptWorkflowContainer) {
        // Initialize the SVG animations
        const svgContent = document.getElementById('workflow-animations-svg');
        if (svgContent) {
            // Clone encrypt workflow
            const encryptSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            encryptSvg.setAttribute('viewBox', '0 0 800 300');
            encryptSvg.setAttribute('class', 'workflow-animation');
            encryptSvg.innerHTML = document.getElementById('encrypt-workflow').outerHTML;
            encryptWorkflowContainer.querySelector('.animation-container').appendChild(encryptSvg);
            
            // Clone decrypt workflow
            const decryptSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            decryptSvg.setAttribute('viewBox', '0 0 800 300');
            decryptSvg.setAttribute('class', 'workflow-animation');
            decryptSvg.innerHTML = document.getElementById('decrypt-workflow').outerHTML;
            decryptWorkflowContainer.querySelector('.animation-container').appendChild(decryptSvg);
        }
    }
}

/**
 * Switch between workflow tabs
 */
function switchWorkflowTab(workflowType) {
    // Update active tab
    const tabs = document.querySelectorAll('.workflow-tab');
    tabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.workflow === workflowType);
    });
    
    // Show corresponding workflow
    const workflows = document.querySelectorAll('.workflow-container');
    workflows.forEach(workflow => {
        workflow.style.display = workflow.id === `${workflowType}-workflow-container` ? 'block' : 'none';
    });
    
    // Reset and restart step animations for the visible workflow
    resetStepAnimations();
    showStepsForWorkflow(workflowType);
}

/**
 * Setup Intersection Observer for step animations
 */
function setupStepAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    };
    
    const stepObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStep(entry.target);
                stepObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all step elements
    document.querySelectorAll('.workflow-step').forEach(step => {
        stepObserver.observe(step);
    });
}

/**
 * Reset all step animations
 */
function resetStepAnimations() {
    document.querySelectorAll('.workflow-step').forEach(step => {
        step.classList.remove('active');
    });
}

/**
 * Show steps one by one for the active workflow
 */
function showStepsForWorkflow(workflowType) {
    const steps = document.querySelectorAll(`#${workflowType}-workflow-container .workflow-step`);
    
    steps.forEach((step, index) => {
        setTimeout(() => {
            step.classList.add('active');
        }, 500 + (index * 700)); // Stagger the animations
    });
}

/**
 * Animate a single step
 */
function animateStep(stepElement) {
    stepElement.classList.add('active');
}

/**
 * Called when a tab is clicked
 */
function onTabSwitch() {
    // Check if we need to show workflow for the active tab
    const activeTab = document.querySelector('.tab-btn.active');
    if (activeTab) {
        const tabId = activeTab.dataset.tab;
        
        if (tabId === 'encrypt-tab') {
            switchWorkflowTab('encrypt');
        } else if (tabId === 'decrypt-tab') {
            switchWorkflowTab('decrypt');
        }
    }
} 