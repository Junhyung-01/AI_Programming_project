import React, { useState } from 'react';
import { useStore } from '../store';
import { ShoppingCart, BedDouble, Swords, User, Map, X, Package } from 'lucide-react';

export default function LobbyScreen() {
  const { gameState, chooseRoute } = useStore();
  const [showInventory, setShowInventory] = useState(false);
  const p = gameState?.player;

  if (!p) return null;

  const hpPercent = (p.hp / p.max_hp) * 100;
  const mpPercent = (p.mp / p.max_mp) * 100;
  
  const isBossStage = gameState.current_stage === 10;

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', padding: 20, position: 'relative' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 20 }}>
        <h1 style={{ margin: 0, color: 'var(--accent-color)' }}>
          CHAPTER {gameState.current_chapter} - {gameState.current_stage}스테이지
        </h1>
        <div style={{ color: 'var(--boss-color)', fontWeight: 'bold' }}>
          {isBossStage ? '⚠️ 다음은 보스 스테이지입니다!' : ''}
        </div>
      </div>

      <div className="grid-container" style={{ gridTemplateColumns: '2fr 1fr' }}>
        <div className="glass-panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <User size={24} /> {p.name} <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>({p.job_class})</span>
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <div style={{ color: '#fbbf24', fontWeight: 'bold', fontSize: '1.2rem' }}>💰 {p.gold} G</div>
            </div>
          </div>
          
          <div style={{ marginBottom: 15 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: 4 }}>
              <span>HP</span>
              <span>{p.hp} / {p.max_hp}</span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill progress-hp" style={{ width: `${hpPercent}%` }}></div>
            </div>
          </div>

          <div style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: 4 }}>
              <span>MP</span>
              <span>{p.mp} / {p.max_mp}</span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill progress-mp" style={{ width: `${mpPercent}%` }}></div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: 20, color: 'var(--text-secondary)', fontSize: '0.9rem', background: 'rgba(0,0,0,0.3)', padding: 12, borderRadius: 8 }}>
            <div><span style={{color: 'white'}}>공격력:</span> {p.atk}</div>
            <div><span style={{color: 'white'}}>방어력:</span> {p.def}</div>
          </div>
          
          <div style={{ marginTop: 20 }}>
            <h4 style={{ marginBottom: 8, color: 'var(--text-secondary)' }}>장착 장비</h4>
            <div style={{ display: 'flex', gap: 10, fontSize: '0.9rem' }}>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: '8px 12px', borderRadius: 6, flex: 1 }}>
                <span style={{ color: 'var(--text-secondary)', display: 'block', fontSize: '0.8rem' }}>무기</span>
                {p.equipment.weapon?.name || '없음'}
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: '8px 12px', borderRadius: 6, flex: 1 }}>
                <span style={{ color: 'var(--text-secondary)', display: 'block', fontSize: '0.8rem' }}>방어구</span>
                {p.equipment.armor?.name || '없음'}
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: '8px 12px', borderRadius: 6, flex: 1 }}>
                <span style={{ color: 'var(--text-secondary)', display: 'block', fontSize: '0.8rem' }}>장신구</span>
                {p.equipment.accessory?.name || '없음'}
              </div>
            </div>
          </div>
        </div>

        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <h3 style={{ marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}><Map size={20} /> 경로 선택</h3>
          <button 
            className="btn" 
            onClick={() => chooseRoute('battle')} 
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, padding: 20, fontSize: '1.1rem' }}
          >
            <Swords size={24} /> 전투 스테이지
          </button>
          {!isBossStage && (
            <>
              <button 
                className="btn btn-secondary" 
                onClick={() => chooseRoute('shop')} 
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, padding: 16 }}
              >
                <ShoppingCart size={20} /> 상점 스테이지
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={() => chooseRoute('rest')} 
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, padding: 16 }}
              >
                <BedDouble size={20} /> 휴식 스테이지
              </button>
            </>
          )}
          <button 
            className="btn btn-secondary" 
            onClick={() => setShowInventory(true)}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, padding: 16, marginTop: 4 }}
          >
            <Package size={20} /> 가방 (인벤토리)
          </button>
          {isBossStage && (
             <div style={{ color: 'var(--boss-color)', fontSize: '0.85rem', textAlign: 'center', marginTop: 8 }}>
               보스전 앞에서는 다른 길을 선택할 수 없습니다.
             </div>
          )}
        </div>
      </div>

      {gameState.logs.length > 0 && (
        <div className="glass-panel" style={{ marginTop: 20 }}>
          <h3 style={{ marginBottom: 10 }}>최근 기록</h3>
          <div className="log-container" style={{ height: 120 }}>
            {[...gameState.logs].reverse().slice(0, 5).map((log, i) => (
              <div key={i} className="log-entry" style={{ opacity: 1 - (i * 0.15) }}>{log}</div>
            ))}
          </div>
        </div>
      )}

      {/* 가방(인벤토리) 모달 */}
      {showInventory && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100
        }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: 400, display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h2 style={{ display: 'flex', alignItems: 'center', gap: 10 }}><Package /> 가방</h2>
              <button onClick={() => setShowInventory(false)} style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {Object.keys(p.inventory).length === 0 ? (
                <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: 20 }}>
                  가방이 비어있습니다.
                </div>
              ) : (
                Object.entries(p.inventory).map(([itemName, count]) => {
                  if (count === 0) return null;
                  return (
                    <div key={itemName} style={{ 
                      display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
                      background: 'rgba(255,255,255,0.05)', padding: 16, borderRadius: 8
                    }}>
                      <span style={{ fontSize: '1.1rem' }}>{itemName}</span>
                      <span style={{ background: 'var(--accent-color)', padding: '4px 12px', borderRadius: 20, fontWeight: 'bold' }}>
                        x {count as number}
                      </span>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
