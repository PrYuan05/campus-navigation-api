import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Send, Navigation } from 'lucide-react';
import './index.css';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

function App() {
  const [messages, setMessages] = useState([
    { id: 1, text: '你好！我是中央大學校園導航助理。請問你要去哪裡？', sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = 'zh-TW';

      rec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        // Can optionally auto-send here by calling handleSend(transcript)
      };

      rec.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setIsRecording(false);
      };

      rec.onend = () => {
        setIsRecording(false);
      };

      setRecognition(rec);
    } else {
      console.warn('Speech Recognition API not supported in this browser.');
    }
  }, []);

  const toggleRecording = () => {
    if (!recognition) return alert('Your browser does not support Speech Recognition.');
    
    if (isRecording) {
      recognition.stop();
    } else {
      recognition.start();
      setIsRecording(true);
    }
  };

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const cleanText = text.replace(/\n()/g, ' ').replace(/[#*_]/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.lang = 'zh-TW';
      utterance.rate = 1.1; 
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleSend = async (textToUse) => {
    const text = typeof textToUse === 'string' ? textToUse : input;
    if (!text.trim()) return;

    const userMessage = { id: Date.now(), text, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      // Send to FastAPI backend
      const res = await fetch('http://localhost:8000/api/v1/chat-navigation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_message: text })
      });
      
      const data = await res.json();
      let botResponse = '';

      if (data.status === 'success') {
        const { parsed_intent, routing } = data;
        const originName = (parsed_intent.origin && parsed_intent.origin !== 'CURRENT_LOCATION') ? parsed_intent.origin : '目前位置';
        let pInfo = `好的，從 ${originName} 前往 ${parsed_intent.destination}。`;
        
        if (routing.info) {
          botResponse = `${pInfo}\n\n${routing.info}`;
        } else if (routing.duration_text) {
          botResponse = `${pInfo}\n\n步行距離大約 ${routing.distance_text}，預計需要 ${routing.duration_text}。`;
        } else {
          botResponse = `${pInfo}\n\n無法獲取路線資訊。`;
        }
      } else {
        botResponse = `抱歉，系統發生錯誤：${data.message || '無法解析您的請求'}`;
      }

      setMessages(prev => [...prev, { id: Date.now() + 1, text: botResponse, sender: 'bot' }]);
      speakText(botResponse);

    } catch (error) {
      console.error(error);
      const errorMsg = '無法連接到伺服器。請確認後端(localhost:8000)是否正在運行。';
      setMessages(prev => [...prev, { id: Date.now() + 1, text: errorMsg, sender: 'bot' }]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSend(input);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <Navigation size={28} color="#a78bfa" />
        <h1>NCU Navigator</h1>
      </header>
      
      <main className="main-container">
        <div className="chat-container">
          <div className="messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.sender}`}>
                {msg.text.split('\n').map((line, i) => (
                  <React.Fragment key={i}>
                    {line}
                    {i !== msg.text.split('\n').length - 1 && <br />}
                  </React.Fragment>
                ))}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="input-area">
            <button 
              className={`icon-btn ${isRecording ? 'recording' : ''}`}
              onClick={toggleRecording}
              title={isRecording ? '停止錄音' : '開始錄音'}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            <input 
              type="text" 
              placeholder="輸入目的地或點擊麥克風發言..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="icon-btn" onClick={() => handleSend(input)}>
              <Send size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
