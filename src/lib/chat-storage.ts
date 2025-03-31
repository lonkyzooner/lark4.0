import * as idbModule from 'idb';
const { openDB } = idbModule;
type DBSchema = idbModule.DBSchema;

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
  return openDB<ChatDBSchema>(DB_NAME, DB_VERSION, {
    upgrade(db) {
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
    await db.put('messages', message);
    return true;
  } catch (error) {
    console.error('Error saving message:', error);
    // Don't throw, just return false to indicate failure
    return false;
  }
};

export const getMessages = async (limit = 100): Promise<ChatMessage[]> => {
  try {
    const db = await initChatDB();
    const messages = await db.getAllFromIndex('messages', 'by-timestamp');
    return messages.slice(-limit);
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
    await db.add('offline-queue', {
      message,
      timestamp: Date.now()
    });
  } catch (error) {
    console.error('Error queuing offline message:', error);
    throw new Error('Failed to queue offline message.');
  }
};

export const getOfflineQueue = async () => {
  const db = await initChatDB();
  return db.getAll('offline-queue');
};

export const clearOfflineQueue = async () => {
  const db = await initChatDB();
  await db.clear('offline-queue');
};
