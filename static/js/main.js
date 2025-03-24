$(document).ready(function() {
    // Animation for page elements on load
    setTimeout(function() {
        $(".hero-title, .hero-subtitle, .hero-buttons, .hero-image").addClass("animate-in");
    }, 100);
    
    setTimeout(function() {
        $(".feature-card").each(function(index) {
            var delay = 100 * index;
            var card = $(this);
            setTimeout(function() {
                card.addClass("animate-in");
            }, delay);
        });
    }, 600);
    
    // Tab switching functionality
    $(".tab-btn").click(function() {
        const tabId = $(this).data("tab");
        
        // Update active tab button
        $(".tab-btn").removeClass("active");
        $(this).addClass("active");
        
        // Show the selected tab content
        $(".tab-pane").removeClass("active");
        $("#" + tabId).addClass("active");
        
        // Update workflow animations based on active tab
        if (typeof onTabSwitch === 'function') {
            onTabSwitch();
        }
    });
    
    // Initialize workflow tabs for the initial active tab
    setTimeout(function() {
        if (typeof onTabSwitch === 'function') {
            onTabSwitch();
        }
    }, 800);
    
    // Media type selection
    $(".toggle-option input[type='radio']").change(function() {
        const parentGroup = $(this).closest(".media-selector");
        parentGroup.find(".toggle-option").removeClass("active");
        $(this).closest(".toggle-option").addClass("active");
        
        // Update file icon based on media type
        const fileDropArea = $(this).closest("form").find(".file-drop-area");
        const mediaType = $(this).val();
        
        if (mediaType === "image") {
            fileDropArea.find(".file-icon i").attr("class", "bi bi-file-earmark-image");
        } else if (mediaType === "audio") {
            fileDropArea.find(".file-icon i").attr("class", "bi bi-file-earmark-music");
        }
    });
    
    // File Drop Area functionality
    $(".file-drop-area").each(function() {
        const dropArea = $(this);
        const inputFile = dropArea.find("input[type='file']");
        
        // Highlight drop area when file is dragged over
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea[0].addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea[0].addEventListener(eventName, unhighlight, false);
        });
        
        // Prevent default behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea[0].addEventListener(eventName, preventDefaults, false);
        });
        
        // Handle dropped files
        dropArea[0].addEventListener('drop', handleDrop, false);
        
        // Handle file selection
        inputFile.on('change', function() {
            handleFiles(this.files);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        function highlight() {
            dropArea.addClass('highlight');
        }
        
        function unhighlight() {
            dropArea.removeClass('highlight');
        }
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            inputFile[0].files = files;
            handleFiles(files);
        }
        
        function handleFiles(files) {
            if (files.length === 0) return;
            
            const fileName = files[0].name;
            const fileIcon = dropArea.find(".file-icon i");
            const fileMessage = dropArea.find(".file-message .main-text");
            
            // Update the UI to show the selected file
            fileMessage.text(fileName);
            
            // Adjust icon based on file type
            if (files[0].type.startsWith("image/")) {
                fileIcon.attr("class", "bi bi-file-earmark-image");
            } else if (files[0].type.startsWith("audio/")) {
                fileIcon.attr("class", "bi bi-file-earmark-music");
            } else {
                fileIcon.attr("class", "bi bi-file-earmark");
            }
            
            // Update file info
            dropArea.addClass("has-file");
        }
    });
    
    // Toggle password field based on auto-generate checkbox
    $("#autoGeneratePassword").change(function() {
        if($(this).is(":checked")) {
            $("#encryptPassword").prop("required", false);
            $("#passwordInputGroup").addClass("muted-field");
        } else {
            $("#encryptPassword").prop("required", true);
            $("#passwordInputGroup").removeClass("muted-field");
        }
    });

    // Encrypt form submission
    $("#encryptForm").submit(function(e) {
        e.preventDefault();
        
        // Show loading state
        const btn = $(this).find('button[type="submit"]');
        const originalBtnText = btn.html();
        btn.html('<div class="loading"><div></div><div></div><div></div></div> Processing...');
        btn.prop('disabled', true);
        
        // Validate form manually when auto-generate is not checked
        if (!$("#autoGeneratePassword").is(":checked") && !$("#encryptPassword").val()) {
            showMessage("#encryptionResult", "error", "Please provide a password or enable auto-generate option.");
            btn.html(originalBtnText);
            btn.prop('disabled', false);
            return;
        }

        var formData = new FormData(this);
        
        $.ajax({
            url: '/api/encrypt',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                btn.html(originalBtnText);
                btn.prop('disabled', false);
                
                if (response.status === 'success') {
                    let resultContent = `
                        <div class="alert alert-success animate-fade-in">
                            <h4 class="alert-heading"><i class="bi bi-check-circle"></i> Success!</h4>
                            <p>Your message has been encrypted and hidden successfully.</p>
                            <hr>
                            <div class="result-details">
                                <p><strong><i class="bi bi-file-earmark"></i> Output File:</strong> ${response.output_filename}</p>
                    `;
                    
                    if (response.auto_generated_password) {
                        resultContent += `
                            <div class="password-box">
                                <div class="d-flex justify-content-between align-items-center">
                                    <p class="mb-0"><strong><i class="bi bi-key"></i> Auto-Generated Password:</strong></p>
                                    <button class="btn btn-sm copy-btn" data-clipboard="${response.auto_generated_password}">
                                        <i class="bi bi-clipboard"></i> Copy
                                    </button>
                                </div>
                                <p class="password-value">${response.auto_generated_password}</p>
                                <p class="text-warning mb-0"><small><i class="bi bi-info-circle"></i> This password is stored in the file and will be extracted automatically during decryption.</small></p>
                            </div>
                        `;
                    }
                    
                    resultContent += `
                                <div class="mt-3">
                                    <a href="/api/download/${response.output_filename}" class="btn btn-primary">
                                        <i class="bi bi-download"></i> Download File
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    showMessage("#encryptionResult", "custom", resultContent);
                    
                    // Reset the form UI for next use
                    resetFormUI($("#encryptForm"));
                } else {
                    showMessage("#encryptionResult", "error", response.message || "An error occurred");
                }
            },
            error: function(xhr) {
                btn.html(originalBtnText);
                btn.prop('disabled', false);
                
                let errorMsg = "An error occurred during encryption";
                try {
                    const response = JSON.parse(xhr.responseText);
                    errorMsg = response.message || errorMsg;
                } catch (e) {}
                
                showMessage("#encryptionResult", "error", errorMsg);
            }
        });
    });

    // Decrypt form submission
    $("#decryptForm").submit(function(e) {
        e.preventDefault();
        
        // Show loading state
        const btn = $(this).find('button[type="submit"]');
        const originalBtnText = btn.html();
        btn.html('<div class="loading"><div></div><div></div><div></div></div> Processing...');
        btn.prop('disabled', true);
        
        var formData = new FormData(this);
        
        $.ajax({
            url: '/api/decrypt',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                btn.html(originalBtnText);
                btn.prop('disabled', false);
                
                console.log("Decrypt response:", response); // Debug log
                
                // Always show result even for error status
                if (response) {
                    let status = response.status || "error";
                    let alertClass = "alert-danger";
                    let icon = "bi-exclamation-triangle";
                    let title = "Error";
                    
                    if (status === "success") {
                        alertClass = "alert-success";
                        icon = "bi-check-circle";
                        title = "Success!";
                    } else if (status === "warning") {
                        alertClass = "alert-warning";
                        icon = "bi-exclamation-triangle";
                        title = "Partial Success";
                    }
                    
                    let resultContent = `
                        <div class="alert ${alertClass} animate-fade-in">
                            <h4 class="alert-heading">
                                <i class="bi ${icon}"></i> ${title}
                            </h4>
                    `;
                    
                    // Check for password using the correct property name
                    if (response.password_found && response.used_password) {
                        resultContent += `
                            <div class="password-box mb-3">
                                <div class="d-flex justify-content-between align-items-center">
                                    <p class="mb-0"><strong><i class="bi bi-key"></i> Extracted Password:</strong></p>
                                    <button class="btn btn-sm copy-btn" data-clipboard="${response.used_password}">
                                        <i class="bi bi-clipboard"></i> Copy
                                    </button>
                                </div>
                                <p class="password-value">${response.used_password}</p>
                            </div>
                        `;
                    }
                    
                    // Add the message content if it exists
                    if (response.message) {
                        resultContent += `
                            <div class="decrypted-message-container">
                                <p><strong><i class="bi bi-chat-left-text"></i> ${status === "error" ? "Error Message:" : "Decrypted Message:"}</strong></p>
                                <div class="decrypted-message">${response.message.replace(/\n/g, '<br>')}</div>
                            </div>
                        `;
                    }
                    
                    resultContent += `</div>`;
                    
                    showMessage("#decryptionResult", "custom", resultContent);
                    
                    // Reset the form UI for next use
                    resetFormUI($("#decryptForm"));
                } else {
                    showMessage("#decryptionResult", "error", "No response from server");
                }
            },
            error: function(xhr) {
                btn.html(originalBtnText);
                btn.prop('disabled', false);
                
                let errorMsg = "An error occurred during decryption";
                try {
                    const response = JSON.parse(xhr.responseText);
                    errorMsg = response.message || response.error || errorMsg;
                } catch (e) {}
                
                showMessage("#decryptionResult", "error", errorMsg);
            }
        });
    });
    
    // Function to reset form UI after submission
    function resetFormUI(form) {
        // Reset file drop area
        const dropArea = form.find(".file-drop-area");
        const fileIcon = dropArea.find(".file-icon i");
        const fileMessage = dropArea.find(".file-message .main-text");
        
        // Reset based on media type
        const mediaType = form.find("input[name='media_type']:checked").val();
        if (mediaType === "image") {
            fileIcon.attr("class", "bi bi-file-earmark-image");
        } else {
            fileIcon.attr("class", "bi bi-file-earmark-music");
        }
        
        fileMessage.text("Drop your file here");
        dropArea.removeClass("has-file highlight");
        
        // Reset text inputs but not select/radio/checkbox
        form.find('input[type="text"], input[type="password"], textarea').val('');
    }
    
    // Handle copy button clicks
    $(document).on('click', '.copy-btn', function() {
        const textToCopy = $(this).data('clipboard');
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = $(this).html();
            $(this).html('<i class="bi bi-check"></i> Copied!');
            setTimeout(() => {
                $(this).html(originalText);
            }, 2000);
        });
    });

    // Function to display messages
    function showMessage(selector, type, message) {
        const element = $(selector);
        element.empty();
        
        if (type === "custom") {
            element.html(message);
        } else if (type === "error") {
            element.html(`
                <div class="alert alert-danger animate-fade-in">
                    <h4 class="alert-heading">
                        <i class="bi bi-exclamation-triangle"></i> Error
                    </h4>
                    <p>${message}</p>
                </div>
            `);
        } else if (type === "success") {
            element.html(`
                <div class="alert alert-success animate-fade-in">
                    <h4 class="alert-heading">
                        <i class="bi bi-check-circle"></i> Success
                    </h4>
                    <p>${message}</p>
                </div>
            `);
        }
        
        // Scroll to the message
        $('html, body').animate({
            scrollTop: element.offset().top - 100
        }, 500);
    }
    
    // Smooth scroll for anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        
        const target = $(this.hash);
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });
}); 