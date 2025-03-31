import React, { useEffect, useState } from 'react';
import { isRunningOnUniHiker, getDeviceInfo } from '../utils/deviceDetection';

interface UniHikerHardwareStatus {
  batteryLevel: number;
  cpuTemperature: number;
  memoryUsage: number;
  storageUsage: number;
  wifiSignal: number;
  isCharging: boolean;
}

interface UniHikerIntegrationProps {
  children: React.ReactNode;
  onHardwareStatusChange?: (status: UniHikerHardwareStatus) => void;
}

/**
 * UniHiker Integration Component
 * 
 * This component handles specific integrations for the UniHiker M10 hardware.
 * It provides hardware status information and optimizes the application for the device.
 */
export const UniHikerIntegration: React.FC<UniHikerIntegrationProps> = ({ 
  children,
  onHardwareStatusChange
}) => {
  const [isUniHiker, setIsUniHiker] = useState<boolean>(false);
  const [hardwareStatus, setHardwareStatus] = useState<UniHikerHardwareStatus>({
    batteryLevel: 100,
    cpuTemperature: 40,
    memoryUsage: 30,
    storageUsage: 50,
    wifiSignal: 80,
    isCharging: true
  });

  // Detect if running on UniHiker device
  useEffect(() => {
    const deviceCheck = isRunningOnUniHiker();
    setIsUniHiker(deviceCheck);
    
    if (deviceCheck) {
      console.log('[UniHiker] Running on UniHiker M10 hardware');
      // Apply device-specific optimizations
      document.documentElement.classList.add('unihiker-device');
      
      // Set viewport for small screen
      const viewportMeta = document.querySelector('meta[name="viewport"]');
      if (viewportMeta) {
        viewportMeta.setAttribute('content', 
          'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
      }
    }
  }, []);

  // Simulate hardware monitoring (would be replaced with actual hardware API calls on UniHiker)
  useEffect(() => {
    if (!isUniHiker) return;

    // In a real implementation, this would use UniHiker's Python APIs
    // to access actual hardware information through a backend service
    const hardwareMonitoringInterval = setInterval(() => {
      // Simulate fluctuating hardware values
      const newStatus: UniHikerHardwareStatus = {
        batteryLevel: Math.max(5, Math.min(100, hardwareStatus.batteryLevel + (Math.random() > 0.7 ? -1 : 1))),
        cpuTemperature: 35 + Math.random() * 15,
        memoryUsage: 20 + Math.random() * 40,
        storageUsage: hardwareStatus.storageUsage,
        wifiSignal: Math.max(0, Math.min(100, hardwareStatus.wifiSignal + (Math.random() > 0.5 ? -5 : 5))),
        isCharging: hardwareStatus.isCharging
      };
      
      setHardwareStatus(newStatus);
      
      if (onHardwareStatusChange) {
        onHardwareStatusChange(newStatus);
      }
    }, 5000);
    
    return () => clearInterval(hardwareMonitoringInterval);
  }, [isUniHiker, hardwareStatus, onHardwareStatusChange]);

  // Optimize performance for low-memory device
  useEffect(() => {
    if (!isUniHiker) return;
    
    // Reduce animation complexity
    document.documentElement.classList.add('reduce-motion');
    
    // Clean up listeners and optimize memory usage
    return () => {
      document.documentElement.classList.remove('reduce-motion', 'unihiker-device');
    };
  }, [isUniHiker]);

  // Handle device orientation changes
  useEffect(() => {
    if (!isUniHiker) return;
    
    const handleOrientationChange = () => {
      const { screenWidth, screenHeight } = getDeviceInfo();
      const isLandscape = screenWidth > screenHeight;
      
      document.documentElement.classList.toggle('landscape', isLandscape);
      document.documentElement.classList.toggle('portrait', !isLandscape);
    };
    
    window.addEventListener('resize', handleOrientationChange);
    handleOrientationChange(); // Initial check
    
    return () => window.removeEventListener('resize', handleOrientationChange);
  }, [isUniHiker]);

  return (
    <>
      {children}
      {isUniHiker && (
        <div id="unihiker-hardware-monitor" style={{ display: 'none' }}>
          {/* Hidden element with hardware status data attributes for debugging */}
          <div 
            data-battery={hardwareStatus.batteryLevel}
            data-temperature={hardwareStatus.cpuTemperature.toFixed(1)}
            data-memory={hardwareStatus.memoryUsage.toFixed(1)}
            data-storage={hardwareStatus.storageUsage.toFixed(1)}
            data-wifi={hardwareStatus.wifiSignal}
            data-charging={hardwareStatus.isCharging ? 'true' : 'false'}
          />
        </div>
      )}
    </>
  );
};

export default UniHikerIntegration;
