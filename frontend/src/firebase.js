// frontend/src/firebase.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// GANTI BAGIAN INI DENGAN CONFIG ANDA DARI FIREBASE CONSOLE
const firebaseConfig = {
  apiKey: "AIzaSyCATbiyGmt5pf3prLFdGuYH6g0LlLlaUuU", 
  authDomain: "eth-predictor-sapar.firebaseapp.com",
  projectId: "eth-predictor-sapar",
  storageBucket: "eth-predictor-sapar.firebasestorage.app",
  messagingSenderId: "583489789404",
  appId: "1:583489789404:web:a80fdbc3ac562baa1f8319"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);