import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Loader2, Target, Book, Palette, FlaskConical, TrendingUp, MonitorPlay, HeartPulse, Scale, Trophy } from 'lucide-react';

const Quiz = () => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  
  // Form State
  const [formData, setFormData] = useState({
    name: '',
    stream: '',
    marks: 50,
    interests: []
  });

  const streams = [
    { id: 'science', label: 'Science', icon: '🔬' },
    { id: 'commerce', label: 'Commerce', icon: '📊' },
    { id: 'arts', label: 'Arts', icon: '🎨' }
  ];

  const interestOptions = [
    { id: 'coding', label: 'Coding', icon: '💻' },
    { id: 'business', label: 'Business', icon: '📈' },
    { id: 'design', label: 'Design', icon: '🎨' },
    { id: 'research', label: 'Research', icon: '🔬' },
    { id: 'teaching', label: 'Teaching', icon: '📚' },
    { id: 'medicine', label: 'Medicine', icon: '🏥' },
    { id: 'law', label: 'Law', icon: '⚖️' },
    { id: 'sports', label: 'Sports', icon: '🏅' }
  ];

  const handleInterestToggle = (id) => {
    setFormData(prev => {
      const isSelected = prev.interests.includes(id);
      return {
        ...prev,
        interests: isSelected 
          ? prev.interests.filter(i => i !== id)
          : [...prev.interests, id]
      };
    });
  };

  const isNextDisabled = () => {
    if (step === 1) return formData.name.trim() === '';
    if (step === 2) return formData.stream === '';
    if (step === 4) return formData.interests.length === 0;
    return false;
  };

  const handleSubmit = () => {
    setLoading(true);
    // Simulate API call and loading state
    setTimeout(() => {
      // Mocking the API response
      const mockResult = {
        name: formData.name,
        stream: formData.stream,
        marks: formData.marks,
        message: "You have a highly analytical profile. Tech and Engineering are your strongest suits!",
        careers: [
          { title: 'Software Engineer', icon: '💻' },
          { title: 'Data Scientist', icon: '📊' },
          { title: 'Product Manager', icon: '🚀' }
        ]
      };
      
      sessionStorage.setItem('careerResults', JSON.stringify(mockResult));
      window.location.href = '/results'; // Redirect to results page
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-[520px] bg-white rounded-3xl shadow-xl overflow-hidden">
        
        {/* Animated Progress Bar */}
        <div className="h-2 w-full bg-gray-100">
          <div 
            className="h-full bg-gradient-to-r from-purple-500 to-indigo-600 transition-all duration-500 ease-out"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>

        <div className="p-8">
          {/* Header */}
          <div className="mb-8 text-center">
            <span className="text-sm font-bold text-purple-600 tracking-wider uppercase">Step {step} of 4</span>
          </div>

          {/* Step 1: Name */}
          {step === 1 && (
            <div className="animate-in fade-in slide-in-from-right-4 duration-500">
              <h2 className="text-3xl font-extrabold text-gray-900 mb-6 text-center">Apna naam kya hai?</h2>
              <input 
                type="text" 
                value={formData.name}
                onChange={e => setFormData({...formData, name: e.target.value})}
                placeholder="Enter your name..."
                className="w-full text-center text-2xl p-4 border-b-2 border-gray-200 focus:border-purple-600 outline-none transition-colors bg-transparent"
                autoFocus
              />
            </div>
          )}

          {/* Step 2: Stream */}
          {step === 2 && (
            <div className="animate-in fade-in slide-in-from-right-4 duration-500">
              <h2 className="text-3xl font-extrabold text-gray-900 mb-6 text-center">Tumhara stream kya hai?</h2>
              <div className="grid gap-4">
                {streams.map(s => (
                  <button
                    key={s.id}
                    onClick={() => setFormData({...formData, stream: s.id})}
                    className={`p-5 rounded-2xl border-2 transition-all duration-300 flex items-center justify-center gap-3 text-xl font-bold ${
                      formData.stream === s.id 
                        ? 'border-transparent bg-gradient-to-r from-purple-500 to-indigo-600 text-white shadow-lg transform scale-105' 
                        : 'border-gray-200 text-gray-600 hover:border-purple-300 hover:bg-purple-50'
                    }`}
                  >
                    <span>{s.icon}</span> {s.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 3: Marks */}
          {step === 3 && (
            <div className="animate-in fade-in slide-in-from-right-4 duration-500 text-center">
              <h2 className="text-3xl font-extrabold text-gray-900 mb-2">12th mein kitne % marks aaye?</h2>
              <p className="text-gray-500 mb-8">Be honest, it helps us recommend better!</p>
              
              <div className="mb-12">
                <div className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600 mb-6">
                  {formData.marks}%
                </div>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  value={formData.marks}
                  onChange={e => setFormData({...formData, marks: parseInt(e.target.value)})}
                  className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
                />
                <div className="flex justify-between text-sm text-gray-400 mt-2 font-bold">
                  <span>0%</span>
                  <span>100%</span>
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Interests */}
          {step === 4 && (
            <div className="animate-in fade-in slide-in-from-right-4 duration-500">
              <h2 className="text-3xl font-extrabold text-gray-900 mb-2 text-center">Tumhe kya pasand hai?</h2>
              <p className="text-gray-500 mb-6 text-center">Select all that apply</p>
              
              <div className="flex flex-wrap justify-center gap-3">
                {interestOptions.map(opt => {
                  const isSelected = formData.interests.includes(opt.id);
                  return (
                    <button
                      key={opt.id}
                      onClick={() => handleInterestToggle(opt.id)}
                      className={`px-5 py-3 rounded-full font-bold text-sm transition-all duration-300 flex items-center gap-2 ${
                        isSelected
                          ? 'bg-gradient-to-r from-purple-500 to-indigo-600 text-white shadow-md transform scale-105'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      {opt.icon} {opt.label}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Navigation */}
          <div className="mt-10 flex gap-4">
            {step > 1 && (
              <button 
                onClick={() => setStep(step - 1)}
                className="w-14 h-14 rounded-2xl bg-gray-100 text-gray-600 flex items-center justify-center hover:bg-gray-200 transition-colors"
                disabled={loading}
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
            )}
            
            {step < 4 ? (
              <button 
                onClick={() => setStep(step + 1)}
                disabled={isNextDisabled()}
                className={`flex-1 h-14 rounded-2xl flex items-center justify-center font-bold text-lg transition-all duration-300 ${
                  isNextDisabled() 
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-900 text-white hover:bg-gray-800 hover:shadow-lg'
                }`}
              >
                Next <ChevronRight className="w-5 h-5 ml-1" />
              </button>
            ) : (
              <button 
                onClick={handleSubmit}
                disabled={isNextDisabled() || loading}
                className={`flex-1 h-14 rounded-2xl flex items-center justify-center font-bold text-lg transition-all duration-300 ${
                  isNextDisabled() || loading
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white hover:shadow-lg hover:shadow-purple-500/30'
                }`}
              >
                {loading ? (
                  <Loader2 className="w-6 h-6 animate-spin" />
                ) : (
                  <>Get My Career Recommendations <ChevronRight className="w-5 h-5 ml-1" /></>
                )}
              </button>
            )}
          </div>

        </div>
      </div>
    </div>
  );
};

export default Quiz;
