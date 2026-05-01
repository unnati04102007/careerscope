import React, { useState } from 'react';
import { MessageCircle, X, Send, MapPin, DollarSign, Award } from 'lucide-react';

const CollegeSearch = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hi! Tell me what kind of college you are looking for (e.g., "Best coding culture in Pune")' }
  ]);

  // Sample data for the main grid cards
  const colleges = [
    { id: 1, name: 'IIT Bombay', state: 'Maharashtra', fees: '2.5L/yr', match: 98 },
    { id: 2, name: 'COEP Pune', state: 'Maharashtra', fees: '1.2L/yr', match: 85 },
    { id: 3, name: 'VIT Vellore', state: 'Tamil Nadu', fees: '3.0L/yr', match: 78 }
  ];

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;
    
    const userText = inputValue;
    setMessages(prev => [...prev, { type: 'user', text: userText }]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Connects to the Flask SBERT backend
      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_query: userText })
      });
      
      const data = await response.json();
      
      if (data.top_matches) {
        setMessages(prev => [
          ...prev, 
          { 
            type: 'bot', 
            text: 'Here are the best matches based on student reviews:',
            suggestions: data.top_matches 
          }
        ]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { type: 'bot', text: 'Sorry, I am having trouble connecting to the AI server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      {/* Header */}
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-4">
          Find Your Dream College
        </h1>
        <p className="text-gray-600 text-lg">AI-powered recommendations based on real student experiences.</p>
      </header>

      {/* Modern Cards Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {colleges.map(college => (
          <div key={college.id} className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-2xl font-bold text-gray-800">{college.name}</h3>
              <span className="bg-gradient-to-r from-green-400 to-emerald-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-sm flex items-center">
                <Award className="w-3 h-3 mr-1" />
                {college.match}% Match
              </span>
            </div>
            
            <div className="space-y-3 mb-6">
              <div className="flex items-center text-gray-600">
                <MapPin className="w-4 h-4 mr-2 text-blue-500" />
                <span>{college.state}</span>
              </div>
              <div className="flex items-center text-gray-600">
                <DollarSign className="w-4 h-4 mr-2 text-green-500" />
                <span>Fees: {college.fees}</span>
              </div>
            </div>
            
            <button className="w-full py-3 rounded-xl bg-blue-50 text-blue-600 font-semibold hover:bg-blue-600 hover:text-white transition-colors duration-300">
              View Details
            </button>
          </div>
        ))}
      </div>

      {/* Floating Chatbot Widget (Glassmorphism) */}
      <div className="fixed bottom-8 right-8 z-50">
        {/* Chat Window */}
        {isChatOpen && (
          <div className="absolute bottom-20 right-0 w-80 md:w-96 h-[500px] bg-white/80 backdrop-blur-xl border border-white/40 shadow-[0_8px_32px_0_rgba(31,38,135,0.37)] rounded-3xl flex flex-col overflow-hidden mb-4 transition-all duration-300 origin-bottom-right">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 flex justify-between items-center text-white">
              <h3 className="font-bold text-lg flex items-center">
                <MessageCircle className="mr-2 w-5 h-5" /> AI Guide
              </h3>
              <button onClick={() => setIsChatOpen(false)} className="hover:bg-white/20 p-1 rounded-full transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex flex-col ${msg.type === 'user' ? 'items-end' : 'items-start'}`}>
                  <div className={`max-w-[80%] p-3 rounded-2xl ${msg.type === 'user' ? 'bg-blue-600 text-white rounded-tr-sm' : 'bg-gray-100 text-gray-800 rounded-tl-sm'}`}>
                    {msg.text}
                  </div>
                  
                  {/* Dynamic Feedback Mini-cards inside chat */}
                  {msg.suggestions && (
                    <div className="mt-3 w-full space-y-2">
                      {msg.suggestions.map((sug, i) => (
                        <div key={i} className="bg-white border border-blue-100 p-3 rounded-xl shadow-sm hover:shadow-md cursor-pointer transition-shadow">
                          <div className="flex justify-between items-center mb-1">
                            <h4 className="font-bold text-blue-700 text-sm">{sug.college_name}</h4>
                            <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-semibold">
                              {sug.match_score}% Match
                            </span>
                          </div>
                          <p className="text-xs text-gray-500 italic line-clamp-2">"{sug.snippet}"</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="flex space-x-2 p-3 bg-gray-100 rounded-2xl rounded-tl-sm w-16">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white/50 border-t border-gray-100">
              <div className="flex items-center bg-white rounded-full p-1 pr-2 shadow-inner border border-gray-200">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask about college culture..."
                  className="flex-1 bg-transparent border-none focus:ring-0 px-4 py-2 text-sm outline-none"
                />
                <button 
                  onClick={handleSendMessage}
                  className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Toggle Button */}
        <button 
          onClick={() => setIsChatOpen(!isChatOpen)}
          className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-full shadow-2xl hover:shadow-[0_0_20px_rgba(79,70,229,0.5)] hover:scale-110 transition-all duration-300"
        >
          {isChatOpen ? <X className="w-6 h-6" /> : <MessageCircle className="w-6 h-6" />}
        </button>
      </div>
    </div>
  );
};

export default CollegeSearch;
