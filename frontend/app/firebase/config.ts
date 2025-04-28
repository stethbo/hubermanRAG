import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyCRPecNk7NvzKWxwYlr6kwVvsNssdI4im4",
  authDomain: "hubermanrag.firebaseapp.com",
  projectId: "hubermanrag",
  storageBucket: "hubermanrag.firebasestorage.app",
  messagingSenderId: "788622629317",
  appId: "1:788622629317:web:4dde77b524104ac4ee53ac",
  databaseURL: "https://hubermanrag.firebaseio.com"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };
export default app; 