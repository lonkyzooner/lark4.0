import React, { useEffect } from 'react';
import './styles/voice-assistant.css';
import './styles/unihiker.css';
import './styles/voice-first.css';
import VoiceFirstInterface from './components/VoiceFirstInterface';
import UniHikerIntegration from './components/UniHikerIntegration';
import { UniHikerVoiceProvider } from './contexts/UniHikerVoiceContext';
import { isRunningOnUniHiker } from './utils/deviceDetection';
import ErrorBoundary from './components/ErrorBoundary';

/**
 * Simplified UniHiker-optimized App component for the LARK application
 * 
 * This version provides a voice-first interface designed specifically for the
 * UniHiker M10 hardware. It uses wake word detection ("Hey LARK") and
 * provides a streamlined, single-screen experience optimized for the
 * 2.8-inch touchscreen.
 * 
 * @param initialTab - Optional initial tab to display (defaults to 'voice')
 */
interface UniHikerAppProps {
  initialTab?: string;
}

function UniHikerApp({ initialTab = 'voice' }: UniHikerAppProps) {
  // Apply UniHiker-specific optimizations on mount
  useEffect(() => {
    // Add device class to html element
    document.documentElement.classList.add('unihiker-device');
    
    // Apply meta tags for better mobile experience
    const viewportMeta = document.querySelector('meta[name="viewport"]');
    if (viewportMeta) {
      viewportMeta.setAttribute('content', 
        'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
    }
    
    // Log that we're running the optimized version
    console.log('[UniHikerApp] Running voice-first interface optimized for UniHiker M10');
    
    // Disable pull-to-refresh on mobile
    document.body.style.overscrollBehavior = 'none';
    
    // Keep screen on if possible
    if (navigator.wakeLock) {
      try {
        navigator.wakeLock.request('screen')
          .then(wakeLock => {
            console.log('[UniHikerApp] Wake Lock is active');
            // Release wake lock when visibility changes
            document.addEventListener('visibilitychange', () => {
              if (document.visibilityState === 'visible') {
                navigator.wakeLock.request('screen');
              }
            });
          })
          .catch(err => {
            console.error('[UniHikerApp] Wake Lock error:', err);
          });
      } catch (err) {
        console.error('[UniHikerApp] Wake Lock API not supported:', err);
      }
    }
  }, []);

  // Handle hardware status updates from UniHiker integration
  const handleHardwareStatusChange = (status: any) => {
    console.log('[UniHikerApp] Hardware status update:', status);
    // This could be used to update battery level, connectivity status, etc.
  };

  return (
    <UniHikerVoiceProvider>
      <UniHikerIntegration onHardwareStatusChange={handleHardwareStatusChange}>
        <ErrorBoundary
          onError={(error, errorInfo) => {
            console.error('[UniHikerApp] Error in voice interface:', error);
            console.error('Component Stack:', errorInfo.componentStack);
          }}
        >
          <VoiceFirstInterface />
        </ErrorBoundary>
      </UniHikerIntegration>
    </UniHikerVoiceProvider>
  );
}

export default UniHikerApp;
