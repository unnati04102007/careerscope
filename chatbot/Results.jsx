import React, { useEffect, useState } from 'react';
import { ArrowRight, MessageCircle, ArrowDownRight, GraduationCap } from 'lucide-react';

const Results = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Read from sessionStorage
    const stored = sessionStorage.getItem('careerResults');
    if (stored) {
      setData(JSON.parse(stored));
      triggerConfetti();
    }
  }, []);

  const triggerConfetti = () => {
    // Simple mock for confetti effect using an injected style
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes floatUp {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
      }
      .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #a855f7;
        animation: floatUp 3s ease-out forwards;
        z-index: 50;
      }
    `;
    document.head.appendChild(style);

    for (let i = 0; i < 30; i++) {
      const el = document.createElement('div');
      el.className = 'confetti';
      el.style.left = Math.random() * 100 + 'vw';
      el.style.backgroundColor = ['#a855f7', '#6366f1', '#ec4899', '#3b82f6'][Math.floor(Math.random() * 4)];
      el.style.animationDelay = Math.random() * 0.5 + 's';
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 3500);
    }
  };

  const handleCardClick = (careerTitle) => {
    sessionStorage.setItem('selectedCareer', careerTitle);
    window.location.href = '/colleges'; // Redirect to college search
  };

  if (!data) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Quiz pehle complete karo!</h2>
        <button 
          onClick={() => window.location.href = '/quiz'}
          className="bg-purple-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-purple-700 transition-colors"
        >
          Go to Quiz
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 font-sans pb-20 overflow-x-hidden">
      
      {/* SECTION 1: Hero */}
      <section className="pt-20 pb-12 px-4 max-w-5xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white shadow-sm border border-gray-100 mb-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <GraduationCap className="w-5 h-5 text-purple-600" />
          <span className="font-bold text-gray-700">Profile Analyzed Successfully</span>
        </div>
        
        <h1 className="text-4xl md:text-5xl font-black text-gray-900 mb-6 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-100">
          Hi <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600">{data.name}</span>! 🎓<br/>
          Yeh hain tumhare best career options
        </h1>

        {/* Glowing Quote Box */}
        <div className="max-w-2xl mx-auto bg-white p-6 rounded-2xl shadow-[0_0_40px_rgba(168,85,247,0.15)] border border-purple-100 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-200 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-2 h-full bg-gradient-to-b from-purple-500 to-indigo-600"></div>
          <p className="text-lg text-gray-700 font-medium italic">"{data.message}"</p>
        </div>

        {/* Badges */}
        <div className="flex justify-center gap-3 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-300">
          <span className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white px-4 py-1.5 rounded-full text-sm font-bold shadow-md">
            Stream: {data.stream.charAt(0).toUpperCase() + data.stream.slice(1)}
          </span>
          <span className="bg-gradient-to-r from-pink-500 to-rose-500 text-white px-4 py-1.5 rounded-full text-sm font-bold shadow-md">
            Marks: {data.marks}%
          </span>
        </div>
      </section>

      {/* SECTION 2: Career Cards Grid */}
      <section className="px-4 max-w-6xl mx-auto mb-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {data.careers.map((career, idx) => (
            <div 
              key={idx}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-xl hover:border-transparent transition-all duration-300 relative group overflow-hidden"
              style={{ animationDelay: `${400 + idx * 100}ms` }}
              className={`bg-white rounded-2xl p-6 shadow-sm border-2 border-transparent hover:border-purple-500 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 animate-in fade-in slide-in-from-bottom-8`}
            >
              {/* Gradient border effect background */}
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-indigo-600 opacity-0 group-hover:opacity-5 transition-opacity duration-300"></div>
              
              <div className="text-5xl mb-4 transform group-hover:scale-110 transition-transform duration-300">
                {career.icon}
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{career.title}</h3>
              <p className="text-gray-500 mb-6 text-sm">Perfect match for your interests and academic profile.</p>
              
              <button 
                onClick={() => handleCardClick(career.title)}
                className="w-full py-3 px-4 bg-gray-50 text-purple-700 font-bold rounded-xl flex items-center justify-center gap-2 group-hover:bg-purple-600 group-hover:text-white transition-colors duration-300"
              >
                Explore Colleges <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 3: CTA Banner */}
      <section className="px-4 max-w-4xl mx-auto mb-20 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-700">
        <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-3xl p-8 md:p-12 text-center shadow-2xl relative overflow-hidden">
          {/* Decorative blur */}
          <div className="absolute -top-20 -right-20 w-64 h-64 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30"></div>
          
          <h2 className="text-3xl md:text-4xl font-black text-white mb-4 relative z-10">Ready to take the next step?</h2>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto relative z-10 text-lg">
            Discover top-rated engineering colleges with detailed insights on fees, ratings, and student placement records.
          </p>
          <button 
            onClick={() => window.location.href = '/colleges'}
            className="bg-white text-gray-900 px-8 py-4 rounded-full font-black text-lg shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:scale-105 transition-transform duration-300 relative z-10"
          >
            Explore Engineering Colleges
          </button>
        </div>
      </section>

      {/* SECTION 4: Chatbot Nudge */}
      <div className="fixed bottom-24 right-8 z-40 animate-bounce hidden md:flex flex-col items-end">
        <div className="bg-white px-4 py-3 rounded-2xl rounded-br-none shadow-lg border border-gray-100 mb-2">
          <p className="font-bold text-gray-800 text-sm flex items-center gap-2">
            Aur questions hain? 💬 <br/> Hamare AI Assistant se pucho!
          </p>
        </div>
        <ArrowDownRight className="w-8 h-8 text-purple-600 mr-2" />
      </div>

    </div>
  );
};

export default Results;
