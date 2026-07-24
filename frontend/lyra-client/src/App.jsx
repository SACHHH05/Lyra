import { useLyra } from './useLyra';
import './App.css';

function App() {
    const { isConnected, messages, connect, disconnect } = useLyra();

    return (
        <div className="dashboard" style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
            <h1>Lyra AI Interface</h1>
            
            <div className="controls" style={{ marginBottom: '2rem' }}>
                {!isConnected ? (
                    <button onClick={connect} style={{ padding: '0.5rem 1rem' }}>
                        Connect & Speak
                    </button>
                ) : (
                    <button onClick={disconnect} style={{ padding: '0.5rem 1rem', color: 'red' }}>
                        Disconnect
                    </button>
                )}
            </div>
            
            <div className="chat-log" style={{ border: '1px solid #ccc', padding: '1rem', minHeight: '300px' }}>
                {messages.length === 0 && <p>No messages yet...</p>}
                {messages.map((msg, index) => (
                    <div key={index} className="message" style={{ margin: '0.5rem 0' }}>
                        <strong>{msg.sender}:</strong> {msg.text}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;