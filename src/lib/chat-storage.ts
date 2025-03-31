// Using dynamic import for idb to fix Vercel build issues
import { type DBSchema } from 'idb/with-async-ittr';

// We'll use dynamic import for openDB to avoid Rollup resolution issues
let openDB: any;

async function getOpenDB() {
  if (!openDB) {
    const idb = await import('idb/with-async-ittr');
    openDB = idb.openDB;
  }
  return openDB;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

interface ChatDBSchema extends DBSchema {
  messages: {
    key: number;
    value: ChatMessage;
    indexes: { 'by-timestamp': number };
  };
  'offline-queue': {
    key: number;
    value: {
      message: string;
      timestamp: number;
    };
  };
}

const DB_NAME = 'lark-chat-db';
const DB_VERSION = 1;

export const initChatDB = async () => {
  const openDBFunc = await getOpenDB();
  // Use type assertion to avoid TypeScript error with generic parameter
  return openDBFunc(DB_NAME, DB_VERSION, {
    upgrade(db: any) {
      const messageStore = db.createObjectStore('messages', {
        keyPath: 'timestamp'
      });
      messageStore.createIndex('by-timestamp', 'timestamp');
      
      db.createObjectStore('offline-queue', {
        keyPath: 'timestamp'
      });
    },
  });
};

export const saveMessage = async (message: ChatMessage) => {
  if (!message.role || !message.content || !message.timestamp) {
    console.error('Invalid message structure:', message);
    throw new Error('Invalid message structure. Ensure role, content, and timestamp are provided.');
  }
  try {
    const db = await initChatDB();
    if (db) {
      await db.put('messages', message);
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error saving message:', error);
    // Don't throw, just return false to indicate failure
    return false;
  }
};

export const getMessages = async (limit = 100): Promise<ChatMessage[]> => {
  try {
    const db = await initChatDB();
    if (db) {
      const messages = await db.getAllFromIndex('messages', 'by-timestamp');
      return messages.slice(-limit);
    }
    return [];
  } catch (error) {
    console.error('Error retrieving messages:', error);
    // Return empty array instead of throwing
    return [];
  }
};

export const queueOfflineMessage = async (message: string) => {
  if (!message) {
    throw new Error('Message cannot be empty.');
  }
  try {
    const db = await initChatDB();
    if (db) {
      await db.add('offline-queue', {
        message,
        timestamp: Date.now()
      });
    }
  } catch (error) {
    console.error('Error queuing offline message:', error);
    throw new Error('Failed to queue offline message.');
  }
};

export const getOfflineQueue = async () => {
  const db = await initChatDB();
  if (db) {
    return db.getAll('offline-queue');
  }
  return [];
};

export const clearOfflineQueue = async () => {
  const db = await initChatDB();
  if (db) {
    await db.clear('offline-queue');
  }
};
