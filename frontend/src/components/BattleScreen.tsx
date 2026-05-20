import React, { useState, useEffect, useRef } from 'react';
import { useStore } from '../store';
import { Skull, Shield, Sword, Package, Wind, Zap } from 'lucide-react';

export default function BattleScreen() {
  const { gameState, doAction } = useStore();
  const [selectedTargetId, setSelectedTargetId] = useState<number | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  const p = gameState?.player;
  const enemies = gameState?.enemies || [];
  const aliveEnemies = enemies.filter(e => e.hp > 0);

  useEffect(() => {
    // 자동 스크롤
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [gameState?.logs]);

  // 타겟이 죽으면 자동 리셋
  useEffect(() => {
    if (selectedTargetId !== null && !aliveEnemies.find(e => e.id === selectedTargetId)) {
      setSelectedTargetId(null);
    }
    if (selectedTargetId === null && aliveEnemies.length > 0) {
      setSelectedTargetId(aliveEnemies[0].id);
    }
  }, [aliveEnemies, selectedTargetId]);

  if (!p) return null;

  const hpPercent = (p.hp / p.max_hp) * 100;
  const mpPercent = (p.mp / p.max_mp) * 100;

  return (
    <div style={{ maxWidth: 1000, margin: '20px auto', padding: 20 }}>
      {/* 적 영역 */}
      <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginBottom: 24, flexWrap: 'wrap' }}>
        {enemies.map((enemy) => {
          const isDead = enemy.hp <= 0;
          const isSelected = selectedTargetId === enemy.id;
          const enemyHpPercent = isDead ? 0 : (enemy.hp / (gameState.is_boss ? 100 : 30)) * 100;
          
          return (
            <div 
              key={enemy.id}
              onClick={() => !isDead && setSelectedTargetId(enemy.id)}
              className="glass-panel"
              style={{
                flex: '1 1 200px',
                maxWidth: 300,
                textAlign: 'center',
                cursor: isDead ? 'default' : 'pointer',
                opacity: isDead ? 0.3 : 1,
                border: isSelected && !isDead ? '2px solid var(--hp-color)' : '1px solid var(--panel-border)',
                transform: isSelected && !isDead ? 'scale(1.05)' : 'none',
                transition: 'all 0.2s',
                position: 'relative',
                overflow: 'hidden'
              }}
            >
              {isDead && (
                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: 'red', fontSize: '3rem', zIndex: 10 }}>
                  <Skull />
                </div>
              )}
              <h3 style={{ margin: 0, color: gameState.is_boss ? 'var(--boss-color)' : 'white' }}>{enemy.name}</h3>
              {enemy.is_taunted && <div style={{ color: '#fbbf24', fontSize: '0.8rem', marginTop: 4 }}>💫 도발됨</div>}
              {enemy.is_blocking && <div style={{ color: '#60a5fa', fontSize: '0.8rem', marginTop: 4 }}>🛡️ 방어 태세</div>}
              
              <div style={{ marginTop: 12 }}>
                <div style={{ fontSize: '0.9rem', marginBottom: 4 }}>HP: {Math.max(0, enemy.hp)}</div>
                <div className="progress-bar">
                  <div className="progress-fill progress-hp" style={{ width: `${enemyHpPercent}%` }}></div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid-container" style={{ gridTemplateColumns: '1fr 1fr' }}>
        {/* 전투 로그 */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ marginBottom: 12 }}>전투 로그</h3>
          <div className="log-container" style={{ flex: 1, maxHeight: 300 }}>
            {gameState.logs.map((log, i) => (
              <div key={i} className="log-entry">{log}</div>
            ))}
            <div ref={logsEndRef} />
          </div>
        </div>

        {/* 플레이어 영역 및 액션 */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ background: 'rgba(0,0,0,0.3)', padding: 16, borderRadius: 8 }}>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
              <Shield size={24} color="var(--accent-color)" /> {p.name}
            </h2>
            <div style={{ marginBottom: 10 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: 4 }}>
                <span>HP</span><span>{p.hp} / {p.max_hp}</span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill progress-hp" style={{ width: `${hpPercent}%` }}></div>
              </div>
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: 4 }}>
                <span>MP</span><span>{p.mp} / {p.max_mp}</span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill progress-mp" style={{ width: `${mpPercent}%` }}></div>
              </div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <button className="btn" onClick={() => doAction('attack', { target_id: selectedTargetId })} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
              <Sword size={20} /> 기본 공격
            </button>
            <button className="btn btn-secondary" onClick={() => doAction('flee')} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
              <Wind size={20} /> 도망치기
            </button>
          </div>

          <div>
            <h4 style={{ marginBottom: 8, color: 'var(--text-secondary)' }}>스킬</h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
              {p.skills.map((skill: any) => (
                <button 
                  key={skill.name}
                  className="btn btn-secondary"
                  disabled={p.mp < skill.mp}
                  onClick={() => doAction('skill', { skill_name: skill.name, target_id: selectedTargetId })}
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px' }}
                >
                  <span>{skill.name}</span>
                  <span style={{ fontSize: '0.8rem', color: p.mp >= skill.mp ? 'var(--mp-color)' : 'var(--text-secondary)' }}>
                    {skill.mp} MP
                  </span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <h4 style={{ marginBottom: 8, color: 'var(--text-secondary)' }}>포션</h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
              <button 
                className="btn btn-secondary" 
                disabled={!p.inventory["HP 물약"]}
                onClick={() => doAction('item', { item_name: 'HP 물약' })}
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}
              >
                <Package size={16} color="var(--hp-color)" /> HP 물약 ({p.inventory["HP 물약"] || 0})
              </button>
              <button 
                className="btn btn-secondary" 
                disabled={!p.inventory["MP 물약"]}
                onClick={() => doAction('item', { item_name: 'MP 물약' })}
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}
              >
                <Package size={16} color="var(--mp-color)" /> MP 물약 ({p.inventory["MP 물약"] || 0})
              </button>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
