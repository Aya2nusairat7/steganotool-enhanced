/**
 * Authentication Protection
 * Forces users to sign in before accessing protected pages
 */

(function() {
    // Immediately run on script load
    
    // Pages that don't require authentication
    const publicPages = [
        '/sign-in',
        '/sign-up',
        '/forgot-password'
    ];
    
    // Check if current page is in the public pages list
    const isPublicPage = publicPages.some(page => 
        window.location.pathname === page || 
        window.location.pathname === page + '.html'
    );
    
    // Check if user is authenticated
    const isAuthenticated = !!localStorage.getItem('auth_token');
    
    // If not on a public page and not authenticated, redirect to sign-in
    if (!isPublicPage && !isAuthenticated) {
        // Store the current URL to redirect back after login
        localStorage.setItem('redirect_after_login', window.location.href);
        
        // Redirect to sign-in page
        window.location.href = '/sign-in';
    }
    
    // If we're on the sign-in page and already authenticated, redirect to home
    if ((window.location.pathname === '/sign-in' || window.location.pathname === '/sign-in.html') && isAuthenticated) {
        window.location.href = '/';
    }
})(); 