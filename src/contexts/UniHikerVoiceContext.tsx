import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { liveKitVoiceService, MicrophonePermission } from '../services/livekit/LiveKitVoiceService';
import { liveKitVoiceServiceFallback } from '../services/livekit/LiveKitVoiceServiceFallback';
import { generateUserToken } from '../services/livekit/tokenService';
import { v4 as uuidv4 } from 'uuid';
import { SynthesisState } from '../services/voice/OpenAIVoiceService';
import { isRunningOnUniHiker } from '../utils/deviceDetection';

// Define the context interface
interface UniHikerVoiceContextType {
  // Voice synthesis
  isSpeaking: boolean;
  synthesisState: SynthesisState;
  
  // Room state
  isConnected: boolean;
  roomName: string;
  
  // Microphone permission
  micPermission: MicrophonePermission;
  requestMicrophonePermission: () => Promise<boolean>;
  
  // Actions
  connect: (roomName?: string) => Promise<void>;
  disconnect: () => void;
  speak: (text: string, voice?: string) => Promise<void>;
  stopSpeaking: () => void;
  
  // Debug info
  debugInfo: string[];
  error: any | null;
  
  // UniHiker specific
  isUniHiker: boolean;
  isUsingFallback: boolean;
}

// Create the context with default values
const UniHikerVoiceContext = createContext<UniHikerVoiceContextType>({
  isSpeaking: false,
  synthesisState: 'idle',
  isConnected: false,
  roomName: '',
  micPermission: 'unknown',
  requestMicrophonePermission: async () => false,
  connect: async () => {},
  disconnect: () => {},
  speak: async () => {},
  stopSpeaking: () => {},
  debugInfo: [],
  error: null,
  isUniHiker: false,
  isUsingFallback: false
});

// Maximum number of debug messages to keep
const MAX_DEBUG_MESSAGES = 50;

// Provider component
export const UniHikerVoiceProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // State
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [synthesisState, setSynthesisState] = useState<SynthesisState>('idle');
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [roomName, setRoomName] = useState<string>('');
  const [debugInfo, setDebugInfo] = useState<string[]>([]);
  const [userId] = useState<string>(uuidv4());
  const [micPermission, setMicPermission] = useState<MicrophonePermission>('unknown');
  const [error, setError] = useState<any | null>(null);
  const [isUniHiker, setIsUniHiker] = useState<boolean>(false);
  const [isUsingFallback, setIsUsingFallback] = useState<boolean>(false);

  // Detect if running on UniHiker
  useEffect(() => {
    const onUniHiker = isRunningOnUniHiker();
    setIsUniHiker(onUniHiker);
    
    // If on UniHiker, default to using the fallback service
    if (onUniHiker) {
      setIsUsingFallback(true);
      addDebugMessage('Running on UniHiker M10, using fallback voice service');
    }
  }, []);

  // Add debug message
  const addDebugMessage = useCallback((message: string) => {
    setDebugInfo(prev => {
      const newMessages = [...prev, `[${new Date().toISOString()}] ${message}`];
      // Keep only the last MAX_DEBUG_MESSAGES messages
      return newMessages.slice(-MAX_DEBUG_MESSAGES);
    });
  }, []);

  // Request microphone permission
  const requestMicrophonePermission = useCallback(async () => {
    try {
      // If on UniHiker, don't even try to request microphone permission
      if (isUniHiker) {
        addDebugMessage('On UniHiker, skipping microphone permission request');
        setIsUsingFallback(true);
        return false;
      }
      
      // Try to request permission with the appropriate service
      const service = isUsingFallback ? liveKitVoiceServiceFallback : liveKitVoiceService;
      const result = await service.requestMicrophonePermission();
      
      addDebugMessage(`Microphone permission ${result ? 'granted' : 'denied'}`);
      
      // If permission denied, switch to fallback
      if (!result) {
        setIsUsingFallback(true);
      }
      
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      addDebugMessage(`Error requesting microphone permission: ${errorMessage}`);
      setError({
        type: 'permission_error',
        message: errorMessage
      });
      
      // Switch to fallback on error
      setIsUsingFallback(true);
      return false;
    }
  }, [isUniHiker, isUsingFallback, addDebugMessage]);

  // Connect to LiveKit room
  const connect = useCallback(async (customRoomName?: string) => {
    try {
      // Generate a room name if not provided
      const newRoomName = customRoomName || `lark-room-${uuidv4()}`;
      
      // Generate a token for the user
      const token = await generateUserToken(newRoomName, userId);
      
      // Choose the appropriate service
      const service = isUsingFallback ? liveKitVoiceServiceFallback : liveKitVoiceService;
      
      // Initialize the service - don't require microphone for UniHiker
      // This allows the service to work even without microphone permissions
      const requireMicrophone = !isUniHiker;
      await service.initialize(newRoomName, token, requireMicrophone);
      
      setRoomName(newRoomName);
      setIsConnected(true);
      addDebugMessage(`Connected to LiveKit room: ${newRoomName} using ${isUsingFallback ? 'fallback' : 'standard'} service`);
      
      return;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      addDebugMessage(`Error connecting to LiveKit room: ${errorMessage}`);
      
      // If standard service fails, try fallback
      if (!isUsingFallback) {
        setIsUsingFallback(true);
        addDebugMessage('Switching to fallback voice service');
        
        // Try again with fallback
        return connect(customRoomName);
      }
      
      setError({
        type: 'connection_error',
        message: errorMessage
      });
      
      throw error;
    }
  }, [userId, addDebugMessage, isUsingFallback]);

  // Disconnect from LiveKit room
  const disconnect = useCallback(() => {
    // Choose the appropriate service
    const service = isUsingFallback ? liveKitVoiceServiceFallback : liveKitVoiceService;
    
    service.disconnect();
    setIsConnected(false);
    setRoomName('');
    addDebugMessage(`Disconnected from LiveKit room using ${isUsingFallback ? 'fallback' : 'standard'} service`);
  }, [isUsingFallback, addDebugMessage]);

  // Speak text using the appropriate service
  const speak = useCallback(async (text: string, voice: string = 'ash'): Promise<void> => {
    // Always use Ash voice unless explicitly overridden
    voice = voice === 'alloy' ? 'ash' : voice;
    
    // Log the voice being used
    addDebugMessage(`Using voice: ${voice}`);
    try {
      // Connect to a room if not already connected
      if (!isConnected) {
        await connect();
      }
      
      // Log the speech request for debugging
      addDebugMessage(`Speaking text using ${isUsingFallback ? 'fallback' : 'standard'} service: ${text.substring(0, 50)}${text.length > 50 ? '...' : ''}`);
      
      // Choose the appropriate service
      const service = isUsingFallback ? liveKitVoiceServiceFallback : liveKitVoiceService;
      
      // Speak the text
      await service.speak(text, voice);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      addDebugMessage(`Error speaking text: ${errorMessage}`);
      
      // If standard service fails, try fallback
      if (!isUsingFallback) {
        setIsUsingFallback(true);
        addDebugMessage('Switching to fallback voice service for speech');
        
        // Try again with fallback
        return speak(text, voice);
      }
      
      throw error;
    }
  }, [isConnected, connect, isUsingFallback, addDebugMessage]);

  // Stop speaking
  const stopSpeaking = useCallback((): void => {
    // Choose the appropriate service
    const service = isUsingFallback ? liveKitVoiceServiceFallback : liveKitVoiceService;
    
    service.stop();
    addDebugMessage(`Stopping speech using ${isUsingFallback ? 'fallback' : 'standard'} service`);
  }, [isUsingFallback, addDebugMessage]);

  // Subscribe to service events
  useEffect(() => {
    // Choose the appropriate service
    const service = isUsingFallback ? liveKitVoiceServiceFallback : liveKitVoiceService;
    
    // Subscribe to speaking state
    const speakingSubscription = service.getSpeakingState().subscribe(speaking => {
      setIsSpeaking(speaking);
    });
    
    // Subscribe to synthesis state
    const synthesisSubscription = service.getSynthesisState().subscribe(state => {
      setSynthesisState(state);
    });
    
    // Subscribe to microphone permission state
    const micPermissionSubscription = service.getMicPermission().subscribe(permission => {
      setMicPermission(permission);
      
      // If permission denied, switch to fallback
      if (permission === 'denied' && !isUsingFallback) {
        setIsUsingFallback(true);
        addDebugMessage('Microphone permission denied, switching to fallback voice service');
      }
      
      addDebugMessage(`Microphone permission: ${permission}`);
    });
    
    // Subscribe to events
    const eventsSubscription = service.getEvents().subscribe(event => {
      addDebugMessage(`Voice service event: ${event.type} - ${JSON.stringify(event.payload)}`);
    });
    
    // Subscribe to errors
    const errorSubscription = service.getErrorEvent().subscribe(error => {
      if (error) {
        setError(error);
        addDebugMessage(`Voice service error: ${error.message || 'Unknown error'}`);
        
        // If standard service errors, try fallback
        if (!isUsingFallback) {
          setIsUsingFallback(true);
          addDebugMessage('Error in standard voice service, switching to fallback');
        }
      }
    });
    
    return () => {
      // Unsubscribe from all subscriptions
      speakingSubscription.unsubscribe();
      synthesisSubscription.unsubscribe();
      micPermissionSubscription.unsubscribe();
      eventsSubscription.unsubscribe();
      errorSubscription.unsubscribe();
    };
  }, [isUsingFallback, addDebugMessage]);

  // Provide context value
  const contextValue: UniHikerVoiceContextType = {
    isSpeaking,
    synthesisState,
    isConnected,
    roomName,
    micPermission,
    requestMicrophonePermission,
    connect,
    disconnect,
    speak,
    stopSpeaking,
    debugInfo,
    error,
    isUniHiker,
    isUsingFallback
  };

  return (
    <UniHikerVoiceContext.Provider value={contextValue}>
      {children}
    </UniHikerVoiceContext.Provider>
  );
};

// Custom hook to use the UniHiker voice context
export const useUniHikerVoice = () => useContext(UniHikerVoiceContext);

// Export the context for direct use if needed
export default UniHikerVoiceContext;
