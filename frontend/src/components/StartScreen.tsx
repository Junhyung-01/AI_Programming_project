import React, { useState } from 'react';
import { useStore } from '../store';
import { Sword, Shield, Zap, Wind, User } from 'lucide-react';

export default function StartScreen() {
  const { gameData, startGame } = useStore();
  const [name, setName] = useState('');
  const [selectedJob, setSelectedJob] = useState('');
  const [imageErrors, setImageErrors] = useState<Record<string, boolean>>({});

  if (!gameData) return <div className="glass-panel" style={{margin: '50px auto', maxWidth: 400}}>로딩 중...</div>;

  const jobIcons: any = {
    "전사": <Sword />,
    "마법사": <Zap />,
    "권사": <User />,
    "도적": <Wind />,
    "용기사": <Shield />
  };

  const jobImages: Record<string, string> = {
    "전사": "/images/jobs/warrior.png",
    "마법사": "/images/jobs/mage.png",
    "권사": "/images/jobs/monk.png",
    "도적": "/images/jobs/thief.png",
    "용기사": "/images/jobs/dragon_knight.png"
  };

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', padding: 20 }}>
      <h1 style={{ textAlign: 'center', marginBottom: 40, color: 'var(--accent-color)', fontSize: '2.5rem' }}>TEXT RPG GAME</h1>
      
      <div className="glass-panel" style={{ marginBottom: 30 }}>
        <h2>캐릭터 생성</h2>
        <div style={{ marginTop: 20, marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 8 }}>캐릭터 이름</label>
          <input 
            type="text" 
            value={name}
            onChange={e => setName(e.target.value)}
            style={{ width: '100%', padding: 12, borderRadius: 8, border: '1px solid var(--panel-border)', background: 'rgba(0,0,0,0.5)', color: 'white', fontSize: '1rem' }}
            placeholder="이름을 입력하세요"
          />
        </div>

        <label style={{ display: 'block', marginBottom: 12 }}>직업 선택</label>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 16 }}>
          {gameData.jobs.map((job: string) => (
            <div 
              key={job}
              onClick={() => setSelectedJob(job)}
              style={{
                padding: '20px 10px',
                borderRadius: 12,
                cursor: 'pointer',
                textAlign: 'center',
                border: `2px solid ${selectedJob === job ? 'var(--accent-color)' : 'var(--panel-border)'}`,
                background: selectedJob === job ? 'rgba(99, 102, 241, 0.2)' : 'rgba(0,0,0,0.3)',
                transition: 'all 0.2s',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                minHeight: 180
              }}
            >
              <div>
                <div style={{ 
                  marginBottom: 12, 
                  color: selectedJob === job ? 'var(--accent-color)' : 'var(--text-secondary)',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  height: 80
                }}>
                  {jobImages[job] && !imageErrors[job] ? (
                    <img 
                      src={jobImages[job]} 
                      alt={job}
                      onError={() => setImageErrors(prev => ({ ...prev, [job]: true }))}
                      style={{ 
                        maxWidth: '100%', 
                        maxHeight: '100%', 
                        objectFit: 'contain',
                        borderRadius: 8
                      }} 
                    />
                  ) : (
                    <div style={{ transform: 'scale(1.5)', display: 'flex', alignItems: 'center' }}>
                      {jobIcons[job]}
                    </div>
                  )}
                </div>
                <h3 style={{ margin: 0, fontSize: '1.2rem' }}>{job}</h3>
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: 8 }}>
                HP: {gameData.job_stats[job].hp}<br/>
                ATK: {gameData.job_stats[job].atk}
              </div>
            </div>
          ))}
        </div>
      </div>

      <button 
        className="btn" 
        style={{ width: '100%', padding: 16, fontSize: '1.2rem' }}
        disabled={!name || !selectedJob}
        onClick={() => startGame(name, selectedJob)}
      >
        모험 시작하기
      </button>
    </div>
  );
}
