import { useState, useRef, useEffect } from 'react';

export function useLyra(url = "ws://localhost:8000/ws/audio") {
    const [isConnected, setIsConnected] = useState(false);
    const [messages, setMessages] = useState([]);
    const wsRef = useRef(null);
    const audioCtxRef = useRef(null);
    const streamRef = useRef(null);

    const connect = async () => {
        wsRef.current = new WebSocket(url);
        wsRef.current.binaryType = "arraybuffer"; 

        wsRef.current.onopen = () => setIsConnected(true);
        wsRef.current.onclose = () => setIsConnected(false);

        audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: 16000
        });

        wsRef.current.onmessage = async (event) => {
            if (event.data instanceof ArrayBuffer) {
                const audioBuffer = await audioCtxRef.current.decodeAudioData(event.data);
                const source = audioCtxRef.current.createBufferSource();
                source.buffer = audioBuffer;
                source.connect(audioCtxRef.current.destination);
                source.start();
            } else {
                const data = JSON.parse(event.data);
                setMessages(prev => [...prev, { sender: 'Lyra', text: data.response }]);
            }
        };

        streamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true });
        
    };

    const disconnect = () => {
        if (wsRef.current) wsRef.current.close();
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
        }
        setIsConnected(false);
    };

    useEffect(() => {
        return () => disconnect(); 
    }, []);

    return { isConnected, messages, connect, disconnect };
}