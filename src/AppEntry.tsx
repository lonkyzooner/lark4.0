import { useEffect, useState } from 'react';
import App from './App';
import UniHikerApp from './UniHikerApp';
import { isRunningOnUniHiker } from './utils/deviceDetection';

/**
 * App Entry Component
 * 
 * This component serves as the entry point for the LARK application.
 * It detects whether the app is running on a UniHiker M10 device
 * and renders the appropriate version of the application.
 */
function AppEntry() {
  const [isUniHiker, setIsUniHiker] = useState<boolean | null>(null);
  
  useEffect(() => {
    // Detect if running on UniHiker M10
    const onUniHiker = isRunningOnUniHiker();
    setIsUniHiker(onUniHiker);
    
    // Add a URL parameter option for testing
    const urlParams = new URLSearchParams(window.location.search);
    const forceUniHiker = urlParams.get('unihiker') === 'true';
    
    if (forceUniHiker) {
      setIsUniHiker(true);
      console.log('[AppEntry] Forced UniHiker mode via URL parameter');
    }
    
    if (onUniHiker || forceUniHiker) {
      console.log('[AppEntry] Running on UniHiker M10, loading optimized version');
      
      // Apply UniHiker-specific meta tags
      const viewportMeta = document.querySelector('meta[name="viewport"]');
      if (viewportMeta) {
        viewportMeta.setAttribute('content', 
          'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
      }
      
      // Add device class to html element
      document.documentElement.classList.add('unihiker-device');
    }
  }, []);
  
  // Show loading state while detecting device
  if (isUniHiker === null) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-foreground font-medium">Loading LARK...</p>
        </div>
      </div>
    );
  }
  
  // Render the appropriate app version
  return isUniHiker ? <UniHikerApp /> : <App />;
}

export default AppEntry;
