/**
 * Device detection utilities for LARK application
 * Specifically focused on UniHiker M10 compatibility
 */

export interface DeviceInfo {
  isUnihikerM10: boolean;
  screenWidth: number;
  screenHeight: number;
  isSmallScreen: boolean;
  isTouch: boolean;
  isMobile: boolean;
  userAgent: string;
}

/**
 * Detects if the current device is a UniHiker M10
 * UniHiker M10 has a 2.8-inch screen with 240x320 resolution
 */
export function detectUniHikerM10(): boolean {
  // Device detection based on screen size and navigator info
  // UniHiker M10 has 240x320 resolution
  const screenWidth = window.innerWidth || document.documentElement.clientWidth;
  const screenHeight = window.innerHeight || document.documentElement.clientHeight;
  
  // Check user agent for Linux-based system (UniHiker runs on Debian)
  const userAgent = navigator.userAgent.toLowerCase();
  const isLinuxBased = userAgent.includes('linux');
  
  // The most reliable way to detect is based on exact screen dimensions
  // and Linux-based OS, as the user agent string might vary
  const isUniHikerSize = (screenWidth <= 240 && screenHeight <= 320) || 
                          (screenWidth <= 320 && screenHeight <= 240);
  
  // For auto-detection in devmode, check for query param or global flag
  const urlParams = new URLSearchParams(window.location.search);
  const isDevMode = urlParams.get('unihiker') === 'true';
  
  // Check for global flag (set by our test script)
  const hasGlobalFlag = typeof window !== 'undefined' && (window as any).FORCE_UNIHIKER === true;
  
  return isUniHikerSize || isDevMode || hasGlobalFlag;
}

/**
 * Gets detailed device information
 */
export function getDeviceInfo(): DeviceInfo {
  const screenWidth = window.innerWidth || document.documentElement.clientWidth;
  const screenHeight = window.innerHeight || document.documentElement.clientHeight;
  
  return {
    isUnihikerM10: detectUniHikerM10(),
    screenWidth,
    screenHeight,
    isSmallScreen: screenWidth < 768,
    isTouch: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
    isMobile: /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase()),
    userAgent: navigator.userAgent
  };
}

/**
 * Apply UniHiker-specific adaptations to the app
 */
export function applyUniHikerAdaptations(): void {
  const { isUnihikerM10 } = getDeviceInfo();
  
  if (isUnihikerM10) {
    // Add device-specific class to body for CSS targeting
    document.body.classList.add('unihiker-device');
    
    // Apply other device-specific adaptations
    console.log('[Device] UniHiker M10 detected, applying adaptations');
    
    // Set viewport meta tag for optimal display
    const viewportMeta = document.querySelector('meta[name="viewport"]');
    if (viewportMeta) {
      viewportMeta.setAttribute('content', 
        'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
    }
  }
}

// Environment check for UniHiker
export function isRunningOnUniHiker(): boolean {
  // For development/testing purposes, allow URL param to simulate UniHiker
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('unihiker') === 'true') {
    return true;
  }
  
  // Actual detection logic
  const userAgent = navigator.userAgent.toLowerCase();
  return userAgent.includes('linux') && detectUniHikerM10();
}
